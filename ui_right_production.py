from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QGroupBox, QGridLayout, QSizePolicy
)
from PyQt5.QtGui import QIntValidator, QFont
from PyQt5.QtCore import Qt

class UIRightProduction(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)

        # "마지막으로 변환한 ID" label and textbox
        top_layout = QVBoxLayout()
        self.last_converted_label = QLabel("마지막으로 변환한 ID")
        self.last_converted_id_textbox = QLineEdit()
        self.last_converted_id_textbox.setReadOnly(True)
        self.last_converted_id_textbox.setFixedWidth(self.width() * 0.3)  # Takes up around 30% of the tab width
        self.last_converted_id_textbox.setFixedWidth(150)
        self.last_converted_id_textbox.setText("000")
        self.last_converted_id_textbox.setAlignment(Qt.AlignCenter)
        
        top_layout.addWidget(self.last_converted_label)
        top_layout.addWidget(self.last_converted_id_textbox)
        main_layout.addLayout(top_layout)

        # Label and textbox for "현재 지정 ID"
        current_id_label = QLabel("현재 지정 ID")
        current_id_label.setProperty("fontSize", "big")
        current_id_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(current_id_label)

        current_id_layout = QHBoxLayout()
        self.decrement_button = QPushButton("-")
        self.increment_button = QPushButton("+")

        self.decrement_button.setFixedSize(50, 50)  # Larger buttons
        self.increment_button.setFixedSize(50, 50)

        self.current_id_textbox = QLineEdit()
        self.current_id_textbox.setMaxLength(3)
        self.current_id_textbox.setAlignment(Qt.AlignCenter)
        self.current_id_textbox.setProperty("fontSize", "big")
        self.current_id_textbox.setValidator(QIntValidator(1, 998, self))

        current_id_layout.addWidget(self.decrement_button)
        current_id_layout.addWidget(self.current_id_textbox)
        current_id_layout.addWidget(self.increment_button)

        main_layout.addLayout(current_id_layout)

        # "Quick 바꾸기" and "Full 바꾸기" buttons next to each other
        button_layout = QHBoxLayout()
        self.full_button = QPushButton("Full 바꾸기")
        self.full_button.setToolTip("Placeholder for Full 바꾸기 explanation")

        button_layout.addWidget(self.full_button)
        main_layout.addLayout(button_layout)

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

    def decrement_id(self):
        current_value = int(self.current_id_textbox.text())
        if current_value > 1:
            self.current_id_textbox.setText(str(current_value - 1))

    def increment_id(self):
        current_value = int(self.current_id_textbox.text())
        if current_value < 998:
            self.current_id_textbox.setText(str(current_value + 1))
