from django.apps import AppConfig


class IdeaForumConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'idea_forum'

    def ready(self):
        import idea_forum.signals