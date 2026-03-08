import csv
import datetime
import os

LOG_FILE = "intrusion_log.csv"

def log_intrusion():

    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, "a", newline="") as file:

        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["Time","Event"])

        writer.writerow([time,"Intrusion detected"])