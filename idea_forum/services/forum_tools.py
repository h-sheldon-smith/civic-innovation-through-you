from django.db import transaction
from machina.core.db.models import get_model

from smart_functionality import converters

Post = get_model('forum_conversation', 'Post')

class ForumInteractionService:
    # returns the raw text
    def get_post_text(self, post):
        if hasattr(post.content, 'raw'):
            text = post.content.raw
        else:
            text = str(post.content)

        raw_text = converters.Convert_Data(text)
        return raw_text
    
    def approve_post(self, post):
        if not post.approved: # prevent race condition
            print("approving post")

            post.approved = True
            post.save(update_fields=['approved'])
            
            # using save() breaks the post UI view's URl redirect, but
            # bypassing the save method and directly doing a SQL-level update
            # also breaks the UI's URL redirect
            # Post.objects.filter(pk=post.id).update(approved=True)
            # post.refresh_from_db()

            post.topic.update_trackers()
            post.topic.forum.update_trackers()

            print(f"post.approved = {post.approved}")
            return True
            
        return False

    def disapprove_post(self, post):
        print("disapproving post")
        post.delete()

        post.topic.update_trackers()
        post.topic.forum.update_trackers()
        return True