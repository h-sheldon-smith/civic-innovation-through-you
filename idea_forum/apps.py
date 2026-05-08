from django.apps import AppConfig
from transformers import pipeline

class IdeaForumConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'idea_forum'

    tranformer_pipe = None

    def ready(self):
        import idea_forum.signals

        if self.tranformer_pipe is None:
            self.tranformer_pipe = pipeline(model="facebook/bart-large-mnli")
            # self.tranformer_pipe("test", candidate_labels=["a"])