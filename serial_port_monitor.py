from PyQt5.QtWidgets import (
    QMainWindow, QTableWidget, QTableWidgetItem, QHeaderView,
    QLineEdit, QTextEdit, QComboBox, QLabel, QMessageBox,
    QPushButton, QInputDialog, QVBoxLayout, QWidget
)
from PyQt5.QtCore import QThread, QTimer, QDateTime, Qt
from protocol_handler import ProtocolHandler
from serial_reader_worker import SerialReaderWorker
from ui_initializer import UIInitializer
from connection_manager import ConnectionManager
from ui_right_generator import update_len_chk

class SerialPortMon(QMainWindow):
    def __init__(self):
        super().__init__()

        self.serial_port = None
        self.reading_thread = None
        self.worker = None
        self.protocol_handler = ProtocolHandler(self)
        self.current_font_size = 12

        self.buffer_timer = QTimer()
        self.buffer_timer.timeout.connect(self.flush_worker_buffer)
        self.buffer_timeout = 500  # Set the buffer flush timeout to 500ms

        # Initialize UI components early
        self.cmd_input = QLineEdit(self)
        self.op_input = QLineEdit(self)
        self.id_input = QLineEdit(self)
        self.data_input = QLineEdit(self)
        self.chk_value = QLineEdit(self)

        self.ui_initializer = UIInitializer(self)
        self.connection_manager = ConnectionManager(self)

        self.initUI()
        self.change_font_size(12)

    def initUI(self):
        self.ui_initializer.setup_ui()

        # Adjust signals to work with the new table and the externalized function
        self.cmd_input.textChanged.connect(lambda: update_len_chk(self))
        self.op_input.textChanged.connect(lambda: update_len_chk(self))
        self.id_input.textChanged.connect(lambda: update_len_chk(self))
        self.data_input.textChanged.connect(lambda: update_len_chk(self))


    def log_message(self, message_type, message, time_taken=""):
        """Log a message in the table."""
        row_position = self.log_table.rowCount()
        self.log_table.insertRow(row_position)

        # Create QTableWidgetItem for each cell and disable editing
        for i, text in enumerate([message_type, message, time_taken]):
            item = QTableWidgetItem(text)
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.log_table.setItem(row_position, i, item)

    def change_font_size(self, size):
        """Helper function to change the font size."""
        self.current_font_size = size
        for widget in self.findChildren((QTextEdit, QLineEdit, QComboBox, QLabel)):
            font = widget.font()  # Get the current font of the widget
            font.setPointSize(size)  # Change only the font size
            widget.setFont(font)  # Set the modified font back to the widget

    def send_generated_message(self):
        """Send the generated message directly and log it."""
        if self.serial_port and self.serial_port.is_open:
            try:
                message = self.message_display.text()
                start_time = QDateTime.currentDateTime()

                if self.protocol_handler.validate_message(message):
                    self.serial_port.write(message.encode('utf-8'))
                    end_time = QDateTime.currentDateTime()
                    elapsed_time = start_time.msecsTo(end_time)
                    self.log_message("Sent", message.strip(), f"{elapsed_time} ms")
                else:
                    QMessageBox.warning(self, "Invalid Input", "Message format is invalid")
            except Exception as e:
                self.log_message("Error", str(e))
        else:
            QMessageBox.warning(self, "Not Connected", "Please select a COM port.")

    def connect_serial(self):
        if not self.serial_port or not self.serial_port.is_open:
            self.connection_manager.connect_serial()
            if self.serial_port:
                self.log_message("Connect", f"Connected to {self.serial_port.port}", "")
        else:
            self.connection_manager.close_serial()
            self.log_message("Disconnect", f"Disconnected from {self.serial_port.port}", "")

    # Replace clear_log method to clear the table
    def clear_log(self):
        self.log_table.setRowCount(0)

    def get_serial_ports(self):
        return self.connection_manager.get_serial_ports()

    def start_reading_thread(self):
        self.reading_thread = QThread()  # Create a new thread
        self.worker = SerialReaderWorker(self.serial_port)  # Create a worker instance for the thread
        self.worker.moveToThread(self.reading_thread)  # Move the worker to the thread

        self.reading_thread.started.connect(self.worker.run)  # Connect thread started signal to worker run method
        self.worker.message_received.connect(self.handle_received_message_with_time)  # Connect worker message_received signal to handler
        self.worker.data_received.connect(self.reset_buffer_timer)  # Reset the buffer timer when new data is received
        self.worker.error_occurred.connect(self.protocol_handler.handle_error)  # Connect worker error_occurred signal to handler
        self.worker.finished.connect(self.reading_thread.quit)  # Connect worker finished signal to thread quit
        self.worker.finished.connect(self.worker.deleteLater)  # Ensure worker is deleted when finished
        self.reading_thread.finished.connect(self.reading_thread.deleteLater)  # Ensure thread is deleted when finished

        self.reading_thread.start()  # Start the thread

    def handle_received_message_with_time(self, message, time_taken):
        """Handle received messages and display the time taken."""
        self.log_message("Received", message.strip(), f"{time_taken} ms")

    def reset_buffer_timer(self):
        """Reset or start the buffer timer when new data is received."""
        self.buffer_timer.start(self.buffer_timeout)

    def flush_worker_buffer(self):
        """Flush the buffer in the worker and print its content if no ETX character is found within the timeout."""
        if self.worker:
            self.worker.flush_buffer()

    def stop_reading_thread(self):
        if self.worker:
            self.worker.running = False
            if self.reading_thread:
                self.reading_thread.quit()
                self.reading_thread.wait()
            self.worker = None
        if self.reading_thread:
            self.reading_thread = None

    def send_message(self):
        if not self.serial_port or not self.serial_port.is_open:
            self.connect_serial()

        if self.serial_port and self.serial_port.is_open:
            try:
                message = self.command_input.text()
                start_time = QDateTime.currentDateTime()

                if self.protocol_handler.validate_message(message):
                    self.serial_port.write(message.encode('utf-8'))
                    end_time = QDateTime.currentDateTime()
                    elapsed_time = start_time.msecsTo(end_time)
                    self.log_message("Sent", message.strip(), f"{elapsed_time} ms")  # Use log_message instead of text_display
                else:
                    QMessageBox.warning(self, "Invalid Input", "Message format is invalid")

            except Exception as e:
                self.log_message("Error", str(e))  # Log the error in the log table
        else:
            QMessageBox.warning(self, "Not Connected", "Please select a COM port.")

    def open_connection_dialog(self):
        self.connection_manager.connect_serial()

    def closeEvent(self, event):
        self.stop_reading_thread()
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
        event.accept()
