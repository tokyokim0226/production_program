from PyQt5.QtCore import QThread, QDateTime
from serial_reader_worker import SerialReaderWorker
from logger import Logger

class CommunicationManager:
    def __init__(self, parent):
        self.parent = parent
        self.reading_thread = None
        self.worker = None
        self.logger = Logger(self.parent.log_table)  # Use Logger with log_table

    def start_reading_thread(self):
        if self.parent.serial_port and self.parent.serial_port.is_open:
            self.reading_thread = QThread()
            self.worker = SerialReaderWorker(self.parent.serial_port)
            self.worker.moveToThread(self.reading_thread)

            self.reading_thread.started.connect(self.worker.run)
            self.worker.message_received.connect(self.handle_received_message_with_time)
            self.worker.data_received.connect(self.reset_buffer_timer)
            self.worker.error_occurred.connect(self.parent.protocol_handler.handle_error)
            self.worker.finished.connect(self.reading_thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.reading_thread.finished.connect(self.reading_thread.deleteLater)

            self.reading_thread.start()

    def stop_reading_thread(self):
        if self.reading_thread and self.reading_thread.isRunning():
            self.worker.running = False
            self.reading_thread.quit()
            self.reading_thread.wait()
            self.worker = None
            self.reading_thread = None

    def flush_worker_buffer(self):
        if self.worker:
            self.worker.flush_buffer()

    def handle_received_message_with_time(self, message, time_taken):
        self.logger.log_message("Received", message.strip(), f"{time_taken} ms")

    def reset_buffer_timer(self):
        self.parent.buffer_timer.start(self.parent.buffer_timeout)

    def send_message(self, message):
        if not self.parent.serial_port or not self.parent.serial_port.is_open:
            self.parent.logger.log_message("Error", "No serial port is connected.")
            return

        try:
            if message:   #Make sure that message is only being sent when there is content in the message box
                start_time = QDateTime.currentDateTime()
                self.parent.serial_port.write(message.encode('utf-8'))
                end_time = QDateTime.currentDateTime()
                elapsed_time = start_time.msecsTo(end_time)
                self.logger.log_message("Sent", message.strip(), f"{elapsed_time} ms")
        except Exception as e:
            self.logger.log_message("Error", str(e))

    def send_generated_message(self):
        message = self.parent.message_display.text()
        self.send_message(message)
