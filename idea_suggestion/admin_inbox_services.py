from django.db.models import QuerySet
from . import forms
from idea_suggestion.models import Idea

# Method to orchestrate view options for admin inbox
# Applies all options (or clears them) as specified by the admin user
# Returns ideas that meet admin-user's specified requirements
#         filter requirements specified by admin-user
#         sort requirements specified by admin-user
#         search requirements specified by admin-user
def Admin_Inbox_Data_Controls(request):
    #query instruction to get all table instances
    ideas = Idea.objects.all()

    #clears all options if specified by admin-user
    if "clear-options" in request.GET:
        filter = forms.IdeaFilterForm()
        sort = forms.IdeaSortForm()
        search = forms.IdeaSearchForm()

    #applies all options as specified by admin-user
    else:
        filter, ideas = Admin_Inbox_Filter(forms.IdeaFilterForm(request.GET), ideas)
        sort, ideas = Admin_Inbox_Sort(forms.IdeaSortForm(request.GET), ideas)
        search, ideas = Admin_Inbox_Search(forms.IdeaSearchForm(request.GET), ideas)

    return ideas, filter, sort, search


# Method to apply admin-user's specified filters
# Returns ideas that meet admin-user's specified filter requirements
#         filter requirements specified by admin-user
def Admin_Inbox_Filter(filter, ideas):
    if filter.is_valid():
        topics = filter.cleaned_data.get('topic_filter')
        read = filter.cleaned_data.get('read_filter')

        if topics:
            ideas = ideas.filter(topic__in=topics)
        if read:
            ideas = ideas.filter(read_status=read)
            
    return filter, ideas

# Method to apply admin-user's specified sort options
# Returns ideas in admin-user's specified order or defaults to time_stamp if other options not selected
#         sort requirements specified by admin-user
def Admin_Inbox_Sort(sort, ideas):
    if sort.is_valid():
        sorting = sort.cleaned_data.get('sort_options')
        if sorting:
            ideas = ideas.order_by(sorting)
        else:
            ideas = ideas.order_by("-time_stamp")

    return sort, ideas

# Method to apply admin-user's specified search options
# Returns ideas that meet admin-user's specified requirements
#         search requirements specified by admin-user
def Admin_Inbox_Search(search, ideas):
    if search.is_valid():
        subject = search.cleaned_data.get('subject_search')
        content = search.cleaned_data.get('content_search')
        to_exclude = []

        #determines which ideas don't meet admin-user requirements
        for idea in ideas:
            if subject and subject not in idea.subject_line:
                to_exclude.append(idea.id)
            if content and content not in idea.message:
                to_exclude.append(idea.id)

        #removes ideas that don't meet admin-user requirements
        if to_exclude:
            ideas = ideas.exclude(id__in=to_exclude)

    return search, ideas

# Method to update an item to read once viewed
def Admin_Mark_Read(idea):
    # more than one idea
    if isinstance(idea, QuerySet):
        idea.update(read_status = True)
        return idea
    
    # one idea
    else:
        idea.read_status = True
        idea.save()
        return idea