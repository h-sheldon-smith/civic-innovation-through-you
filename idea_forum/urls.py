from django.urls import path
from . import views

urlpatterns = [
    path('post/<int:post_id>/vote/', views.toggle_post_upvote, name="toggle_post_upvote"),
]