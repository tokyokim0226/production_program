from PyQt5.QtCore import QThread, QDateTime
from serial_reader_worker import SerialReaderWorker
from logger import Logger

# CommunicationManager 클래스: 시리얼 데이터의 송수신을 관리하는 클래스
class CommunicationManager:
    # 소통 메니지맨트 클래스 만들기
    # 시리얼 데이터 처리를 백그라운드 thread에서 관리
    def __init__(self, parent):
        self.parent = parent  # parent (SerialPortMon 또는 이 CLASS)
        self.reading_thread = None  # 시리얼 데이터를 읽기 위한 thread
        self.worker = None  # SerialReaderWorker 객체 (시리얼 데이터 처리 담당)
        self.logger = Logger(self.parent.log_table)  # 로그를 기록할 Logger 객체 만들기

    # 시리얼 데이터를 읽는 thread 시작
    def start_reading_thread(self):
        # 시리얼 포트가 열려 있는지 확인한 후, 백그라운드 작업을 위한 QThread 생성
        # SerialReaderWorker가 시리얼 포트에서 데이터를 읽고, 해당 작업을 thread로 옮김
        if self.parent.serial_port and self.parent.serial_port.is_open:
            self.reading_thread = QThread()  # 새로운 thread 생성
            self.worker = SerialReaderWorker(self.parent.serial_port)  # 시리얼 포트에서 데이터를 읽는 작업자
            self.worker.moveToThread(self.reading_thread)  # 작업자를 thread로 이동

            # thread 시작 시 worker의 run 메서드 실행
            self.reading_thread.started.connect(self.worker.run)
            # 메시지를 받았을 때 처리 (시간 포함)
            self.worker.message_received.connect(self.handle_received_message_with_time)
            # 데이터가 수신될 때 버퍼 타이머 리셋
            self.worker.data_received.connect(self.reset_buffer_timer)
            # 에러가 발생할 때 parent의 프로토콜 핸들러에서 에러 처리
            self.worker.error_occurred.connect(self.parent.protocol_handler.handle_error)
            # 작업이 완료되면 thread 및 worker 정리
            self.worker.finished.connect(self.cleanup_thread)
            self.reading_thread.finished.connect(self.reading_thread.deleteLater)

            # thread 시작
            self.reading_thread.start()

    # 시리얼 데이터를 읽는 thread 종료
    def stop_reading_thread(self):
        if self.reading_thread and self.reading_thread.isRunning():
            self.worker.running = False  # worker 실행 중지
            self.reading_thread.quit()  # thread 종료
            self.reading_thread.wait()  # thread가 종료될 때까지 대기

    # thread 정리 메서드
    def cleanup_thread(self):
        if self.worker:
            self.worker.deleteLater()  # worker 객체 삭제
            self.worker = None  # worker 만들기
        if self.reading_thread:
            self.reading_thread = None  # thread 객체 만들기

    # worker의 버퍼를 비우는 메서드
    def flush_worker_buffer(self):
        if self.worker:
            self.worker.flush_buffer()  # worker의 버퍼 비우기

    # 메시지 수신 시 메시지와 수신 시간을 기록하는 메서드
    def handle_received_message_with_time(self, message, time_taken):
        self.logger.log_message("Received", message.strip(), f"{time_taken} ms")  # 로그에 수신 메시지 기록

    # 버퍼 타이머 리셋 메서드
    def reset_buffer_timer(self):
        self.parent.buffer_timer.start(self.parent.buffer_timeout)  # 버퍼 타이머 시작 (타임아웃 재설정)

    # 메시지 전송 메서드
    def send_message(self, message):
        # 시리얼 포트가 연결되어 있고 열려 있는지 확인
        if not self.parent.serial_port or not self.parent.serial_port.is_open:
            self.parent.logger.log_message("Error", "No serial port is connected.")  # 연결 오류 메시지 기록
            return

        try:
            # 메시지가 존재하는지 확인한 후 전송
            if message:
                start_time = QDateTime.currentDateTime()  # 전송 시작 시간 기록
                self.parent.serial_port.write(message.encode('utf-8'))  # 메시지를 UTF-8로 인코딩하여 시리얼 포트로 전송
                end_time = QDateTime.currentDateTime()  # 전송 완료 시간 기록
                elapsed_time = start_time.msecsTo(end_time)  # 전송에 소요된 시간 계산
                self.logger.log_message("Sent", message.strip(), f"{elapsed_time} ms")  # 전송된 메시지 기록
        except Exception as e:
            self.logger.log_message("Error", str(e))  # 오류 발생 시 오류 메시지 기록

    # UI에서 생성된 메시지를 전송하는 메서드
    def send_generated_message(self):
        message = self.parent.message_display.text()  # 생성된 메시지 가져오기
        self.send_message(message)  # 가져온 메시지를 전송
