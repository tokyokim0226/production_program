# ui_left_components.py
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QTableWidget, QHeaderView, QPushButton, QWidget, QLineEdit
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton

def create_port_layout(parent):
    port_widget = QWidget()
    port_layout = QVBoxLayout(port_widget)

    # Connect button only
    parent.connect_button = QPushButton("Connect")
    parent.connect_button.setMaximumWidth(100)
    parent.connect_button.clicked.connect(parent.open_connection_dialog)

    # Add the connect button to the layout
    port_layout.addWidget(parent.connect_button)

    return port_widget


def create_text_display_layout(parent):
    text_display_widget = QWidget()  # Create a QWidget to hold the layout
    text_display_layout = QVBoxLayout(text_display_widget)  # Apply layout to the widget

    # Create the log table display
    parent.log_table = QTableWidget()
    parent.log_table.setColumnCount(3)
    parent.log_table.setHorizontalHeaderLabels(["Type", "Message", "Time Taken (ms)"])
    parent.log_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    parent.log_table.setEditTriggers(QTableWidget.NoEditTriggers)  # Prevent editing

    # Create the Clear button
    clear_button = QPushButton("Clear Log")
    clear_button.setMaximumWidth(100)
    clear_button.clicked.connect(parent.clear_log)

    # Add the text display and clear button to the layout
    text_display_layout.addWidget(parent.log_table)
    text_display_layout.addWidget(clear_button)

    return text_display_widget  # Return the QWidget with the layout

def create_input_layout(parent):
    input_widget = QWidget()
    input_layout = QHBoxLayout(input_widget)
    parent.command_input = QLineEdit()
    send_button = QPushButton("Send")
    send_button.setMaximumWidth(80)
    send_button.clicked.connect(parent.send_message)

    input_layout.addWidget(parent.command_input, 1)  # Ensure command_input takes more space
    input_layout.addWidget(send_button)

    return input_widget