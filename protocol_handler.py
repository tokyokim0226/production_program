from PyQt5.QtWidgets import QTableWidgetItem

class ProtocolHandler:
    STX = '['
    ETX = ']'

    def __init__(self, parent=None):
        self.parent = parent

    def validate_message(self, message):
        if not message.startswith(self.STX) or not message.endswith(self.ETX):
            return False
        return True
    
    def calculate_checksum(self, content):
        xor_value = 0
        for char in content:
            xor_value ^= ord(char)
        return f'{xor_value:02X}'

    def parse_message(self, message):
        if not self.validate_message(message):
            raise ValueError("Invalid message format")

        content, checksum = message[1:-1].rsplit(',', 1)  # Split content and checksum, excluding STX and ETX

        calculated_checksum = self.calculate_checksum(content + ',')
        if checksum != calculated_checksum:
            raise ValueError("Checksum does not match")

        # Parsing the content assuming the structure: IDCMDOPDATA
        id_value = content[:3]  # Assuming ID is always 4 characters
        cmd_op_data = content[3:]  # The rest is CMD, OP, and DATA combined

        return {
            "id": id_value,
            "cmd_op_data": cmd_op_data,
            "checksum": checksum    
        }
    
    def handle_received_message(self, message):
        try:
            if self.parent:
                if not message.strip():  # Skip empty messages
                    return
                self.parent.text_display.append(f"Received: {message.strip()}")  # Display the received message
        except ValueError as e:
            if self.parent:
                self.parent.text_display.append(f"Invalid message received: {message.strip()}")

    def handle_error(self, error_message):
        """Handle errors by logging them in the log table."""
        self.log_error(f"Error reading from serial port: {error_message}")
        if "disconnected unexpectedly" in error_message.lower():
            self.parent.communication_manager.stop_reading_thread()
            self.parent.logger.log_message("Disconnect", "Serial port disconnected unexpectedly")
            if self.parent.serial_port and self.parent.serial_port.is_open:
                self.parent.serial_port.close()
            self.parent.connect_button.setText("Connect")

    def log_error(self, message):
        """Log an error message in the log table."""
        log_table = self.parent.log_table

        row_count = log_table.rowCount()
        log_table.insertRow(row_count)
        log_table.setItem(row_count, 0, QTableWidgetItem("Error"))
        log_table.setItem(row_count, 1, QTableWidgetItem(message))
        log_table.setItem(row_count, 2, QTableWidgetItem("0 ms"))  # You might want to calculate the actual time taken
