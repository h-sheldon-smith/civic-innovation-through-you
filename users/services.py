from django import forms
from service_objects.services import Service
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from machina.core.db.models import get_model

from common.choices import RES_GROUP_NAME, MOD_GROUP_NAME, ADMIN_GROUP_NAME

class GetOrCreateUser(Service):
    username = forms.CharField(max_length=255)
    email = forms.EmailField()
    password = forms.CharField(max_length=255)

    def process(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        User = get_user_model()

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            created = False
        else:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )

            created = True
        
        return user, created

class GetOrCreateResidentUser(Service):
    username = forms.CharField(max_length=255)
    email = forms.EmailField()
    password = forms.CharField(max_length=255)

    def process(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        user, created = GetOrCreateUser.execute({
            'username': username,
            'email': email,
            'password': password,
        })

        user, promoted = PromoteUserToGroup.execute({
            'username': username,
            'group_name': RES_GROUP_NAME,
        })

        return user, created

class GetOrCreateModUser(Service):
    username = forms.CharField(max_length=255)
    email = forms.EmailField()
    password = forms.CharField(max_length=255)

    def process(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        user, created = GetOrCreateUser.execute({
            'username': username,
            'email': email,
            'password': password,
        })

        user, promoted_a = PromoteUserToGroup.execute({
            'username': username,
            'group_name': MOD_GROUP_NAME,
        })

        user, promoted_b = PromoteUserToGroup.execute({
            'username': username,
            'group_name': ADMIN_GROUP_NAME,
        })

        return user, created, promoted_a or promoted_b

class PromoteUserToGroup(Service):
    username = forms.CharField(max_length=255)
    group_name = forms.CharField(max_length=255)

    def process(self):
        username = self.cleaned_data['username']
        group_name = self.cleaned_data['group_name']

        User = get_user_model()
        user = User.objects.get(username=username)

        if not user.groups.filter(name=group_name).exists():
            if not Group.objects.filter(name=group_name).exists():
                if group_name == MOD_GROUP_NAME:
                    CreateModGroupWithPermissions.execute({})
                elif group_name == ADMIN_GROUP_NAME:
                    CreateAdminGroup.execute({})
                elif group_name == RES_GROUP_NAME:
                    CreateResidentGroup.execute({})

            group = Group.objects.get(name=group_name)
            user.groups.add(group)

            promoted = True
        else:
            promoted = False

        return user, promoted
    
class CreateResidentGroup(Service):
    def process(self):
        group, _ = Group.objects.get_or_create(name=RES_GROUP_NAME)
        return group
    
class CreateAdminGroup(Service):
    def process(self):
        group, _ = Group.objects.get_or_create(name=ADMIN_GROUP_NAME)
        return group

class CreateModGroupWithPermissions(Service):
    def process(self):
        group, created = Group.objects.get_or_create(name=MOD_GROUP_NAME)

        if created:
            self.add_group_permissions(group)

        return group
    
    def add_group_permissions(self, group):
        # Machina's permissions are in a Machina-specific internal permission table, ForumPermission
        ForumPermission = get_model('forum_permission', 'ForumPermission')
        GroupForumPermission = get_model('forum_permission', 'GroupForumPermission')

        perm_names = []
        # topic creation
        perm_names += ["can_start_new_topics", "can_post_announcements", "can_post_stickies"]
        # poll creation
        perm_names += ["can_create_polls"]
        # forum moderation
        perm_names += ["can_lock_topics", "can_move_topics", "can_edit_posts", "can_delete_posts", "can_reply_to_locked_topics"]
        # can post without AutoMod screening
        perm_names += ["can_post_without_approval"]
        
        for perm_codename in perm_names:
            # add Machina permission to Machina's internal ForumPermission table (instead of the general Django Group.permissions table)
            try:
                forum_perm = ForumPermission.objects.get(codename=perm_codename)
            except ForumPermission.DoesNotExist:
                # self.stdout.write(f"Machina permission {perm_codename} not found; make sure Django-Machina is installed, run manage.py migrate and try again")
                return

            perm, created = GroupForumPermission.objects.get_or_create(
                group=group,
                permission=forum_perm,
                forum=None, # global, apply to all forums
                has_perm=True
            )