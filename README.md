# 🚗 Project Overview

NeuroRacer is an autonomous RC car project powered by a Raspberry Pi 3 B+. The goal is to explore robotics, embedded systems, and computer vision using Python and OpenCV.

# 🔧 Current Features

The prototype supports basic motor control and manual driving using a Wiimote. Line following using OpenCV is under development. Obstacle avoidance is planned for a future stage of the prototype.

# 🧠 Learning Goals

This project is designed as a learning platform for working with low-level hardware, GPIO-based motor control, and real-time image processing. It also serves as a foundation for future work in AI and machine learning.

# 🛠️ Hardware Components

The car uses a standard RC chassis powered by four 3V–6V DC motors. Two L298N motor drivers control the motors. One battery pack powers the raspberry pi while another battery pack powers the motors, and all components are connected using male-to-female and male-to-male jumper wires.

# 💻 Software & Libraries

The code is written in Python 3. Motor control is handled with the gpiozero library. Manual control is implemented using python3-wiimote. OpenCV will be used for image processing. Bluetooth dependencies include bison, flex, automake, and libbluetooth-dev.

# 🚀 Future Plans

Future versions will include obstacle detection using ultrasonic sensors, camera-based vision, and AI/ML-driven navigation. A web interface for remote control and monitoring is also planned.
