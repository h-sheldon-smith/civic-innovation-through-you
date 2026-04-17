from django.core.management.base import BaseCommand
from users.services import GetOrCreateModUser

class Command(BaseCommand):
    help = "Create or get a mod user"

    def add_arguments(self, parser):
        parser.add_argument('username')
        # parser.add_argument('email')
        # parser.add_argument('password')

    def handle(self, *args, **options):
        email = 'foo@bar.com'
        password = 'letmein!'

        user, created, promoted = GetOrCreateModUser.execute({
            'username': options['username'],
            'email': email,
            'password': password,
        })

        if created:
            self.stdout.write(f'New mod user created: {user.username}')
        elif promoted:
            self.stdout.write(f'Existing user promoted to mod: {user.username}')
        else:
            self.stdout.write(f'User already exists and is a mod: {user.username}')