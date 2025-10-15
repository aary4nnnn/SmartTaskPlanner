#Smart Task Planner 🤖✨

An AI-powered web application that takes a high-level goal and breaks it down into a detailed, actionable plan with tasks, timelines, and dependencies.

^ Add a screenshot or GIF of your application here!

Features
🎯 AI-Powered Planning: Leverages the Google Gemini API to understand goals and create structured, logical plans.

📑 Detailed Breakdowns: Generates a list of tasks, provides estimated timelines for each, and identifies dependencies between them.

💻 Simple Web Interface: A clean, intuitive, and responsive frontend to input a goal and view the generated plan.

🚀 RESTful Backend: A lightweight Flask API that processes user requests and communicates with the AI model.

Technology Stack
Backend: Python, Flask, Flask-Cors

Frontend: HTML, Tailwind CSS, Vanilla JavaScript

AI Model: Google Gemini

Installation & Setup
Follow these instructions to get the project up and running on your local machine.

Prerequisites
Python 3.7+

A Google Gemini API Key. You can get one for free from Google AI Studio.

1. Clone the Repository
First, clone the project to your local machine (or simply download the files).

git clone [https://github.com/your-username/SmartTaskPlanner.git](https://github.com/your-username/SmartTaskPlanner.git)
cd SmartTaskPlanner

2. Backend Setup
Create and activate a virtual environment:
Open your terminal in the project directory.

For Unix/macOS:

python3 -m venv venv
source venv/bin/activate

For Windows:

python -m venv venv
.\venv\Scripts\activate

Install the required Python packages:

pip install Flask Flask-Cors requests

Set your API Key as an environment variable:
This is a crucial step. The application will not work without it.

For Unix/macOS:

export GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"

For Windows (PowerShell):

$env:GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"

Note: You must set this variable in the same terminal session from which you run the Flask app.

Run the Flask server:
In the same terminal, run the following command:

flask --app app run --port=5001

The backend server will now be running at http://127.0.0.1:5001. Keep this terminal open.

3. Frontend Setup
Open the index.html file in your web browser.
You can simply double-click the file in your file explorer. For best results, use a modern browser like Chrome, Firefox, or Edge.

Usage
Make sure the backend server is running in your terminal.

With index.html open in your browser, type your goal into the text box (e.g., "Launch a new website in 3 weeks" or "Learn Python in 2 months").

Click the Generate Plan button.

The AI will process your request, and the generated action plan will appear below the form.

Contributing
Contributions are welcome! If you have suggestions for improvements, please feel free to open an issue or submit a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for details.

(You would typically create a new file named LICENSE and put the full MIT license text in it).
