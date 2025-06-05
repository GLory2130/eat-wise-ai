import unittest
from chatbot.bot import ChatBot

class TestChatBot(unittest.TestCase):

    def setUp(self):
        self.chatbot = ChatBot()

    def test_response_to_known_query(self):
        response = self.chatbot.get_response("What is your name?")
        self.assertEqual(response, "I am a chatbot created to assist you.")

    def test_response_to_unknown_query(self):
        response = self.chatbot.get_response("Tell me about something I don't know.")
        self.assertEqual(response, "I'm sorry, I don't have information on that.")

    def test_response_format(self):
        response = self.chatbot.get_response("How can I help you?")
        self.assertIsInstance(response, str)

if __name__ == '__main__':
    unittest.main()