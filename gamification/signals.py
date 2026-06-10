from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from gamification.game_services import award_points
from gamification.game_choices import PointType

@receiver(user_logged_in)
def reward_login(sender, user, request, **kwargs):
    print("LOGIN SIGNAL FIRED FOR: ", user.username)
    if not user.has_perm('users.can_admin_site'):
        award_points(user, PointType.LOGIN)