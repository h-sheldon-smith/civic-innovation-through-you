from service_objects.services import Service
from django.db import models
from machina.core.db.models import get_model
# from mptt.models import MPTTModel

from common.choices import Topic_Options

# create the forum containers if they don't exist
class CreateForumContainers(Service):
    def process(self):
        Forum = get_model('forum', 'Forum')
        created_forums = []

        for forum_name in Topic_Options.labels:
            forum, created = Forum.objects.get_or_create(
                name=forum_name,
                parent=None,
                defaults={'type': Forum.FORUM_POST}
            )

            if created:
                created_forums.append(forum_name)

        Forum.objects.rebuild()

        return created_forums