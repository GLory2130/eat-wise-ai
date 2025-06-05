from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import os
import logging
import uuid
from .services import get_session_history, get_chat_model, get_chat_prompt, load_knowledge_base_content

from langchain_core.runnables import (
    ConfigurableFieldSpec,
    RunnablePassthrough,
)
from langchain_core.runnables.history import RunnableWithMessageHistory
# Set up logging
logger = logging.getLogger(__name__)

# Create your views here.

@api_view(['GET'])
def welcome_view(request):
    return Response({
        "message": "Welcome to Afya LLM API",
        "endpoints": {
            "machine_learning": "/afya/ml/",
            "intents": "/afya/intents/",
            "rag": "/afya/rag/"
        }
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
def machine_learning_view(request):
    try:
        # Get the message from the request
        message = request.data.get('message')
        logger.info(f"Received message: {message}")
        
        if not message:
            logger.warning("No message provided in request")
            return Response(
                {"error": "No message provided"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get or create session ID from the request session
        if 'session_id' not in request.session:
            request.session['session_id'] = str(uuid.uuid4())
        session_id = request.session['session_id']

        # Configure the chatbot
        config = {
            "user_id": session_id,
            "conversation_id": session_id,
            "knowledge_base": ""  # You can add knowledge base content here if needed
        }

        # Get response from chatbot
        try:
            ai_response = chatbot(message, config)
            response_text = str(ai_response)
        except ValueError as ve:
            # Handle missing environment variables
            logger.error(f"Environment variable error: {str(ve)}")
            return Response(
                {"error": "Service configuration error. Please try again later."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        except Exception as e:
            logger.error(f"Chatbot error: {str(e)}")
            return Response(
                {"error": "An error occurred while processing your request"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        logger.info(f"Sending response: {response_text}")
        return Response({
            "response": response_text
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        return Response({
            "error": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def chatbot(message: str, config: dict = None):
    """
    Process a chat message and return a response
    
    Args:
        message (str): The user's message
        config (dict): Configuration containing user_id, conversation_id, and knowledge_base
    """
    logger.info(f"Processing message: {message}")
    if config is None:
        config = {
            "user_id": "default_user",
            "conversation_id": "default_conversation",
            "knowledge_base": ""
        }

    try:
        model = get_chat_model()
        document_path = "d:/project/eat-wise-ai/afya_llm_backend/generate_rag/chatbot-project/src/data"
        # Load the knowledge base content first
        knowledge_base_content = load_knowledge_base_content(document_path)
        # Then pass it to get_chat_prompt
        prompt = get_chat_prompt(knowledge_base_content)
        
        chain = prompt | model 
        
        chain_with_history = RunnableWithMessageHistory(
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

        AI_RESPONSE = chain_with_history.invoke(
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
        response_text = str(AI_RESPONSE.content)
        logging.debug(f"AI_RESPONSE: {response_text}")
        return response_text

    except Exception as e:
        logging.error(f"Error in chatbot: {str(e)}")
        raise
