from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from . import forms
from idea_suggestion.models import Idea

# Create your views here (http request/response handling)
# Don't forget to update urls.py

# Popup form for residents to fill out
def Resident_Idea_Submission_View(request):
    #processing goes here: can look things up in DB, render HTML template
    if request.method == 'POST':
        #try:
            #if request.user.is_authenticated and request.user.moderation.is_restricted():
                #return JsonResponse({"success": False, "error": "muted"})
        #except Exception:
            #pass

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

    # parameters: request, the template that will use this, the data for the template
    # optional: content_type (type for resulting doc, default is text/html), 
    # optional: status (default code 200), using (template engine name)
    return render(request, 'ideas/ideas_resident.html', {'idea_form': idea_form})


# City Admin Inbox for viewing suggestions sent in by residents
@permission_required("users.can_admin_site", raise_exception=True)
def CityAdmin_Idea_Inbox_View(request):

    ideas = Idea.objects.all() #query instruction to get all table instances

    if "clear-options" in request.GET:
        filter = forms.IdeaFilterForm()
        sort = forms.IdeaSortForm()
        search = forms.IdeaSearchForm()

    else:
        filter = forms.IdeaFilterForm(request.GET)
        if filter.is_valid():
            topics = filter.cleaned_data.get('topic_filter')
            read = filter.cleaned_data.get('read_filter')

            if topics:
                ideas = ideas.filter(topic__in=topics)

            if read:
                ideas = ideas.filter(read_status=read) 

        sort = forms.IdeaSortForm(request.GET)
        if sort.is_valid():
            sorting = sort.cleaned_data.get('sort_options')
            if sorting:
                ideas = ideas.order_by(sorting)
            else:
                ideas = ideas.order_by("-time_stamp")

        search = forms.IdeaSearchForm(request.GET)
        if search.is_valid():
            subject = search.cleaned_data.get('subject_search')
            content = search.cleaned_data.get('content_search')
            to_exclude = []

            for idea in ideas:
                if subject and subject not in idea.subject_line:
                    to_exclude.append(idea.id)
                if content and content not in idea.message:
                    to_exclude.append(idea.id)

            if to_exclude:
                ideas = ideas.exclude(id__in=to_exclude)
            
    return render(request, 'ideas/ideas_city_admin_inbox.html', {'ideas': ideas, 'sort': sort, 'filter': filter, 'search': search})



# City Admin idea detail page
# Updates an idea status to read and navigates to a detail page to display contents
@permission_required("users.can_admin_site", raise_exception=True)
def CityAdmin_Idea_Detail(request, pk):
    idea = Idea.objects.get(pk=pk)
    idea.read_status = True
    idea.save()
    return render(request, 'ideas/ideas_admin_detail.html', {'idea': idea})