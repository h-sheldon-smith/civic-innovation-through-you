import strip_markdown

# ML-based checker (linear SVM)
import profanity_check

# LLM-based checker
# from smart_functionality import pipeline
# from idea_forum.services.prompts import SCREEN_POST

class ScreeningService:
    def screen_post_text(self, post_text):
        profanity_check_result = self.profanity_check(post_text)
        
        # llm_pass_result = self.screen_pass_llm(self, post_text)
        
        return profanity_check_result
    
    def profanity_check(self, post_text):
        print(f"post_text = {post_text}")

        cleaned_text = strip_markdown.strip_markdown(post_text)

        print(f"cleaned_text = {cleaned_text}")

        # ML-based pofanity detection, doesn't handle leetspeek-style 'obfuscated profanity'
        result = not bool(profanity_check.predict([cleaned_text])[0])

        print(f"profanity_checker_result = {result}")

        return result
     
    # def screen_pass_llm(self, post_text):
    #     response = pipeline.Ask_AI(SCREEN_POST['task'], SCREEN_POST['format'], post_text)
    #     llm_result = (response == SCREEN_POST['true'])
    #     return llm_result