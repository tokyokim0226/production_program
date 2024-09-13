import serial
from PyQt5.QtWidgets import QMessageBox, QDialog
from connection_settings_dialog import ConnectionSettingsDialog
from serial.tools import list_ports

# ConnectionManager 클래스: 시리얼 포트 연결 및 해제 관리
class ConnectionManager:
    # 클래스 초기화 (생성자)
    def __init__(self, parent):
        self.parent = parent  # parent는 주로 메인 윈도우를 참조

    # 사용 가능한 시리얼 포트 목록을 가져오는 메서드
    def get_serial_ports(self):
        ports = [port.device for port in list_ports.comports()]  # 사용 가능한 시리얼 포트 목록 가져오기
        return ports if ports else ["No COM ports"]  # 포트가 없으면 "No COM ports" 

    # 시리얼 포트 연결 메서드
    def connect_serial(self):
        # 시리얼 포트가 이미 열려 있는 경우, 먼저 연결을 종료
        if self.parent.serial_port and self.parent.serial_port.is_open:
            self.close_serial()
        else:
            # 연결 설정 다이얼로그를 열어 사용자로부터 설정을 받음
            dialog = ConnectionSettingsDialog(self.parent)
            result = dialog.exec_()  # 다이얼로그 실행

            # 사용자가 설정 창에서 [확인]을 눌렀을 경우 (QDialog.Accepted)
            if result == QDialog.Accepted:
                settings = dialog.get_settings()  # 설정 값 가져오기
                port = settings['port']  # 선택한 포트
                try:
                    # 시리얼 포트 설정에 맞춰 연결 시도
                    self.parent.serial_port = serial.Serial(
                        port,
                        baudrate=settings["baud_rate"],  # 설정된 baud rate
                        bytesize=settings["data_bits"],  # 데이터 비트 수
                        parity=self.get_parity(settings["parity"]),  # 패리티 설정
                        stopbits=settings["stop_bits"],  # 스탑 비트 설정
                        timeout=0.1  # 타임아웃 설정 (0.1초)
                    )
                    # 성공적으로 연결되면 로그에 기록하고 통신을 시작
                    self.parent.logger.log_message("Connect", f"Connected to {port}")
                    self.parent.communication_manager.start_reading_thread()  # thread 시작
                    self.parent.connect_button.setText("Close")  # 버튼 텍스트를 "Close"로 변경

                except Exception as e:
                    # 연결 오류가 발생하면 에러 메시지 표시
                    QMessageBox.critical(self.parent, "Connection Error", f"Could not connect to {port}: {str(e)}")
                    self.parent.serial_port = None  # 포트를 None으로 초기화

    # 시리얼 포트 연결 종료 메서드
    def close_serial(self):
        # 시리얼 포트가 열려 있는 경우, 포트를 닫음
        if self.parent.serial_port and self.parent.serial_port.is_open:
            port = self.parent.serial_port.port  # 현재 포트
            self.parent.communication_manager.stop_reading_thread()  # thread 중지
            self.parent.serial_port.close()  # 시리얼 포트 닫기
            self.parent.logger.log_message("Disconnect", f"Disconnected from {port}")  # 로그에 기록
            self.parent.connect_button.setText("Connect")  # 버튼 텍스트를 "Connect"로 변경
        else:
            # 열려 있는 시리얼 포트가 없는 경우, 로그에 기록
            self.parent.logger.log_message("Info", "No open serial port to disconnect.")

    # 패리티 설정 변환 메서드
    def get_parity(self, parity_str):
        parity_dict = {
            "None": serial.PARITY_NONE,  # 패리티 없음
            "Odd": serial.PARITY_ODD,    # 홀수 패리티
            "Even": serial.PARITY_EVEN   # 짝수 패리티
        }
        return parity_dict.get(parity_str, serial.PARITY_NONE)  # 설정된 패리티 반환 (없으면 기본값 None)
