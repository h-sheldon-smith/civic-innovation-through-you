from django.apps import AppConfig
from machina.apps.forum_conversation.apps import ForumConversationAppConfig as BaseForumConversationAppConfig

class ForumConversationAppConfig(BaseForumConversationAppConfig):
    name = 'forum_conversation'
    default = True
    # default_auto_field = 'django.db.models.BigAutoField'