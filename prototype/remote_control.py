from directions import Direction  # Import the motor control class
import cwiid                     # Import the library for Wiimote interaction
import time                     # Used for delays and sleep control

# Create an instance of the Direction class to control the robot
robo = Direction()

# Prompt the user to connect the Wiimote
print("Press and hold 1 + 2 on your Wiimote now...")

# Try to connect to the Wiimote
try:
    wii = cwiid.Wiimote()
except RuntimeError:
    print("Failed to connect to the Wiimote. Try again.")
    exit()

# Confirm the connection
print("Wiimote connected!")

# Set the reporting mode to button presses
wii.rpt_mode = cwiid.RPT_BTN

# Keep track of the last command sent to avoid repeating it unnecessarily
last_command = None

# Main control loop
while True:
    # Read the current state of the Wiimote buttons
    buttons = wii.state["buttons"]
    command = None

    # Determine which button is pressed and assign a command
    if buttons & cwiid.BTN_LEFT:
        command = "left"  # Turn left
    elif buttons & cwiid.BTN_RIGHT:
        command = "right"  # Turn right
    elif buttons & cwiid.BTN_UP:
        command = "forward"  # Move forward
    elif buttons & cwiid.BTN_DOWN:
        command = "backward"  # Move backward
    else:
        command = "stop"  # No button pressed, stop movement

    # Only send the command if it's different from the last one
    if command != last_command:
        getattr(robo, command)()  # Dynamically call the method (e.g., robo.forward())
        last_command = command    # Update the last command

    # Small delay to reduce CPU usage and avoid spamming commands
    time.sleep(0.2)
