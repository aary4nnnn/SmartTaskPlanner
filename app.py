import os
import json
import requests
from flask import Flask, request, jsonify,render_template
from flask_cors import CORS

# Initialize the Flask application
app = Flask(__name__)
# Enable Cross-Origin Resource Sharing (CORS) to allow the frontend to communicate with the backend
CORS(app)

# Retrieve the Gemini API Key from environment variables.
# Replace "YOUR_API_KEY_HERE" with a default key if the environment variable is not set,
# but it's strongly recommended to use environment variables for security.
API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_API_KEY_HERE")
if API_KEY == "YOUR_API_KEY_HERE":
    print("Warning: GEMINI_API_KEY environment variable not set. Using placeholder.")

# The API endpoint for the Gemini model
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={API_KEY}"

@app.route('/', methods=['GET'])
def start():
    return render_template('index.html')



@app.route('/plan', methods=['POST'])
def generate_plan():
    """
    API endpoint to generate a task plan from a user's goal.
    Accepts a POST request with a JSON body containing a "goal" key.
    """
    # Check if the request contains valid JSON and the 'goal' key
    if not request.json or 'goal' not in request.json:
        return jsonify({"error": "Request must be JSON and include a 'goal' field."}), 400

    user_goal = request.json['goal']

    # This system prompt instructs the AI on how to behave and what format to use for its response.
    # It's crucial for getting reliable, structured JSON output.
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

    # The payload for the Gemini API call, structured as per the API's requirements.
    payload = {
        "contents": [{"parts": [{"text": f"Create a plan for this goal: {user_goal}"}]}],
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "generationConfig": {
            "responseMimeType": "application/json",
        }
    }

    headers = {'Content-Type': 'application/json'}

    try:
        # Make the POST request to the Gemini API
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        # Raise an HTTPError for bad responses (4xx or 5xx)
        response.raise_for_status()
        
        # The AI's response is already JSON, so we can return it directly.
        # Flask's jsonify will set the correct Content-Type header.
        return response.json()

    except requests.exceptions.RequestException as e:
        # Handle network-related errors or bad HTTP responses
        print(f"Error calling Gemini API: {e}")
        return jsonify({"error": "Failed to communicate with the AI service."}), 502
    except Exception as e:
        # Handle other unexpected errors
        print(f"An unexpected error occurred: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500

# This allows the script to be run directly
if __name__ == '__main__':
    # Run the app on port 5001 in debug mode for development.
    # Debug mode provides helpful error messages but should be disabled in production.
    app.run(port=5001, debug=True)
