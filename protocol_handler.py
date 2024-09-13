from PyQt5.QtWidgets import QTableWidgetItem

# ProtocolHandler 클래스: 시리얼 통신에서 메시지 검증, 체크섬 계산, 오류 처리 등을 관리
class ProtocolHandler:
    STX = '['  # 메시지의 시작 문자 (Start of Text)
    ETX = ']'  # 메시지의 종료 문자 (End of Text)

    def __init__(self, parent=None):
        self.parent = parent  # parent는 주로 메인 애플리케이션을 참조

    # 메시지 검증 메서드
    def validate_message(self, message):
        """메시지가 STX로 시작하고 ETX로 끝나는지 확인하여 메시지를 검증."""
        if not message.startswith(self.STX) or not message.endswith(self.ETX):
            return False  
        return True  

    # 체크섬 계산 메서드
    def calculate_checksum(self, content):
        """메시지의 내용을 기반으로 XOR 체크섬을 계산합니다."""
        xor_value = 0
        for char in content:        # 메시지 내용의 각 문자를 순회하며 XOR 연산
            xor_value ^= ord(char)  # 문자의 ASCII 값을 XOR
        return f'{xor_value:02X}'   # 계산된 값을 2자리 16진수로 반환

    # 오류 처리 메서드
    def handle_error(self, error_message):
        """시리얼 포트 읽기 중 발생한 오류를 처리하고 로그 테이블에 기록"""
        self.log_error(f"Error reading from serial port: {error_message}")  # 오류 로그 기록
        if "disconnected unexpectedly" in error_message.lower():            # 예기치 않게 연결이 끊어진 경우
            self.parent.communication_manager.stop_reading_thread()         # thread 중지
            self.parent.logger.log_message("Disconnect", "Serial port disconnected unexpectedly")  # 연결 끊김 로그
            if self.parent.serial_port and self.parent.serial_port.is_open:
                self.parent.serial_port.close()              # 시리얼 포트 닫기
            self.parent.connect_button.setText("Connect")    # 'Close' 버튼을 'Connect'로 다시 바꾸기

    # 오류 로그 기록 메서드
    def log_error(self, message):
        """로그 테이블에 오류 메시지를 기록합니다."""
        log_table = self.parent.log_table  # 로그 테이블 참조

        row_count = log_table.rowCount()  # 현재 테이블의 행 수
        log_table.insertRow(row_count)    # 새로운 행 추가
        log_table.setItem(row_count, 0, QTableWidgetItem("Error"))  # 첫 번째 열에 'Error' 추가
        log_table.setItem(row_count, 1, QTableWidgetItem(message))  # 두 번째 열에 오류 메시지 추가
        log_table.setItem(row_count, 2, QTableWidgetItem("0 ms"))   # 세 번째 열에 시간 기록 (여기선 기본값 0 ms)
