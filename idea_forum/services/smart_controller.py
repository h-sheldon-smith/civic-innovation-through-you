from smart_functionality.pipeline import Ask_AI

from idea_forum.services.moderation import ModerationService
from idea_forum.services.prompts import MOD_SCREEN_TASK, MOD_SCREEN_FORMAT

# might change this to a celery task later on (so it's an async task)
class SmartController:
    def run_smart_post_moderation(post_id):
        modservice = ModerationService()

        post_text = modservice.get_post_text(post_id)

        response = Ask_AI(MOD_SCREEN_TASK, MOD_SCREEN_FORMAT, post_text)

        if response == "Accept":
            modservice.approve_post(post_id)
        elif response == "Reject":
            modservice.disapprove_post(post_id)
        else:
            return False