from django.db import models
from vote.models import VoteModel
from machina.apps.forum_conversation.abstract_models import AbstractPost

# add the VoteModel mixin when creating the concrete Post model from the AbstracPost abstract model
class Post(VoteModel, AbstractPost):
    # TODO: add a num_net_votes field to the Post model (or possibly something that inherits the VoteModel mxin and plugs in to the django-vote internals)

    pass

# Custom models should be declared above before importing django-machina's models
from machina.apps.forum_conversation.models import * # noqa