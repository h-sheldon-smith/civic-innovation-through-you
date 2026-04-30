# wordlist-based checker (plus leetspeek-style substitutions)
# from better_profanity import profanity

# ML-based checker (linear SVM)
import profanity_check

# LLM-based checker
# from smart_functionality import pipeline
# from idea_forum.services.prompts import POST_SCREEN

# 3 options, currently I'm using the ML checker
class ScreeningService:
    def screen_post_text(post_text):
        # # wordlist-based checker, also handles leetspeek-style 'obfuscated profanity'
        # wordlist_result = profanity.contains_profanity(post_text)

        # ML-based checker, doesn't handle leetspeek-style 'obfuscated profanity'
        ml_result = bool(profanity_check.predict(post_text)[0])

        # response = pipeline.Ask_AI(POST_SCREEN['task'], POST_SCREEN['format'], post_text)
        # llm_result = (response == POST_SCREEN['true'])

        return ml_result