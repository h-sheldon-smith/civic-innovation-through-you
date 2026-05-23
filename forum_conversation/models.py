from django.db import models
from vote.models import VoteModel
from machina.apps.forum_conversation.abstract_models import AbstractPost

# add the VoteModel mixin when creating the concrete Post model from the AbstracPost abstract model
class Post(VoteModel, AbstractPost):
    pass

# Custom models should be declared above before importing django-machina's models
from machina.apps.forum_conversation.models import * # noqa