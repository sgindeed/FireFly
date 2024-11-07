import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np
import cv2
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import winsound

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

cnn = tf.keras.models.load_model(r'G:\\FireFly\\model\\dpmodel.keras')


def sound_alarm():
    duration = 1000  
    freq = 1500 
    winsound.Beep(freq, duration)


def send_email_alert():
    sender_email = "anny14062110@gmail.com"
    receiver_email = "sup512551@gmail.com"
    password = "vcdgnodeeklwtfsq" 
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

def detect_fire(frame):
    test_image = cv2.resize(frame, (256, 256))
    test_image = img_to_array(test_image)  
    test_image = np.expand_dims(test_image, axis=0) 
    result = (cnn.predict(test_image) > 0.5).astype("int32") 
    return result[0][0] == 0  

def monitor_camera():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if detect_fire(frame):
            print("Fire detected!")
            sound_alarm()
            send_email_alert()
        cv2.imshow('Camera Feed', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

monitor_camera()