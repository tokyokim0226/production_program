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
        self.current_device_id = None  # To keep track of the current device ID
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)

        # Replace the '마지막으로 변환한 ID' label and textbox with two buttons
        button_layout = QHBoxLayout()

        self.address_check_button = QPushButton("ADDRESS 체크하기")
        self.address_check_button.clicked.connect(self.address_check)

        self.device_reset_button = QPushButton("기기 초기화하기")

        button_layout.addWidget(self.address_check_button)
        button_layout.addWidget(self.device_reset_button)

        main_layout.addLayout(button_layout)

        main_layout.addSpacing(30)

        # Label and textbox for "지정 ID"
        current_id_label = QLabel("지정 ID")
        current_id_label.setAlignment(Qt.AlignCenter)
        current_id_label.setObjectName("IDLabel")
        main_layout.addWidget(current_id_label)

        current_id_layout = QHBoxLayout()

        # Set object names for specific styling
        self.decrement_button = QPushButton("-")
        self.decrement_button.setFixedSize(50, 50)  # Larger buttons
        self.decrement_button.setObjectName("IDButton")

        self.increment_button = QPushButton("+")
        self.increment_button.setFixedSize(50, 50)
        self.increment_button.setObjectName("IDButton")

        self.current_id_textbox = QLineEdit()
        self.current_id_textbox.setMaxLength(3)
        self.current_id_textbox.setAlignment(Qt.AlignCenter)
        self.current_id_textbox.setValidator(QIntValidator(1, 998, self))
        self.current_id_textbox.setFixedHeight(50)  # Match the height of the buttons
        self.current_id_textbox.setObjectName("IDTextBox")  # Set object name for specific styling
        self.current_id_textbox.setText("1")  # Set the default value to 1

        current_id_layout.addWidget(self.decrement_button)
        current_id_layout.addWidget(self.current_id_textbox)
        current_id_layout.addWidget(self.increment_button)

        main_layout.addLayout(current_id_layout)

        # "Quick 바꾸기" and "Full 바꾸기" buttons next to each other
        full_button_layout = QHBoxLayout()
        self.full_button = QPushButton("ADDRESS 바꾸기")
        self.full_button.setFixedHeight(50)  # Match the height of the buttons
        self.full_button.setToolTip("Placeholder for Full 바꾸기 explanation")
        self.full_button.clicked.connect(self.address_change_process)  # Connect to the single process function

        full_button_layout.addWidget(self.full_button)
        main_layout.addLayout(full_button_layout)

        # Adding space between buttons and 상태 label
        main_layout.addSpacing(20)

        # Status bar with three textboxes
        status_layout = QHBoxLayout()
        status_label = QLabel("상태:")
        status_layout.addWidget(status_label)

        status_layout.addSpacing(20)

        self.status_box = QGroupBox()
        status_box_layout = QGridLayout()

        self.original_id_label = QLabel("기존 ID")
        self.converted_id_label = QLabel("변환 ID")
        self.check_label = QLabel("변환 ID 체크")

        # Make the textboxes centered
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

        # Placeholder textbox to take up remaining space
        self.placeholder_textbox = QLineEdit()
        self.placeholder_textbox.setReadOnly(True)
        self.placeholder_textbox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Expands to take up remaining space
        main_layout.addWidget(self.placeholder_textbox)

        # Connect increment and decrement buttons
        self.decrement_button.clicked.connect(self.decrement_id)
        self.increment_button.clicked.connect(self.increment_id)

    def address_check(self):
        """Send a message to check the address."""
        message = "[999ADD?,30]"
        self.parent.communication_manager.send_message(message)

    def address_change_process(self):
        if not self.parent.serial_port or not self.parent.serial_port.is_open:
            self.parent.logger.log_message("Error", "No serial port is connected.")
            return
        
        """Handle the entire address change process based on receiving messages."""
        # Disable the button to prevent multiple clicks
        self.full_button.setEnabled(False)

        # Clear status boxes and reset color
        self.clear_status_boxes()

        # Log the start of the process
        self.log_address_change_start()

        self.parent.communication_manager.worker.message_received.connect(self.handle_initial_response)
        self.address_check()

    def clear_status_boxes(self):
        """Clear the text and reset the background color of the status boxes."""
        self.original_id_status.clear()
        self.converted_id_status.clear()
        self.check_status.clear()

        self.original_id_status.setStyleSheet("background-color: white;")
        self.converted_id_status.setStyleSheet("background-color: white;")
        self.check_status.setStyleSheet("background-color: white;")

    def log_address_change_start(self):
        """Log the start of the ADDRESS 바꾸기 process."""
        log_table = self.parent.log_table  # Assuming you have a QTableWidget for logs

        row_count = log_table.rowCount()
        log_table.insertRow(row_count)
        log_table.setSpan(row_count, 0, 1, 3)  # Span across 3 columns

        item = QTableWidgetItem("ADD 바꾸기")
        item.setBackground(Qt.green)
        item.setTextAlignment(Qt.AlignCenter)
        log_table.setItem(row_count, 0, item)

    def handle_initial_response(self, message, time_taken):
        if "ADD=" in message:
            current_id = message[1:4]  # Extract the current device address (XXX)
            self.original_id_status.setText(current_id)

            # Apply color based on the ID
            if current_id == "000":
                self.original_id_status.setStyleSheet("background-color: #34a853; color: white;")  # Darker green
            else:
                self.original_id_status.setStyleSheet("background-color: #fbbc05; color: white;")  # Darker orange

            # Step 2: Send the command to change the address after 0.2 seconds delay
            QTimer.singleShot(200, self.send_change_command)

            # Disconnect this handler to avoid repeated handling
            self.parent.communication_manager.worker.message_received.disconnect(self.handle_initial_response)

    def send_change_command(self):
        new_id = f"{int(self.current_id_textbox.text()):03}"
        current_id = self.original_id_status.text()
        change_command = f"[{current_id}ADD!{new_id},"
        checksum = self.parent.protocol_handler.calculate_checksum(change_command)
        change_message = f"{change_command}{checksum}]"
        self.parent.communication_manager.send_message(change_message)

        # Connect to handle the response after address change
        self.parent.communication_manager.worker.message_received.connect(self.handle_address_change_response)

    def handle_address_change_response(self, message, time_taken):
        if "ADD=" in message:
            current_id = message[1:4]
            new_id = f"{int(self.current_id_textbox.text()):03}"

            # Check if the address has changed
            if current_id == new_id:
                self.converted_id_status.setText(new_id)
                self.converted_id_status.setStyleSheet("background-color: #34a853; color: white;")  # Darker green
            else:
                self.converted_id_status.setStyleSheet("background-color: #ea4335; color: white;")  # Red

            # Step 3: Verify the address change after 0.2 seconds delay
            QTimer.singleShot(200, self.address_check)

            # Disconnect this handler to avoid repeated handling
            self.parent.communication_manager.worker.message_received.disconnect(self.handle_address_change_response)

            # Connect to handle the final verification
            self.parent.communication_manager.worker.message_received.connect(self.handle_verification_response)

    def handle_verification_response(self, message, time_taken):
        new_id = f"{int(self.current_id_textbox.text()):03}"

        if f"ADD={new_id}" in message:
            self.check_status.setText("OK")  # Show "OK" for successful address change
            self.check_status.setStyleSheet("background-color: #34a853; color: white;")  # Darker green

            # Increment the address for the next device
            self.increment_id()

        else:
            self.check_status.setText("NOT OK")  # Show "NOT OK" for unsuccessful address change
            self.check_status.setStyleSheet("background-color: #ea4335; color: white;")  # Red

        # Apply lighter shade after 3 seconds
        QTimer.singleShot(750, self.apply_lighter_shade)

        # Re-enable the button after the process is complete
        QTimer.singleShot(750, lambda: self.full_button.setEnabled(True))

        # Disconnect this handler after verification
        self.parent.communication_manager.worker.message_received.disconnect(self.handle_verification_response)

    def apply_lighter_shade(self):
        """Apply a lighter shade to all status textboxes."""
        lighter_green = "background-color: #b7e1cd; color: white;"  # Lighter green
        lighter_orange = "background-color: #fce8b2; color: white;"  # Lighter orange
        lighter_red = "background-color: #f8c7c4; color: white;"  # Lighter red

        # Apply the lighter shade based on the current color
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
        if current_text == "":  # Handle empty case
            self.current_id_textbox.setText("999")
        else:
            current_value = int(current_text)
            if current_value > 1:
                self.current_id_textbox.setText(str(current_value - 1))

    def increment_id(self):
        current_text = self.current_id_textbox.text()
        if current_text == "":  # Handle empty case
            self.current_id_textbox.setText("1")
        else:
            current_value = int(current_text)
            if current_value < 998:
                self.current_id_textbox.setText(str(current_value + 1))
