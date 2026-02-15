from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from . import forms

# Create your views here (http request/response handling)
# Don't forget to update urls.py

# Popup form for residents to fill out
# TODO: Make sure the resident sending is attached to this
def Resident_Idea_Submission_View(request):
    #processing goes here: can look things up in DB, render HTML template
    if request.method == 'POST':
        idea_form = forms.SubmitIdeaForm(request.POST) # make an idea submission using the request.POST contents

        # django checks that required fields are present, data type is correct, check against constraints specified in the model
        if idea_form.is_valid():
            idea_form.save() # django makes an instance and writes to the database

            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False})

    idea_form = forms.SubmitIdeaForm()

    # parameters: request, the template that will use this, the data for the template
    # optional: content_type (type for resulting doc, default is text/html), 
    # optional: status (default code 200), using (template engine name)
    return render(request, 'ideas/ideas_resident.html', {'idea_form': idea_form})






# City Admin Inbox for viewing suggestions sent in by residents
def CityAdmin_Idea_Inbox_View(request):
    return HttpResponse("Idea Suggestion Placeholder")