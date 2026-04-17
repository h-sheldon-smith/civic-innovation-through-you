from django import forms
from service_objects.services import Service
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from machina.core.db.models import get_model

from common.choices import RES_GROUP_NAME, MOD_GROUP_NAME

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

        # residents have no special permissions, so if group doesn't exist just create it
        group, b = Group.objects.get_or_create(name=RES_GROUP_NAME)
        user.groups.add(group)

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

        user, promoted = PromoteUserToMod.execute({
            'username': username,
        })

        return user, created, promoted

class PromoteUserToMod(Service):
    username = forms.CharField(max_length=255)

    def process(self):
        username = self.cleaned_data['username']

        User = get_user_model()
        user = User.objects.get(username=username)

        if not user.groups.filter(name=MOD_GROUP_NAME).exists():
            if not Group.objects.filter(name=MOD_GROUP_NAME).exists():
                CreateModGroupWithPermissions.execute()

            group = Group.objects.get(name=MOD_GROUP_NAME)
            user.groups.add(group)

            promoted = True
        else:
            promoted = False

        return user, promoted

class CreateModGroupWithPermissions(Service):
    def process(self):
        group, created = Group.objects.get_or_create(name=MOD_GROUP_NAME)

        if created:
            self.add_group_permissions(self, group)

        return group
    
    def add_group_permissions(self, group):
        # Machina's permissions are in a Machina-specific internal permission table, ForumPermission
        ForumPermission = get_model('forum_permission', 'ForumPermission')
        GroupForumPermission = get_model('forum_permission', 'GroupForumPermission')

        perm_names = []
        # topic creation
        perm_names += ["can_start_new_topics", "can_post_announcements", "can_post_stickies", "can_post_without_approval"]
        # poll creation
        perm_names += ["can_create_polls"]
        # forum moderation
        perm_names += ["can_lock_topics", "can_move_topics", "can_edit_posts", "can_delete_posts", "can_approve_posts", "can_reply_to_locked_topics"]
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
                group=MOD_GROUP_NAME,
                permission=forum_perm,
                forum=None, # global, apply to all forums
                has_perm=True
            )