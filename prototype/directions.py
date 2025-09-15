from gpiozero import Motor
from time import sleep

class Direction:
    def __init__(self):
        # GPIO pin setup (BCM numbering)
        left_front_pins = (17, 27)    # Forward, Backward
        left_rear_pins = (6, 5)       # Swapped due to wiring polarity
        right_front_pins = (23, 22)   # Swapped due to wiring polarity
        right_rear_pins = (12, 13)    # Forward, Backward

        # Initialize motors
        self.left_front = Motor(forward=left_front_pins[0], backward=left_front_pins[1])
        self.left_rear = Motor(forward=left_rear_pins[0], backward=left_rear_pins[1])
        self.right_front = Motor(forward=right_front_pins[0], backward=right_front_pins[1])
        self.right_rear = Motor(forward=right_rear_pins[0], backward=right_rear_pins[1])

        self.left_motor = [self.left_front, self.left_rear]
        self.right_motor = [self.right_front, self.right_rear]

    def run_motors(self, motors, direction, speed=1.0):
        for motor in motors:
            getattr(motor, direction)(speed)

    def stop_motors(self, motors):
        for motor in motors:
            motor.stop()

    def forward(self, speed=1.0):
        print("Moving forward")
        # Swap forward/backward due to wiring polarity
        self.run_motors(self.left_motor, "backward", speed)
        self.run_motors(self.right_motor, "backward", speed)

    def backward(self, speed=1.0):
        print("Moving backward")
        # Swap forward/backward due to wiring polarity
        self.run_motors(self.left_motor, "forward", speed)
        self.run_motors(self.right_motor, "forward", speed)

    def left(self, speed=1.0):
        print("Turning left")
        # Swap directions to fix turning polarity
        self.run_motors(self.left_motor, "forward", speed)
        self.run_motors(self.right_motor, "backward", speed)

    def right(self, speed=1.0):
        print("Turning right")
        # Swap directions to fix turning polarity
        self.run_motors(self.left_motor, "backward", speed)
        self.run_motors(self.right_motor, "forward", speed)

    def stop(self):
        print("Stopping")
        self.stop_motors(self.left_motor)
        self.stop_motors(self.right_motor)