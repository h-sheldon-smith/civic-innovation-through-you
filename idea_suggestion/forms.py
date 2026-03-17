from django import forms
from . import models
from common.choices import Topic_Options

# A form for users to fillout so they can submit their ideas
class SubmitIdeaForm(forms.ModelForm):
    class Meta:
        # Use a model you created and choose which of its fields you want to explicitly use
        model = models.Idea
        fields = ['subject_line', 'location', 'topic', 'message', 'picture']


# A form used for filtering city admin inbox options
class IdeaFilterForm(forms.Form):
    topic_filter = forms.MultipleChoiceField(
        choices = Topic_Options.choices,
        required = False,
        widget = forms.CheckboxSelectMultiple
    )

    read_filter = forms.ChoiceField(
        choices = [("", "All"), ("True", True), ("False", False)],
        required = False)
    
# A form used for sorting city admin inbox options
class IdeaSortForm(forms.Form):
    sort_options = forms.ChoiceField(
        choices = [
            ("", "Auto"),
            ("topic", "Topic (A-Z)"),
            ("-topic", "Topic (Z-A)"),
            ("subject_line", "Subject Line (A-Z)"),
            ("-subject_line", "Subject Line (Z-A)"),
            ("time_stamp", "Date (Oldest)"),
            ("-time_stamp", "Date (Newest)"),
            ("read_status", "Unread"),
            ("-read_status", "Read")
        ],
        required = False
    )

#A form used to search for terms in the city admin inbox
class IdeaSearchForm(forms.Form):
    subject_search = forms.CharField(max_length = 50, required = False)
    content_search = forms.CharField(max_length = 50, required = False)