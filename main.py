# main.py
import sys
from PyQt5.QtWidgets import QApplication
from serial_port_monitor import SerialPortMon

def load_stylesheet(app):
    with open("style.qss", "r") as file:
        app.setStyleSheet(file.read())

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Load the stylesheet
    load_stylesheet(app)

    ex = SerialPortMon()
    ex.show()
    sys.exit(app.exec_())
