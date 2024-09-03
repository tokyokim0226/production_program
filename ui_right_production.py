from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QGroupBox, QGridLayout, QSizePolicy
)

from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt

class UIRightProduction(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
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

        full_button_layout.addWidget(self.full_button)
        main_layout.addLayout(full_button_layout)

        # Adding space between buttons and 상태 label
        main_layout.addSpacing(20)

        # Status bar with three labels
        status_layout = QVBoxLayout()
        status_label = QLabel("상태:")
        status_layout.addWidget(status_label)

        self.status_box = QGroupBox()
        status_box_layout = QGridLayout()

        self.original_id_label = QLabel("기존 ID")
        self.converted_id_label = QLabel("변환 ID")
        self.check_label = QLabel("변환 ID 체크")

        self.original_id_status = QLabel()
        self.converted_id_status = QLabel()
        self.check_status = QLabel()

        # Double the height of the grid boxes
        self.original_id_status.setStyleSheet("background-color: gray; height: 40px")
        self.converted_id_status.setStyleSheet("background-color: gray; height: 40px")
        self.check_status.setStyleSheet("background-color: gray; height: 40px")

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
