from service_objects.services import Service
from django.db import models
from machina.core.db.models import get_model

from users.services import GetOrCreateModUser
from common.choices import Topic_Options

# create the forum containers if they don't exist
class CreateForumContainers(Service):
    def process(self):
        Forum = get_model('forum', 'Forum')

        forum_names = Topic_Options.labels
        created_forums = []
        for forum_name in forum_names:
            forum, created = Forum.objects.get_or_create(
                name=forum_name,
                parent=None,
                defaults={'type': Forum.FORUM_POST}
            )

            if created:
                created_forums.append(forum_name)
        
        # expensive and looks like it's unneccesary
        # Forum.objects.rebuild()

        return created_forums


class CreateAutoModUser(Service):
    def process(self):
        username = 'AutoMod'
        email = 'civicinnovationthroughyou@gmail.com'
        password = 'letmein!' # TODO: make a secure version of password storage

        user, created, promoted = GetOrCreateModUser.execute({
            'username': username,
            'email': email,
            'password': password,
        })

        if not created:
            status = None
        else:
            status = user

        return status