from django.test import TestCase
from smart_functionality import client

class TestBatching(TestCase):
    def setUp(self):
        self.batch_size = 5
        self.message = "Test message 1, 2, 3"

        self.prompt = f"[METADATA] count: {self.count} [CONTENT] {self.message}"
        
        
        def test_send_message(self):
            expected = "TEST RESPONSE: " + self.prompt
            actual = client.Send_Message(self.prompt)