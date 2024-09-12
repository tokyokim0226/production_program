#ui_right_generator.py

from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QButtonGroup, QLineEdit, QWidget, QTextEdit, 
    QGridLayout, QInputDialog, QMessageBox, QSizePolicy
)
from PyQt5.QtCore import Qt

class UIRightGenerator(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.cmd_buttons_layout = None  # Store the layout here
        self.op_button_group = None  # Store the OP button group
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        id_layout = self.create_manual_input_layout()
        len_chk_layout = self.create_len_chk_layout()
        message_display_layout = self.create_message_display_layout()

        layout.addLayout(id_layout)
        layout.addLayout(len_chk_layout)
        layout.addLayout(message_display_layout)

        placeholder = self.create_placeholder_widget()
        layout.addWidget(placeholder)

        self.setLayout(layout)

        # Set default values and update the UI accordingly
        self.parent.id_input.setText("999")
        self.set_cmd("ADD")
        self.set_op("?")

        # Connect signals to update the generated message in real-time
        self.parent.id_input.textChanged.connect(self.update_len_chk)
        self.parent.data_input.textChanged.connect(self.update_len_chk)
        self.parent.cmd_input.textChanged.connect(self.update_len_chk)
        self.parent.op_input.textChanged.connect(self.update_len_chk)

        # Connect the DATA input field to the new limitation and upper-case handler
        self.parent.data_input.textChanged.connect(self.limit_and_convert_data)

    def limit_and_convert_data(self):
        # Get the current input text
        current_text = self.parent.data_input.text()
        
        # Limit the text to 6 characters and convert to uppercase
        limited_text = current_text[:6].upper()
        
        # Block signals temporarily to avoid recursive textChanged triggering
        self.parent.data_input.blockSignals(True)
        
        # Update the DATA input field with the modified text
        self.parent.data_input.setText(limited_text)
        
        # Re-enable signals
        self.parent.data_input.blockSignals(False)

        # Update length and checksum after modifying the input
        self.update_len_chk()

    def create_manual_input_layout(self):
        # Initialize UI components early to set up dependencies
        self.parent.cmd_input = QLineEdit(self.parent)
        self.parent.op_input = QLineEdit(self.parent)
        self.parent.id_input = QLineEdit(self.parent)
        self.parent.data_input = QLineEdit(self.parent)
        self.parent.chk_value = QLineEdit(self.parent)

        layout = QGridLayout()

        id_label = QLabel("ID")
        id_label.setAlignment(Qt.AlignCenter)
        cmd_label = QLabel("CMD")
        cmd_label.setAlignment(Qt.AlignCenter)
        op_label = QLabel("OP")
        op_label.setAlignment(Qt.AlignCenter)
        data_label = QLabel("DATA")
        data_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(id_label, 0, 0, 1, 1)
        layout.addWidget(cmd_label, 0, 1, 1, 2)
        layout.addWidget(op_label, 0, 3, 1, 1)
        layout.addWidget(data_label, 0, 4, 1, 1)

        id_input_layout = QHBoxLayout()
        self.parent.id_input = QLineEdit()
        self.parent.id_input.setAlignment(Qt.AlignCenter)
        self.parent.id_input.setMaximumWidth(80)
        self.parent.id_input.setMaxLength(3)

        down_button = QPushButton("-")
        down_button.setMaximumWidth(40)
        down_button.clicked.connect(self.decrement_id)

        up_button = QPushButton("+")
        up_button.setMaximumWidth(40)
        up_button.clicked.connect(self.increment_id)

        id_input_layout.addWidget(down_button)
        id_input_layout.addWidget(self.parent.id_input)
        id_input_layout.addWidget(up_button)

        layout.addLayout(id_input_layout, 1, 0, 1, 1)

        self.parent.cmd_button_group = QButtonGroup(self.parent)
        self.parent.cmd_buttons = ["ADD", "COL", "POW", "MIN", "MAX", "DBG", "INF", "D_C", "DET", "SEA", "MGS"]
        self.parent.custom_cmd_buttons = []
        self.cmd_buttons_layout = QGridLayout()  # Store the layout here

        self.update_cmd_buttons_layout()

        self.op_button_group = QButtonGroup(self.parent)
        op_buttons = ["!", "?", "="]
        op_buttons_layout = QVBoxLayout()
        for op in op_buttons:
            button = QPushButton(op)
            button.setCheckable(True)
            button.clicked.connect(lambda checked, op=op: self.set_op(op))
            self.op_button_group.addButton(button)
            op_buttons_layout.addWidget(button)

        layout.addLayout(op_buttons_layout, 1, 3, len(op_buttons), 1)

        self.parent.data_input = QLineEdit()
        self.parent.data_input.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.parent.data_input, 1, 4, 1, 1)

        layout.addLayout(self.cmd_buttons_layout, 1, 1, (len(self.parent.cmd_buttons) + len(self.parent.custom_cmd_buttons)) // 2 + 1, 2)

        return layout

    def update_cmd_buttons_layout(self):
        # Ensure the stored layout is used
        for i in reversed(range(self.cmd_buttons_layout.count())):
            widget = self.cmd_buttons_layout.itemAt(i).widget()
            if widget:
                self.cmd_buttons_layout.removeWidget(widget)
                widget.setParent(None)

        for i, cmd in enumerate(self.parent.cmd_buttons):
            button = QPushButton(cmd)
            button.setCheckable(True)
            button.clicked.connect(lambda checked, cmd=cmd: self.set_cmd(cmd))
            self.parent.cmd_button_group.addButton(button)
            self.cmd_buttons_layout.addWidget(button, i // 2, i % 2)

        for i, cmd in enumerate(self.parent.custom_cmd_buttons, len(self.parent.cmd_buttons)):
            button = QPushButton(cmd)
            button.setCheckable(True)
            button.clicked.connect(lambda checked, cmd=cmd: self.set_cmd(cmd))
            self.parent.cmd_button_group.addButton(button)
            self.cmd_buttons_layout.addWidget(button, i // 2, i % 2)

    def set_cmd(self, cmd):
        # Check the corresponding button visually
        for button in self.parent.cmd_button_group.buttons():
            if button.text() == cmd:
                button.setChecked(True)
                break

        self.parent.cmd_input.setText(cmd)
        self.update_len_chk()

    def set_op(self, op):
        # Check the corresponding button visually
        for button in self.op_button_group.buttons():
            if button.text() == op:
                button.setChecked(True)
                break

        self.parent.op_input.setText(op)
        if op == "?":
            self.parent.data_input.setText("")  # Clear the DATA input
            self.parent.data_input.setReadOnly(True)
            self.parent.data_input.setStyleSheet("background-color: #e0e0e0;")  # Lighter grey for the DATA input
        else:
            self.parent.data_input.setReadOnly(False)
            self.parent.data_input.setStyleSheet("")  # Reset the DATA input styling
        self.update_len_chk()

    def increment_id(self):
        current_text = self.parent.id_input.text()
        if current_text.isdigit():
            current_value = int(current_text)
            if current_value < 999:
                self.parent.id_input.setText(str(current_value + 1))
            else:
                self.parent.id_input.setText("0")
        else:
            self.parent.id_input.setText("1")

    def decrement_id(self):
        current_text = self.parent.id_input.text()
        if current_text.isdigit():
            current_value = int(current_text)
            if current_value > 0:
                self.parent.id_input.setText(str(current_value - 1))
            else:
                self.parent.id_input.setText("999")
        else:
            self.parent.id_input.setText("999")

    def create_len_chk_layout(self):
        len_chk_layout = QHBoxLayout()

        chk_layout = QHBoxLayout()
        chk_label = QLabel("CHK")
        self.parent.chk_value = QLineEdit()
        self.parent.chk_value.setMaximumWidth(200)
        self.parent.chk_value.setReadOnly(True)
        self.parent.chk_value.setAlignment(Qt.AlignCenter)
        chk_layout.addWidget(chk_label)
        chk_layout.addWidget(self.parent.chk_value)

        len_chk_layout.addLayout(chk_layout)

        return len_chk_layout

    def create_message_display_layout(self):
        message_display_layout = QHBoxLayout()

        self.parent.message_display = QLineEdit()
        self.parent.message_display.setObjectName("generated_message")
        self.parent.message_display.setReadOnly(True)
        self.parent.message_display.setAlignment(Qt.AlignCenter)

        send_button = QPushButton("Send")
        send_button.clicked.connect(self.parent.send_generated_message)

        message_display_layout.addWidget(self.parent.message_display)
        message_display_layout.addWidget(send_button)

        return message_display_layout

    def create_placeholder_widget(self):
        placeholder = QTextEdit()
        placeholder.setReadOnly(True)
        placeholder.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Ensure it fills available space
        return placeholder

    def update_len_chk(self):
        id_value = self.parent.id_input.text()
        cmd_value = self.parent.cmd_input.text()
        op_value = self.parent.op_input.text()
        data_value = self.parent.data_input.text()

        # Format the ID as a 3-digit number for the message
        if id_value.isdigit():
            id_value = f"{int(id_value):03}"

        stx = self.parent.protocol_handler.STX
        etx = self.parent.protocol_handler.ETX

        # Adjust the content based on whether the "?" operator is selected
        if op_value == "?":
            stx_and_content = f"{stx}{id_value}{cmd_value}{op_value},"
        else:
            stx_and_content = f"{stx}{id_value}{cmd_value}{op_value}{data_value},"

        chk_value = self.parent.protocol_handler.calculate_checksum(stx_and_content)

        self.parent.chk_value.setText(chk_value)

        full_message = f"{stx_and_content}{chk_value}{etx}"
        self.parent.message_display.setText(full_message)
