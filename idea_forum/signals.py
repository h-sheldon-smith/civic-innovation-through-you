from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from machina.core.db.models import get_model

from services.rate_limiter import RateLimiter
from common.choices import MOD_GROUP_NAME
from idea_forum.services.smart_controller import SmartController

Post = get_model('forum_conversation', 'Post')

@receiver(post_save, sender=Post)
def trigger_on_forum_post_creation(sender, instance, created, **kwargs):
    # instance is the Post object that was created
    # instance.poster is the User object that created the post

    rate_limiter = RateLimiter("resident_forum_posting")
    smart_controller = SmartController()

    poster = instance.poster

    # trigger when a post is created and that post needs approval (so not moderator posts if they're set to not require approval)
    if created and not instance.approved:
        # Muted users should not be able to post — delete immediately as a backstop
        # in case the middleware check was bypassed.
        try:
            if poster and poster.moderation.is_muted():
                instance.delete()
                return
        except Exception:
            pass

        # resident rate-limiting for posts
        try:
            # if user is a resident and hasn't hit their posting rate limit yet
            if not poster.groups.filter(MOD_GROUP_NAME).exists() and rate_limiter.enforce_rate_limit(poster.id):
                instance.delete()
                return
        except Exception:
            pass
        
        # transaction.on_commit makes execution of its argument lambda wait until the db update is complete for creating the Post
        transaction.on_commit(lambda: smart_controller.run_smart_post_moderation(instance))