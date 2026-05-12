from django.db import migrations


def add_officer_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.get_or_create(name='Officer')
    Group.objects.get_or_create(name='Managing Officer')
    Group.objects.get_or_create(name='PST')


def remove_officer_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name__in=['Officer', 'Managing Officer', 'PST']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0041_add_engineering_manager_group'),
    ]

    operations = [
        migrations.RunPython(add_officer_groups, remove_officer_groups),
    ]
