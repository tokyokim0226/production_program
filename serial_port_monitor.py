from PyQt5.QtWidgets import (
    QMainWindow, QLineEdit, QTextEdit, QComboBox, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QTableWidget, QPushButton
)
from PyQt5.QtCore import QTimer
from protocol_handler import ProtocolHandler
from connection_manager import ConnectionManager
from communication_manager import CommunicationManager
from logger import Logger
from ui_left_components import UILeftComponents
from ui_right_generator import UIRightGenerator
from ui_right_production import UIRightProduction
from ui_menu import UIMenu

class SerialPortMon(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize the core attributes first
        self.serial_port = None
        self.protocol_handler = ProtocolHandler(self)

        # Initialize UI components early to set up dependencies
        self.cmd_input = QLineEdit(self)
        self.op_input = QLineEdit(self)
        self.id_input = QLineEdit(self)
        self.data_input = QLineEdit(self)
        self.chk_value = QLineEdit(self)

        # Set up the UI layout
        self.initUI()

        # Initialize the ConnectionManager and CommunicationManager
        self.connection_manager = ConnectionManager(self)
        self.communication_manager = CommunicationManager(self)

        # Initialize the logger after log_table is set up in initUI
        self.logger = Logger(self.log_table)

        self.buffer_timer = QTimer(self)
        self.buffer_timeout = 500
        self.buffer_timer.timeout.connect(self.flush_worker_buffer)

    def initUI(self):
        self.setWindowTitle("SerialPortMon")
        self.setGeometry(100, 100, 1200, 750)
        self.setMinimumSize(600, 300)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        # Left UI components
        self.ui_left_components = UILeftComponents(self)
        main_layout.addWidget(self.ui_left_components, 1)

        # Create a QTabWidget for the right side
        self.tabs = QTabWidget()

        # Tab 1: Original right side layout
        self.ui_right_generator = UIRightGenerator(self)
        tab1_widget = QWidget()
        tab1_layout = QVBoxLayout(tab1_widget)
        tab1_layout.addWidget(self.ui_right_generator)
        self.tabs.addTab(tab1_widget, "1 - 메시지 자동 생성")

        # Tab 2: New tab with the described layout
        self.ui_right_production = UIRightProduction(self)
        self.tabs.addTab(self.ui_right_production, "2 - ADD 자동 할당")

        main_layout.addWidget(self.tabs, 1)

        # Menu
        self.menu = UIMenu(self)

    def connect_serial(self):
        self.connection_manager.connect_serial()

    def clear_log(self):
        self.logger.clear_log()

    def send_message(self):
        message = self.command_input.text()
        self.communication_manager.send_message(message)

    def send_generated_message(self):
        self.communication_manager.send_generated_message()

    def open_connection_dialog(self):
        self.connection_manager.connect_serial()

    def flush_worker_buffer(self):
        """Flush the buffer in the worker and print its content if no ETX character is found within the timeout."""
        self.communication_manager.flush_worker_buffer()

    def closeEvent(self, event):
        self.communication_manager.stop_reading_thread()
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
        event.accept()
