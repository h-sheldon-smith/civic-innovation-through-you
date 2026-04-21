from django.core.management.base import BaseCommand

from idea_forum.services import CreateAutoModUser

class Command(BaseCommand):
    held = "Create the AutoMod user"

    def handle(self, *args, **options):
        status = CreateAutoModUser.execute({})

        if status is not None:
            self.stdout.write(f'AutoMod account succesfully created')
        else:
            self.stderr.write(f'Error: AutoMod account already exists')