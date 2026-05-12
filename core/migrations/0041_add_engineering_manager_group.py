from django.db import migrations


def add_engineering_manager_group(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.get_or_create(name='Engineering Manager')


def remove_engineering_manager_group(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name='Engineering Manager').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0040_create_role_groups'),
    ]

    operations = [
        migrations.RunPython(add_engineering_manager_group, remove_engineering_manager_group),
    ]
