from PyQt5.QtWidgets import (
    QMainWindow, QLineEdit, QTextEdit, QComboBox, QLabel, QMessageBox, QWidget
)
from PyQt5.QtCore import QTimer
from protocol_handler import ProtocolHandler
from ui_initializer import UIInitializer
from connection_manager import ConnectionManager
from communication_manager import CommunicationManager
from logger import Logger
from ui_left_components import UILeftComponents
from ui_right_generator import UIRightGenerator

class SerialPortMon(QMainWindow):
    def __init__(self):
        super().__init__()

        self.serial_port = None
        self.protocol_handler = ProtocolHandler(self)
        self.current_font_size = 12

        self.cmd_input = QLineEdit(self)
        self.op_input = QLineEdit(self)
        self.id_input = QLineEdit(self)
        self.data_input = QLineEdit(self)
        self.chk_value = QLineEdit(self)

        self.ui_initializer = UIInitializer(self)
        self.ui_left_components = UILeftComponents(self)
        self.ui_right_generator = UIRightGenerator(self)

        self.buffer_timer = QTimer(self)
        self.buffer_timeout = 500
        self.buffer_timer.timeout.connect(self.flush_worker_buffer)

        self.initUI()
        
        # Initialize the ConnectionManager
        self.connection_manager = ConnectionManager(self)  # This line was missing
        
        self.communication_manager = CommunicationManager(self)
        self.logger = Logger(self.log_table)
        # self.change_font_size(12)

    def initUI(self):
        self.ui_initializer.setup_ui()

        self.cmd_input.textChanged.connect(lambda: self.ui_right_generator.update_len_chk())
        self.op_input.textChanged.connect(lambda: self.ui_right_generator.update_len_chk())
        self.id_input.textChanged.connect(lambda: self.ui_right_generator.update_len_chk())
        self.data_input.textChanged.connect(lambda: self.ui_right_generator.update_len_chk())

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
