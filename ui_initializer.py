from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QTableWidget, QHeaderView, QAbstractItemView
from PyQt5.QtCore import Qt, pyqtSlot, QModelIndex
from ui_left_components import create_port_layout, create_input_layout, create_log_table
from ui_right_generator import create_manual_input_layout, create_len_chk_layout, create_message_display_layout, create_placeholder_widget, update_len_chk
from ui_menu import Menu

class UIInitializer:
    def __init__(self, parent):
        self.parent = parent

    def setup_ui(self):
        self.parent.setWindowTitle("SerialPortMon")
        self.parent.setGeometry(100, 100, 1200, 750)
        self.parent.setMinimumSize(600, 300)

        # Create the main widget and set it as the central widget
        central_widget = QWidget()
        self.parent.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        # Create communication layout
        communication_layout = QVBoxLayout()
        port_layout = create_port_layout(self.parent)

        # Create the log table using the function in ui_left_components.py
        self.parent.log_table = create_log_table(self.parent)

        communication_layout.addWidget(port_layout)
        communication_layout.addWidget(self.parent.log_table)  # Add log_table to the layout

        input_layout = create_input_layout(self.parent)
        communication_layout.addWidget(input_layout)

        # Create generator layout
        generator_layout = QVBoxLayout()
        generator_input_layout = create_manual_input_layout(self.parent)
        generator_layout.addLayout(generator_input_layout)

        self.parent.cmd_op_widget = QWidget()  # Widget to contain the CMD/OP layout
        generator_layout.addWidget(self.parent.cmd_op_widget)

        # Create LEN and CHK layout
        len_chk_layout = create_len_chk_layout(self.parent)
        generator_layout.addLayout(len_chk_layout)

        # Create message display layout
        message_display_layout = create_message_display_layout(self.parent)
        generator_layout.addLayout(message_display_layout)

        # Placeholder for future components
        placeholder = create_placeholder_widget()
        generator_layout.addWidget(placeholder)

        # Add communication and generator layouts to the main layout
        main_layout.addLayout(communication_layout, 1)
        main_layout.addLayout(generator_layout, 1)

        # Create and set the menu bar
        menubar = self.parent.menuBar()
        self.parent.setMenuBar(menubar)

        # Initialize the menu
        self.parent.menu = Menu(self.parent)

        # Connect signals to update LEN and CHK when ID, CMD, OP, or DATA changes
        self.parent.id_input.textChanged.connect(lambda: update_len_chk(self.parent))
        self.parent.cmd_input.textChanged.connect(lambda: update_len_chk(self.parent))
        self.parent.op_input.textChanged.connect(lambda: update_len_chk(self.parent))
        self.parent.data_input.textChanged.connect(lambda: update_len_chk(self.parent))

    def update_cmd_buttons_layout(self):
        """Update the CMD buttons layout whenever changes are made."""
        # Clear existing buttons and widgets
        while self.parent.cmd_buttons_layout.count():
            child = self.parent.cmd_buttons_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Re-add original CMD buttons
        for i, cmd in enumerate(self.parent.cmd_buttons):
            button = QPushButton(cmd)
            button.setCheckable(True)
            button.clicked.connect(lambda checked, cmd=cmd: set_cmd(self.parent, cmd))
            self.parent.cmd_button_group.addButton(button)
            self.parent.cmd_buttons_layout.addWidget(button, i // 2, i % 2)

        # Re-add custom CMD buttons
        for i, cmd in enumerate(self.parent.custom_cmd_buttons, len(self.parent.cmd_buttons)):
            button = QPushButton(cmd)
            button.setCheckable(True)
            button.clicked.connect(lambda checked, cmd=cmd: set_cmd(self.parent, cmd))
            self.parent.cmd_button_group.addButton(button)
            self.parent.cmd_buttons_layout.addWidget(button, i // 2, i % 2)

def set_cmd(parent, cmd):
    """Set the selected CMD value."""
    parent.cmd_input.setText(cmd)
    update_len_chk(parent)
