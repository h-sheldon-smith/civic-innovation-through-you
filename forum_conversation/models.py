from django.db import models
from vote.models import VoteModel
from machina.apps.forum_conversation.abstract_models import AbstractPost

from common.choices import MOD_GROUP_NAME
from services.rate_limiter import RateLimiter
from idea_forum.services.screening_tools import ScreeningService

# add the VoteModel mixin when creating the concrete Post model from the AbstracPost abstract model
class Post(VoteModel, AbstractPost):
    def save(self, *args, **kwargs):
        rate_limiter = RateLimiter("resident_forum_posting")

        if not self.approved:
            # Muted users should not be able to post — don't save post to the db
            # (and delete if it's there already) as a backstop
            # in case the middleware check was bypassed.
            try:
                if self.poster and self.poster.moderation.is_muted():
                    if self.pk:
                        # delete post from the db if it's there
                        self.delete()
                    # don't do super().save()
                    return
            except Exception:
                pass

            # if user is a resident and hasn't hit their posting rate limit yet
            if not self.poster.groups.filter(name=MOD_GROUP_NAME).exists() and rate_limiter.enforce_rate_limit(self.poster.id):
                if self.pk:
                    # delete post from the db if it's there
                    self.delete()
                # don't do super().save()
                return
            
            # post smart screening
            screening_service = ScreeningService()
            if not screening_service.screen_post(self):
                self.approved = True
            else:
                if self.pk:
                    # delete post from the db if it's there
                    self.delete()
                # don't do super().save()
                return

        super().save(*args, **kwargs)

# Custom models should be declared above before importing django-machina's models
from machina.apps.forum_conversation.models import * # noqa