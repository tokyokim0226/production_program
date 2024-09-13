import serial
from PyQt5.QtCore import QObject, pyqtSignal, QElapsedTimer
from protocol_handler import ProtocolHandler

# SerialReaderWorker 클래스: 시리얼 포트에서 데이터를 읽는 작업을 처리
# 별도의 thread에서 실행되며, 메시지 수신, 오류 발생, 데이터 수신 등의 시그널을 보냄

class SerialReaderWorker(QObject):
    '''pyQt5에서 시그널이란 이벤트를 의미하며, 이벤트가 발생하면 연결된 슬롯을 호출하는 방식으로 동작함 (슬롯은 이벤트 발생시 실행될 행동/함수가 들어가는 공간을 의미함)'''
    message_received = pyqtSignal(str, int)  # 메시지가 수신되면 (메시지 내용, 시간) 시그널 발생
    data_received = pyqtSignal()  # 데이터가 수신되면 시그널 발생
    error_occurred = pyqtSignal(str)  # 오류가 발생하면 오류 메시지 시그널 발생
    finished = pyqtSignal()  # 작업이 완료되면 시그널 발생

    def __init__(self, serial_port):
        super().__init__()
        self.serial_port = serial_port  # 시리얼 포트 객체
        self.running = True  # 작업 실행 여부
        self.received_buffer = ''  # 수신된 데이터 버퍼
        self.protocol_handler = ProtocolHandler()  # ProtocolHandler 초기화 (parent 없음)
        self.elapsed_timer = QElapsedTimer()  # 메시지 수신 시간을 측정할 타이머

    # thread에서 실행될 메인 메서드
    def run(self):
        try:
            # running이 True이고 시리얼 포트가 열려 있을 때까지 반복
            while self.running and self.serial_port and self.serial_port.is_open:
                data = self.serial_port.read_all()  # 시리얼 포트로부터 모든 데이터를 읽음
                if data:
                    if not self.elapsed_timer.isValid():  # 타이머가 유효하지 않으면
                        self.elapsed_timer.start()  # 타이머 시작

                    # 데이터를 문자열로 변환하여 버퍼에 추가
                    self.received_buffer += data.decode('utf-8', errors='ignore')
                    self.data_received.emit()  # 데이터 수신 시그널 발생

                    # 메시지 종료 문자(ETX)로 나눈 후, 버퍼에서 마지막 메시지를 유지
                    lines = self.received_buffer.split(self.protocol_handler.ETX)
                    self.received_buffer = lines.pop()

                    # 완전한 메시지들을 처리
                    for line in lines:
                        full_message = f"{line}{self.protocol_handler.ETX}"  # 메시지 완성
                        elapsed_time = self.elapsed_timer.elapsed()  # 메시지 수신에 걸린 시간 계산
                        self.message_received.emit(full_message, elapsed_time)  # 메시지 수신 시그널 발생
                        self.elapsed_timer.invalidate()  # 타이머 무효화 (정지하게 됨)
        except serial.SerialException as e:
            # 시리얼 포트 오류 발생 시
            self.error_occurred.emit(f"Serial port disconnected unexpectedly: {str(e)}")  # 오류 시그널 발생
            self.running = False  # 작업 종료
        finally:
            self.finished.emit()  # 작업 완료 시그널 발생

    # 버퍼의 데이터를 강제로 처리하는 메서드
    def flush_buffer(self):
        if self.received_buffer:
            elapsed_time = self.elapsed_timer.elapsed()  # 마지막으로 측정된 시간
            self.message_received.emit(self.received_buffer.strip(), elapsed_time)  # 버퍼의 데이터를 메시지로 변환
            self.received_buffer = ''  # 버퍼 초기화
            self.elapsed_timer.invalidate()  # 타이머 무효화
