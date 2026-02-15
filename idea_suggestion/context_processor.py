from . import forms

def idea_form_processor(request):
    return{ "idea_form": forms.SubmitIdeaForm()}
