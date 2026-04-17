from django.core.management.base import BaseCommand
from users.services import GetOrCreateResidentUser

class Command(BaseCommand):
    help = "Create or get a resident user"

    def add_arguments(self, parser):
        parser.add_argument('username')
        # parser.add_argument('email')
        # parser.add_argument('password')

    def handle(self, *args, **options):
        email = 'foo@bar.com'
        password = 'letmein!'

        user, created = GetOrCreateResidentUser.execute({
            'username': options['username'],
            'email': email,
            'password': password,
        })

        if created:
            self.stdout.write(f'New resident user created: {user.username}')
        else:
            self.stdout.write(f'User already exists: {user.username}')