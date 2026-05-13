from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from . import forms
from idea_suggestion.admin_inbox_services import Admin_Inbox_Data_Controls, Admin_Mark_Read
from idea_suggestion.models import Idea
from idea_suggestion.smart_summary import Get_Smart_Inbox_Summary

# Create your views here (http request/response handling)
# Don't forget to update urls.py

# Popup form for residents to fill out
def Resident_Idea_Submission_View(request):
    #processing goes here: can look things up in DB, render HTML template
    if request.method == 'POST':
        try:
            if request.user.is_authenticated and request.user.moderation.is_restricted():
                return JsonResponse({"success": False, "error": "muted"})
        except Exception:
            pass

        idea_form = forms.SubmitIdeaForm(request.POST, request.FILES) # make an idea submission using the request.POST contents

        # django checks that required fields are present, data type is correct, check against constraints specified in the model
        if idea_form.is_valid():
            idea_instance = idea_form.save(commit = False) # django makes an instance of the form
            idea_instance.resident = request.user # add the logged in user
            idea_instance.save()
           
            return JsonResponse({"success": True})
        
        else:
            return JsonResponse({"success": False})

    idea_form = forms.SubmitIdeaForm()

    return render(request, 'ideas/ideas_resident.html', {'idea_form': idea_form})


# City Admin Inbox for viewing suggestions sent in by residents
@permission_required("users.can_admin_site", raise_exception=True)
def CityAdmin_Idea_Inbox_View(request):
    ideas, filter, sort, search = Admin_Inbox_Data_Controls(request)    

    return render(request, 'ideas/ideas_city_admin_inbox.html', {'ideas': ideas, 'sort': sort, 'filter': filter, 'search': search})


# City Admin idea detail page
# Updates an idea status to read and navigates to a detail page to display contents
@permission_required("users.can_admin_site", raise_exception=True)
def CityAdmin_Idea_Detail(request, pk):
    idea = Admin_Mark_Read(Idea.objects.get(pk=pk))

    return render(request, 'ideas/ideas_admin_detail.html', {'idea': idea})


# Popup for smart summary
def CityAdmin_Inbox_Smart_Summary_View(request):
    ideas, filter, sort, search = Admin_Inbox_Data_Controls(request) 
    status, summary = Get_Smart_Inbox_Summary(ideas)

    data = {
        "status": status,
        "summary": summary
    }

    if status:
        Admin_Mark_Read(ideas)

    return JsonResponse(data)