from django.urls import path
from . import views

# Define a list of url patterns
urlpatterns = [
    path('admin/inbox/', views.CityAdmin_Idea_Review_View, name = 'admin_idea_inbox'),
    path('resident/submission/', views.Resident_Idea_Submission_View, name = 'resident_idea_submission')
]