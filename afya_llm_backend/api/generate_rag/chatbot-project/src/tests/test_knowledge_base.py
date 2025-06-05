import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from chatbot.knowledge_base import KnowledgeBase

class TestKnowledgeBase(unittest.TestCase):

    def setUp(self):
        self.kb = KnowledgeBase(os.path.join(os.path.dirname(__file__), '..', 'data'))

    def test_load_documents(self):
        self.assertTrue(len(self.kb.documents) > 0, "Documents should be loaded.")

    def test_retrieve_information(self):
        query = "What are the essential nutrients?"
        response = self.kb.get_response(query)
        self.assertIsNotNone(response, "Response should not be None for a valid query.")

    def test_empty_query(self):
        query = ""
        response = self.kb.get_response(query)
        self.assertIsNone(response, "Response should be None for an empty query.")

    def test_specific_query(self):
        query = "proteins"
        response = self.kb.get_response(query)
        self.assertIsNotNone(response, "Response should not be None for a valid query.")
        print(response)  # This will print the response for manual verification

from chatbot.bot import ChatBot

if __name__ == '__main__':
    unittest.main()

class TestChatBotIntegration(unittest.TestCase):

    def setUp(self):
        self.kb = KnowledgeBase(os.path.join(os.path.dirname(__file__), '..', 'data'))
        self.chatbot = ChatBot(self.kb)

    def test_chatbot_uses_knowledge_base(self):
        query = "proteins"
        response = self.chatbot.get_response(query)
        self.assertIn("proteins", response.lower(), "ChatBot response should include information from the knowledge base.")
