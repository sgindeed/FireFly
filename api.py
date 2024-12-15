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

cnn = tf.keras.models.load_model(r'G:\\FireFly\\model\\dpmodel.keras')

templates = Jinja2Templates(directory=".")

def sound_alarm():
    duration = 1000
    freq = 1500
    winsound.Beep(freq, duration)

def send_email_alert():
    sender_email = "SENDER_MAIL"
    receiver_email = "RECIEVER_MAIL"
    password = "**************"
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
    except Exception as e:
        print("Error sending email:", e)

def detect_fire(frame):
    test_image = cv2.resize(frame, (256, 256))
    test_image = np.expand_dims(test_image, axis=0)
    result = (cnn.predict(test_image) > 0.5).astype("int32")
    return result[0][0] == 0

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    with open("index.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

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
        
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        
        await websocket.send_bytes(frame_bytes)
        await websocket.send_text(message)
        
    cap.release()
