from django.test import TestCase
from django.urls import reverse, resolve
from common.choices import Topic_Options
from idea_suggestion.models import Idea
from idea_suggestion.views import CityAdmin_Idea_Inbox_View, CityAdmin_Inbox_Smart_Summary_View, CityAdmin_Idea_Detail, Resident_Idea_Submission_View

# Note: test folder must contain __init__.py
# To run: in cli, type python manage.py test your_app

class TestUrls(TestCase):
    def setUp(self):
        #use when the url contains a pk
        self.idea = Idea.objects.create(
            subject_line = "test subject line",
            topic = Topic_Options.ART,
            location = "test location",
            message = "test message"
        )

    def test_resident_idea_submission_url_resolve(self):
        url = reverse('resident_idea_submission')
        self.assertEquals(resolve(url).func, Resident_Idea_Submission_View) # arg = the name from urls.py path

    def test_admin_inbox_url_resolve(self):
        url = reverse('admin_idea_inbox') 
        self.assertEquals(resolve(url).func, CityAdmin_Idea_Inbox_View)

    def test_admin_smart_summary(self):
        url = reverse('admin_inbox_smart_summary')
        self.assertEquals(resolve(url).func, CityAdmin_Inbox_Smart_Summary_View)

    def test_admin_idea_detail_url_resolve(self):
        url = reverse('admin_idea_detail', kwargs={'pk': self.idea.pk})
        self.assertEquals(resolve(url).func, CityAdmin_Idea_Detail)