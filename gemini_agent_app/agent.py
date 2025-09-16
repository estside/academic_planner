# gemini_agent_app/agent.py
import google.generativeai as genai
import os
import json
from . import tools 
from django.db.models import F

class StudyPlanAgent:
    def __init__(self, user):
        self.user = user
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        
        self.chat_model = genai.GenerativeModel(
            'gemini-1.5-pro',
            tools=[
                tools.add_new_course,
                tools.add_calendar_event,
                tools.add_assignment,
                tools.add_exam,
                tools.get_academic_summary, 
            ]
        )

        system_instruction = (
            "You are an AI academic planner assistant. You have access to tools that can get "
            "and modify the user's academic data. Do NOT ask for the user's ID; "
            "it is handled automatically by your tool calls. \n\n"
            "Available tools:\n"
            "- get_academic_summary: Get overview of courses, assignments, exams, and events\n"
            "- add_new_course: Add a new course with name, code, and instructor\n"
            "- add_calendar_event: Add events to the calendar\n"
            "- add_assignment: Add assignments to specific courses\n"
            "- add_exam: Add exams to specific courses\n\n"
            "Always use the get_academic_summary tool when users ask about their academic data. "
            "Be helpful, friendly, and use emojis in your responses to make them engaging. "
            "When adding items, provide clear confirmation messages with details."
        )
        self.chat_session = self.chat_model.start_chat(history=[
            {"role": "user", "parts": [system_instruction]}
        ])

    def generate_response(self, query):
        try:
            # 1. Send the query to the model.
            response = self.chat_session.send_message(query)

            # 2. Iterate through all parts of the response
            response_parts = response.candidates[0].content.parts
            
            for part in response_parts:
                if part.function_call:
                    tool_call = part.function_call
                    tool_name = tool_call.name
                    tool_kwargs = {arg: tool_call.args[arg] for arg in tool_call.args}

                    # Check for missing required arguments
                    if tool_name == 'add_new_course':
                        required_args = ['name', 'code', 'instructor']
                        missing_args = [arg for arg in required_args if arg not in tool_kwargs]
                        if missing_args:
                            return f"I need the {', '.join(missing_args)} to add the course. Can you provide it?"

                    # Automatically add the user_id
                    tool_kwargs['user_id'] = self.user.id
                    
                    # Execute the tool
                    tool_function = getattr(tools, tool_name)
                    tool_result = tool_function(**tool_kwargs)
                    
                    # Send the tool's result back to the model for a final, natural response.
                    # This is the correct way to handle a function call result in the new API.
                    final_response = self.chat_session.send_message(tool_result)
                    return final_response.text

                elif part.text:
                    # If the part is text, just return it directly.
                    return part.text
            
            # Fallback if no parts are found (shouldn't happen with valid input)
            return "I'm sorry, I couldn't process that request."
                
        except Exception as e:
            print(f"Error generating response: {e}")
            return "I'm sorry, an error occurred. Please try again later."