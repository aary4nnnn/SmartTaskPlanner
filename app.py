import os
import json
import requests
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_API_KEY_HERE")
if API_KEY == "YOUR_API_KEY_HERE":
    print("Warning: GEMINI_API_KEY environment variable not set. Using placeholder.")

API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={API_KEY}"

@app.route('/', methods=['GET'])
def start():
    return render_template('index.html')

@app.route('/plan', methods=['POST'])
def generate_plan():
    if not request.json or 'goal' not in request.json:
        return jsonify({"error": "Request must be JSON and include a 'goal' field."}), 400

    user_goal = request.json['goal']

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

    payload = {
        "contents": [{"parts": [{"text": f"Create a plan for this goal: {user_goal}"}]}],
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "generationConfig": {
            "responseMimeType": "application/json",
        }
    }

    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling Gemini API: {e}")
        return jsonify({"error": "Failed to communicate with the AI service."}), 502
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)
