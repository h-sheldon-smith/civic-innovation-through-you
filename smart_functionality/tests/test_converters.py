from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime, timezone
from smart_functionality import converters
from idea_suggestion.models import Idea

class TestConverters(TestCase):
    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="test-resident",
            password="test-password-1234",
            email="test@email.com"
        )

        self.idea = Idea(
                resident = self.user,
                subject_line = "test subject line",
                topic = "test topic",
                location = "test location",
                message = "Test sentence. Test question? Test exclamation!",
                time_stamp = datetime(2026, 1, 1, 11, 55, 55, tzinfo=timezone.utc)
            )

    def test_converts_string(self):
        string_empty = ""
        result_empty = converters.Convert_Data(string_empty)
        self.assertIsInstance(result_empty, str)
        self.assertEqual(result_empty, "")

        string = "Test message."
        result = converters.Convert_Data(string)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "Test message.")

    def test_converts_integers(self):
        zero = 0
        result_zero = converters.Convert_Data(zero)
        self.assertIsInstance(result_zero, str)
        self.assertEqual(result_zero, "0")

        num_integer = 123456
        result_int = converters.Convert_Data(num_integer)
        self.assertIsInstance(result_int, str)
        self.assertEqual(result_int, "123456")

    def test_converts_floats(self):
        zero = 0.0
        result_zero = converters.Convert_Data(zero)
        self.assertIsInstance(result_zero, str)
        self.assertEqual(result_zero, "0.0")

        num_integer = 1.23456
        result_int = converters.Convert_Data(num_integer)
        self.assertIsInstance(result_int, str)
        self.assertEqual(result_int, "1.23456")

    def test_converts_bool(self):
        truth = True
        result_true = converters.Convert_Data(truth)
        self.assertIsInstance(result_true, str)
        self.assertEqual(result_true, "True")

        false = False
        result_false = converters.Convert_Data(false)
        self.assertIsInstance(result_false, str)
        self.assertEqual(result_false, "False")

    def test_converts_idea(self):
        idea_no_image = self.idea
        result_no_img = converters.Convert_Data(idea_no_image)

        expected_no_img = (
            "resident: test-resident. subject_line: test subject line. location: test location. "
            "topic: test topic. message: Test sentence. Test question? Test exclamation!. "
            "time_stamp: 2026-01-01 11:55:55+00:00. "
        )

        self.assertIsInstance(result_no_img, str)
        self.assertEqual(result_no_img, expected_no_img)

        self.idea.picture = SimpleUploadedFile("testing123.jpg", b"testfilecontent", content_type="image/jpeg")
        
        idea_w_image = self.idea
        result_w_img = converters.Convert_Data(idea_w_image)

        expected_w_img = (
            "resident: test-resident. subject_line: test subject line. location: test location. "
            "topic: test topic. message: Test sentence. Test question? Test exclamation!. "
            "picture: testing123.jpg. time_stamp: 2026-01-01 11:55:55+00:00. "
        )

        self.assertIsInstance(result_w_img, str)
        self.assertEqual(result_w_img, expected_w_img)