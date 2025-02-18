# Production Program

This repository contains part of a larger production program written in Python to automate sensor configuration and integration with custom PCBs. It uses PyQt for a graphical user interface (GUI) and communicates via serial connections to streamline sensor setup at a hardware level.

---

## Overview

This application automates the process of configuring sensors by interacting with custom PCBs through serial communication. By automating routine tasks (like setting parameters and reading sensor data), it helps reduce errors and speeds up production workflows.

---

## Features

- **Serial Communication**: Establishes and manages connections to sensors via custom PCB hardware.
- **Automated Setup**: Reads and writes sensor settings with minimal user intervention.
- **PyQt GUI**: Provides a clear, user-friendly interface to control and monitor sensor status.
- **Modular Design**: Enables easy updates or extensions to handle additional sensor types and communication protocols.

---

## File Descriptions

| **File**              | **Purpose**                                                                                                                                   |
|-----------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| **main.py**           | Entry point of the program. Initializes the PyQt interface and manages the main workflow for sensor configuration.                            |
| **gui_layout.py**     | Defines the PyQt-based layout and widgets, separating user interface elements from the rest of the logic.                                     |
| **serial_comm.py**    | Handles all serial communication tasks, including opening ports, sending commands, and reading data from the sensors through the custom PCB. |
| **config_manager.py** | Contains functions to load, validate, and update sensor parameters. Helps keep configuration logic organized.                                 |
| **logger.py**         | Offers a simple logging mechanism for debugging and tracing sensor communication or user actions.                                             |
| **utilities.py**      | Provides shared helper functions (e.g., data parsing, formatting) to avoid code duplication.                                                  |
| **requirements.txt**  | Lists Python dependencies (including PyQt) needed to run the application.                                                                     |
| **README.md**         | This documentation file.                                                                                                                      |

---

## Installation

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/tokyokim0226/production_program.git
   cd production_program
Install Dependencies
Make sure Python 3.x is installed, then run:
bash
Copy
Edit
pip install -r requirements.txt
Connect Hardware
Attach your sensors to the custom PCB.
Connect the PCB to your computer via an available COM port or USB-to-serial adapter.
Usage
Launch the Application

bash
Copy
Edit
python main.py
The PyQt GUI will open, showing fields for sensor parameters.

Select COM Port
In the GUI, choose the correct port (especially important if multiple ports exist).

Adjust Sensor Settings
Enter parameters such as baud rate, calibration data, or other sensor-specific options.

## Author
- Full GitHub Code: The entire Python code in this repository was solely developed by the author.
### Additional Tasks:
- Contributed to basic PCB design and lower-level firmware coding.
- Ensured all hardware components worked together for an automated production workflow.
- Coordinated system integration to validate the final solution on real machines.

