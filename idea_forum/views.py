from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import login_required
from machina.apps.forum.models import Forum

from django.contrib import messages
from machina.apps.forum_conversation.views import PostCreateView as BasePostCreateView

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