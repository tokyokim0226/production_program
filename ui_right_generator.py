from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QButtonGroup, QLineEdit, QWidget, QTextEdit, 
    QGridLayout, QInputDialog, QMessageBox
)
from PyQt5.QtCore import Qt

class UIRightGenerator:
    def __init__(self, parent):
        self.parent = parent

    def create_manual_input_layout(self):
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
        self.parent.id_input.setMaxLength(4)

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
        self.parent.cmd_buttons = ["ADD", "COL", "POW", "CEN", "MAX", "DBG", "INF", "D_C"]
        self.parent.custom_cmd_buttons = []
        self.parent.cmd_buttons_layout = QGridLayout()

        self.update_cmd_buttons_layout(layout)

        op_button_group = QButtonGroup(self.parent)
        op_buttons = ["!", "?", "="]
        op_buttons_layout = QVBoxLayout()
        for op in op_buttons:
            button = QPushButton(op)
            button.setCheckable(True)
            button.clicked.connect(lambda checked, op=op: self.set_op(op))
            op_button_group.addButton(button)
            op_buttons_layout.addWidget(button)

        layout.addLayout(op_buttons_layout, 1, 3, len(op_buttons), 1)

        self.parent.data_input = QLineEdit()
        self.parent.data_input.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.parent.data_input, 1, 4, 1, 1)

        return layout

    def update_cmd_buttons_layout(self, layout):
        for i in reversed(range(self.parent.cmd_buttons_layout.count())):
            widget = self.parent.cmd_buttons_layout.itemAt(i).widget()
            if widget:
                self.parent.cmd_buttons_layout.removeWidget(widget)
                widget.setParent(None)

        for i, cmd in enumerate(self.parent.cmd_buttons):
            button = QPushButton(cmd)
            button.setCheckable(True)
            button.clicked.connect(lambda checked, cmd=cmd: self.set_cmd(cmd))
            self.parent.cmd_button_group.addButton(button)
            self.parent.cmd_buttons_layout.addWidget(button, i // 2, i % 2)

        for i, cmd in enumerate(self.parent.custom_cmd_buttons, len(self.parent.cmd_buttons)):
            button = QPushButton(cmd)
            button.setCheckable(True)
            button.clicked.connect(lambda checked, cmd=cmd: self.set_cmd(cmd))
            # button.setStyleSheet("background-color: #87CEFA;")
            self.parent.cmd_button_group.addButton(button)
            self.parent.cmd_buttons_layout.addWidget(button, i // 2, i % 2)

        layout.addLayout(self.parent.cmd_buttons_layout, 1, 1, (len(self.parent.cmd_buttons) + len(self.parent.custom_cmd_buttons)) // 2 + 1, 2)

    def set_cmd(self, cmd):
        self.parent.cmd_input.setText(cmd)
        self.update_len_chk()

    def set_op(self, op):
        self.parent.op_input.setText(op)
        self.update_len_chk()

    def increment_id(self):
        current_text = self.parent.id_input.text()
        if current_text == "9999":
            self.parent.id_input.setText("0000")
        else:
            try:
                current_value = int(current_text)
                if current_value < 9999:
                    self.parent.id_input.setText(f"{current_value + 1:04}")
            except ValueError:
                self.parent.id_input.setText("0001")

    def decrement_id(self):
        current_text = self.parent.id_input.text()
        if current_text == "0000":
            self.parent.id_input.setText("9999")
        else:
            try:
                current_value = int(current_text)
                if current_value > 0:
                    self.parent.id_input.setText(f"{current_value - 1:04}")
            except ValueError:
                self.parent.id_input.setText("0000")

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
        return placeholder

    def update_len_chk(self):
        id_value = self.parent.id_input.text()
        cmd_value = self.parent.cmd_input.text()
        op_value = self.parent.op_input.text()
        data_value = self.parent.data_input.text()

        stx = self.parent.protocol_handler.STX
        etx = self.parent.protocol_handler.ETX

        stx_and_content = f"{stx}{id_value}{cmd_value}{op_value}{data_value},"
        chk_value = self.parent.protocol_handler.calculate_checksum(stx_and_content)

        self.parent.chk_value.setText(chk_value)

        full_message = f"{stx_and_content}{chk_value}{etx}"
        self.parent.message_display.setText(full_message)
