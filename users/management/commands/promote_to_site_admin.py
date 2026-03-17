from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from machina.core.db.models import get_model


from machina.apps import forum_permission
# from machina.apps.forum_permission import ForumPermission

class Command(BaseCommand):
    help = "Add a user to the site_admin group"

    # We need to load these manually (since machina permissions use an Abstract Model)
    ForumPermission = get_model('forum_permission', 'ForumPermission')

    def add_arguments(self, parser):
        parser.add_argument("username", type=str, help="The user's username")

    def add_group_permissions(self, group):
        # perm = Permission.objects.get_or_create(codename="can_admin_site")
        # group.permissions.add(perm)

        self.add_forum_permissions(group)

    def add_forum_permissions(self, group):
        perm_names = []
        # topic creation
        perm_names = perm_names + ["can_start_new_topics", "can_post_announcements", "can_post_stickies", "can_post_without_approval"]
        # forum moderation
        perm_names = perm_names + ["can_lock_topics", "can_move_topics", "can_edit_posts", "can_delete_posts", "can_approve_posts", "can_reply_to_locked_topics"]
        
        # Ensure the Machina model is loaded into the registry
        # This prevents 'AppRegistryNotReady' or missing ContentType errors
        ForumPermission = get_model('forum_permission', 'ForumPermission')

        for perm_codename in perm_names:
            self.add_a_forum_permission(group, perm_codename)

    def add_a_forum_permission(self, group, perm_codename):
        # Ensure the ContentType exists for the Machina permission app
        # Machina permissions are logically tied to the 'forum_permission' app label
        content_type, _ = ContentType.objects.get_or_create(
            app_label='forum_permission', 
            model='forumpermission'
        )

        # Get or create the specific permission
        # We use get_or_create here to bypass the DoesNotExist error entirely
        perm, created = Permission.objects.get_or_create(
            codename=perm_codename,
            content_type=content_type,
            # defaults={'name': 'Can lock topics'}
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f"Created missing permission: {perm.codename}"))

        # Assign the permission to the group
        if not group.permissions.filter(id=perm.id).exists():
            group.permissions.add(perm)
            self.stdout.write(self.style.SUCCESS(f"Successfully added {perm.codename} to {group.name} group"))

    def handle(self, *args, **options):
        User = get_user_model()
        username = options["username"]

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(f'No user found with username="{username}"')

        group_name = "site_admin"

        # try:
        #     group_get = Group.objects.get()
        #     print(f"Group '{group_name}' already exists")
        # except Group.DoesNotExist:
        #     print(f"Group '{group_name}' does not exist; creating it and adding permissions")

        group, _ = Group.objects.get_or_create(name=group_name)

        self.add_group_permissions(group)

        user.groups.add(group)

        self.stdout.write(self.style.SUCCESS(
            f'User "{user.username}" added to group "site_admin".'
        ))