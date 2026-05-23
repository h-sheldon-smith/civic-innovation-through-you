from django.urls import path
from . import views

urlpatterns = [
    path({'forum/posts/<int:post_id>/vote/'}, views.vote_post, name="vote_post"),
]