# wordlist-based checker (plus leetspeek-style substitutions)
# from better_profanity import profanity

# ML-based checker (linear SVM)
import profanity_check

# LLM-based checker
# from smart_functionality import pipeline
# from idea_forum.services.prompts import SCREEN_POST

# 3 options, currently I'm using the ML checker to screen for profanity only
class ScreeningService:
    def screen_post_text(self, post_text):
        result = self.screen_pass_profanity(post_text)

        # response = pipeline.Ask_AI(SCREEN_POST['task'], SCREEN_POST['format'], post_text)
        # llm_result = (response == SCREEN_POST['true'])

        return result
    
    def screen_pass_profanity(self, post_text):
        # # wordlist-based checker, also handles leetspeek-style 'obfuscated profanity'
        # wordlist_result = profanity.contains_profanity(post_text)

        # ML-based checker, doesn't handle leetspeek-style 'obfuscated profanity'
        ml_result = bool(profanity_check.predict(post_text)[0])

        return ml_result