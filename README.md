# AI Intrusion Detection Surveillance System

## Overview

This project implements an AI-powered surveillance system capable of detecting human intrusions in restricted areas using real-time video feeds. The system uses computer vision and deep learning techniques to monitor a camera stream, detect persons, and trigger alerts when a restricted zone is violated.

The solution is built using the YOLOv8 object detection model and OpenCV for video processing.

---

## Features

* Real-time human detection using YOLOv8
* Restricted area monitoring
* Automatic intrusion alerts
* Event logging system
* Monitoring dashboard using Streamlit

---

## System Architecture

Camera Feed
↓
Frame Processing (OpenCV)
↓
Object Detection (YOLOv8)
↓
Restricted Zone Detection
↓
Alert System
↓
Event Logging & Dashboard

---

## Technology Stack

* Python
* OpenCV
* YOLOv8
* Streamlit
* NumPy
* Pandas

---

## Project Structure

```
defence_ai_surveillance
│
├── detection.py          # Main AI detection engine
├── alert.py              # Intrusion alert system
├── zone_config.py        # Restricted area configuration
├── logger.py             # Event logging
├── dashboard.py          # Monitoring dashboard
├── requirements.txt      # Project dependencies
└── intrusion_log.csv     # Intrusion event storage
```

---

## Installation

Clone the repository:

```
git clone https://github.com/yourusername/defence-ai-surveillance.git
```

Install dependencies:

```
pip install -r requirements.txt
```

---

## Running the System

Start the AI detection system:

```
python detection.py
```

Launch the monitoring dashboard:

```
streamlit run dashboard.py
```

---

## Example Use Case

This system can be used for:

* Restricted area monitoring
* Smart security systems
* Industrial facility surveillance
* Research in AI-based security solutions

---

## Future Improvements

* Multi-camera monitoring
* Cloud event storage (MongoDB)
* Mobile notification alerts
* Suspicious behavior detection

---

## License

This project is released for educational and research purposes.
