from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import forms
from .models import Idea

# Create your views here (http request/response handling)
# Don't forget to update urls.py

# Popup form for residents to fill out
def Resident_Idea_Submission_View(request):
    #processing goes here: can look things up in DB, render HTML template
    if request.method == 'POST':
        idea_form = forms.SubmitIdeaForm(request.POST) # make an idea submission using the request.POST contents

        # django checks that required fields are present, data type is correct, check against constraints specified in the model
        if idea_form.is_valid():
            idea_instance = idea_form.save(commit = False) # django makes an instance of the form
            idea_instance.resident = request.user # add the logged in user
            idea_instance.save()
           
            return JsonResponse({"success": True})
        
        else:
            return JsonResponse({"success": False})

    idea_form = forms.SubmitIdeaForm()

    # parameters: request, the template that will use this, the data for the template
    # optional: content_type (type for resulting doc, default is text/html), 
    # optional: status (default code 200), using (template engine name)
    return render(request, 'ideas/ideas_resident.html', {'idea_form': idea_form})



# City Admin Inbox for viewing suggestions sent in by residents
# @permission_required("users.can_admin_site", raise_exception=True)
def CityAdmin_Idea_Inbox_View(request):
    ideas = Idea.objects.all().order_by('-time_stamp') #grab all entries from the Idea table
    return render(request, 'ideas/ideas_city_admin_inbox.html', {'ideas': ideas})

# City Admin idea detail page
# Updates an idea status to read and navigates to a detail page to display contents
# @permission_required("users.can_admin_site", raise_exception=True)
def CityAdmin_Idea_Detail(request, pk):
    idea = Idea.objects.get(pk=pk)
    idea.read_status = True
    idea.save()
    return render(request, 'ideas/ideas_admin_detail.html', {'idea': idea})