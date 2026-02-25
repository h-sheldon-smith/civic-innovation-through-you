from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime
from freezegun import freeze_time
from common.choices import Topic_Options
from idea_suggestion.models import Idea

# Test Methods
class TestMethods(TestCase):
    @freeze_time("2026-01-01 11:55:55")
    def setUp(self):
        self.idea = Idea.objects.create(
            subject_line = "test subject line",
            topic = Topic_Options.ART,
            location = "test location",
            message = "test message"
        )

        User = get_user_model()

        self.user = User.objects.create_user(
            username="test-resident",
            password="test-password-1234",
            email="test@email.com"
        )

    def test__str__no_resident(self):
        expected = "Topic: Art, From: None, Subject: test subject line, Time: 2026-01-01 11:55:55"
        self.assertEquals(str(self.idea), expected)
    
    def test__str__with_resident(self):
        self.idea.resident = self.user
        expected = "Topic: Art, From: test-resident, Subject: test subject line, Time: 2026-01-01 11:55:55"
        self.assertEquals(str(self.idea), expected)

    def test__get_resident__no_resident(self):
        expected = None
        self.assertEquals(self.idea.get_resident(), expected)

    def test__get_resident__with_resident(self):
        self.idea.resident = self.user
        expected = "test-resident"
        self.assertEquals(self.idea.get_resident(), expected)

class TestFields(TestCase):
    @freeze_time("2026-01-01 11:55:55")
    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="test-resident",
            password="test-password-1234",
            email="test@email.com"
        )   

        self.idea = Idea.objects.create(
            resident = self.user,
            subject_line = "test subject line",
            topic = Topic_Options.ART,
            location = "test location",
            message = "test message"
        )

    # Test Relationships with Foreign Key(s)
    def test_delete_user(self):
        expected = None
        self.user.delete()
        self.idea.refresh_from_db()
        self.assertEquals(self.idea.resident, expected)
    
    # Test Ennum Fields Won't Allow Incorrect Values
    def test_topic_valid(self):
        an_idea = Idea.objects.create(
                topic = "random",
                location = "test location",
                message = "test message"
            )

        with self.assertRaises(ValidationError):
            an_idea.full_clean()

    # Test Default Value(s)
    def test_time_stamp_default_value(self):
        expected = timezone.make_aware(datetime(2026, 1, 1, 11, 55, 55))
        self.assertEquals(self.idea.time_stamp, expected)

    def test_read_status_default_value(self):
        expected = False
        self.assertEquals(self.idea.read_status, expected)

    def test_file_location_default_value(self):
        expected = 'Inbox'
        self.assertEquals(self.idea.file_location, expected)            