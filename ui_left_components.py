# ui_left_components.py
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QTableWidget, QHeaderView, QPushButton, QWidget, QLineEdit
from PyQt5.QtCore import Qt, pyqtSlot

from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton

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

def create_log_table(parent):
    # Create the log table widget
    log_table = QTableWidget()
    log_table.setColumnCount(3)
    log_table.setHorizontalHeaderLabels(["Type", "Message", "Time (ms)"])

    # Set stretch factors for the columns (1:2:1 ratio)
    header = log_table.horizontalHeader()
    header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
    header.setSectionResizeMode(1, QHeaderView.Stretch)
    header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
    header.setStretchLastSection(False)

    # Allow rows to expand dynamically to fit content
    log_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
    log_table.verticalHeader().setDefaultAlignment(Qt.AlignCenter)  # Center numbering in vertical header

    # Enable alternating row colors
    log_table.setAlternatingRowColors(True)

    # Disable horizontal scrolling
    log_table.setWordWrap(True)
    log_table.setHorizontalScrollMode(QTableWidget.ScrollPerPixel)
    log_table.setVerticalScrollMode(QTableWidget.ScrollPerPixel)

    # Connect the table's signal to auto-scroll to the bottom
    log_table.model().rowsInserted.connect(lambda: scroll_to_bottom(log_table))

    return log_table

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

# Add the scroll_to_bottom function within the ui_left_components.py
@pyqtSlot()
def scroll_to_bottom(log_table):
    """Auto-scroll to the bottom of the table when new rows are inserted."""
    log_table.scrollToBottom()
    