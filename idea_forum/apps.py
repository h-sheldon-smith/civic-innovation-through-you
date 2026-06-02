from django.apps import AppConfig
import os
from pathlib import Path
from transformers import pipeline

from civic_innovation_through_you.settings import BASE_DIR

class IdeaForumConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'idea_forum'

    ZERO_SHOT_NAME = "facebook/bart-large-mnli"
    ZERO_SHOT_PATH = BASE_DIR / "huggingface_cache" / "zero-shot-classification"
    zero_shot_task = "zero-shot-classification"

    zero_shot_pipeline = None

    def ready(self):
        # set up transformer
        if self.zero_shot_pipeline is None and os.environ.get("RUN_MAIN") == 'true':
            if not self.ZERO_SHOT_PATH.exists():
                self.ZERO_SHOT_PATH.mkdir(parents=True, exist_ok=True)

            if not any(self.ZERO_SHOT_PATH.iterdir()):
                # download model from huggingface to memory
                print(f"Downloading {self.ZERO_SHOT_NAME} from HuggingFace")

                self.zero_shot_pipeline = pipeline(
                    task=self.zero_shot_task,
                    model=self.ZERO_SHOT_NAME,
                )

                # cache a copy of model to disk
                self.zero_shot_pipeline.save_pretrained(str(self.ZERO_SHOT_PATH))

            else:
                # load model from disk
                print(f"Loading {self.ZERO_SHOT_NAME} from local disk")
                self.zero_shot_pipeline = pipeline(
                    task=self.zero_shot_task,
                    model=str(self.ZERO_SHOT_PATH),
                )

            self.zero_shot_pipeline("warmup", candidate_labels=["warmup"])