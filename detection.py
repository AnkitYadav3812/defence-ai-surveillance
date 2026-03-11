from ultralytics import YOLO
import cv2
import time
from zone_config import ZONE1, ZONE2
from alert import alert_intruder
from logger import log_intrusion


def open_camera(index):
    cap = cv2.VideoCapture(index, cv2.CAP_MSMF)
    if not cap.isOpened():
        cap = cv2.VideoCapture(index, cv2.CAP_ANY)
    if not cap.isOpened():
        return None

    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)

    # Warmup
    for _ in range(10):
        cap.read()

    ret, frame = cap.read()
    if not ret or frame is None:
        cap.release()
        return None

    b, g, r = cv2.mean(frame)[:3]
    print(f"[INFO] Camera {index} | B={b:.1f} G={g:.1f} R={r:.1f} | Resolution: {frame.shape[1]}x{frame.shape[0]}")
    return cap


# Load YOLO model
model = YOLO("yolov8n.pt")

print("[INFO] Opening cameras...")

# ✅ Camera 0 = IR/Orange (skip), Camera 1 = Real camera
cap1 = open_camera(1)   # Real camera
cap2 = open_camera(2)   # Try index 2 as second camera

if cap1 is None:
    print("[ERROR] No real camera found. Exiting.")
    exit()

if cap2 is None:
    print("[WARNING] Second camera not found. Running single camera mode.")
    cap2 = None

# Cooldown trackers
last_alert_time1 = 0
last_alert_time2 = 0
ALERT_COOLDOWN = 10  # seconds


def process_frame(frame, zone, model, last_alert_time, cooldown=10):
    if frame is None or frame.mean() < 1.0:
        return frame, last_alert_time

    results = model(frame, verbose=False)
    intruder = False

    for r in results:
        boxes = r.boxes.xyxy.cpu().numpy()
        classes = r.boxes.cls.cpu().numpy()

        for box, cls in zip(boxes, classes):
            if int(cls) == 0:  # person
                x1, y1, x2, y2 = map(int, box)
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                if zone["x1"] < cx < zone["x2"] and zone["y1"] < cy < zone["y2"]:
                    intruder = True
                    text_y = max(y1 - 10, 10)
                    cv2.putText(frame, "INTRUDER", (x1, text_y),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    # Draw blue zone
    cv2.rectangle(frame,
                  (zone["x1"], zone["y1"]),
                  (zone["x2"], zone["y2"]),
                  (255, 0, 0), 2)

    if intruder and (time.time() - last_alert_time > cooldown):
        alert_intruder()
        log_intrusion()
        last_alert_time = time.time()

    return frame, last_alert_time


print("[INFO] Surveillance started. Press ESC to quit.")
print("[INFO] ⚡ If screen is dark — turn on lights or remove lens cover!")

consecutive_failures = 0
MAX_FAILURES = 30

while True:
    ret1, frame1 = cap1.read()

    if not ret1:
        consecutive_failures += 1
        if consecutive_failures >= MAX_FAILURES:
            print("[ERROR] Camera feed lost. Exiting.")
            break
        continue

    consecutive_failures = 0

    # Boost brightness if frame is too dark (mean < 30)
    if frame1.mean() < 30:
        frame1 = cv2.convertScaleAbs(frame1, alpha=3.0, beta=30)

    frame1, last_alert_time1 = process_frame(
        frame1, ZONE1, model, last_alert_time1, ALERT_COOLDOWN
    )
    cv2.imshow("Camera 1 Surveillance", frame1)

    # Camera 2 (if available)
    if cap2 is not None:
        ret2, frame2 = cap2.read()
        if ret2:
            if frame2.mean() < 30:
                frame2 = cv2.convertScaleAbs(frame2, alpha=3.0, beta=30)
            frame2, last_alert_time2 = process_frame(
                frame2, ZONE2, model, last_alert_time2, ALERT_COOLDOWN
            )
            cv2.imshow("Camera 2 Surveillance", frame2)

    if cv2.waitKey(1) == 27:
        print("[INFO] ESC pressed. Exiting.")
        break

cap1.release()
if cap2 is not None:
    cap2.release()
cv2.destroyAllWindows()
