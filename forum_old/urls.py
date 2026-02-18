from django.urls import path
from . import views

urlpatterns = [
    path("forum/placeholder", views.Forum_Placeholder_View, name = "forum_placeholder")
]