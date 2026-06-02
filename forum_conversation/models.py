from django.db import models
from vote.models import VoteModel
from machina.apps.forum_conversation.abstract_models import AbstractPost

from services.rate_limiter import RateLimiter
from common.choices import MOD_GROUP_NAME
# from idea_forum.services.smart_controller import SmartController
from idea_forum.services.screening_tools import ScreeningService

# add the VoteModel mixin when creating the concrete Post model from the AbstracPost abstract model
class Post(VoteModel, AbstractPost):
    def save(self, *args, **kwargs):
        rate_limiter = RateLimiter("resident_forum_posting")
        # smart_controller = SmartController()

        if not self.approved:
            # Muted users should not be able to post — don't save post to the db
            # (and delete if it's there already) as a backstop
            # in case the middleware check was bypassed.
            try:
                if self.poster and self.poster.moderation.is_muted():
                    if self.pk:
                        # delete post from the db if it's there
                        self.delete()

                    return
            except Exception:
                pass
            
            # post smart screening
            screening_service = ScreeningService()
            if not screening_service.screen_post(self):
                self.approved = True
            else:
                if self.pk:
                    # delete post from the db if it's there
                    self.delete()

                return
            
            # screen_flagged = smart_controller.run_smart_post_moderation(self)

        super().save(*args, **kwargs)




# Custom models should be declared above before importing django-machina's models
from machina.apps.forum_conversation.models import * # noqa