from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from machina.core.db.models import get_model

from idea_forum.services.smart_controller import SmartController

Post = get_model('forum_conversation', 'Post')

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