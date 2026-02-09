from django.shortcuts import render
from django.http import HttpResponse

# Create your views here (http request/response)
# Don't forget to update urls.py

# Popup form for residents to fill out
def Resident_Idea_Submission_View (request):
    return HttpResponse("Idea Suggestion Placeholder")

# City Admin Inbox for viewing suggestions sent in by residents
def CityAdmin_Idea_Review_View (request):
    return HttpResponse("Idea Suggestion Placeholder")