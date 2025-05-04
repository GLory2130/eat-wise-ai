from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import os
import logging
import uuid
from .services import chatbot

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
