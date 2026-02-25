from gpiozero import DigitalOutputDevice, PWMOutputDevice
from time import sleep


class Directions:

    def __init__(self, speed=0.4):

        # ===== MOTOR PIN DEFINITIONS =====
        # M1 = Front Left
        self.m1_fwd = DigitalOutputDevice(17)
        self.m1_rev = DigitalOutputDevice(18)

        # M2 = Rear Left
        self.m2_fwd = DigitalOutputDevice(24)
        self.m2_rev = DigitalOutputDevice(25)

        # M3 = Front Right
        self.m3_fwd = DigitalOutputDevice(22)
        self.m3_rev = DigitalOutputDevice(23)

        # M4 = Rear Right
        self.m4_fwd = DigitalOutputDevice(26)
        self.m4_rev = DigitalOutputDevice(16)

        # ===== OPTIONAL PWM ENABLE PINS =====
        # (These behave like your old NSLEEP pins)
        self.en_left  = PWMOutputDevice(12, frequency=1000)
        self.en_right = PWMOutputDevice(13, frequency=1000)

        # Store speed (0.0–1.0)
        self.speed = speed

        # Apply initial speed
        self._apply_speed()

    # ===================================
    # INTERNAL HELPERS
    # ===================================

    def _apply_speed(self):
        """Apply PWM speed to both sides."""
        self.en_left.value = self.speed
        self.en_right.value = self.speed

    def set_speed(self, value):
        """Set speed 0.0–1.0."""
        self.speed = max(0.0, min(1.0, value))
        self._apply_speed()

    # ===================================
    # LOW LEVEL CONTROL
    # ===================================

    def stop_all(self):
        for pin in [
            self.m1_fwd, self.m1_rev,
            self.m2_fwd, self.m2_rev,
            self.m3_fwd, self.m3_rev,
            self.m4_fwd, self.m4_rev
        ]:
            pin.off()

    # ===================================
    # HIGH LEVEL MOVEMENT
    # ===================================

    def forward(self):
        self.stop_all()
        self.m1_fwd.on()
        self.m2_fwd.on()
        self.m3_fwd.on()
        self.m4_fwd.on()

    def backward(self):
        self.stop_all()
        self.m1_rev.on()
        self.m2_rev.on()
        self.m3_rev.on()
        self.m4_rev.on()

    def rotate_left(self):
        self.stop_all()
        # Left side backward
        self.m1_rev.on()
        self.m2_rev.on()
        # Right side forward
        self.m3_fwd.on()
        self.m4_fwd.on()

    def rotate_right(self):
        self.stop_all()
        # Left side forward
        self.m1_fwd.on()
        self.m2_fwd.on()
        # Right side backward
        self.m3_rev.on()
        self.m4_rev.on()

    def stop(self):
        self.stop_all()


# ===================================
# TEST SCRIPT (same behavior as before)
# ===================================

def main():
    bot = Directions(speed=0.3)

    print("Testing forward")
    bot.forward()
    sleep(5)

    print("Testing backward")
    bot.backward()
    sleep(5)

    print("Testing left rotation")
    bot.rotate_left()
    sleep(5)

    print("Testing right rotation")
    bot.rotate_right()
    sleep(5)

    print("Stopping")
    bot.stop()
    print("Test complete.")


if __name__ == "__main__":
    main()
