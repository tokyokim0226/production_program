# logger.py
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt

class Logger:
    def __init__(self, log_table: QTableWidget):
        self.log_table = log_table

    def log_message(self, message_type, message, time_taken=""):
        """Log a message in the table."""
        row_position = self.log_table.rowCount()
        self.log_table.insertRow(row_position)

        # Create QTableWidgetItem for each cell and disable editing
        for i, text in enumerate([message_type, message, time_taken]):
            item = QTableWidgetItem(text)
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.log_table.setItem(row_position, i, item)

    def clear_log(self):
        """Clear the log table."""
        self.log_table.setRowCount(0)
