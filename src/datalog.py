import csv
import os

class DataLog:
    def __init__(self, filename="robot_log.csv"):
        self.filename = filename
        file_exists = os.path.isfile(self.filename)

        self.file = open(self.filename, mode='a', newline='')
        self.writer = csv.DictWriter(
            self.file,
            fieldnames=[
                "timestamp",
                "state",
                "direction",
                "distance_front_left",
                "distance_front_right",
                "distance_back",
                "status"
            ]
        )

        if not file_exists:
            self.writer.writeheader()

    def record(
        self,
        timestamp,
        state,
        direction,
        distance_front_left,
        distance_front_right,
        status,
        distance_back=None   # Optional parameter
    ):
        """Record a single log entry"""

        self.writer.writerow({
            "timestamp": timestamp,
            "state": state,
            "direction": direction,
            "distance_front_left": distance_front_left,
            "distance_front_right": distance_front_right,
            "distance_back": distance_back,
            "status": status
        })

        self.file.flush()

    def close(self):
        self.file.close()