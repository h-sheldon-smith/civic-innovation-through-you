from django.db import transaction
from machina.core.db.models import get_model

from smart_functionality import converters

Post = get_model('forum_conversation', 'Post')

class ForumInteractionService:
    # returns the raw text
    def get_post_text(self, post_id):
        post = Post.objects.get(pk=post_id)
        
        if hasattr(post.content, 'raw'):
            text = post.content.raw
        else:
            text = str(post.content)

        raw_text = converters.Convert_Data(text)
        return raw_text
    
    def approve_post(self, post_id):
        # within an atomic transaction to prevent race condition
        with transaction.atomic():
            post = Post.objects.select_for_update().get(pk=post_id)
            if not post.approved: # prevent race condition
                post.approved == True
                post.save()
                
                # update the post's thread's and forum container's trackers
                post.topic.update_trackers()
                post.topic.forum.update_trackers()
                
                return True
            
        return False

    def disapprove_post(self, post_id):
        try:
            post = Post.objects.get(pk=post_id)

            post.delete()

            post.topic.update_trackers()
            post.topic.forum.update_trackers()
            
            return True
        except Post.DoesNotExist:
            return False