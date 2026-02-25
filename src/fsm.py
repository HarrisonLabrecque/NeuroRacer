# ------------------------------
# Use pigpio as gpiozero backend
# ------------------------------
from gpiozero import Device
from gpiozero.pins.pigpio import PiGPIOFactory

Device.pin_factory = PiGPIOFactory()

# ------------------------------
# Imports
# ------------------------------
from direction import Directions
from sensor import Sensor
from datalog import DataLog
import time


# ------------------------------
# RCState Class (Manual FSM)
# ------------------------------
class RCState:

    # State constants
    IDLE = "Idle"
    MOVE = "Moving"
    STOP = "Stopped"
    END = "Shutdown"

    def __init__(self):

        # ----- Hardware -----
        self.directions = Directions()

        self.sensor_front_left = Sensor(trigger_pin=20, echo_pin=21)
        self.sensor_front_right = Sensor(trigger_pin=5, echo_pin=6)

        self.log = DataLog()

        # Timers
        self.start_time = time.time()
        self.move_start_time = None
        self.move_duration = 10  # seconds per move

        # Movement sequence
        self.move_sequence = ["forward", "backward", "left", "right"]
        self.current_move_index = 0

        # Initial state
        self.state = self.IDLE
        self.on_enter_idle()

    # ------------------------------
    # State Transition Helper
    # ------------------------------
    def transition_to(self, new_state):
        self.state = new_state

        if new_state == self.IDLE:
            self.on_enter_idle()
        elif new_state == self.MOVE:
            self.on_enter_move()
        elif new_state == self.STOP:
            self.on_enter_stop()
        elif new_state == self.END:
            self.on_enter_end()

    # ------------------------------
    # State Handlers
    # ------------------------------
    def on_enter_idle(self):
        print("Entered idle")
        self.directions.stop()

    def on_enter_move(self):
        print("Started moving")
        self.log_current_state(self.state)

        direction = self.move_sequence[self.current_move_index]
        self.move_in_current_direction(direction)

    def on_enter_stop(self):
        print("Entered stop")
        self.directions.stop()
        self.log_current_state(self.state)

    def on_enter_end(self):
        print("Shutting down")
        self.directions.stop()
        self.sensor_front_left.close()
        self.sensor_front_right.close()
        self.log_current_state(self.state)
        self.log.close()

    # ------------------------------
    # Main Loop Logic
    # ------------------------------
    def update_state(self):
        elapsed_time = time.time() - self.start_time

        # IDLE → MOVE
        if self.state == self.IDLE:
            self.current_move_index = 0
            self.move_start_time = time.time()
            self.transition_to(self.MOVE)

        # MOVE
        elif self.state == self.MOVE:
            direction = self.move_sequence[self.current_move_index]

            # Obstacle detected in forward movement
            if direction == "forward" and not self.is_direction_clear(direction):
                print("Obstacle detected → stopping")
                self.transition_to(self.STOP)
                return

            # Rotate direction every X seconds
            if time.time() - self.move_start_time > self.move_duration:
                self.current_move_index = (
                    (self.current_move_index + 1)
                    % len(self.move_sequence)
                )
                self.move_start_time = time.time()
                self.move_in_current_direction(
                    self.move_sequence[self.current_move_index]
                )

            # Overall runtime limit (10 minutes)
            if elapsed_time >= 10 * 60:
                self.transition_to(self.END)

        # STOP
        elif self.state == self.STOP:
            direction = self.move_sequence[self.current_move_index]

            if direction == "forward" and self.is_direction_clear(direction):
                self.transition_to(self.MOVE)
            elif elapsed_time >= 10 * 60:
                self.transition_to(self.END)

    # ------------------------------
    # Obstacle Logic
    # ------------------------------
    def is_direction_clear(self, direction):
        if direction == "forward":
            left_blocked = self.sensor_front_left.check_threshold()
            right_blocked = self.sensor_front_right.check_threshold()
            return not (left_blocked and right_blocked)
        return True

    # ------------------------------
    # Movement Logic
    # ------------------------------
    def move_in_current_direction(self, direction):
        print(f"Attempting to move {direction}")

        if direction == "forward":
            left_blocked = self.sensor_front_left.check_threshold()
            right_blocked = self.sensor_front_right.check_threshold()

            if left_blocked and right_blocked:
                print("Both sides blocked. Stopping.")
                self.directions.stop()
                return

            if left_blocked:
                print("Left blocked → rotating right")
                self.directions.rotate_right()
                return

            if right_blocked:
                print("Right blocked → rotating left")
                self.directions.rotate_left()
                return

            self.directions.forward()

        elif direction == "backward":
            self.directions.backward()

        elif direction == "left":
            self.directions.rotate_left()

        elif direction == "right":
            self.directions.rotate_right()

    # ------------------------------
    # Logging
    # ------------------------------
    def log_current_state(self, state_name):
        direction = self.move_sequence[self.current_move_index]

        distance_left = self.sensor_front_left.get_distance()
        distance_right = self.sensor_front_right.get_distance()

        if direction == "forward":
            left_blocked = self.sensor_front_left.check_threshold()
            right_blocked = self.sensor_front_right.check_threshold()

            if left_blocked and right_blocked:
                status = "Obstacle both sides"
            elif left_blocked:
                status = "Obstacle left"
            elif right_blocked:
                status = "Obstacle right"
            else:
                status = "No obstacles"
        else:
            status = "Not forward movement"

        self.log.record(
            timestamp=time.time(),
            state=state_name,
            direction=direction,
            distance_front_left=distance_left,
            distance_front_right=distance_right,
            distance_back=None,
            status=status
        )


# ------------------------------
# Main Loop
# ------------------------------
if __name__ == "__main__":
    rc_fsm = RCState()

    try:
        while rc_fsm.state != rc_fsm.END:
            rc_fsm.update_state()
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Interrupted by user, shutting down...")
        rc_fsm.transition_to(rc_fsm.END)
