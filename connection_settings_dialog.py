from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton

# ConnectionSettingsDialog 클래스: 시리얼 포트 연결 설정을 위한 다이얼로그
class ConnectionSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent  # parent는 메인 애플리케이션 윈도우를 참조
        self.setWindowTitle("Connection Settings")  # 다이얼로그의 제목 설정
        self.setFixedSize(500, 400)  # 다이얼로그 크기 고정

        layout = QVBoxLayout(self)  # 수직 레이아웃으로 전체 구성

        # 상단에 "Refresh Connections" 버튼 추가
        refresh_button = QPushButton("Refresh Connections")  # 새로고침 버튼
        refresh_button.clicked.connect(self.refresh_connections)  # 버튼 클릭 시 포트 목록 새로고침
        layout.addWidget(refresh_button)

        # 시리얼 포트 선택 섹션
        port_layout = QHBoxLayout()  # 수평 레이아웃
        port_label = QLabel("Select Port:")  # 포트 선택 레이블
        self.port_combo = QComboBox()  # 포트 선택 콤보박스
        self.port_combo.addItems(parent.connection_manager.get_serial_ports())  # 현재 사용 가능한 시리얼 포트 목록 추가
        port_layout.addWidget(port_label)  # 레이블 추가
        port_layout.addWidget(self.port_combo)  # 콤보박스 추가
        layout.addLayout(port_layout)  # 전체 레이아웃에 수평 레이아웃 추가

        # Baud rate (전송 속도) 선택 섹션
        baud_rate_layout = QHBoxLayout()
        baud_rate_label = QLabel("Baud Rate:")  # Baud rate 레이블
        self.baud_rate_combo = QComboBox()  # Baud rate 선택 콤보박스
        self.baud_rate_combo.addItems(["1200", "2400", "4800", "9600", "19200", "38400", "57600", "115200", "230400", "460800", "921600"])
        self.baud_rate_combo.setCurrentText("2400")  # 기본값으로 9600 설정
        baud_rate_layout.addWidget(baud_rate_label)  # 레이블 추가
        baud_rate_layout.addWidget(self.baud_rate_combo)  # 콤보박스 추가
        layout.addLayout(baud_rate_layout)  # 전체 레이아웃에 추가

        # 데이터 비트 선택 섹션
        data_bits_layout = QHBoxLayout()
        data_bits_label = QLabel("Data Bits:")  # 데이터 비트 레이블
        self.data_bits_combo = QComboBox()  # 데이터 비트 선택 콤보박스
        self.data_bits_combo.addItems(["5", "6", "7", "8"])  # 선택 가능한 데이터 비트 값들
        self.data_bits_combo.setCurrentText("8")  # 기본값으로 8 설정
        data_bits_layout.addWidget(data_bits_label)  # 레이블 추가
        data_bits_layout.addWidget(self.data_bits_combo)  # 콤보박스 추가
        layout.addLayout(data_bits_layout)  # 전체 레이아웃에 추가

        # 패리티(Parity) 선택 섹션
        parity_layout = QHBoxLayout()
        parity_label = QLabel("Parity:")  # 패리티 레이블
        self.parity_combo = QComboBox()  # 패리티 선택 콤보박스
        self.parity_combo.addItems(["None", "Odd", "Even"])  # 선택 가능한 패리티 값들
        self.parity_combo.setCurrentText("None")  # 기본값으로 None 설정
        parity_layout.addWidget(parity_label)  # 레이블 추가
        parity_layout.addWidget(self.parity_combo)  # 콤보박스 추가
        layout.addLayout(parity_layout)  # 전체 레이아웃에 추가

        # 스탑 비트 선택 섹션
        stop_bits_layout = QHBoxLayout()
        stop_bits_label = QLabel("Stop Bits:")  # 스탑 비트 레이블
        self.stop_bits_combo = QComboBox()  # 스탑 비트 선택 콤보박스
        self.stop_bits_combo.addItems(["1", "1.5", "2"])  # 선택 가능한 스탑 비트 값들
        self.stop_bits_combo.setCurrentText("1")  # 기본값으로 1 설정
        stop_bits_layout.addWidget(stop_bits_label)  # 레이블 추가
        stop_bits_layout.addWidget(self.stop_bits_combo)  # 콤보박스 추가
        layout.addLayout(stop_bits_layout)  # 전체 레이아웃에 추가

        # 확인(OK) 및 취소(Cancel) 버튼 섹션
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK")  # OK 버튼
        self.cancel_button = QPushButton("Cancel")  # Cancel 버튼
        button_layout.addWidget(self.ok_button)  # OK 버튼 추가
        button_layout.addWidget(self.cancel_button)  # Cancel 버튼 추가
        layout.addLayout(button_layout)  # 전체 레이아웃에 추가

        # 버튼 클릭 시 다이얼로그 동작 연결
        self.ok_button.clicked.connect(self.accept)  # OK 버튼 클릭 시 다이얼로그 확인
        self.cancel_button.clicked.connect(self.reject)  # Cancel 버튼 클릭 시 다이얼로그 취소

    # 포트 목록 새로고침 메서드
    def refresh_connections(self):
        """현재 사용 가능한 시리얼 포트 목록을 새로 고침."""
        self.port_combo.clear()  # 기존 콤보박스의 항목들 지우기
        self.port_combo.addItems(self.parent.connection_manager.get_serial_ports())  # 새로 가져온 포트 목록으로 업데이트

    # 현재 설정 값을 가져오는 메서드
    def get_settings(self):
        """사용자가 선택한 시리얼 포트 설정 값을 딕셔너리로 반환."""
        return {
            "port": self.port_combo.currentText(),  # 선택된 포트
            "baud_rate": int(self.baud_rate_combo.currentText()),  # 선택된 Baud rate
            "data_bits": int(self.data_bits_combo.currentText()),  # 선택된 데이터 비트
            "parity": self.parity_combo.currentText(),  # 선택된 패리티
            "stop_bits": float(self.stop_bits_combo.currentText())  # 선택된 스탑 비트
        }
