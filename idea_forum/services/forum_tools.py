from django.db import transaction
# from machina.core.db.models import get_model

from smart_functionality import converters

# Post = get_model('forum_conversation', 'Post')

class ForumInteractionService:
    # returns the raw text
    def get_post_text(self, post):
        if hasattr(post.content, 'raw'):
            text = post.content.raw
        else:
            text = str(post.content)

        raw_text = converters.Convert_Data(text, [])
        return raw_text