import os
import json
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

# Configure API Key
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def analyze_image(image_path):
    if not GEMINI_API_KEY:
        return {
            "category": "Uncategorized",
            "hashtags": "#photography #studio",
            "details": "No AI details available (API Key missing).",
            "improvement_tips": "Configure Gemini API key for insights."
        }
    
    try:
        model = genai.GenerativeModel('gemini-3.6-flash')
        img = Image.open(image_path)
        
        prompt = """
        You are an expert photography critic and AI analyst. Analyze this photo.
        Return ONLY a valid JSON object with the following keys, and nothing else (no markdown blocks, no extra text):
        - "category": A single word category (e.g. Portrait, Nature, Architecture, Product, Wedding)
        - "hashtags": A string of 5-7 popular hashtags separated by spaces (e.g. "#portrait #moody #studio")
        - "details": A 2-sentence rich description of the image composition and subject.
        - "improvement_tips": A 2-sentence constructive tip on lighting, framing, or post-processing to make it perfect.
        """
        
        response = model.generate_content([prompt, img])
        text = response.text.strip()
        
        # Clean up any potential markdown formatting
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
            
        result = json.loads(text.strip())
        return result
    except Exception as e:
        print(f"Error in Gemini Analysis: {e}")
        return {
            "category": "Error",
            "hashtags": "",
            "details": f"Failed to analyze image: {str(e)}",
            "improvement_tips": ""
        }