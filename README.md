Here’s an updated **README** for your **FIREFLY** project based on the repository URL you provided:

---

# 🔥 FIREFLY: Fire Identification In Realtime with Event Feedback from a Learning-Based Yield 🚨

![API Live](https://img.shields.io/badge/API%20Live-Render-brightgreen?logo=render)

---

## 🔍 Overview  

**FIREFLY** is a real-time fire detection system built using machine learning and computer vision techniques. It captures video streams, analyzes frames through a pre-trained deep learning model, and provides alerts (sound and email) upon detecting a fire. This system is designed to enhance safety by quickly identifying fire hazards and alerting relevant parties.

Key Features:
- **Real-Time Fire Detection** using a deep learning-based model.
- **Sound Alerts** for immediate local notification.
- **Email Notifications** to notify stakeholders when fire is detected.
- **Live Video Streaming** using WebSocket for real-time video feed and detection results.

---

## 🚀 Features  

- 🔥 **Fire Detection**: Detects fire in video frames with high accuracy.
- 🎧 **Sound Alarm**: Triggers a local alarm when fire is detected.
- 📧 **Email Alerts**: Sends an email notification to a specified recipient in case of fire.
- 🌐 **Real-Time Video Streaming**: Streams video frames with detection status over WebSocket.

---

## 📂 Project Structure  

```
FireFly/
├── api.py                    # FastAPI backend with WebSocket for real-time video and fire detection
├── model/                     # Directory containing the pre-trained deep learning model
│   └── firemodel.keras        # Pre-trained model for fire detection
├── requirements.txt          # Dependencies required to run the project
├── index.html                # (Optional) HTML page for testing locally
└── README.md                 # Project documentation
```  

---


## 📊 API Usage  

### **WebSocket Endpoint**  

**WebSocket** `/ws`  
This endpoint allows you to connect and receive real-time video frames with fire detection status:

1. Connect to the WebSocket server.
2. Stream video frames and receive a fire detection message.

---

### **Example Request**  

```bash  
# WebSocket connection:
wscat -c "ws://localhost:8000/ws"
```

---

### **Example Response**  

The WebSocket will stream video frames and send detection messages:

```json  
{
  "message": "Fire detected! Alert triggered."
}
```

---

## 🛠️ Getting Started  

### Prerequisites  

- Python 3.x  
- Libraries listed in `requirements.txt`  

---

### Installation  

1. **Clone the Repository** 📥:  
   ```bash  
   git clone https://github.com/sgindeed/FireFly.git  
   cd FireFly  
   ```  

2. **Install Dependencies** 📦:  
   ```bash  
   pip install -r requirements.txt  
   ```  

3. **Run the FastAPI Application** 🚀:  
   ```bash  
   uvicorn api:app --reload  
   ```  
   The FastAPI server will be running locally, and you can connect to the WebSocket endpoint at `ws://localhost:8000/ws`.

---

## 📒 Model Training  

The **firemodel.keras** model in the **model/** directory is used for detecting fire. The model is trained on images of fire and non-fire scenes and can be further trained or fine-tuned as per your needs.

---

## 🛠️ Tech Stack  

- **Backend**: FastAPI, WebSocket  
- **Machine Learning**: TensorFlow (Keras)  
- **Sound Alerts**: Winsound (for Windows users)  
- **Email Notifications**: SMTP  

---

## 🤝 Contributions  

Contributions are welcome! Please follow these steps:

1. Fork the repository 🍴.  
2. Create a branch (`feature/YourFeatureName`) 🌱.  
3. Commit your changes 💾.  
4. Push and create a pull request 🚀.  

---

## 📬 Contact  

For questions or feedback, reach out to [@sgindeed](https://github.com/sgindeed).  
