from django.core.management.base import BaseCommand
from idea_forum.services.service_objs import CreateForumContainers

class Command(BaseCommand):
    help = "Create the forum containers if any don't exist"

    def handle(self, *args, **options):
        created_forums = CreateForumContainers.execute({})

        if len(created_forums) > 0:
            self.stdout.write(f'Created forum containers')
        else:
            self.stdout.write(f'Forum containers already exist')