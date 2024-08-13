from PyQt5.QtWidgets import (
    QMainWindow, QLineEdit, QTextEdit, QComboBox, QLabel, QMessageBox, QWidget
)
from PyQt5.QtCore import QTimer
from protocol_handler import ProtocolHandler
from ui_initializer import UIInitializer
from connection_manager import ConnectionManager
from communication_manager import CommunicationManager
from logger import Logger
from ui_right_generator import update_len_chk


class SerialPortMon(QMainWindow):
    def __init__(self):
        super().__init__()

        self.serial_port = None
        self.protocol_handler = ProtocolHandler(self)
        self.current_font_size = 12

        # Initialize UI components early
        self.cmd_input = QLineEdit(self)
        self.op_input = QLineEdit(self)
        self.id_input = QLineEdit(self)
        self.data_input = QLineEdit(self)
        self.chk_value = QLineEdit(self)

        self.ui_initializer = UIInitializer(self)
        self.connection_manager = ConnectionManager(self)
        
        # Initialize buffer timer and timeout
        self.buffer_timer = QTimer(self)
        self.buffer_timeout = 500  # Set the buffer flush timeout to 500ms
        self.buffer_timer.timeout.connect(self.flush_worker_buffer)

        self.initUI()
        self.communication_manager = CommunicationManager(self)
        self.logger = Logger(self.log_table)
        self.change_font_size(12)

    def initUI(self):
        self.ui_initializer.setup_ui()

        self.cmd_input.textChanged.connect(lambda: update_len_chk(self))
        self.op_input.textChanged.connect(lambda: update_len_chk(self))
        self.id_input.textChanged.connect(lambda: update_len_chk(self))
        self.data_input.textChanged.connect(lambda: update_len_chk(self))

    def change_font_size(self, size):
        self.current_font_size = size
        for widget in self.findChildren((QTextEdit, QLineEdit, QComboBox, QLabel)):
            font = widget.font()
            font.setPointSize(size)
            widget.setFont(font)

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
