# serial_reader_worker.py

import serial
from PyQt5.QtCore import QObject, pyqtSignal, QElapsedTimer
from protocol_handler import ProtocolHandler

class SerialReaderWorker(QObject):
    message_received = pyqtSignal(str, int)
    data_received = pyqtSignal()
    error_occurred = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, serial_port):
        super().__init__()
        self.serial_port = serial_port
        self.running = True
        self.received_buffer = ''
        self.protocol_handler = ProtocolHandler()  # Initialize without parent
        self.elapsed_timer = QElapsedTimer()

    def run(self):
        try:
            while self.running and self.serial_port and self.serial_port.is_open:
                data = self.serial_port.read_all()
                if data:
                    if not self.elapsed_timer.isValid():
                        self.elapsed_timer.start()

                    self.received_buffer += data.decode('utf-8', errors='ignore')
                    self.data_received.emit()

                    lines = self.received_buffer.split(self.protocol_handler.ETX)
                    self.received_buffer = lines.pop()
                    for line in lines:
                        full_message = f"{line}{self.protocol_handler.ETX}"
                        elapsed_time = self.elapsed_timer.elapsed()
                        self.message_received.emit(full_message, elapsed_time)
                        self.elapsed_timer.invalidate()
        except serial.SerialException as e:
            self.error_occurred.emit(f"Serial port disconnected unexpectedly: {str(e)}")
            self.running = False
        finally:
            self.finished.emit()

    def flush_buffer(self):
        if self.received_buffer:
            elapsed_time = self.elapsed_timer.elapsed()
            self.message_received.emit(self.received_buffer.strip(), elapsed_time)
            self.received_buffer = ''
            self.elapsed_timer.invalidate()
