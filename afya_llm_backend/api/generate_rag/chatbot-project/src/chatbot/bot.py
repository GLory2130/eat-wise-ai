class ChatBot:
    def __init__(self, knowledge_base):
        self.knowledge_base = knowledge_base

    def get_response(self, user_query):
        relevant_info = self.knowledge_base.get_response(user_query)
        if relevant_info:
            return self.format_response(relevant_info)
        else:
            return "I'm sorry, I don't have information on that."

    def format_response(self, info):
        return f"Here is what I found: {info}"