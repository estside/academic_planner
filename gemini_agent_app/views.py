# gemini_agent_app/views.py
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .agent import StudyPlanAgent # Import the new agent class
import json

@login_required
def chat_view(request):
    """
    Renders the chat interface HTML page.
    """
    return render(request, "chat_ui.html")

@csrf_exempt # Use this for API endpoints to ignore CSRF for simplicity, but for production, use proper tokens
def chat_api(request):
    """
    Handles the API requests from the chatbot frontend.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message')
        
        if not user_message:
            return JsonResponse({"error": "No message provided"}, status=400)
        
        # Initialize the AI agent for the current user
        agent = StudyPlanAgent(request.user)
        
        # Call the agent to get a response
        ai_response = agent.generate_response(user_message)
        
        return JsonResponse({"response": ai_response}, status=200)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)