from idea_forum.services.forum_tools import ForumInteractionService
from idea_forum.services.screening_tools import ScreeningService

# TODO: change this to a celery task later on, so it's an async task
class SmartController:
    def run_smart_post_moderation(self, post):
        forum_tools = ForumInteractionService()
        screening_tools = ScreeningService()

        post_text = forum_tools.get_post_text(post)
        flagged = screening_tools.screen_post_text(post_text)

        if not flagged:
            forum_tools.approve_post(post)
        else:
            forum_tools.disapprove_post(post)