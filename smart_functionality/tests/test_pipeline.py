from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import datetime, timezone
import re
from smart_functionality import batching, pipeline, constants
from idea_suggestion.models import Idea

class TestBatching(TestCase):
    def setUp(self):
        self.batch_size = 500
        self.task = "test task: do something."
        self.format = "test format: some formatting."
        self.hard_limit = 5

        User = get_user_model()

        self.user = User.objects.create_user(
            username="test-resident",
            password="test-password-1234",
            email="test@email.com"
        )

        self.idea0 = Idea(
                resident = self.user,
                subject_line = "test subject line 0",
                topic = "test topic 0",
                location = "test location 0",
                message = "Test 0 sentence. Test 0 question? Test 0 exclamation!",
                time_stamp = datetime(2026, 1, 1, 11, 55, 55, tzinfo=timezone.utc)
            )
        
        base_size = len(str(self.idea0)) / self.batch_size
        
        self.data = []

        for i in range(int(base_size * (2 ** (self.hard_limit -1)))):
            self.data.append(Idea(
                resident = self.user,
                subject_line = "test subject line " + str(i),
                topic = "test topic " + str(i),
                location = "test location " + str(i),
                message = "Test sentence " + str(i) + ". Test question " + str(i) + "? Test exclamation " + str(i) + "!",
                time_stamp = datetime(2026, 1, 1, 11, 55, 55, tzinfo=timezone.utc)
            ))

        self.big_data = []
        for i in range(int(base_size * (2 ** self.hard_limit + 1))):
            self.big_data.append(Idea(
                resident = self.user,
                subject_line = "test subject line " + str(i),
                topic = "test topic " + str(i),
                location = "test location " + str(i),
                message = "Test sentence " + str(i) + ". Test question " + str(i) + "? Test exclamation " + str(i) + "!",
                time_stamp = datetime(2026, 1, 1, 11, 55, 55, tzinfo=timezone.utc)
            ))

    def get_limit():
         return constants.AI_HARD_LIMIT


    # Tests that the values of batches created by Get_Batches is as expected    
    def test_get_batches_contents(self):
        actual_batches, actual_count = pipeline.Get_Batches(self.task, self.format, self.data, self.batch_size)
        expected_batches, expected_count = batching.Batch_Data(self.batch_size, self.data, self.task + self.format)

        self.assertEqual(actual_batches, expected_batches)
        self.assertEqual(actual_count, expected_count)


    # Tests that the content type of batches created by Get_Batches is of type string
    def test_get_batches_type(self):
        actual_batches, actual_count = pipeline.Get_Batches(self.task, self.format, self.data, self.batch_size)

        for b in actual_batches:
            self.assertIsInstance(b, str)
    

    # Tests that the consolidate responses method 
    @patch("smart_functionality.pipeline.client.Send_Message")
    def test_consolidate_responses(self, mock_call):
            
            def shrink_response(prompt):
                return prompt[:len(prompt)//2]
            
            mock_call.side_effect = shrink_response

            batches = pipeline.Get_Batches(self.task, self.format, self.data, self.batch_size)
            big_batches = pipeline.Get_Batches(self.task, self.format, self.big_data, self.batch_size)

            result, loops = pipeline.Consolidate_Responses(batches, self.batch_size)
            big_result, big_loops  = pipeline.Consolidate_Responses(big_batches, self.batch_size)

            self.assertLess(len(result), len(batches)) # Tests that the batches get consolidated
            self.assertLess(len(big_result), len(big_batches))

            self.assertLess(loops, self.hard_limit) # Ensures rate limit not exceeded
            self.assertLess(big_loops, self.hard_limit)


    # Tests that generated prompt matches the correct format
    @patch("smart_functionality.pipeline.client.Send_Message")
    def test_query_ai_format(self, mock_call):
        batches, count = batching.Batch_Data(self.batch_size, self.data, self.task + self.format)

        def no_change(prompt):
                return prompt
            
        mock_call.side_effect = no_change

        actual = pipeline.Query_AI(batches, count)
        expected = r"^\[METADATA\] count: (\d+) \[CONTENT\](.*)$"

        for a in actual:
            match = re.match(expected, a)
            self.assertTrue(match)