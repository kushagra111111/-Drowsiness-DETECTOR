Drowsiness Detection System
📌 Project Overview
This Drowsiness Detection System monitors a user's eye activity in real time using a webcam. If drowsiness is detected, an alert is triggered, and if the user remains drowsy for too long, an emergency alert is sent along with their live location to a pre-defined emergency contact via WhatsApp.

✨ Features
✅ Real-time Eye Tracking - Uses OpenCV and Dlib to detect eye closure.
✅ Drowsiness Alert - Uses text-to-speech (TTS) to warn the user.
✅ Emergency Alert - Sends a WhatsApp message via Twilio after prolonged drowsiness.
✅ Live Location Sharing - Captures user's location via geolocation API and includes it in the emergency message.

🛠 How it Works
The program captures a video stream from the webcam.
It detects the face and tracks eye landmarks.
It calculates the Eye Aspect Ratio (EAR) to determine if the eyes are closed.
If eyes remain closed for more than 3 seconds, a WhatsApp emergency alert is sent along with live GPS coordinates.
📍 Live Location Sharing
The script fetches latitude and longitude using geopy.
The emergency message includes a Google Maps link for tracking.

📢 Future Improvements
Add sound alarm instead of just TTS.
Improve GPS accuracy using device sensors.
Integrate cloud storage for incident reports.
