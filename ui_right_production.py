from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QGroupBox, QGridLayout, QSizePolicy
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

        # Label and textbox for "현재 지정 ID"
        current_id_label = QLabel("현재 지정 ID")
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
        self.full_button.setToolTip("Placeholder for Full 바꾸기 explanation")
        self.full_button.clicked.connect(self.address_change_process)  # Connect to the single process function

        full_button_layout.addWidget(self.full_button)
        main_layout.addLayout(full_button_layout)

        # Adding space between buttons and 상태 label
        main_layout.addSpacing(20)

        # Status bar with three textboxes
        status_layout = QVBoxLayout()
        status_label = QLabel("상태:")
        status_layout.addWidget(status_label)

        self.status_box = QGroupBox()
        status_box_layout = QGridLayout()

        self.original_id_label = QLabel("기존 ID")
        self.converted_id_label = QLabel("변환 ID")
        self.check_label = QLabel("변환 ID 체크")

        self.original_id_status = QLineEdit()
        self.original_id_status.setReadOnly(True)
        self.converted_id_status = QLineEdit()
        self.converted_id_status.setReadOnly(True)
        self.check_status = QLineEdit()
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
        """Handle the entire address change process without nested functions."""
        self.parent.communication_manager.worker.message_received.connect(self.handle_initial_response)
        self.address_check()

    def handle_initial_response(self, message, time_taken):
        if "ADD=" in message:
            current_id = message[1:4]  # Extract the current device address (XXX)
            self.original_id_status.setText(current_id)

            # Step 2: Send the command to change the address after a delay
            new_id = f"{int(self.current_id_textbox.text()):03}"
            change_command = f"[{current_id}ADD!{new_id},"
            checksum = self.parent.protocol_handler.calculate_checksum(change_command)
            change_message = f"{change_command}{checksum}]"

            QTimer.singleShot(1000, lambda: self.parent.communication_manager.send_message(change_message))
            QTimer.singleShot(2000, lambda: self.verify_address_change(new_id))

            # Disconnect to prevent multiple calls
            self.parent.communication_manager.worker.message_received.disconnect(self.handle_initial_response)

    def verify_address_change(self, new_id):
        """Verify if the address was successfully changed."""
        self.address_check()

        def handle_verification(message, time_taken):
            if f"ADD={new_id}" in message:
                self.converted_id_status.setText(new_id)
                self.check_status.setText("Address changed successfully")

                # Increment the address for the next device
                self.increment_id()
            else:
                self.check_status.setText("Address change failed")

            # Disconnect after verification
            self.parent.communication_manager.worker.message_received.disconnect(handle_verification)

        self.parent.communication_manager.worker.message_received.connect(handle_verification)

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
