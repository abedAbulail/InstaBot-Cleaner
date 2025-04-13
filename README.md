# InstaBot-Cleaner

# 🤖 InstaBot Cleaner – Delete Inappropriate Instagram Comments with AI

This project is a smart Instagram bot built with **FastAPI**, **Google Gemini AI**, and **ReactJS**, that automatically detects and deletes inappropriate or profane comments from your latest posts.

## 🚀 Features

- 🔐 Login securely to your Instagram account
- 🧠 Uses Google Gemini AI + `better_profanity` to detect:
  - Hate speech
  - Bullying
  - Profane language
- 🔄 Automatically deletes the flagged comments
- 🖥️ React frontend for easy access

## 🛠️ Tech Stack

- Backend: FastAPI, instagrapi, Google Gemini AI, better_profanity
- Frontend: ReactJS + Axios + Bootstrap

## 🔧 How to Run

### Backend (FastAPI)

1. Navigate to backend:
   ```bash
   cd backend

2. Install dependencies:

pip install -r requirements.txt
3. Run the server:
  uvicorn main:app --reload

## Frontend (ReactJS)
1. Navigate to frontend:
  cd frontend

2. Install dependencies:
  npm install


4. Run the app:
  npm start


Make sure the backend is running at http://127.0.0.1:8000 and frontend is connected to it.

⚠️ You need your own Google Gemini API Key for this to work!
