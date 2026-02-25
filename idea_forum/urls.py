from django.urls import path
from . import views

urlpatterns = [
    path("forum_foo/", views.Idea_Forum_View, name="my_forum_template"),
    path("forum_boardbase/", views.BoardBase_View, name="idea_forum_board_base"),
]