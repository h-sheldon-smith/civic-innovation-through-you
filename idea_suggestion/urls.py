from django.urls import path
from . import views

# Define a list of url patterns

urlpatterns = [
    # route (what goes in browser), the view that will populate, what we're calling it
    # use the name in the templates
    path('admin/inbox/', views.CityAdmin_Idea_Inbox_View, name = 'admin_idea_inbox'),
    path('resident/submission/', views.Resident_Idea_Submission_View, name = 'resident_idea_submission')
]