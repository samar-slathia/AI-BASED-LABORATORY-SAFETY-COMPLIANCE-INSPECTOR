# AI-Based Laboratory Safety Compliance Inspector

An AI-powered computer vision system designed to monitor laboratory safety compliance by detecting whether individuals are wearing required Personal Protective Equipment (PPE).

The system uses a custom-trained YOLO model to analyze camera footage, identify safety equipment, and make an access decision based on PPE compliance.

## 🚀 Features

* Real-time PPE detection using computer vision
* Custom YOLO object detection model
* Detects laboratory safety equipment
* Automatic safety compliance verification
* Green/Red safety indicator
* Access decision based on PPE status
* Camera-based monitoring
* Student identification and logging
* CSV-based activity records
* Admin dashboard for monitoring
* Safety alerts for non-compliant entries
* Exportable compliance records
* Streamlit-based dashboard

## 🧠 How It Works

The system follows a simple workflow:

```text
Camera
   ↓
Video/Image Input
   ↓
YOLO Object Detection
   ↓
PPE Detection
   ↓
Safety Compliance Check
   ↓
┌─────────────────┐
│ PPE Compliant?  │
└────────┬────────┘
         │
    ┌────┴────┐
    ↓         ↓
   YES        NO
    ↓         ↓
  ALLOW      DENY
    ↓         ↓
  GREEN       RED
```

The camera captures the person entering the laboratory. The AI model checks the required PPE and determines whether the person meets the defined safety requirements.

## 🛠️ Tech Stack

### AI & Computer Vision

* Python
* YOLO
* OpenCV
* Custom-trained YOLO model

### Frontend / Dashboard

* Streamlit

### Data & Logging

* CSV
* Pandas

### Development

* Python
* Conda
* Git & GitHub

## 📂 Project Structure

```text
lab_ppe_project/
│
├── lab_ppe_ai.py
├── admin_dashboard.py
├── student.py
├── lab_ppe_log.csv
├── yolov8s_custom.pt
└── README.md
```

## 🔍 PPE Detection

The project uses a custom-trained YOLO model to identify safety-related objects from camera input.

The detection pipeline can be used to check whether a person has the required protective equipment before allowing laboratory access.

Example:

```text
Person detected
      ↓
Safety equipment checked
      ↓
PPE requirements satisfied?
      ↓
YES → Access Allowed
NO  → Access Denied
```

## 🟢 Safety Decision System

The system provides a simple visual decision:

### 🟢 Compliant

The required PPE is detected.

**Decision:** Access Allowed

### 🔴 Non-Compliant

Required PPE is missing.

**Decision:** Access Denied

This makes the system easier to understand and suitable for use at a laboratory entrance.

## 📊 Admin Dashboard

The project includes a Streamlit-based admin dashboard for monitoring laboratory safety activity.

The dashboard can provide:

* Total entries
* Compliant entries
* Non-compliant entries
* Safety alerts
* PPE status
* Student/roll number
* Camera information
* Timestamp
* Activity logs
* CSV export

## 📝 Activity Logging

Safety events are stored in a CSV file.

Example structure:

```text
time, roll_no, camera, ppe_status, decision
```

This allows administrators to maintain a record of laboratory access and safety compliance.

## 📹 Camera Support

The initial system was developed and tested using a laptop camera.

The architecture can be extended to support cameras installed at laboratory entrances, including multiple cameras for different entry points.

Example:

```text
Camera 1 → Laboratory Entrance
Camera 2 → Laboratory Exit
Camera 3 → Additional Monitoring Area
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/lab-ppe-project.git
cd lab-ppe-project
```

### 2. Create the Conda environment

```bash
conda create -n lab_safety python=3.10
conda activate lab_safety
```

### 3. Install dependencies

```bash
pip install ultralytics opencv-python streamlit pandas
```

### 4. Add the trained model

Place the trained YOLO model inside the project directory:

```text
yolov8s_custom.pt
```

### 5. Run the AI detection system

```bash
python lab_ppe_ai.py
```

### 6. Run the admin dashboard

```bash
streamlit run admin_dashboard.py
```

## 🧪 Testing

The system was initially tested using a camera-based setup to verify:

* Person detection
* PPE detection
* Safety compliance decisions
* Green/Red status indication
* Access decisions
* Activity logging
* Dashboard monitoring

## 🔐 Potential Real-World Deployment

For a real laboratory deployment, the system could be connected to cameras positioned at laboratory entrances.

A future implementation could integrate the compliance decision with an electronic access-control system:

```text
Camera
   ↓
AI PPE Detection
   ↓
Compliance Verification
   ↓
Access Control
   ↓
Laboratory Door
```

Additional features such as multiple-camera monitoring, centralized administration, notifications, and database storage can also be added.

## 🎯 Project Objectives

The main objectives of this project are:

* Improve laboratory safety monitoring
* Reduce dependence on manual PPE inspection
* Detect PPE compliance automatically
* Prevent entry when required safety equipment is missing
* Maintain digital safety records
* Provide administrators with an easy monitoring interface

## 📚 What I Learned

Through this project, I gained practical experience with:

* Computer vision
* Object detection
* YOLO
* OpenCV
* Python
* AI model integration
* Real-time camera processing
* Streamlit dashboards
* Data logging
* Safety automation
* Building an end-to-end AI application

## 🚀 Future Improvements

* Support for multiple live cameras
* Face/ID-based student identification
* Database-based logging
* Real-time notifications
* Email/SMS safety alerts
* Hardware-based door access control
* Centralized multi-lab monitoring
* Improved PPE detection accuracy
* Cloud-based administration
* Historical analytics and safety reports

## 👨‍💻 Project

**AI-Based Laboratory Safety Compliance Inspector**

Developed as a college group project focused on applying AI and computer vision to improve laboratory safety and automate PPE compliance monitoring.
