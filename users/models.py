from django.db import models
from django.contrib.auth.models import AbstractUser

class AdminAccess(models.Model):
    class Meta:
        managed = False  # no table needed
        default_permissions = ()
        permissions = [
            ("can_admin_site", "Can access city admin pages"),
        ]
