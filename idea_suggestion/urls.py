from django.urls import path
from . import views

# Define a list of url patterns

urlpatterns = [
    # route (what goes in browser), the view that will populate, what we're calling it
    # use the name in the templates
    path('admin/inbox/', views.CityAdmin_Idea_Inbox_View, name = 'admin_idea_inbox'),
    path('admin/idea_detail/<int:pk>/', views.CityAdmin_Idea_Detail, name = 'admin_idea_detail'),
    path('admin/inbox_smart_summary/', views.CityAdmin_Inbox_Smart_Summary_View, name = 'admin_inbox_smart_summary'),
    path('resident/submission/', views.Resident_Idea_Submission_View, name = 'resident_idea_submission')
]