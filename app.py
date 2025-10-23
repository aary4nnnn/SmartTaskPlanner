import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions

app = Flask(__name__)
CORS(app)

model = None
try:
    API_KEY = os.environ.get("GEMINI_API_KEY")
    if not API_KEY:
        print("Warning: GEMINI_API_KEY environment variable not set.")
    
    genai.configure(api_key=API_KEY)
    
    generation_config = {
        "response_mime_type": "application/json",
    }
    
    system_prompt = """
    You are an expert project manager AI. Your task is to break down a user's goal into a structured, actionable plan.
    The output must be a valid JSON object. This object must have a single key named "tasks".
    The value for "tasks" must be an array of JSON objects.
    Each object in this array represents a single task and must contain exactly three keys:
    1. "task": A string that clearly and concisely describes the task.
    2. "dependencies": An array of strings. Each string must be the exact "task" name of another task that this one depends on. If there are no dependencies, this must be an empty array.
    3. "timeline": A string providing an estimated duration for the task (e.g., "3-4 hours", "2 days", "1 week").
    Do not include any explanations or text outside of the main JSON object.
    """

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction=system_prompt
    )
    print("Gemini model initialized successfully.")

except Exception as e:
    print(f"Fatal error during app initialization: {e}")

@app.route('/plan', methods=['POST'])
def generate_plan():
    if model is None:
        print("Error: Model was not initialized.")
        return jsonify({"error": "AI Model not initialized. Check server logs for API key or configuration issues."}), 500

    if not request.json or 'goal' not in request.json:
        return jsonify({"error": "Request must be JSON and include a 'goal' field."}), 400

    user_goal = request.json['goal']

    try:
        response = model.generate_content(f"Create a plan for this goal: {user_goal}")
        return response.text, 200

    except google_exceptions.GoogleAPICallError as e:
        print(f"Error calling Gemini API: {e.code} {e.message}") 
        return jsonify({"error": "Failed to communicate with the AI service."}), 502
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return jsonify({"error": "An internal server error occurred."}), 500

if __name__ == '__main__':
    app.run(port=os.environ.get("PORT", 5001), debug=True)
