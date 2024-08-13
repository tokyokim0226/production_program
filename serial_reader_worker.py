import serial
from PyQt5.QtCore import QObject, pyqtSignal, QDateTime, QElapsedTimer
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
        self.elapsed_timer = QElapsedTimer()  # Timer to measure elapsed time

    def run(self):
        while self.running and self.serial_port and self.serial_port.is_open:
            try:
                data = self.serial_port.read_all()
                if data:
                    if not self.elapsed_timer.isValid():  # Start the timer when data is first received
                        self.elapsed_timer.start()

                    self.received_buffer += data.decode('utf-8', errors='ignore')
                    self.data_received.emit()  # Emit the signal to reset/start the buffer timer

                    # Process buffer and emit each line separately if it ends with ETX
                    lines = self.received_buffer.split(self.protocol_handler.ETX)
                    self.received_buffer = lines.pop()  # Keep the last partial message in the buffer
                    for line in lines:
                        full_message = f"{line}{self.protocol_handler.ETX}"
                        elapsed_time = self.elapsed_timer.elapsed()
                        self.message_received.emit(full_message, elapsed_time)  # Emit each full message
                        self.elapsed_timer.invalidate()  # Invalidate the timer after use

            except Exception as e:
                self.error_occurred.emit(str(e))
                break
        self.finished.emit()

    def flush_buffer(self):
        """Flush the buffer and print its content if no ETX character is found."""
        if self.received_buffer:
            elapsed_time = self.elapsed_timer.elapsed()  # Get the elapsed time
            self.message_received.emit(self.received_buffer.strip(), elapsed_time)  # Emit the current buffer content
            self.received_buffer = ''  # Clear the buffer
            self.elapsed_timer.invalidate()  # Invalidate the timer after use
