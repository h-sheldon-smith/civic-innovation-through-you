# from django.shortcuts import render, get_object_or_404
# from django.http import JsonResponse
# from django.contrib.auth.decorators import login_required
# from django.views.decorators.http import require_POST
# from machina.core.db.models import get_model

# from django.contrib import messages
# from machina.apps.forum.models import Forum
# from machina.apps.forum_conversation.views import PostCreateView as BasePostCreateView

# Post = get_model('forum_conversation', 'Post')

# # like or unlike the post
# @login_required
# @require_POST
# def vote_post(request, post_id):
#     post = get_object_or_404(Post, pk=post_id)
#     user_id = request.user.id

#     # if the user hasn't voted already
#     if post.votes.exists(user_id):
#         post.votes.down(user_id) # removes the upvote (not Reddit-style)
#         voted = False
#     else:
#         post.votes.up(user_id)
#         voted = True

#     return JsonResponse({
#         'voted': voted,
#         'post_total_votes': post.vote_count,
#     })


# class PostCreateView(BasePostCreateView):
#     def get_success_url(self):
#         print("get_success_url")

#         # if post has been deleted by the auto-screening
#         if not self.model.objects.filter(pk=self.object.pk).exists():
#             print("overriding messages for deletion message")

#             storage = messages.get_messages(self.request)
#             # this consumes all existing messages
#             for message in storage:
#                 pass
            
#             # add the deletion message
#             messages.warning(self.request, "Your post was flagged by our automated moderation and removed. Reason: profanity.")
            
#             # redirect to the topic instead of the (now deleted) post
#             return self.object.topic.get_absolute_url()
            
#         return super().get_success_url()
        
#     # def get_success_message(self, cleaned_data):
#     #     if not self.model.objects.filter(pk=self.object.pk).exists():
#     #         return None
#     #     return super().get_success_message(cleaned_data)