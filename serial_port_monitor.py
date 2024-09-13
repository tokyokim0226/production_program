from PyQt5.QtWidgets import (
    QMainWindow, QLineEdit, QTextEdit, QComboBox, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QTableWidget, QPushButton
)
from PyQt5.QtGui import QIcon

from PyQt5.QtCore import QTimer

#다른 모듈 모두 불러오기
from protocol_handler import ProtocolHandler
from connection_manager import ConnectionManager
from communication_manager import CommunicationManager
from logger import Logger
from ui_left_components import UILeftComponents
from ui_right_generator import UIRightGenerator
from ui_right_production import UIRightProduction
from ui_menu import UIMenu

# SerialPortMon 클래스: 메인 애플리케이션 윈도우 정의 (가장 상위 레벨)
class SerialPortMon(QMainWindow):
    def __init__(self):
        super().__init__()

        self.serial_port = None                          # 시리얼 포트 객체 (현재 연결된 포트)
        self.protocol_handler = ProtocolHandler(self)    # 프로토콜 처리기

        # UI 레이아웃 
        self.initUI()

        # 연결 관리자 및 통신 관리자 초기화
        self.connection_manager = ConnectionManager(self)          # 시리얼 포트 연결 관리
        self.communication_manager = CommunicationManager(self)    # 시리얼 통신 관리

        # Logger 초기화 (log_table이 initUI에서 설정된 후)
        self.logger = Logger(self.log_table)  # 로그 메시지를 기록하는 Logger

        # 버퍼 타이머 설정
        self.buffer_timer = QTimer(self)                             # 일정 시간 후에 버퍼를 비우기 위한 타이머
        self.buffer_timeout = 500                                    # 타임아웃 설정 (500ms)
        self.buffer_timer.timeout.connect(self.flush_worker_buffer)  # 타임아웃 시 버퍼 비우기

    # UI 설정 메서드
    def initUI(self):
        self.setWindowTitle("TMEE 생산 PG")    # 창 제목 설정
        self.setGeometry(100, 100, 1200, 750)   # 창의 크기 및 위치 설정
        self.setMinimumSize(600, 300)           # 최소 크기 설정

        # 애플리케이션 아이콘 설정
        self.setWindowIcon(QIcon('tmee_icon.ico'))  # 아이콘 경로 설정 (ico 파일)

        # 중앙 위젯 설정
        central_widget = QWidget()                  # 메인 중앙 위젯 생성
        self.setCentralWidget(central_widget)       # 중앙 위젯 설정

        # 메인 레이아웃 설정
        main_layout = QHBoxLayout(central_widget)   # 수평 레이아웃 생성

        # 왼쪽 UI 컴포넌트 추가 (로그 테이블, 명령 입력 등)
        self.ui_left_components = UILeftComponents(self)   # 왼쪽 UI 구성요소 생성
        main_layout.addWidget(self.ui_left_components, 1)  # 왼쪽 UI 레이아웃에 추가

        # 오른쪽 탭 위젯 생성 (탭으로 구분된 화면)
        self.tabs = QTabWidget()  # 탭 위젯 생성

        # 첫 번째 탭: 메시지 자동 생성 화면
        self.ui_right_generator = UIRightGenerator(self)        # 자동 생성 탭 UI
        tab1_widget = QWidget()                                 # 탭1 위젯 생성
        tab1_layout = QVBoxLayout(tab1_widget)                  # 수직 레이아웃
        tab1_layout.addWidget(self.ui_right_generator)          # 탭에 자동 생성 UI 추가
        self.tabs.addTab(tab1_widget, "1 - 메시지 자동 생성")    # 탭1 추가

        # 두 번째 탭: ADD 자동 할당 화면
        self.ui_right_production = UIRightProduction(self)  # 자동 할당 탭 UI
        self.tabs.addTab(self.ui_right_production, "2 - ADD 자동 할당")  # 탭2 추가

        main_layout.addWidget(self.tabs, 1)  # 오른쪽 탭 위젯을 메인 레이아웃에 추가

        # 메뉴 설정
        self.menu = UIMenu(self)  # 메뉴바 생성

    # 시리얼 포트 연결 메서드
    def connect_serial(self):
        self.connection_manager.connect_serial()  # 연결 관리자에서 연결 수행

    # 로그 초기화 메서드 (로그 테이블 지우기)
    def clear_log(self):
        self.logger.clear_log()  # Logger에서 로그 지우기

    # 사용자가 입력한 메시지를 시리얼 포트로 전송하는 메서드
    def send_message(self):
        message = self.command_input.text()                 # 입력 필드에서 메시지 가져오기
        self.communication_manager.send_message(message)    # 통신 관리자를 통해 메시지 전송

    # 자동 생성된 메시지를 시리얼 포트로 전송하는 메서드
    def send_generated_message(self):
        self.communication_manager.send_generated_message()  # 자동 생성 메시지 전송

    # 연결 설정 다이얼로그를 열어 시리얼 포트 연결을 시도하는 메서드
    def open_connection_dialog(self):
        self.connection_manager.connect_serial()  # 연결 관리자에서 연결 수행

    # 타임아웃 발생 시 버퍼를 비우는 메서드
    def flush_worker_buffer(self):
        """버퍼가 일정 시간 내에 비워지지 않으면 버퍼 내용을 출력하고 비웁니다."""
        self.communication_manager.flush_worker_buffer()  # 버퍼 비우기 호출
