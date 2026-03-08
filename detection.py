from ultralytics import YOLO
import cv2
from zone_config import ZONE
from alert import alert_intruder
from logger import log_intrusion

# Load YOLO model
model = YOLO("yolov8n.pt")

# Initialize two cameras
cap1 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)

while True:

    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()

    if not ret1 and not ret2:
        break

    # Process Camera 1
    if ret1:

        results1 = model(frame1)

        intruder1 = False

        for r in results1:

            boxes = r.boxes.xyxy.cpu().numpy()
            classes = r.boxes.cls.cpu().numpy()

            for box, cls in zip(boxes, classes):

                if int(cls) == 0:

                    x1, y1, x2, y2 = map(int, box)

                    cx = (x1 + x2) // 2
                    cy = (y1 + y2) // 2

                    cv2.rectangle(frame1,(x1,y1),(x2,y2),(0,255,0),2)

                    if ZONE["x1"] < cx < ZONE["x2"] and ZONE["y1"] < cy < ZONE["y2"]:

                        intruder1 = True

                        cv2.putText(frame1,
                                    "INTRUDER",
                                    (x1,y1-10),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    1,
                                    (0,0,255),
                                    2)

        cv2.rectangle(frame1,
                      (ZONE["x1"],ZONE["y1"]),
                      (ZONE["x2"],ZONE["y2"]),
                      (255,0,0),2)

        if intruder1:
            alert_intruder()
            log_intrusion()

        cv2.imshow("Camera 1 Surveillance", frame1)

    # Process Camera 2
    if ret2:

        results2 = model(frame2)

        intruder2 = False

        for r in results2:

            boxes = r.boxes.xyxy.cpu().numpy()
            classes = r.boxes.cls.cpu().numpy()

            for box, cls in zip(boxes, classes):

                if int(cls) == 0:

                    x1, y1, x2, y2 = map(int, box)

                    cx = (x1 + x2) // 2
                    cy = (y1 + y2) // 2

                    cv2.rectangle(frame2,(x1,y1),(x2,y2),(0,255,0),2)

                    if ZONE["x1"] < cx < ZONE["x2"] and ZONE["y1"] < cy < ZONE["y2"]:

                        intruder2 = True

                        cv2.putText(frame2,
                                    "INTRUDER",
                                    (x1,y1-10),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    1,
                                    (0,0,255),
                                    2)

        cv2.rectangle(frame2,
                      (ZONE["x1"],ZONE["y1"]),
                      (ZONE["x2"],ZONE["y2"]),
                      (255,0,0),2)

        if intruder2:
            alert_intruder()
            log_intrusion()

        cv2.imshow("Camera 2 Surveillance", frame2)

    # Exit key
    if cv2.waitKey(1) == 27:
        break

cap1.release()
cap2.release()

cv2.destroyAllWindows()