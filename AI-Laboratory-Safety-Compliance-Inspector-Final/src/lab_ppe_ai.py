import cv2
import csv
import os
import winsound
import pyttsx3
from ultralytics import YOLO
from datetime import datetime
import smtplib
from email.message import EmailMessage

# ================= CONFIG =================
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@example.com")
SMTP_EMAIL = os.getenv("SMTP_EMAIL", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
CSV_FILE = "data/lab_ppe_log.csv"
YOLO_MODEL = "models/yolov8s_custom.pt"
REQUIRED_PPE = ["helmet", "mask", "gloves"]
MAX_WARNINGS = 3

# ================= FUNCTIONS =================
engine = pyttsx3.init()
engine.setProperty("rate", 150)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def buzzer():
    winsound.Beep(1000, 800)

def send_email(to_email, subject, body):
    try:
        msg = EmailMessage()
        msg["From"] = SMTP_EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(body)
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print("Email failed:", e)

def log_event(roll_no, camera, ppe_status, decision):
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["time","roll_no","camera","ppe_status","decision"])
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            roll_no,
            camera,
            ppe_status,
            decision
        ])

# ================= STUDENT INPUT =================
student_name = input("Enter Student Name: ")
roll_no = input("Enter Roll Number: ")
student_email = f"{roll_no}@mietjammu.in"

# ================= LOAD MODEL =================
model = YOLO(YOLO_MODEL)

# ================= CAMERA START =================
print("Camera starting...")
cam = cv2.VideoCapture(0)

warnings_count = 0
last_decision = None

print("AI LAB SAFETY SYSTEM STARTED")
print("Press Q to exit")

while True:
    ret, frame = cam.read()
    if not ret:
        print("Camera not detected")
        break

    # YOLO detection
    results = model(frame, conf=0.4, verbose=False)
    detected = [model.names[int(box.cls[0])] for r in results for box in r.boxes]

    # Draw boxes
    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            label = model.names[int(box.cls[0])]
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255,0,0), 2)
            cv2.putText(frame, label, (x1, y1-5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 2)

    # PPE check
    person_present = "person" in detected
    ppe_present = all(p in detected for p in REQUIRED_PPE)
    ppe_ok = person_present and ppe_present

    if ppe_ok:
        decision = "ALLOWED"
        text = "PPE OK - ACCESS ALLOWED"
        color = (0,255,0)
    else:
        decision = "DENIED"
        text = "PPE NOT DETECTED"
        color = (0,0,255)

    cv2.putText(frame, text, (20,40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
    cv2.rectangle(frame, (10,10), (620,460), color, 3)

    # Log + warnings
    if decision != last_decision:
        log_event(roll_no, "Laptop Camera", "PPE OK" if ppe_ok else "PPE NOT DETECTED", decision)

        if decision == "DENIED":
            warnings_count += 1
            buzzer()
            speak(f"PPE not detected. Warning {warnings_count} issued.")

            send_email(
                student_email,
                "PPE Violation Alert",
                f"You violated PPE rules in Chemistry Lab. Warning {warnings_count}."
            )

            if warnings_count >= MAX_WARNINGS:
                speak("Access denied. Administrator alerted.")
                send_email(
                    ADMIN_EMAIL,
                    "Critical Lab Safety Alert",
                    f"Student {roll_no} violated PPE rules 3 times."
                )
                # Open admin dashboard automatically
                os.system("start cmd /k streamlit run src/admin_dashboard.py")
                break

        last_decision = decision

    cv2.imshow("Lab PPE Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cam.release()
cv2.destroyAllWindows()
