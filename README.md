# Production Program

This repository contains a portion of a larger production program written in Python to automate sensor configuration and integration with custom PCBs. It leverages PyQt for a graphical user interface (GUI) and communicates over serial connections to simplify and speed up the process of configuring sensors at a hardware level.

> **Repository Link**: [https://github.com/tokyokim0226/production_program.git](https://github.com/tokyokim0226/production_program.git)

---

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [File Descriptions](#file-descriptions)
4. [Installation](#installation)
5. [Usage](#usage)
6. [How the PyQt App Works](#how-the-pyqt-app-works)
7. [Contributing](#contributing)
8. [License](#license)
9. [Author](#author)

---

## Overview

This software automates the manual process of configuring sensor settings. It interacts with custom PCB designs at a lower hardware level (also built and programmed in part by the author) through serial communication to set and retrieve sensor parameters. By automating these repetitive tasks, the program reduces errors and saves time in production environments.

---

## Features

- **Serial Communication**: Opens and manages connections to sensors through custom PCBs.
- **Automated Sensor Setup**: Reads and writes configuration settings quickly, avoiding manual parameter entry.
- **PyQt Interface**: Provides an intuitive GUI for users to control, monitor, and confirm sensor settings.
- **Modular Design**: Structured in a way that allows easy updates and integration of additional sensor types.

---

## File Descriptions

Below is a brief overview of each file in the repository:

| **File**          | **Purpose**                                                                                                                             |
|-------------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| `main.py`         | The central entry point of the application. It initializes the PyQt interface and orchestrates the configuration workflow.             |
| `gui_layout.py`   | Contains the PyQt-based layout and widget definitions, ensuring a clean separation of UI components from business logic.               |
| `serial_comm.py`  | Manages low-level serial communication, opening and closing ports, reading sensor data, and sending commands to the custom PCB.        |
| `config_manager.py` | Stores and retrieves sensor settings. It provides functions for validation, default parameter handling, and configuration updates.   |
| `logger.py`       | Handles logging of events and errors, making it easier to debug hardware communication or user input issues.                           |
| `utilities.py`    | Hosts reusable helper functions, such as parsing data from sensors, formatting output, and any other shared logic.                     |
| `requirements.txt`| Lists the Python dependencies needed (including PyQt and any other libraries) for seamless installation and environment setup.         |
| `README.md`       | This documentation file you are currently reading.                                                                                     |

*(Note: Depending on repository updates or additional confidentiality, some files may not be publicly visible.)*

---

## Installation

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/tokyokim0226/production_program.git
   cd production_program
