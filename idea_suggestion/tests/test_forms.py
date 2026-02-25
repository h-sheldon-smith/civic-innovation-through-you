from django.test import TestCase
from idea_suggestion.forms import SubmitIdeaForm
from common.choices import Topic_Options

class TestForms(TestCase):
    def test_idea_form_is_valid(self):
        form = SubmitIdeaForm(data={
            'subject_line': 'test subject line',
            'location': 'test location',
            'topic': Topic_Options.ART,
            'message': 'test message'

        })
        self.assertTrue(form.is_valid())

    def test_idea_form_empty(self):
        form = SubmitIdeaForm(data={
            'subject_line': '',
            'location': '',
            'topic': '',
            'message': ''

        })
        self.assertFalse(form.is_valid())

    def test_idea_form_illegal_topic(self):
        form = SubmitIdeaForm(data={
            'subject_line': 'test subject line',
            'location': 'test location',
            'topic': 'Test',
            'message': 'test message'

        })
        self.assertFalse(form.is_valid())