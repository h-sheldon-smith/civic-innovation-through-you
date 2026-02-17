from django import forms
from . import models

# A form for users to fillout so they can submit their ideas
class SubmitIdeaForm(forms.ModelForm):
    class Meta:
        # Use a model you created and choose which of its fields you want to explicitly use
        model = models.Idea
        fields = ['subject_line', 'location', 'topic', 'message']