import datetime

def alert_intruder():

    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"⚠ INTRUDER DETECTED at {time}")