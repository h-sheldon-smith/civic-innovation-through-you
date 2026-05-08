import strip_markdown

# ML-based checker (linear SVM)
import profanity_check

from transformers import pipeline

# from idea_forum.services.ml.MLModels import transformer_pipe
from django.apps import apps

# smart_functionality's LLM
# from smart_functionality import pipeline
# from idea_forum.services.prompts import SCREEN_POST

class ScreeningService:
    # returns True if it's flagged, False if it's ok to post
    def screen_post_text(self, post_text):
        print(f"post_text = {post_text}")

        # we use model cascading
        # profanity_check is faster + more accurate for profanity
        # if not flagged then check with huggingface zero-shot classification for more categories
        profanity_check_result = self.profanity_check_classification(post_text)
        
        if profanity_check_result:
            result = profanity_check_result
            model_name = "profanity_check"
        else:
            candidate_labels = ["profanity", "abuse", "NSFW", "political speech", "spam", "sales"]
            zero_shot_threshold = 0.65
            result = self.zero_shot_classification(post_text, candidate_labels, zero_shot_threshold)
            model_name = "zero-shot classification with transformer"

        print(f"model = {model_name}")
        print(f"result = {result}")

        return result
    
    # linear SVM model for profanity detection only
    def profanity_check_classification(self, post_text):
        cleaned_text = strip_markdown.strip_markdown(post_text)

        # print(f"cleaned_text = {cleaned_text}")

        # ML-based pofanity detection, doesn't handle leetspeek-style 'obfuscated profanity'
        result = bool(profanity_check.predict([cleaned_text])[0])

        return result

    # zero-shot classification using a huggingface transformer fine-tuned on zero-shot classification
    def zero_shot_classification(self, post_text, candidate_labels, threshold):
        pipe = apps.get_app_config('idea_forum').zero_shot_pipeline

        pipe_out = pipe(post_text, candidate_labels=candidate_labels)

        print(pipe_out['labels'])
        print(pipe_out['scores'])
        print(f"threshold = {threshold}")

        return max(pipe_out['scores']) >= threshold

     
    # def screen_pass_smart_functionality_llm(self, post_text):
    #     response = pipeline.Ask_AI(SCREEN_POST['task'], SCREEN_POST['format'], post_text)
    #     llm_result = (response == SCREEN_POST['true'])
    #     return llm_result