from django.apps import AppConfig
from django.db.models.signals import post_migrate


def ensure_site_admin_group(sender, **kwargs):
    from django.contrib.auth.models import Group, Permission
    
    group, _ = Group.objects.get_or_create(name="site_admin")

    # Find the permission (tied to app_label="users")
    perm = Permission.objects.filter(
        content_type__app_label="users",
        codename="can_admin_site",
    ).first()

    if perm:
        group.permissions.add(perm)

class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self):
        post_migrate.connect(ensure_site_admin_group, sender=self)
