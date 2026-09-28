# AI-Based Laboratory Safety Compliance Inspector

An AI-powered laboratory safety monitoring system that uses computer vision to check Personal Protective Equipment (PPE) compliance before laboratory access.

The system uses a custom YOLO model to detect a person and the required PPE — helmet, mask, and gloves — and produces an `ALLOWED` or `DENIED` access decision.

## 🚀 What This Project Does

The project combines three parts:

1. **AI PPE Inspector** — processes a live camera feed with YOLO and checks PPE compliance.
2. **Admin Dashboard** — provides safety metrics, violation alerts, activity logs, CSV export, and PDF reporting.
3. **Student Dashboard** — lets a student view lab visits, allowed entries, violations, attendance percentage, and violation history.

## 🧠 How It Works

```text
Camera
   ↓
YOLO Object Detection
   ↓
Person + Required PPE Detection
   ↓
Helmet + Mask + Gloves Check
   ↓
┌───────────────────────┐
│    PPE compliant?     │
└───────────┬───────────┘
            │
       ┌────┴────┐
       ↓         ↓
      YES        NO
       ↓         ↓
   ALLOWED     DENIED
       ↓         ↓
    Green       Red
       │         │
       └────┬────┘
            ↓
       Activity Log
            ↓
   Admin / Student Dashboard
```

## ✨ Features

### AI Safety Inspector

- Real-time camera-based PPE detection
- Custom YOLO model
- Helmet, mask, and gloves verification
- Access decision: `ALLOWED` / `DENIED`
- Visual detection boxes
- Voice warnings
- Audible buzzer for violations
- Event logging
- Email alerts
- Escalation after repeated violations

### Admin Dashboard

- Admin login
- Total safety checks
- Allowed/denied metrics
- Decision performance chart
- Activity-over-time chart
- PPE violation list
- Recent activity logs
- CSV report download
- PDF report generation
- Grant/Deny access controls

### Student Dashboard

- Student login
- Total lab entries
- Allowed entries
- PPE violations
- Attendance percentage
- Warning status
- PPE violation history
- Complete lab activity log
- Laboratory safety rules

## 🛠️ Technology Stack

- Python
- YOLO / Ultralytics
- OpenCV
- Streamlit
- Pandas
- Matplotlib
- pyttsx3
- Windows `winsound`
- SMTP email
- CSV-based activity logging

## 📂 Project Structure

```text
AI-Laboratory-Safety-Compliance-Inspector/
│
├── README.md
├── requirements.txt
├── .gitignore
├── run_project.bat
│
├── src/
│   ├── lab_ppe_ai.py
│   ├── admin_dashboard.py
│   └── student.py
│
├── models/
│   └── yolov8s_custom.pt
│
├── data/
│   └── lab_ppe_log.csv
│
├── screenshots/
│   ├── ppe-detection.png
│   ├── admin-dashboard.png
│   ├── student-dashboard.png
│   ├── access-allowed.png
│   └── access-denied.png
│
└── docs/
    └── project-report.pdf
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/AI-Laboratory-Safety-Compliance-Inspector.git
cd AI-Laboratory-Safety-Compliance-Inspector
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## ▶️ Running the Project

### AI PPE Inspector

Run from the repository root:

```bash
python src/lab_ppe_ai.py
```

The system starts the camera and performs real-time PPE detection.

Press `Q` to exit the camera window.

### Admin Dashboard

```bash
streamlit run src/admin_dashboard.py
```

### Student Dashboard

```bash
streamlit run src/student.py
```

You can also use the included Windows launcher:

```text
run_project.bat
```

## 🔐 Configuration

The email alert system is designed to use environment variables rather than storing credentials in source code.

Example:

```text
ADMIN_EMAIL=admin@example.com
SMTP_EMAIL=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

For Gmail, use an App Password rather than your normal account password.

Do not commit real credentials, API keys, passwords, or private student data to GitHub.

## 📋 PPE Rules

The current implementation checks for:

- Helmet
- Mask
- Gloves

If a person is detected and all required PPE is detected:

```text
PPE OK → ACCESS ALLOWED
```

Otherwise:

```text
PPE NOT DETECTED → ACCESS DENIED
```

## 🚨 Warning & Alert System

When a PPE violation is detected, the application can:

- Record the event
- Trigger an audible buzzer
- Provide a voice warning
- Send an email alert
- Track repeated warnings
- Alert the administrator after the configured warning limit

The current configuration uses a maximum of three warnings.

## 📊 Data Logging

Safety events are stored using:

```text
time, roll_no, camera, ppe_status, decision
```

The public repository contains only demonstration records. Real student records should not be uploaded to a public repository.

## 📸 Screenshots

Add your actual project screenshots to the `screenshots/` folder and they will appear here.

### AI PPE Detection

![AI PPE Detection](screenshots/ppe-detection.png)

### Access Allowed

![Access Allowed](screenshots/access-allowed.png)

### Access Denied

![Access Denied](screenshots/access-denied.png)

### Admin Dashboard

![Admin Dashboard](screenshots/admin-dashboard.png)

### Student Dashboard

![Student Dashboard](screenshots/student-dashboard.png)

## 🔮 Future Improvements

- Multiple laboratory cameras
- Centralized database instead of CSV storage
- Hardware-based door access control
- Improved identity verification
- Real-time centralized monitoring
- More detailed safety analytics
- Cloud deployment
- Mobile notifications
- Improved model accuracy and additional PPE classes

## 🎓 Project Objective

The project was developed as a practical AI and computer vision application for laboratory safety. The goal is to reduce dependence on manual PPE inspection by automatically detecting safety equipment and maintaining digital compliance records.

## 📚 Learning Outcomes

This project provided practical experience with:

- Computer vision
- Object detection
- YOLO
- OpenCV
- Real-time camera processing
- Python application development
- Streamlit dashboards
- Data logging
- Email automation
- Safety-rule automation
- Building an end-to-end AI application

## 👥 Project

**AI-Based Laboratory Safety Compliance Inspector**

A college project focused on applying AI and computer vision to laboratory safety and PPE compliance monitoring.
