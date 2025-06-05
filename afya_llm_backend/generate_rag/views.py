from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import logging

# Set up logging
logger = logging.getLogger(__name__)

@api_view(['GET'])
def welcome_view(request):
    return Response({
        "message": "Welcome to Afya RAG API",
        "endpoints": {
            "rag": "/afya/rag/",
        }
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
def rag_view(request):
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

        # TODO: Implement RAG functionality
        response = {
            "message": "RAG functionality coming soon",
            "received_message": message
        }

        return Response(response, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        return Response({
            "error": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 