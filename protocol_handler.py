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
        id_value = content[:4]  # Assuming ID is always 4 characters
        cmd_op_data = content[4:]  # The rest is CMD, OP, and DATA combined

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
        if self.parent:
            self.parent.text_display.append(f"Error reading from serial port: {error_message}")
