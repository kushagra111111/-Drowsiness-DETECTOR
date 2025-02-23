import cv2
import dlib
import pyttsx3
import time
import numpy as np
from scipy.spatial import distance
from twilio.rest import Client
import geocoder  # Import geocoder for GPS-based location

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Start webcam
cap = cv2.VideoCapture(0)

# Load face detector and facial landmarks model
face_detector = dlib.get_frontal_face_detector()
dlib_facelandmark = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Twilio Credentials (Use environment variables for security)
TWILIO_SID = "AC4302f265f32f25359cefc860c8368d2a"
TWILIO_AUTH_TOKEN = "5690f4cf2acaafebf8fbb54c7c1c5a0d"
TWILIO_PHONE_NUMBER = "whatsapp:+14155238886"
EMERGENCY_CONTACT = "whatsapp:+919839162226"

# Initialize Twilio client
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

# Function to calculate Eye Aspect Ratio (EAR)
def Detect_Eye(eye):
    poi_A = distance.euclidean(eye[1], eye[5])
    poi_B = distance.euclidean(eye[2], eye[4])
    poi_C = distance.euclidean(eye[0], eye[3])
    return (poi_A + poi_B) / (2 * poi_C)

# Function to get GPS-based location with fallback to IP
def get_location():
    try:
        location = geocoder.osm('me', method='geocode')  # Try GPS-based location
        if not location.latlng:
            location = geocoder.ip('me')  # Fallback to IP-based geolocation
        
        if location.latlng:
            lat, lng = location.latlng
            return f"🌍 Google Maps: https://www.google.com/maps?q={lat},{lng}"
        return "⚠️ Location unavailable"
    except Exception as e:
        return f"⚠️ Location error: {e}"

# Variables to track drowsiness duration
drowsy_start_time = None
DROWSINESS_THRESHOLD = 0.14
ALERT_DURATION = 3  # Time in seconds before alerting emergency contact
emergency_alert_sent = False

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector(gray)

    for face in faces:
        face_landmarks = dlib_facelandmark(gray, face)
        leftEye, rightEye = [], []

        for n in range(36, 42):
            x, y = face_landmarks.part(n).x, face_landmarks.part(n).y
            leftEye.append((x, y))

        for n in range(42, 48):
            x, y = face_landmarks.part(n).x, face_landmarks.part(n).y
            rightEye.append((x, y))

        # Calculate Eye Aspect Ratio (EAR)
        left_EAR = Detect_Eye(leftEye)
        right_EAR = Detect_Eye(rightEye)
        EAR = (left_EAR + right_EAR) / 2
        EAR = round(EAR, 2)

        if EAR < DROWSINESS_THRESHOLD:
            if drowsy_start_time is None:
                drowsy_start_time = time.time()  # Start tracking drowsiness

            elapsed_time = time.time() - drowsy_start_time

            cv2.putText(frame, "DROWSINESS DETECTED!", (50, 100),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)
            cv2.putText(frame, "Alert! WAKE UP", (50, 450),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)
            
            engine.say("Boss Wake Up")
            engine.runAndWait()

            # Send emergency alert only if drowsiness lasts more than ALERT_DURATION
            if elapsed_time >= ALERT_DURATION and not emergency_alert_sent:
                print("🚨 Sending emergency WhatsApp message with location...")
                try:
                    location_msg = get_location()  # Get the current location
                    message = client.messages.create(
                        body=f"🚨 Emergency! Drowsiness detected. {location_msg}",
                        from_=TWILIO_PHONE_NUMBER,
                        to=EMERGENCY_CONTACT
                    )
                    print(f"✅ Emergency WhatsApp alert sent. Message SID: {message.sid}")
                    emergency_alert_sent = True  # Prevent multiple alerts
                except Exception as e:
                    print(f"❌ Error sending WhatsApp message: {e}")

        else:
            drowsy_start_time = None  # Reset drowsy timer when eyes are open
            emergency_alert_sent = False  # Reset emergency flag

    cv2.imshow("Drowsiness Detector", frame)
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
