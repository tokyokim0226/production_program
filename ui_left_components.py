from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QTableWidget, QHeaderView, QPushButton, QWidget, QLineEdit
from PyQt5.QtCore import Qt, pyqtSlot

class UILeftComponents:
    def __init__(self, parent):
        self.parent = parent

    def create_connect_and_clearlog_layout(self):
        connect_and_clearlog_widget = QWidget()
        connect_and_clearlog_layout = QHBoxLayout(connect_and_clearlog_widget)

        self.parent.connect_button = QPushButton("Connect")
        self.parent.connect_button.setMaximumWidth(100)
        self.parent.connect_button.clicked.connect(self.parent.open_connection_dialog)
        
        clear_log_button = QPushButton("Clear Log")
        clear_log_button.setMaximumWidth(100)
        clear_log_button.clicked.connect(self.parent.clear_log)

        connect_and_clearlog_layout.addWidget(self.parent.connect_button)
        connect_and_clearlog_layout.addStretch(1)
        connect_and_clearlog_layout.addWidget(clear_log_button)

        return connect_and_clearlog_widget

    def create_log_table(self):
        log_table = QTableWidget()
        log_table.setColumnCount(3)
        log_table.setHorizontalHeaderLabels(["Type", "Message", "Time (ms)"])

        header = log_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setStretchLastSection(False)

        log_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        log_table.verticalHeader().setDefaultAlignment(Qt.AlignCenter)

        log_table.setAlternatingRowColors(True)
        log_table.setWordWrap(True)
        log_table.setHorizontalScrollMode(QTableWidget.ScrollPerPixel)
        log_table.setVerticalScrollMode(QTableWidget.ScrollPerPixel)

        log_table.model().rowsInserted.connect(lambda: self.scroll_to_bottom(log_table))

        return log_table

    def create_input_layout(self):
        input_widget = QWidget()
        input_layout = QHBoxLayout(input_widget)
        self.parent.command_input = QLineEdit()
        send_button = QPushButton("Send")
        send_button.setMaximumWidth(80)
        send_button.clicked.connect(self.parent.send_message)

        input_layout.addWidget(self.parent.command_input, 1)
        input_layout.addWidget(send_button)

        return input_widget

    @pyqtSlot()
    def scroll_to_bottom(self, log_table):
        log_table.scrollToBottom()
