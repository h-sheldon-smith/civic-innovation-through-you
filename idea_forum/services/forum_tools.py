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
            # with transaction.atomic():
            post.approved = True
            # post.save() updates the topic/forum trackers internally
            post.save()
            # post.refresh_from_db()

            posts_count = Post.objects.filter(topic=post.topic, approved=True).count()
            total_posts_in_db = Post.objects.all().count()
            posts_this_topic_any_status = Post.objects.filter(topic=post.topic).count()

            print(f"Total Posts in DB: {total_posts_in_db}")
            print(f"Total Posts in this Topic (any status): {posts_this_topic_any_status}")
            print(f"Approved Posts in this Topic: {posts_count}")
            # print(f"post.position(): {post.position()}")

            post.topic.posts_count = posts_count
            post.topic.save()

            post.topic.forum.posts_count = posts_count
            post.topic.forum.save()

            post.save()
            
            print(f"post.approved = {post.approved}")
            return True
            
        return False

    def disapprove_post(self, post):
        print("disapproving post")
        # post.delete() updates the topic/forum trackers internally
        post.delete()
        return True