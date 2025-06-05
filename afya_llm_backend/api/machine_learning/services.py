import logging
from langchain_community.chat_models import ChatDeepInfra
import os
from typing import List
import dotenv
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel, Field, ConfigDict
from langchain_core.runnables import (
    ConfigurableFieldSpec,
    RunnablePassthrough,
)
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnableLambda
import sys
sys.path.append(r'd:\project\eat-wise-ai\afya_llm_backend\generate_rag\chatbot-project\src')
import chatbot.knowledge_base as kb_module
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


def load_knowledge_base_content(document_path: str, max_chars=2000) -> str:
    kb = kb_module.KnowledgeBase(document_path)
    content_pieces = []
    total_chars = 0
    for doc in kb.documents:
        if total_chars >= max_chars:
            break
        to_add = doc['content'][:max_chars - total_chars]
        content_pieces.append(to_add)
        total_chars += len(to_add)
    return "\n\n".join(content_pieces)

def get_chat_prompt(knowledge_base_content: str):
    return ChatPromptTemplate.from_messages([
        (
            "system",
            "You are NutriChat, a friendly virtual health assistant. You help users build balanced diets and prevent conditions like obesity and diabetes. Keep responses concise (under 200 words), respond in English unless asked to use Kiswahili, and personalize suggestions based on user info and food intake history."
        ),
        (
            "system",
            "Start by asking the user: 'What foods have you eaten today so far?' This helps you identify any missing food groups and ensure a balanced diet."
        ),
        (
            "system",
            "Once the user shares their food intake, ask for their weight (kg) and height (cm) so you can calculate their BMI. Based on the BMI, classify them as underweight, normal, overweight, or obese and tailor suggestions accordingly."
        ),
        (
            "system",
            "If not yet shared, also ask the user for their age. Age helps in tailoring nutrition advice."
        ),
        (
            "system",
            "Once you have food intake, weight, height, and age, ask for any health conditions (e.g., diabetes, hypertension) or financial constraints so your suggestions are affordable and relevant."
        ),
        (
            "system",
            "Consider food already consumed to avoid repetition and ensure nutritional balance. Use the user's history and past messages for context."
        ),
        (
            "system",
            "Use Kiswahili only if the user requests it (e.g., 'Please speak in Kiswahili')."
        ),
        (
            "system",
            f"Use this knowledge base to guide your answers: {knowledge_base_content}"
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ])


