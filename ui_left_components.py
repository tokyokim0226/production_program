from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QTableWidget, QHeaderView, QPushButton, QWidget, QLineEdit
from PyQt5.QtCore import Qt, pyqtSlot

# UILeftComponents 클래스: 왼쪽 UI 컴포넌트를 관리하는 클래스
# 여기에는 연결 버튼, 로그 클리어 버튼, 로그 테이블, 수동 명령어 입력및 전송 기능이 포함됨
class UILeftComponents(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent  # parent는 주로 메인 애플리케이션을 참조
        self.initUI()  # UI 생성 메서드 호출

    # UI 생성 메서드
    def initUI(self):
        main_layout = QVBoxLayout(self)  # 전체 UI를 관리할 수직 레이아웃

        # 연결 버튼 및 클리어로그 버튼을 포함하는 레이아웃 생성 (같은 줄에 배치하기 위해 레이아웃 합침)
        connect_and_clearlog_widget = self.create_connect_and_clearlog_layout()
        # 로그 테이블 생성
        self.parent.log_table = self.create_log_table()
        # 명령어 입력 창 생성
        input_layout = self.create_input_layout()

        # 현재 레이아웃을 메인 레이아웃에 추가
        main_layout.addWidget(connect_and_clearlog_widget)
        main_layout.addWidget(self.parent.log_table)
        main_layout.addWidget(input_layout)

        self.setLayout(main_layout)  # 전체 레이아웃을 위젯에 설정

    # 연결 및 클리어 로그 버튼 레이아웃 생성
    def create_connect_and_clearlog_layout(self):
        connect_and_clearlog_widget = QWidget()  # 위젯 생성
        connect_and_clearlog_layout = QHBoxLayout(connect_and_clearlog_widget)  # 수평 레이아웃

        # 연결 버튼 생성 및 설정
        self.parent.connect_button = QPushButton("Connect")  # "Connect" 버튼 생성
        self.parent.connect_button.setMaximumWidth(100)  # 버튼의 최대 너비 설정
        self.parent.connect_button.clicked.connect(self.parent.open_connection_dialog)  # 버튼 클릭 시 연결 대화 상자 열기

        # 클리어 로그 버튼 생성 및 설정
        clear_log_button = QPushButton("Clear Log")  # "Clear Log" 버튼 생성
        clear_log_button.setMaximumWidth(100)  # 버튼의 최대 너비 설정
        clear_log_button.clicked.connect(self.parent.clear_log)  # 버튼 클릭 시 로그 생성

        # 버튼들을 레이아웃에 추가
        connect_and_clearlog_layout.addWidget(self.parent.connect_button)
        connect_and_clearlog_layout.addStretch(1)  # 버튼 사이에 공간 추가
        connect_and_clearlog_layout.addWidget(clear_log_button)

        return connect_and_clearlog_widget  # 최종적으로 생성된 위젯 반환

    # 로그 테이블 생성 메서드
    def create_log_table(self):
        log_table = QTableWidget()  # 로그 테이블 위젯 생성
        log_table.setColumnCount(3)  # 3개의 열 설정
        log_table.setHorizontalHeaderLabels(["Type", "Message", "Time (ms)"])  # 열 헤더 레이블 설정

        header = log_table.horizontalHeader()  # 테이블의 헤더 설정
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # 첫 번째 열의 크기를 내용에 맞춤
        header.setSectionResizeMode(1, QHeaderView.Stretch)           # 두 번째 열은 남은 공간을 차지
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # 세 번째 열의 크기를 내용에 맞춤
        header.setStretchLastSection(False)  # 마지막 열 자동 확장 비활성화

        # 테이블의 세로 헤더 설정
        log_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)  # 세로 헤더 크기 내용에 맞춤
        log_table.verticalHeader().setDefaultAlignment(Qt.AlignCenter)  # 세로 헤더의 기본 정렬을 중앙으로 설정

        log_table.setAlternatingRowColors(True)  # 행의 색상을 교차하여 설정
        log_table.setWordWrap(True)  # 단어가 긴 경우 줄 바꿈 허용
        log_table.setHorizontalScrollMode(QTableWidget.ScrollPerPixel)  # 가로 스크롤을 픽셀 단위로 설정
        log_table.setVerticalScrollMode(QTableWidget.ScrollPerPixel)  # 세로 스크롤을 픽셀 단위로 설정

        # 새 행이 삽입되면 테이블을 자동으로 아래로 스크롤
        log_table.model().rowsInserted.connect(lambda: self.scroll_to_bottom(log_table))

        return log_table  # 최종적으로 생성된 테이블 반환

    # 명령어 입력 레이아웃 생성 메서드
    def create_input_layout(self):
        input_widget = QWidget()  # 입력 위젯 생성
        input_layout = QHBoxLayout(input_widget)  # 수평 레이아웃 설정
        self.parent.command_input = QLineEdit()  # 명령어 입력 창 생성
        send_button = QPushButton("Send")  # "Send" 버튼 생성
        send_button.setMaximumWidth(80)  # 버튼의 최대 너비 설정
        send_button.clicked.connect(self.parent.send_message)  # 버튼 클릭 시 메시지 전송

        # 레이아웃에 입력창과 버튼 추가
        input_layout.addWidget(self.parent.command_input, 1)  # 명령어 입력 창을 1의 비율로 추가
        input_layout.addWidget(send_button)  # 전송 버튼 추가

        return input_widget  # 최종적으로 생성된 입력 위젯 반환

    # 테이블을 자동으로 마지막 행까지 스크롤
    @pyqtSlot()
    def scroll_to_bottom(self, log_table):
        log_table.scrollToBottom()  # 테이블의 스크롤을 맨 아래로 이동
