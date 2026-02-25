from django.test import TestCase,Client
from django.urls import reverse
from idea_suggestion.models import Idea
from common.choices import Topic_Options

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

        #use when the url contains a pk
        self.idea = Idea.objects.create(
            subject_line = "test subject line",
            topic = Topic_Options.ART,
            location = "test location",
            message = "test message"
        )

    # Core Tests
    def check_status_code(self, actual):
        self.assertEquals(actual, 200)

    def check_template(self, actual, expected):
        self.assertTemplateUsed(actual, expected)

    # Test Views
    def test_resident_submission(self):
        expected_template = 'ideas/ideas_resident.html'
        response = self.client.get(reverse('resident_idea_submission'))
        self.check_status_code(response.status_code)
        self.check_template(response, expected_template)
        

    def test_admin_inbox(self):
        expected_template = 'ideas/ideas_resident.html'
        response = self.client.get(reverse('admin_idea_inbox'))
        self.check_status_code(response.status_code)
        self.check_template(response, expected_template)

    def test_admin_idea_detail(self):
        expected_template = 'ideas/ideas_admin_detail.html'
        response = self.client.get(reverse('admin_idea_detail', kwargs={'pk': self.idea.pk}))
        self.check_status_code(response.status_code)
        self.check_template(response, expected_template)