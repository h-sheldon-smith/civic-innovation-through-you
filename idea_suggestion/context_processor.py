from . import resident_form

def idea_form_processor(request):
    return{ "idea_form": resident_form.SubmitIdea()}
