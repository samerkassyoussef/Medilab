from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from .models import MaintenanceRequest, Driver
from webpush import send_group_notification
import threading

def _send_push_async(payload):
    try:
        send_group_notification(group_name="Engineer", payload=payload, ttl=1000)
    except Exception as e:
        print(f"Webpush notification failed: {e}")

@receiver(post_save, sender=MaintenanceRequest)
def send_maintenance_notification(sender, instance, created, **kwargs):
    if created:
        payload = {
            "head": "New Maintenance Request",
            "body": f"{instance.facility_name}\n({instance.urgency}) - {instance.get_location_display() or instance.location}",
            "icon": "/static/icons/icon-192x192.png",
            "url": f"/requests/{instance.id}/"
        }
        
        # Dispatch notification to a background thread to prevent blocking
        # the HTTP response for 2-5 seconds while waiting for remote push servers
        threading.Thread(target=_send_push_async, args=(payload,), daemon=True).start()


@receiver(m2m_changed, sender=User.groups.through)
def sync_driver_profile(sender, instance, action, pk_set, **kwargs):
    """Sync Driver profile when a user is added to or removed from the 'Driver' group."""
    if action not in ('post_add', 'post_remove') or not pk_set:
        return
    try:
        driver_group = Group.objects.get(name='Driver')
    except Group.DoesNotExist:
        return
    if driver_group.pk not in pk_set:
        return
    if action == 'post_add':
        Driver.objects.get_or_create(
            user=instance,
            defaults={'name': instance.get_full_name() or instance.username},
        )
    else:
        Driver.objects.filter(user=instance).delete()
