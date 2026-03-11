import winsound
from datetime import datetime

def alert_intruder():
    print(f"[ALERT] Intruder detected at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    # Beep sound: frequency=1000Hz, duration=500ms
    winsound.Beep(1000, 500)
