# 🧠 Smart Task Planner 🤖✨

An **AI-powered web application** that transforms your goals into structured, actionable task plans — complete with **timelines**, **dependencies**, and now even **persistent task history storage**!

---

## 🌐 UI Preview

## 🖥️ User Interface:
<img width="1919" height="956" alt="image" src="https://github.com/user-attachments/assets/cb9bfe28-623c-4329-b79f-0bce8f75274b" />


## 📋 Generated Output:
<img width="1919" height="948" alt="image" src="https://github.com/user-attachments/assets/340c003e-0e55-4ec6-a7bc-38f293db5a8b" />
<img width="1919" height="947" alt="image" src="https://github.com/user-attachments/assets/5c31f169-05e7-4e49-9f0b-51afd02b3ef5" />

### 💾 Task History Storage:
All generated tasks are now **saved and viewable anytime**.
<img width="1919" height="934" alt="Stored Tasks" src="https://github.com/user-attachments/assets/62606af3-8bcc-46ed-a5af-65fb7d94c623" />

---

## ✨ Features

✅ **AI-Powered Planning**  
Leverages the **Google Gemini API** to understand user goals and generate structured, detailed, and logical project plans.

✅ **Detailed Task Breakdown**  
Each plan includes:
- 📑 Clearly defined tasks  
- 🕒 Estimated timelines  
- 🔗 Dependency mapping  

✅ **Task History Storage**  
All previously generated plans are automatically **stored locally**, allowing users to **view their older task lists anytime** — no data loss on refresh!

✅ **Modern, Responsive UI**  
A beautiful and responsive **TailwindCSS-based** interface with animations and transitions for a delightful experience.

✅ **Lightweight RESTful Backend**  
Built with **Flask**, communicating seamlessly with Gemini API.

---

## 🧰 Technology Stack

| Component   | Technology Used |
|--------------|-----------------|
| **Backend**  | Python, Flask, Flask-Cors |
| **Frontend** | HTML, Tailwind CSS, Vanilla JavaScript |
| **AI Model** | Google Gemini API |

---
'''
📁 Project Structure

SmartTaskPlanner/

│

├── app.py               # Flask backend (Gemini API integration)

│

├── templates/

│   └── index.html       # Frontend UI

│

├── static/

│   ├── css/             # Tailwind styling

│   ├── js/              # Client-side logic

│   └── storage/         # Stores generated tasks (new feature)

│

└── README.md


'''



## ⚙️ Installation & Setup

Follow these steps to run the project locally:

### 🪶 Prerequisites
- Python **3.10+**
- A valid **Google Gemini API Key** (available free at [Google AI Studio](https://aistudio.google.com))

---

### 1️⃣ Clone the Repository

-git clone https://github.com/aary4nnnn/SmartTaskPlanner.git
-cd SmartTaskPlanner

2️⃣ Backend Setup
Create and Activate a Virtual Environment

-For macOS/Linux:

python3 -m venv venv
source venv/bin/activate

-For Windows:

python -m venv venv
.\venv\Scripts\activate

-Install Dependencies:

pip install Flask Flask-Cors requests

###Set Your API Key
-macOS/Linux:

export GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"

-Windows (PowerShell):

$env:GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"

-Run the Flask Server

flask --app app run --port=5001

Backend will be available at http://127.0.0.1:5001

3️⃣ Frontend Setup

Simply open index.html in your browser.

For best results, use Chrome, Edge, or Firefox.

🚀 Usage

Ensure the Flask backend is running.

Open index.html in your browser.

Enter your goal (e.g., "Build a personal portfolio website", "Learn Python in 1 month").

Click “Create my plan”.

View your structured AI-generated task plan instantly.

All previous tasks are automatically saved and retrievable.

