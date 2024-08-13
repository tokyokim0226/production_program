from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                             QButtonGroup, QLineEdit, QWidget, QTextEdit, 
                             QGridLayout, QInputDialog, QMessageBox)
from PyQt5.QtCore import Qt

def create_manual_input_layout(parent):
    layout = QGridLayout()

    # Create labels
    id_label = QLabel("ID")
    id_label.setAlignment(Qt.AlignCenter)
    cmd_label = QLabel("CMD")
    cmd_label.setAlignment(Qt.AlignCenter)
    op_label = QLabel("OP")
    op_label.setAlignment(Qt.AlignCenter)
    data_label = QLabel("DATA")
    data_label.setAlignment(Qt.AlignCenter)

    # Add labels to the grid layout in the first row
    layout.addWidget(id_label, 0, 0, 1, 1)
    layout.addWidget(cmd_label, 0, 1, 1, 2)
    layout.addWidget(op_label, 0, 3, 1, 1)
    layout.addWidget(data_label, 0, 4, 1, 1)

    # ID Input with buttons
    id_input_layout = QHBoxLayout()
    parent.id_input = QLineEdit()
    parent.id_input.setAlignment(Qt.AlignCenter)
    parent.id_input.setMaximumWidth(80)
    parent.id_input.setMaxLength(4)

    down_button = QPushButton("-")
    down_button.setMaximumWidth(40)
    down_button.clicked.connect(lambda: decrement_id(parent.id_input))

    up_button = QPushButton("+")
    up_button.setMaximumWidth(40)
    up_button.clicked.connect(lambda: increment_id(parent.id_input))

    id_input_layout.addWidget(down_button)
    id_input_layout.addWidget(parent.id_input)
    id_input_layout.addWidget(up_button)

    # Add the ID input layout to the grid layout
    layout.addLayout(id_input_layout, 1, 0, 1, 1)

    # CMD buttons
    parent.cmd_button_group = QButtonGroup(parent)
    parent.cmd_buttons = ["ADD", "COL", "POW", "CEN", "MAX", "DBG", "INF", "D_C"]  # Original commands
    parent.custom_cmd_buttons = []
    parent.cmd_buttons_layout = QGridLayout()

    update_cmd_buttons_layout(parent, layout)

    # OP buttons
    op_button_group = QButtonGroup(parent)
    op_buttons = ["!", "?", "="]
    op_buttons_layout = QVBoxLayout()
    for op in op_buttons:
        button = QPushButton(op)
        button.setCheckable(True)
        button.clicked.connect(lambda checked, op=op: set_op(parent, op))
        op_button_group.addButton(button)
        op_buttons_layout.addWidget(button)

    # Add OP buttons to the grid layout
    layout.addLayout(op_buttons_layout, 1, 3, len(op_buttons), 1)

    # Data input
    parent.data_input = QLineEdit()
    parent.data_input.setAlignment(Qt.AlignCenter)

    # Add DATA input to the grid layout
    layout.addWidget(parent.data_input, 1, 4, 1, 1)

    return layout

def update_cmd_buttons_layout(parent, layout):
    """Update the CMD buttons layout whenever changes are made."""
    # Clear existing buttons
    for i in reversed(range(parent.cmd_buttons_layout.count())):
        widget = parent.cmd_buttons_layout.itemAt(i).widget()
        if widget:
            parent.cmd_buttons_layout.removeWidget(widget)
            widget.setParent(None)

    # Add original CMD buttons
    for i, cmd in enumerate(parent.cmd_buttons):
        button = QPushButton(cmd)
        button.setCheckable(True)
        button.clicked.connect(lambda checked, cmd=cmd: set_cmd(parent, cmd))
        parent.cmd_button_group.addButton(button)
        parent.cmd_buttons_layout.addWidget(button, i // 2, i % 2)

    # Add custom CMD buttons
    for i, cmd in enumerate(parent.custom_cmd_buttons, len(parent.cmd_buttons)):
        button = QPushButton(cmd)
        button.setCheckable(True)
        button.clicked.connect(lambda checked, cmd=cmd: set_cmd(parent, cmd))
        button.setStyleSheet("background-color: #87CEFA;")  # Different color for custom buttons
        parent.cmd_button_group.addButton(button)
        parent.cmd_buttons_layout.addWidget(button, i // 2, i % 2)

    layout.addLayout(parent.cmd_buttons_layout, 1, 1, (len(parent.cmd_buttons) + len(parent.custom_cmd_buttons)) // 2 + 1, 2)

def set_cmd(parent, cmd):
    """Set the selected CMD value."""
    parent.cmd_input.setText(cmd)
    update_len_chk(parent)

def set_op(parent, op):
    """Set the selected OP value."""
    parent.op_input.setText(op)
    update_len_chk(parent)

def increment_id(id_input):
    current_text = id_input.text()
    if current_text == "XXXX":
        id_input.setText("0001")
    else:
        try:
            current_value = int(current_text)
            if current_value < 9999:
                id_input.setText(f"{current_value + 1:04}")
        except ValueError:
            id_input.setText("0001")

def decrement_id(id_input):
    current_text = id_input.text()
    if current_text == "XXXX":
        id_input.setText("0000")
    else:
        try:
            current_value = int(current_text)
            if current_value > 0:
                id_input.setText(f"{current_value - 1:04}")
        except ValueError:
            id_input.setText("0000")

def create_len_chk_layout(parent):
    """Create the layout for the CHK field."""
    len_chk_layout = QHBoxLayout()

    chk_layout = QHBoxLayout()
    chk_label = QLabel("CHK")
    parent.chk_value = QLineEdit()
    parent.chk_value.setMaximumWidth(200)
    parent.chk_value.setReadOnly(True)
    parent.chk_value.setAlignment(Qt.AlignCenter)
    chk_layout.addWidget(chk_label)
    chk_layout.addWidget(parent.chk_value)

    len_chk_layout.addLayout(chk_layout)

    return len_chk_layout

def create_message_display_layout(parent):
    """Create the layout for the message display."""
    message_display_layout = QHBoxLayout()

    parent.message_display = QLineEdit()
    parent.message_display.setReadOnly(True)
    parent.message_display.setAlignment(Qt.AlignCenter)

    send_button = QPushButton("Send")
    send_button.clicked.connect(parent.send_generated_message)

    message_display_layout.addWidget(parent.message_display)
    message_display_layout.addWidget(send_button)

    return message_display_layout

def create_placeholder_widget():
    """Create a placeholder widget."""
    placeholder = QTextEdit()
    placeholder.setReadOnly(True)
    return placeholder

def update_len_chk(parent):
    id_value = parent.id_input.text()
    cmd_value = parent.cmd_input.text()
    op_value = parent.op_input.text()
    data_value = parent.data_input.text()

    stx = parent.protocol_handler.STX
    etx = parent.protocol_handler.ETX

    stx_and_content = f"{stx}{id_value}{cmd_value}{op_value}{data_value},"
    chk_value = parent.protocol_handler.calculate_checksum(stx_and_content)

    parent.chk_value.setText(chk_value)

    full_message = f"{stx_and_content}{chk_value}{etx}"
    parent.message_display.setText(full_message)