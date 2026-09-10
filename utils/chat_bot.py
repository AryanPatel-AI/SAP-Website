import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Define the system instructions for the chatbot
SYSTEM_INSTRUCTION = """
You are an expert photography assistant for 'Studioza'.
Your job is to help customers find studios, book photoshoots, and answer general photography questions.
Be concise, friendly, and helpful. Do not offer services outside of booking photography studios or giving photo tips.
"""

def get_chat_response(messages):
    """
    messages is a list of dicts: [{'role': 'user'|'model', 'parts': ['text']}]
    """
    if not GEMINI_API_KEY:
        return "I'm currently offline because my Gemini API key is missing!"
        
    try:
        model = genai.GenerativeModel(
            model_name='gemini-3.6-flash',
            system_instruction=SYSTEM_INSTRUCTION
        )
        
        # We need to format messages for the Gemini API
        formatted_messages = []
        for msg in messages:
            role = "user" if msg['role'] == "user" else "model"
            formatted_messages.append({"role": role, "parts": [msg['content']]})
            
        # The last message is what we want to send
        if not formatted_messages:
            return "How can I help you?"
            
        history = formatted_messages[:-1]
        current_message = formatted_messages[-1]['parts'][0]
        
        chat = model.start_chat(history=history)
        response = chat.send_message(current_message)
        
        return response.text
    except Exception as e:
        print(f"Chatbot error: {e}")
        return "Sorry, I ran into an error processing your request."
