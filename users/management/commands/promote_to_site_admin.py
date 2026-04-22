from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from machina.core.db.models import get_model

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

        group_name = "site_admin"
        
        group, created = Group.objects.get_or_create(name=group_name)

        if created:
            self.stdout.write(f"The group {group_name} doesn't exist; creating it and adding machina permissions to it")
            self.add_group_permissions(group)

        user.groups.add(group)

        self.stdout.write(self.style.SUCCESS(
            f'User "{user.username}" added to group "{group_name}"'
        ))

    def add_group_permissions(self, group):
        # Note: Machina's permissions are in a Machina-specific internal permission table, ForumPermission
        ForumPermission = get_model('forum_permission', 'ForumPermission')
        GroupForumPermission = get_model('forum_permission', 'GroupForumPermission')

        perm_names = []
        # topic creation
        perm_names = perm_names + ["can_start_new_topics", "can_post_announcements", "can_post_stickies", "can_post_without_approval"]
        # poll creation
        perm_names = perm_names + ["can_create_polls"]
        # forum moderation
        perm_names = perm_names + ["can_lock_topics", "can_move_topics", "can_edit_posts", "can_delete_posts", "can_approve_posts", "can_reply_to_locked_topics"]
        
        for perm_codename in perm_names:
            # add Machina permission to Machina's internal ForumPermission table (instead of the general Django Group.permissions table)
            try:
                forum_perm = ForumPermission.objects.get(codename=perm_codename)
            except ForumPermission.DoesNotExist:
                self.stdout.write(f"Machina permission {perm_codename} not found; make sure Django-Machina is installed, run manage.py migrate and try again")
                return

            obj, created = GroupForumPermission.objects.get_or_create(
                group=group,
                permission=forum_perm,
                forum=None, # global, apply to all forums
                has_perm=True
            )