from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QGroupBox, QGridLayout, QSizePolicy, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt, QTimer

class UIRightProduction(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.retry_count = 0
        self.max_retries = 3
        self.timeout_duration = 1000  # 1 second timeout
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.handle_timeout)
        self.current_step = 0
        self.current_message = None
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)

        button_layout = QHBoxLayout()

        self.address_check_button = QPushButton("ADDRESS 체크하기")
        self.address_check_button.clicked.connect(self.address_check_only)

        self.device_reset_button = QPushButton("기기 초기화하기")
        self.device_reset_button.clicked.connect(self.factory_reset)

        button_layout.addWidget(self.address_check_button)
        button_layout.addWidget(self.device_reset_button)

        main_layout.addLayout(button_layout)
        main_layout.addSpacing(30)

        current_id_label = QLabel("지정 ID")
        current_id_label.setAlignment(Qt.AlignCenter)
        current_id_label.setObjectName("IDLabel")
        main_layout.addWidget(current_id_label)

        current_id_layout = QHBoxLayout()

        self.decrement_button = QPushButton("-")
        self.decrement_button.setFixedSize(50, 50)
        self.decrement_button.setObjectName("IDButton")

        self.increment_button = QPushButton("+")
        self.increment_button.setFixedSize(50, 50)
        self.increment_button.setObjectName("IDButton")

        self.current_id_textbox = QLineEdit()
        self.current_id_textbox.setMaxLength(3)
        self.current_id_textbox.setAlignment(Qt.AlignCenter)
        self.current_id_textbox.setValidator(QIntValidator(0, 998, self))
        self.current_id_textbox.setFixedHeight(50)
        self.current_id_textbox.setObjectName("IDTextBox")
        self.current_id_textbox.setText("1")

        current_id_layout.addWidget(self.decrement_button)
        current_id_layout.addWidget(self.current_id_textbox)
        current_id_layout.addWidget(self.increment_button)

        main_layout.addLayout(current_id_layout)

        full_button_layout = QHBoxLayout()
        self.full_button = QPushButton("ADDRESS 바꾸기")
        self.full_button.setFixedHeight(50)
        self.full_button.setToolTip("Placeholder for Full 바꾸기 explanation")
        self.full_button.clicked.connect(self.address_change_process)

        full_button_layout.addWidget(self.full_button)
        main_layout.addLayout(full_button_layout)

        main_layout.addSpacing(20)

        status_layout = QHBoxLayout()
        status_label = QLabel("상태:")
        status_label.setObjectName("status")
        status_layout.addWidget(status_label)

        status_layout.addSpacing(20)

        self.status_box = QGroupBox()
        status_box_layout = QGridLayout()

        self.original_id_label = QLabel("기존 ID")
        self.converted_id_label = QLabel("변환 ID")
        self.check_label = QLabel("변환 ID 체크")

        self.original_id_status = QLineEdit()
        self.original_id_status.setAlignment(Qt.AlignCenter)
        self.original_id_status.setReadOnly(True)

        self.converted_id_status = QLineEdit()
        self.converted_id_status.setAlignment(Qt.AlignCenter)
        self.converted_id_status.setReadOnly(True)

        self.check_status = QLineEdit()
        self.check_status.setAlignment(Qt.AlignCenter)
        self.check_status.setReadOnly(True)

        status_box_layout.addWidget(self.original_id_label, 0, 0, Qt.AlignCenter)
        status_box_layout.addWidget(self.converted_id_label, 0, 1, Qt.AlignCenter)
        status_box_layout.addWidget(self.check_label, 0, 2, Qt.AlignCenter)

        status_box_layout.addWidget(self.original_id_status, 1, 0)
        status_box_layout.addWidget(self.converted_id_status, 1, 1)
        status_box_layout.addWidget(self.check_status, 1, 2)

        self.status_box.setLayout(status_box_layout)
        status_layout.addWidget(self.status_box)

        main_layout.addLayout(status_layout)

        self.placeholder_textbox = QLineEdit()
        self.placeholder_textbox.setReadOnly(True)
        self.placeholder_textbox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_layout.addWidget(self.placeholder_textbox)

        self.decrement_button.clicked.connect(self.decrement_id)
        self.increment_button.clicked.connect(self.increment_id)

    def address_check_only(self):
        """Send a message to check the address."""
        self.current_message = "[999ADD?,30]"
        self.parent.communication_manager.send_message(self.current_message)

    def factory_reset(self):
        if not self.parent.serial_port or not self.parent.serial_port.is_open:
            self.parent.logger.log_message("Error", "No serial port is connected.")
            return
        # Step 1: Send the message to check the current address
        self.current_message = "[999ADD?,30]"
        self.parent.communication_manager.send_message(self.current_message)

        # Connect the message_received signal to handle the response
        self.parent.communication_manager.worker.message_received.connect(self.factory_reset_response)

    def factory_reset_response(self, message, time_taken):
        # Step 2: Process the received address and send the factory reset command
        if "ADD=" in message:
            current_id = message[1:4]  # Extract the address (XXX) from the message

            # Create the factory reset command using the extracted address
            reset_command = f"[{current_id}POW!FRESET,"
            checksum = self.parent.protocol_handler.calculate_checksum(reset_command)
            factory_reset_message = f"{reset_command}{checksum}]"

            # Send the factory reset command
            self.parent.communication_manager.send_message(factory_reset_message)

            # Disconnect the signal to avoid it being called again unintentionally
            self.parent.communication_manager.worker.message_received.disconnect(self.factory_reset_response)

    def address_change_process(self):
        if not self.parent.serial_port or not self.parent.serial_port.is_open:
            self.parent.logger.log_message("Error", "No serial port is connected.")
            return

        self.full_button.setEnabled(False)
        self.clear_status_boxes()
        self.log_address_change_start()

        self.current_step = 1
        self.current_message = "[999ADD?,30]"
        self.retry_count = 0
        self.send_message_with_retry()

    def send_message_with_retry(self):
        """Send the current message with retry mechanism."""
        # Check if the connection is valid and worker exists
        if not self.parent.serial_port or not self.parent.serial_port.is_open:
            self.abort_process("No serial port is connected.")
            return

        if not self.parent.communication_manager.worker:
            self.abort_process("Communication worker is not initialized.")
            return

        # Retry mechanism
        if self.retry_count < self.max_retries:
            self.retry_count += 1
            self.parent.communication_manager.send_message(self.current_message)

            # Ensure the timer starts only when a message is sent
            self.timer.start(self.timeout_duration)

            # Connect the signal to handle the message, but make sure worker exists
            try:
                self.parent.communication_manager.worker.message_received.connect(self.handle_message_received)
            except AttributeError:
                self.abort_process("Failed to connect to communication worker. Process aborted.")
        else:
            self.abort_process("No response received after 3 attempts. Process aborted.")


    def handle_message_received(self, message, time_taken):
        """Handle the received message based on the current step."""
        self.timer.stop()
        self.parent.communication_manager.worker.message_received.disconnect(self.handle_message_received)

        if self.current_step == 1:
            if "ADD=" in message:
                current_id = message[1:4]
                self.original_id_status.setText(current_id)

                if current_id == "000":
                    self.original_id_status.setStyleSheet("background-color: #34a853; color: white;")
                else:
                    self.original_id_status.setStyleSheet("background-color: #fbbc05; color: white;")

                self.current_step = 2
                QTimer.singleShot(200, self.send_change_command)

        elif self.current_step == 2:
            if "ADD=" in message:
                current_id = message[1:4]
                new_id = f"{int(self.current_id_textbox.text()):03}"

                if current_id == new_id:
                    self.converted_id_status.setText(new_id)
                    self.converted_id_status.setStyleSheet("background-color: #34a853; color: white;")
                else:
                    self.converted_id_status.setStyleSheet("background-color: #ea4335; color: white;")

                self.current_step = 3
                QTimer.singleShot(200, self.verify_address_change)

        elif self.current_step == 3:
            new_id = f"{int(self.current_id_textbox.text()):03}"
            if f"ADD={new_id}" in message:
                self.check_status.setText("OK")
                self.check_status.setStyleSheet("background-color: #34a853; color: white;")
                self.increment_id()
                self.reset_after_success()

    def send_change_command(self):
        new_id = f"{int(self.current_id_textbox.text()):03}"
        current_id = self.original_id_status.text()
        change_command = f"[{current_id}ADD!{new_id},"
        checksum = self.parent.protocol_handler.calculate_checksum(change_command)
        self.current_message = f"{change_command}{checksum}]"
        self.retry_count = 0
        self.send_message_with_retry()

    def verify_address_change(self):
        self.current_message = "[999ADD?,30]"
        self.retry_count = 0
        self.send_message_with_retry()

    def handle_timeout(self):
        """Handle the timeout, retry the message or abort the process."""
        self.timer.stop()
        if self.retry_count < self.max_retries:
            self.send_message_with_retry()
        else:
            self.abort_process("No response received after 3 attempts. Process aborted.")

    def abort_process(self, error_message):
        """Abort the current process, log the error, and update the UI."""
        self.timer.stop()

        # Safely disconnect signals
        try:
            if self.parent.communication_manager.worker:
                self.parent.communication_manager.worker.message_received.disconnect(self.handle_message_received)
        except (TypeError, AttributeError):
            pass  # Ignore errors if worker is already None or not connected

        # Re-enable the ADD 바꾸기 button after the abort
        self.full_button.setEnabled(True)

        # Log the error message
        self.parent.logger.log_message("Error", error_message)

        # Update UI to indicate failure
        self.check_status.setText("FAILED")
        self.check_status.setStyleSheet("background-color: #ea4335; color: white;")


    def reset_after_success(self):
        """Reset the process after successful completion."""
        QTimer.singleShot(750, self.apply_lighter_shade)
        QTimer.singleShot(750, lambda: self.full_button.setEnabled(True))

    def clear_status_boxes(self):
        self.original_id_status.clear()
        self.converted_id_status.clear()
        self.check_status.clear()
        self.original_id_status.setStyleSheet("background-color: white;")
        self.converted_id_status.setStyleSheet("background-color: white;")
        self.check_status.setStyleSheet("background-color: white;")

    def log_address_change_start(self):
        log_table = self.parent.log_table
        row_count = log_table.rowCount()
        log_table.insertRow(row_count)
        log_table.setSpan(row_count, 0, 1, 3)
        item = QTableWidgetItem("ADD 바꾸기")
        item.setBackground(Qt.green)
        item.setTextAlignment(Qt.AlignCenter)
        log_table.setItem(row_count, 0, item)

    def apply_lighter_shade(self):
        lighter_green = "background-color: #b7e1cd; color: white;"
        lighter_orange = "background-color: #fce8b2; color: white;"
        lighter_red = "background-color: #f8c7c4; color: white;"

        if "#34a853" in self.original_id_status.styleSheet():
            self.original_id_status.setStyleSheet(lighter_green)
        elif "#fbbc05" in self.original_id_status.styleSheet():
            self.original_id_status.setStyleSheet(lighter_orange)

        if "#34a853" in self.converted_id_status.styleSheet():
            self.converted_id_status.setStyleSheet(lighter_green)
        elif "#ea4335" in self.converted_id_status.styleSheet():
            self.converted_id_status.setStyleSheet(lighter_red)

        if "#34a853" in self.check_status.styleSheet():
            self.check_status.setStyleSheet(lighter_green)
        elif "#ea4335" in self.check_status.styleSheet():
            self.check_status.setStyleSheet(lighter_red)

    def decrement_id(self):
        current_text = self.current_id_textbox.text()
        if current_text == "":
            self.current_id_textbox.setText("999")
        else:
            current_value = int(current_text)
            if current_value > 1:
                self.current_id_textbox.setText(str(current_value - 1))

    def increment_id(self):
        current_text = self.current_id_textbox.text()
        if current_text == "":
            self.current_id_textbox.setText("1")
        else:
            current_value = int(current_text)
            if current_value < 998:
                self.current_id_textbox.setText(str(current_value + 1))

