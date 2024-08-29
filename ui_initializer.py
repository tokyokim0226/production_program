from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QTableWidget, QHeaderView, QAbstractItemView
from PyQt5.QtCore import Qt, pyqtSlot, QModelIndex
from ui_left_components import UILeftComponents
from ui_right_generator import UIRightGenerator
from ui_menu import Menu

from PyQt5.QtWidgets import QTabWidget

class UIInitializer:
    def __init__(self, parent):
        self.parent = parent

    def setup_ui(self):
        self.parent.setWindowTitle("SerialPortMon")
        self.parent.setGeometry(100, 100, 1200, 750)
        self.parent.setMinimumSize(600, 300)
 
        central_widget = QWidget()
        self.parent.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        communication_layout = QVBoxLayout()

        left_ui = UILeftComponents(self.parent)
        connect_and_clearlog_widget = left_ui.create_connect_and_clearlog_layout()

        self.parent.log_table = left_ui.create_log_table()

        communication_layout.addWidget(connect_and_clearlog_widget)
        communication_layout.addWidget(self.parent.log_table)

        input_layout = left_ui.create_input_layout()  # No need to pass self.parent
        communication_layout.addWidget(input_layout)

        # Create a QTabWidget for the right side
        self.parent.tabs = QTabWidget()
        
        # Tab 1: Original right side layout
        right_ui = UIRightGenerator(self.parent)
        tab1_widget = QWidget()
        tab1_layout = QVBoxLayout(tab1_widget)
        generator_input_layout = right_ui.create_manual_input_layout()
        tab1_layout.addLayout(generator_input_layout)

        self.parent.cmd_op_widget = QWidget()
        tab1_layout.addWidget(self.parent.cmd_op_widget)

        len_chk_layout = right_ui.create_len_chk_layout()
        tab1_layout.addLayout(len_chk_layout)

        message_display_layout = right_ui.create_message_display_layout()
        tab1_layout.addLayout(message_display_layout)

        placeholder = right_ui.create_placeholder_widget()
        tab1_layout.addWidget(placeholder)

        self.parent.tabs.addTab(tab1_widget, "Tab 1")

        # Tab 2: New tab with a simple layout
        tab2_widget = QWidget()
        tab2_layout = QVBoxLayout(tab2_widget)
        
        tab2_text = QLabel("This is Tab 2")
        tab2_button = QPushButton("Button in Tab 2")
        
        tab2_layout.addWidget(tab2_text)
        tab2_layout.addWidget(tab2_button)
        tab2_layout.addStretch(1)

        self.parent.tabs.addTab(tab2_widget, "Tab 2")

        # Add the QTabWidget to the main layout
        main_layout.addLayout(communication_layout, 1)
        main_layout.addWidget(self.parent.tabs, 1)

        menubar = self.parent.menuBar()
        self.parent.setMenuBar(menubar)

        self.parent.menu = Menu(self.parent)

        self.parent.id_input.textChanged.connect(lambda: right_ui.update_len_chk())
        self.parent.cmd_input.textChanged.connect(lambda: right_ui.update_len_chk())
        self.parent.op_input.textChanged.connect(lambda: right_ui.update_len_chk())
        self.parent.data_input.textChanged.connect(lambda: right_ui.update_len_chk())

    def update_cmd_buttons_layout(self):
        """Update the CMD buttons layout whenever changes are made."""
        while self.parent.cmd_buttons_layout.count():
            child = self.parent.cmd_buttons_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for i, cmd in enumerate(self.parent.cmd_buttons):
            button = QPushButton(cmd)
            button.setCheckable(True)
            button.clicked.connect(lambda checked, cmd=cmd: self.parent.ui_right_generator.set_cmd(cmd))
            self.parent.cmd_button_group.addButton(button)
            self.parent.cmd_buttons_layout.addWidget(button, i // 2, i % 2)

        for i, cmd in enumerate(self.parent.custom_cmd_buttons, len(self.parent.cmd_buttons)):
            button = QPushButton(cmd)
            button.setCheckable(True)
            button.clicked.connect(lambda checked, cmd=cmd: self.parent.ui_right_generator.set_cmd(cmd))
            self.parent.cmd_button_group.addButton(button)
            self.parent.cmd_buttons_layout.addWidget(button, i // 2, i % 2)

