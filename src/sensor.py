from gpiozero import DistanceSensor

class Sensor:
    def __init__(self, trigger_pin, echo_pin, threshold_cm=20):
        self.threshold_cm = threshold_cm
        self.sensor = DistanceSensor(
            trigger=trigger_pin,
            echo=echo_pin
        )

    def get_distance(self):
        return round(self.sensor.distance * 100, 2)

    def check_threshold(self,threshold_cm = None):
        return self.get_distance() <= self.threshold_cm

    def close(self):
        self.sensor.close()
