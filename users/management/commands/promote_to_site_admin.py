from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = "Add a user to the site_admin group"

    def add_arguments(self, parser):
        parser.add_argument("username", type=str, help="The user's username")

    def handle(self, *args, **options):
        User = get_user_model()
        username = options["username"]

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(f'No user found with username="{username}"')

        group, _ = Group.objects.get_or_create(name="site_admin")
        user.groups.add(group)

        self.stdout.write(self.style.SUCCESS(
            f'User "{user.username}" added to group "site_admin".'
        ))