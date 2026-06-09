from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction
from vote.models import Vote, UP
from machina.core.db.models import get_model
from django.contrib.auth import get_user_model

from idea_forum.services.smart_controller import SmartController

from common.choices import ADMIN_GROUP_NAME
from gamification import game_services, game_choices

Post = get_model('forum_conversation', 'Post')
User = get_user_model()

@receiver(post_save, sender=Post)
def trigger_smart_controller(sender, instance, created, **kwargs):
    smart_controller = SmartController()

    # trigger when a post is created and that post needs approval (so not moderator posts if they're set to not require approval)
    if created and not instance.approved:
        # Muted users should not be able to post — delete immediately as a backstop
        # in case the middleware check was bypassed.
        try:
            if instance.poster and instance.poster.moderation.is_muted():
                instance.delete()
                return
        except Exception:
            pass

        transaction.on_commit(lambda: smart_controller.run_smart_post_moderation(instance))


@receiver(post_save, sender=Post)
def post_create_gamification(sender, instance, created, **kwargs):
    if created and is_resident(instance.poster):
        game_services.award_points(instance.poster, game_choices.PointType.COMMENT)


@receiver(post_delete, sender=Post)
def post_create_gamification(sender, instance, **kwargs):
    pass
    # if is_resident(instance.poster):
    #     game_services.deduct_points(instance.poster, game_choices.PointType.COMMENT)


@receiver(post_save, sender=Vote)
def upvote_create_or_update_gamification(sender, instance, created, **kwargs):
    if created and instance.content_type.model == 'post' and instance.action == UP:
        liking_user = User.objects.get(id=instance.user_id)
        post = Post.objects.get(pk=instance.object_id)

        if is_resident(liking_user):
            game_services.award_points(liking_user, game_choices.PointType.LIKE)

        if is_resident(post.poster):
            game_services.award_points(post.poster, game_choices.PointType.RECEIVE_LIKE)


@receiver(post_delete, sender=Vote)
def vote_delete_gamification(sender, instance, **kwargs):
    if instance.content_type.model == 'post':
        unliking_user = User.objects.get(id=instance.user_id)
        post = Post.objects.get(pk=instance.object_id)

        # if is_resident(unliking_user):
        #     game_services.deduct_points(unliking_user, game_choices.PointType.LIKE)

        # if is_resident(post.poster):
        #     game_services.deduct_points(post.poster, game_choices.PointType.RECEIVE_LIKE)


def is_resident(user):
    return not user.groups.filter(name=ADMIN_GROUP_NAME).exists()