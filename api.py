import cv2
import numpy as np
import tensorflow as tf
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import winsound
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from starlette.requests import Request
import asyncio
import threading

app = FastAPI()

# Load your pre-trained model
cnn = tf.keras.models.load_model(r'G:\\FireFly\\model\\dpmodel.keras')

# Initialize Jinja2 templates to serve from the root directory
templates = Jinja2Templates(directory=".")

# Function to play the alarm sound
def sound_alarm():
    duration = 1000  
    freq = 1500 
    winsound.Beep(freq, duration)

# Function to send an email alert
def send_email_alert():
    sender_email = "anny14062110@gmail.com"
    receiver_email = "sup512551@gmail.com"
    password = "vcdgnodeeklwtfsq"  # Consider using environment variables instead
    subject = "Fire Alert!"
    body = "Warning! A fire has been detected. Please check the surveillance footage immediately."

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(message)
        print("Alert email sent successfully.")
    except Exception as e:
        print("Error sending email:", e)

# Function to detect fire in a frame
def detect_fire(frame):
    test_image = cv2.resize(frame, (256, 256))
    test_image = np.expand_dims(test_image, axis=0)
    result = (cnn.predict(test_image) > 0.5).astype("int32")
    return result[0][0] == 0  # Fire detected if result is 0

# Route to serve the HTML page
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    with open("index.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

# WebSocket to stream the video feed
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        if detect_fire(frame):
            sound_alarm()
            send_email_alert()
            message = "Fire detected! Alert triggered."
        else:
            message = "No fire detected."
        
        # Encode frame to JPEG format
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        
        # Send frame to client
        await websocket.send_bytes(frame_bytes)
        await websocket.send_text(message)
        
    cap.release()
