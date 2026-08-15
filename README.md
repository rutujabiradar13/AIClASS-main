🎓 AICLASS — AI Attendance Management System

AICLASS is an AI-based attendance platform that uses facial and voice recognition to identify students and automatically record attendance.

🚀 Live Demo: https://rutujabiradar13-aiclass-main-app-mquvkk.streamlit.app/ 

✨ Features
👨‍🎓 Student
Register and log in using facial recognition
Enroll in subjects using a subject code
View enrolled subjects and attendance
👨‍🏫 Teacher
Register and log in
Create subjects with unique codes
Share subjects using QR codes or enrollment links
Take attendance using camera, uploaded photos, or voice
View attendance records

🧠 AI Recognition
Dlib + Face Recognition Models — Facial recognition and student identification
Resemblyzer + Librosa — Voice recognition and student identification

🔄 How It Works
Teacher creates subject
        ↓
Shares Code / QR / Link
        ↓
Student enrolls
        ↓
Teacher starts attendance
        ↓
Face / Photo / Voice Recognition
        ↓
Student identified
        ↓
Attendance recorded

🛠️ Tech Stack

Python • Streamlit • Dlib • Face Recognition Models • Resemblyzer • Librosa • Supabase • Scikit-learn • NumPy • Pandas • Pillow • Bcrypt • Segno

🎯 What This Project Demonstrates
Facial and voice recognition integration
Student and teacher role-based workflows
Subject and enrollment management
QR/link-based subject enrollment
Automated attendance recording
Camera, image, and voice input handling
Database integration with Supabase
Streamlit application development and deployment

▶️ Run Locally
git clone YOUR_GITHUB_REPOSITORY_URL
cd YOUR_PROJECT_FOLDER
pip install -r requirements.txt
streamlit run app.py

