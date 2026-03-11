from datetime import datetime

LOG_FILE = "intrusion_log.txt"

def log_intrusion():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[INTRUSION DETECTED] {timestamp}\n")
    print(f"[LOG] Intrusion logged at {timestamp}")
