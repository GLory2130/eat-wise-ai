import logging
from langchain_community.chat_models import ChatDeepInfra
import os
from typing import List
import dotenv
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel, Field, ConfigDict
from langchain_core.runnables import (
    ConfigurableFieldSpec,
    RunnablePassthrough,
)
from langchain_core.runnables.history import RunnableWithMessageHistory

class InMemoryHistory(BaseChatMessageHistory, BaseModel):
    """In memory implementation of chat message history."""
    messages: List[BaseMessage] = Field(default_factory=list)
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def add_messages(self, messages: List[BaseMessage]) -> None:
        """Add a list of messages to the store"""
        self.messages.extend(messages)

    def clear(self) -> None:
        self.messages = []

# Store for chat history
store = {}

def get_session_history(user_id: str, conversation_id: str) -> BaseChatMessageHistory:
    if (user_id, conversation_id) not in store:
        store[(user_id, conversation_id)] = InMemoryHistory()
    return store[(user_id, conversation_id)]

# Load environment variables
dotenv.load_dotenv()

def get_chat_model():
    """Get the chat model instance"""
    DEEPINFRA_API_TOKEN = os.environ.get("DEEPINFRA_API_TOKEN")
    DEEPINFRA_LANG_MODEL = os.environ.get("DEEPINFRA_LANG_MODEL")

    if not DEEPINFRA_API_TOKEN or not DEEPINFRA_LANG_MODEL:
        raise ValueError("Missing required environment variables: DEEPINFRA_API_TOKEN or DEEPINFRA_LANG_MODEL")

    return ChatDeepInfra(
        model_id=DEEPINFRA_LANG_MODEL,
        deepinfra_api_token=DEEPINFRA_API_TOKEN,
        top_k=1,
        temperature=0.8,
    )

def get_chat_prompt():
    """Get the chat prompt template"""
    return ChatPromptTemplate.from_messages([
        (
            "system",
            "You're a health assistant named nutrichat who is skilled in health-related topics, primarily meals and foods to maintain body fitness and prevent obesity and diabetes. You respond in English, even if the question is in Swahili. Be strict and concise, and keep your response organized and under 200 words.",
        ),
        (
            "system",
            "You should answer all questions referring to the provided knowledge base. The following is the knowledge base: {knowledge_base}",
        ),
        (
            "system",
            "Always start conversations with a warm and friendly greeting, showing interest in the user's health. Example: 'Hello! How can I assist you with your health today?'",
        ),
        (
            "system",
            "Politely ask users to share their current weight and target weight to offer personalized health advice. For example: 'Please share your current weight and target weight. I'll help you with a plan to reach those goals.'",
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ])

def chatbot(message: str, config: dict = None):
    """
    Process a chat message and return a response
    
    Args:
        message (str): The user's message
        config (dict): Configuration containing user_id, conversation_id, and knowledge_base
    """
    if config is None:
        config = {
            "user_id": "default_user",
            "conversation_id": "default_conversation",
            "knowledge_base": ""
        }

    try:
        model = get_chat_model()
        prompt = get_chat_prompt()
        
        chain = prompt | model | RunnablePassthrough()
        
        chain_ = RunnableWithMessageHistory(
            chain,
            get_session_history,
            input_messages_key="question",
            history_messages_key="history",
            history_factory_config=[
                ConfigurableFieldSpec(
                    id="user_id",
                    annotation=str,
                    name="User ID",
                    description="Unique identifier for the user.",
                    default="",
                    is_shared=True,
                ),
                ConfigurableFieldSpec(
                    id="conversation_id",
                    annotation=str,
                    name="Conversation ID",
                    description="Unique identifier for the conversation.",
                    default="",
                    is_shared=True,
                ),
            ],
        )

        AI_RESPONSE = chain_.invoke(
            {
                "question": message,
                "knowledge_base": config.get("knowledge_base", ""),
            },
            config={
                "configurable": {
                    "user_id": config.get("user_id"),
                    "conversation_id": config.get("conversation_id"),
                }
            },
        )

        # Extract and return only the response text
        response_text = str(AI_RESPONSE)
        logging.info(f"AI_RESPONSE: {response_text}")
        return response_text

    except Exception as e:
        logging.error(f"Error in chatbot: {str(e)}")
        raise