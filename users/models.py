from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class AdminAccess(models.Model):
    class Meta:
        managed = False  # no table needed
        default_permissions = ()
        permissions = [
            ("can_admin_site", "Can access city admin pages"),
        ]


class UserModeration(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('muted', 'Muted'),
        ('suspended', 'Suspended'),
        ('banned', 'Banned'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='moderation')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    mute_until = models.DateTimeField(null=True, blank=True)
    suspended_until = models.DateTimeField(null=True, blank=True)
    reason = models.TextField(blank=True)
    actioned_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='moderation_actions'
    )
    actioned_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.status}"

    def is_muted(self):
        if self.status == 'muted':
            if self.mute_until and self.mute_until < timezone.now():
                self.status = 'active'
                self.mute_until = None
                self.save(update_fields=['status', 'mute_until'])
                return False
            return True
        return False

    def is_suspended(self):
        if self.status == 'suspended':
            if self.suspended_until and self.suspended_until < timezone.now():
                self.status = 'active'
                self.suspended_until = None
                self.save(update_fields=['status', 'suspended_until'])
                return False
            return True
        return False

    def is_banned(self):
        return self.status == 'banned'

    def is_restricted(self):
        """Returns True if the user cannot post (muted, suspended, or banned)."""
        return self.is_muted() or self.is_suspended() or self.is_banned()


@receiver(post_save, sender=User)
def create_user_moderation(sender, instance, created, **kwargs):
    if created:
        UserModeration.objects.create(user=instance)
