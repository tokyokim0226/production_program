from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QGroupBox, QGridLayout, QSizePolicy, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt, QTimer

class UIRightProduction(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent  # 부모 위젯 설정
        self.retry_count = 0  # 재시도 횟수 초기화
        self.max_retries = 3  # 최대 재시도 횟수 설정
        self.timeout_duration = 1000  # 타임아웃 시간 설정 (1초)
        self.timer = QTimer(self)  # 타이머 객체 생성
        self.timer.timeout.connect(self.handle_timeout)  # 타이머가 만료되면 handle_timeout 메서드 실행
        self.current_step = 0  # 현재 단계 트래킹
        self.current_message = None  # 현재 전송 중인 메시지 저장
        self.initUI()

    # UI 초기화 메서드
    def initUI(self):
        main_layout = QVBoxLayout(self)  # 메인 레이아웃

        # 버튼 레이아웃 설정
        button_layout = QHBoxLayout()

        # ADDRESS 체크 버튼
        self.address_check_button = QPushButton("ADDRESS 체크하기")
        self.address_check_button.clicked.connect(self.address_check_only)

        # 기기 초기화 버튼
        self.device_reset_button = QPushButton("기기 초기화하기")
        self.device_reset_button.clicked.connect(self.factory_reset)

        button_layout.addWidget(self.address_check_button)
        button_layout.addWidget(self.device_reset_button)

        main_layout.addLayout(button_layout)
        main_layout.addSpacing(30)

        # 현재 ID 설정 UI 구성
        current_id_label = QLabel("지정 ID")
        current_id_label.setAlignment(Qt.AlignCenter)
        current_id_label.setObjectName("IDLabel")
        main_layout.addWidget(current_id_label)

        # ID 입력 필드와 증가/감소 버튼 구성
        current_id_layout = QHBoxLayout()

        self.decrement_button = QPushButton("-")
        self.decrement_button.setFixedSize(50, 50)
        self.decrement_button.setObjectName("IDButton")

        self.increment_button = QPushButton("+")
        self.increment_button.setFixedSize(50, 50)
        self.increment_button.setObjectName("IDButton")

        self.current_id_textbox = QLineEdit()  # ID 입력 필드
        self.current_id_textbox.setMaxLength(3)
        self.current_id_textbox.setAlignment(Qt.AlignCenter)
        self.current_id_textbox.setValidator(QIntValidator(0, 998, self))  # 0에서 998 사이의 값만 허용
        self.current_id_textbox.setFixedHeight(50)
        self.current_id_textbox.setObjectName("IDTextBox")
        self.current_id_textbox.setText("1")  # 초기 값 설정

        current_id_layout.addWidget(self.decrement_button)
        current_id_layout.addWidget(self.current_id_textbox)
        current_id_layout.addWidget(self.increment_button)

        main_layout.addLayout(current_id_layout)

        # ADDRESS 바꾸기 버튼
        full_button_layout = QHBoxLayout()
        self.full_button = QPushButton("ADDRESS 바꾸기")
        self.full_button.setFixedHeight(50)
        self.full_button.setToolTip("ADDRESS 변경 프로세스 실행")  # 툴팁 설명
        self.full_button.clicked.connect(self.address_change_process)

        full_button_layout.addWidget(self.full_button)
        main_layout.addLayout(full_button_layout)

        main_layout.addSpacing(20)

        # 상태 레이아웃 (기존 ID, 변환 ID, 체크 상태 표시)
        status_layout = QHBoxLayout()
        status_label = QLabel("상태:")
        status_label.setObjectName("status")
        status_layout.addWidget(status_label)

        status_layout.addSpacing(20)

        self.status_box = QGroupBox()  # 상태 표시 상자
        status_box_layout = QGridLayout()

        self.original_id_label = QLabel("기존 ID")
        self.converted_id_label = QLabel("변환 ID")
        self.check_label = QLabel("변환 ID 체크")

        self.original_id_status = QLineEdit()  # 기존 ID 상태
        self.original_id_status.setAlignment(Qt.AlignCenter)
        self.original_id_status.setReadOnly(True)

        self.converted_id_status = QLineEdit()  # 변환된 ID 상태
        self.converted_id_status.setAlignment(Qt.AlignCenter)
        self.converted_id_status.setReadOnly(True)

        self.check_status = QLineEdit()  # 체크 결과 상태
        self.check_status.setAlignment(Qt.AlignCenter)
        self.check_status.setReadOnly(True)

        # 상태 박스에 각 위젯 추가
        status_box_layout.addWidget(self.original_id_label, 0, 0, Qt.AlignCenter)
        status_box_layout.addWidget(self.converted_id_label, 0, 1, Qt.AlignCenter)
        status_box_layout.addWidget(self.check_label, 0, 2, Qt.AlignCenter)

        status_box_layout.addWidget(self.original_id_status, 1, 0)
        status_box_layout.addWidget(self.converted_id_status, 1, 1)
        status_box_layout.addWidget(self.check_status, 1, 2)

        self.status_box.setLayout(status_box_layout)
        status_layout.addWidget(self.status_box)

        main_layout.addLayout(status_layout)

        # 빈 공간을 차지하는 stretch 추가
        main_layout.addStretch()

        # ID 증가/감소 버튼에 클릭 이벤트 연결
        self.decrement_button.clicked.connect(self.decrement_id)
        self.increment_button.clicked.connect(self.increment_id)

        self.setLayout(main_layout)  # 메인 레이아웃 설정

    # ADDRESS를 체크하는 메시지를 전송하는 메서드
    def address_check_only(self):
        """Send a message to check the address."""
        self.current_message = "[999ADD?,30]"  # ADDRESS 확인 명령 메시지
        self.parent.communication_manager.send_message(self.current_message)

    # 기기를 초기화하는 메시지를 전송하는 메서드
    def factory_reset(self):
        if not self.parent.serial_port or not self.parent.serial_port.is_open:
            self.parent.logger.log_message("Error", "No serial port is connected.")
            return
        # Step 1: 현재 ADDRESS를 확인하는 메시지 전송
        self.current_message = "[999ADD?,30]"
        self.parent.communication_manager.send_message(self.current_message)

        # 메시지 수신 시 응답 처리 메서드 연결
        self.parent.communication_manager.worker.message_received.connect(self.factory_reset_response)

    # 기기 초기화 응답 처리
    def factory_reset_response(self, message, time_taken):
        # Step 2: 수신한 주소를 처리하고 기기 초기화 명령 전송
        if "ADD=" in message:
            current_id = message[1:4]  # 메시지에서 ADDRESS 추출

            # 추출한 ADDRESS를 이용해 초기화 명령 생성
            reset_command = f"[{current_id}POW!FRESET,"
            checksum = self.parent.protocol_handler.calculate_checksum(reset_command)
            factory_reset_message = f"{reset_command}{checksum}]"

            # 초기화 명령 전송
            self.parent.communication_manager.send_message(factory_reset_message)

            # 신호 연결 해제
            self.parent.communication_manager.worker.message_received.disconnect(self.factory_reset_response)

    # ADDRESS 변경 프로세스 시작
    def address_change_process(self):
        if not self.parent.serial_port or not self.parent.serial_port.is_open:
            self.parent.logger.log_message("Error", "No serial port is connected.")
            return

        self.full_button.setEnabled(False)  # 버튼 비활성화
        self.clear_status_boxes()  # 상태창 초기화
        self.log_address_change_start()  # 로그 기록

        self.current_step = 1
        self.current_message = "[999ADD?,30]"
        self.retry_count = 0
        self.send_message_with_retry()  # 메시지 전송 및 재시도 메커니즘 시작

    # 메시지 전송 및 재시도 메커니즘
    def send_message_with_retry(self):
        """Send the current message with retry mechanism."""
        # 연결이 유효한지 및 worker가 있는지 확인
        if not self.parent.serial_port or not self.parent.serial_port.is_open:
            self.abort_process("No serial port is connected.")
            return

        if not self.parent.communication_manager.worker:
            self.abort_process("Communication worker is not initialized.")
            return

        # 재시도 메커니즘
        if self.retry_count < self.max_retries:
            self.retry_count += 1
            self.parent.communication_manager.send_message(self.current_message)

            # 메시지 전송 시 타이머 시작
            self.timer.start(self.timeout_duration)

            # 메시지 수신 처리 연결
            try:
                self.parent.communication_manager.worker.message_received.connect(self.handle_message_received)
            except AttributeError:
                self.abort_process("Failed to connect to communication worker. Process aborted.")
        else:
            self.abort_process("No response received after 3 attempts. Process aborted.")

    # 메시지 수신 시 처리
    def handle_message_received(self, message, time_taken):
        """Handle the received message based on the current step."""
        self.timer.stop()  # 타이머 중지
        self.parent.communication_manager.worker.message_received.disconnect(self.handle_message_received)

        if self.current_step == 1:  # 첫 번째 단계: 현재 ADDRESS 수신 처리
            if "ADD=" in message:
                current_id = message[1:4]
                self.original_id_status.setText(current_id)

                if current_id == "000":
                    self.original_id_status.setStyleSheet("background-color: #34a853; color: white;")
                else:
                    self.original_id_status.setStyleSheet("background-color: #fbbc05; color: white;")

                self.current_step = 2
                QTimer.singleShot(200, self.send_change_command)  # 200ms 후 ADDRESS 변경 명령 전송

        elif self.current_step == 2:  # 두 번째 단계: ADDRESS 변경 확인
            if "ADD=" in message:
                current_id = message[1:4]
                new_id = f"{int(self.current_id_textbox.text()):03}"

                if current_id == new_id:
                    self.converted_id_status.setText(new_id)
                    self.converted_id_status.setStyleSheet("background-color: #34a853; color: white;")
                else:
                    self.converted_id_status.setStyleSheet("background-color: #ea4335; color: white;")

                self.current_step = 3
                QTimer.singleShot(200, self.verify_address_change)

        elif self.current_step == 3:  # 세 번째 단계: 변경된 ADDRESS 확인
            new_id = f"{int(self.current_id_textbox.text()):03}"
            if f"ADD={new_id}" in message:
                self.check_status.setText("OK")
                self.check_status.setStyleSheet("background-color: #34a853; color: white;")
                self.increment_id()
                self.reset_after_success()

    # ADDRESS 변경 명령 전송
    def send_change_command(self):
        new_id = f"{int(self.current_id_textbox.text()):03}"
        current_id = self.original_id_status.text()
        change_command = f"[{current_id}ADD!{new_id},"
        checksum = self.parent.protocol_handler.calculate_checksum(change_command)
        self.current_message = f"{change_command}{checksum}]"
        self.retry_count = 0
        self.send_message_with_retry()

    # ADDRESS 변경 검증
    def verify_address_change(self):
        self.current_message = "[999ADD?,30]"
        self.retry_count = 0
        self.send_message_with_retry()

    # 타임아웃 처리
    def handle_timeout(self):
        """Handle the timeout, retry the message or abort the process."""
        self.timer.stop()
        if self.retry_count < self.max_retries:
            self.send_message_with_retry()
        else:
            self.abort_process("No response received after 3 attempts. Process aborted.")

    # 프로세스 중단
    def abort_process(self, error_message):
        """Abort the current process, log the error, and update the UI."""
        self.timer.stop()

        # 신호 안전하게 해제
        try:
            if self.parent.communication_manager.worker:
                self.parent.communication_manager.worker.message_received.disconnect(self.handle_message_received)
        except (TypeError, AttributeError):
            pass  # worker가 이미 None이거나 연결되지 않은 경우 무시

        # 버튼 다시 활성화
        self.full_button.setEnabled(True)

        # 에러 메시지 로그 기록
        self.parent.logger.log_message("Error", error_message)

        # UI 업데이트 (실패 표시)
        self.check_status.setText("FAILED")
        self.check_status.setStyleSheet("background-color: #ea4335; color: white;")

    # 성공 후 리셋
    def reset_after_success(self):
        """Reset the process after successful completion."""
        QTimer.singleShot(750, self.apply_lighter_shade)
        QTimer.singleShot(750, lambda: self.full_button.setEnabled(True))

    # 상태창 초기화
    def clear_status_boxes(self):
        self.original_id_status.clear()
        self.converted_id_status.clear()
        self.check_status.clear()
        self.original_id_status.setStyleSheet("background-color: white;")
        self.converted_id_status.setStyleSheet("background-color: white;")
        self.check_status.setStyleSheet("background-color: white;")

    # 주소 변경 로그 기록
    def log_address_change_start(self):
        log_table = self.parent.log_table
        row_count = log_table.rowCount()
        log_table.insertRow(row_count)
        log_table.setSpan(row_count, 0, 1, 3)
        item = QTableWidgetItem("ADD 바꾸기")
        item.setBackground(Qt.green)
        item.setTextAlignment(Qt.AlignCenter)
        log_table.setItem(row_count, 0, item)

    # 색상 밝게 변경
    def apply_lighter_shade(self):
        lighter_green = "background-color: #b7e1cd; color: white;"
        lighter_orange = "background-color: #fce8b2; color: white;"
        lighter_red = "background-color: #f8c7c4; color: white;"

        if "#34a853" in self.original_id_status.styleSheet():
            self.original_id_status.setStyleSheet(lighter_green)
        elif "#fbbc05" in self.original_id_status.styleSheet():
            self.original_id_status.setStyleSheet(lighter_orange)

        if "#34a853" in self.converted_id_status.styleSheet():
            self.converted_id_status.setStyleSheet(lighter_green)
        elif "#ea4335" in self.converted_id_status.styleSheet():
            self.converted_id_status.setStyleSheet(lighter_red)

        if "#34a853" in self.check_status.styleSheet():
            self.check_status.setStyleSheet(lighter_green)
        elif "#ea4335" in self.check_status.styleSheet():
            self.check_status.setStyleSheet(lighter_red)

    # ID 감소
    def decrement_id(self):
        current_text = self.current_id_textbox.text()
        if current_text == "":
            self.current_id_textbox.setText("999")
        else:
            current_value = int(current_text)
            if current_value > 1:
                self.current_id_textbox.setText(str(current_value - 1))

    # ID 증가
    def increment_id(self):
        current_text = self.current_id_textbox.text()
        if current_text == "":
            self.current_id_textbox.setText("1")
        else:
            current_value = int(current_text)
            if current_value < 998:
                self.current_id_textbox.setText(str(current_value + 1))
