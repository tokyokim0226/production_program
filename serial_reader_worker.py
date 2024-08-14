import serial
from PyQt5.QtCore import QObject, pyqtSignal, QElapsedTimer
from protocol_handler import ProtocolHandler

class SerialReaderWorker(QObject):
    message_received = pyqtSignal(str, int)  # Emit the message and the time taken in ms
    data_received = pyqtSignal()  # Signal emitted when data is received, to trigger the buffer timer
    error_occurred = pyqtSignal(str)  # Signal emitted when an error occurs
    finished = pyqtSignal()  # Signal emitted when the worker finishes

    def __init__(self, serial_port):
        super().__init__()
        self.serial_port = serial_port
        self.running = True
        self.received_buffer = ''
        self.protocol_handler = ProtocolHandler()  # Initialize without parent
        self.elapsed_timer = None  # Initialize timer as None

    def run(self):
        while self.running and self.serial_port and self.serial_port.is_open:
            try:
                data = self.serial_port.read_all()
                if data:
                    if self.elapsed_timer is None:  # Start the timer if not already running
                        self.elapsed_timer = QElapsedTimer()
                        self.elapsed_timer.start()

                    self.received_buffer += data.decode('utf-8', errors='ignore')

                    # Process buffer if we have a complete message ending with ETX
                    if self.protocol_handler.ETX in self.received_buffer:
                        lines = self.received_buffer.split(self.protocol_handler.ETX)
                        for line in lines[:-1]:  # Process all complete messages
                            if line.strip():  # Ensure we don't process empty lines
                                full_message = f"{line}{self.protocol_handler.ETX}"
                                elapsed_time = self.elapsed_timer.elapsed() if self.elapsed_timer else 0
                                self.message_received.emit(full_message, elapsed_time)
                        self.received_buffer = lines[-1]  # Keep the last partial message in the buffer

                        # Reset the timer if the last part of the buffer is empty after splitting
                        if not self.received_buffer.strip():
                            self.elapsed_timer = None

                    self.data_received.emit()  # Reset/start the buffer timer

            except Exception as e:
                self.error_occurred.emit(str(e))
                break
        self.finished.emit()

    def flush_buffer(self):
        """Flush the buffer and print its content if no ETX character is found."""
        if self.received_buffer and not self.received_buffer.endswith(self.protocol_handler.ETX):
            elapsed_time = self.elapsed_timer.elapsed() if self.elapsed_timer else 0
            if self.received_buffer.strip():  # Ensure we only log non-empty buffers
                self.message_received.emit(self.received_buffer.strip(), elapsed_time)
            self.received_buffer = ''  # Clear the buffer
            self.elapsed_timer = None  # Reset the timer after flushing
