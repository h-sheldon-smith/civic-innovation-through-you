from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import datetime, timezone
from smart_functionality import converters, batching
from idea_suggestion.models import Idea

class TestBatching(TestCase):
    def setUp(self):

        self.batch_size = 500
        self.task = "test task: do something."

        User = get_user_model()

        self.user = User.objects.create_user(
            username="test-resident",
            password="test-password-1234",
            email="test@email.com"
        )

        self.idea1 = Idea(
                resident = self.user,
                subject_line = "test subject line 1",
                topic = "test topic 1",
                location = "test location 1",
                message = "Test 1 sentence. Test 1 question? Test 1 exclamation!",
                time_stamp = datetime(2026, 1, 1, 11, 55, 55, tzinfo=timezone.utc)
            )
        
        self.idea2 = Idea(
                resident = self.user,
                subject_line = "test subject line 2",
                topic = "test topic 2",
                location = "test location 2",
                message = "Test 2 sentence. Test 2 question? Test 2 exclamation!",
                time_stamp = datetime(2026, 1, 1, 11, 55, 55, tzinfo=timezone.utc)
            )
        
        self.idea3 = Idea(
                resident = self.user,
                subject_line = "test subject line 3",
                topic = "test topic 3",
                location = "test location 3",
                message = "Test 3 sentence. Test 3 question? Test 3 exclamation!",
                time_stamp = datetime(2026, 1, 1, 11, 55, 55, tzinfo=timezone.utc)
            )
        
        self.idea4 = Idea(
                resident = self.user,
                subject_line = "test subject line 4",
                topic = "test topic 4",
                location = "test location 4",
                message = "Test 4 sentence. Test 4 question? Test 4 exclamation!",
                time_stamp = datetime(2026, 1, 1, 11, 55, 55, tzinfo=timezone.utc)
            )
        
        self.idea_wildcard = Idea(
                resident = self.user,
                subject_line = "test subject line wildcard",
                topic = "test topic wildcard",
                location = "test location wildcard",
                message = "Test wildcard sentence. Test wildcard question? Test wildcard exclamation!",
                time_stamp = datetime(2026, 1, 1, 11, 55, 55, tzinfo=timezone.utc)
            )
        
        self.batch_empty, self.count_empty = batching.Batch_Data(self.batch_size, [], self.task)
        self.batch_single, self.count_single = batching.Batch_Data(self.batch_size, [self.idea1], self.task)
        self.batch_multi, self.count_multi = batching.Batch_Data(self.batch_size, 
                                                                 [self.idea1, 
                                                                  self.idea2, 
                                                                  self.idea3, 
                                                                  self.idea4, 
                                                                  self.idea_wildcard], 
                                                                  self.task)


    # Test that no unexpected values are generated from empty data
    def test_empty_data(self):
        self.assertFalse(self.batch_empty)
        self.assertFalse(self.count_empty)


    # Tests the size of batch (number of chars) vs size requirements
    def test_batch_size(self):
        self.assertLessEqual(len(self.batch_single[0]), self.batch_size)
        for batch in self.batch_multi:
            self.assertLessEqual(len(batch), self.batch_size)


    # Tests the quantities for batches and count
    def test_batch_number(self):
        self.assertEqual(len(self.count_empty), len(self.batch_empty))
        self.assertEqual(len(self.batch_empty), 0)
        self.assertEqual(len(self.count_empty), 0)

        self.assertEqual(len(self.count_single), len(self.batch_single))
        self.assertEqual(len(self.batch_single), 1)
        self.assertEqual(len(self.count_single), 1)

        self.assertEqual(len(self.count_multi), len(self.batch_multi))
        self.assertEqual(len(self.batch_multi), 3)
        self.assertEqual(len(self.count_multi), 3)


    # Tests the number of data inputs per batch
    def test_batch_weight(self):
        self.assertEqual(self.count_single[0], 1)

        expected_multi = [2, 2, 1]
        for index, count in enumerate(self.count_multi):
            self.assertEqual(count, expected_multi[index])


    # Tests output type of batches
    def test_batch_type(self):
        self.assertIsInstance(self.batch_single[0], str)

        for batch in self.batch_multi:
            self.assertIsInstance(batch, str)


    # Tests that output in batches matches expected output
    def test_batch_output(self):
        expected_single = self.task + " " + converters.Convert_Data(self.idea1)
        self.assertEqual(self.batch_single[0], expected_single)

        expected_multi_0 = self.task + " " + converters.Convert_Data(self.idea1) + converters.Convert_Data(self.idea2)
        self.assertEqual(self.batch_multi[0], expected_multi_0)

        expected_multi_1 = self.task + " " + converters.Convert_Data(self.idea3) + converters.Convert_Data(self.idea4)
        self.assertEqual(self.batch_multi[1], expected_multi_1)

        expected_multi_2 = self.task + " " + converters.Convert_Data(self.idea_wildcard)
        self.assertEqual(self.batch_multi[2], expected_multi_2)