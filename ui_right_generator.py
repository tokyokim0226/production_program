from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QButtonGroup, QLineEdit, QWidget, QTextEdit, 
    QGridLayout, QInputDialog, QMessageBox, QSizePolicy
)
from PyQt5.QtCore import Qt

class UIRightGenerator(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.cmd_buttons_layout = None  # 명령어 버튼 레이아웃 저장
        self.op_button_group = None  # OP 버튼 그룹 저장
        self.initUI()

    # UI 초기화 메서드
    def initUI(self):
        layout = QVBoxLayout(self)

        # 각 레이아웃을 생성하여 추가
        id_layout = self.create_manual_input_layout()
        len_chk_layout = self.create_len_chk_layout()
        message_display_layout = self.create_message_display_layout()

        layout.addLayout(id_layout)
        layout.addLayout(len_chk_layout)
        layout.addLayout(message_display_layout)

        placeholder = self.create_placeholder_widget()
        layout.addWidget(placeholder)

        self.setLayout(layout)

        # 기본값 설정 및 UI 업데이트
        self.parent.id_input.setText("999")
        self.set_cmd("ADD")
        self.set_op("?")

        # 실시간으로 생성된 메시지를 업데이트하는 신호 연결
        self.parent.id_input.textChanged.connect(self.update_len_chk)
        self.parent.data_input.textChanged.connect(self.update_len_chk)
        self.parent.cmd_input.textChanged.connect(self.update_len_chk)
        self.parent.op_input.textChanged.connect(self.update_len_chk)

        # 데이터 입력 필드를 6자 제한 및 대문자로 변경하는 핸들러 연결
        self.parent.data_input.textChanged.connect(self.limit_and_convert_data)

    # 데이터 입력 필드에 대해 입력 제한 및 대문자 변환
    def limit_and_convert_data(self):
        current_text = self.parent.data_input.text()
        limited_text = current_text[:6].upper()

        # 신호 차단 후 입력 필드 업데이트 및 다시 신호 연결
        self.parent.data_input.blockSignals(True)
        self.parent.data_input.setText(limited_text)
        self.parent.data_input.blockSignals(False)

        # 길이 및 체크섬 업데이트
        self.update_len_chk()

    # 수동 입력 레이아웃 생성
    def create_manual_input_layout(self):
        self.parent.cmd_input = QLineEdit(self.parent)
        self.parent.op_input = QLineEdit(self.parent)
        self.parent.id_input = QLineEdit(self.parent)
        self.parent.data_input = QLineEdit(self.parent)
        self.parent.chk_value = QLineEdit(self.parent)

        layout = QGridLayout()

        id_label = QLabel("ID")
        id_label.setAlignment(Qt.AlignCenter)
        cmd_label = QLabel("CMD")
        cmd_label.setAlignment(Qt.AlignCenter)
        op_label = QLabel("OP")
        op_label.setAlignment(Qt.AlignCenter)
        data_label = QLabel("DATA")
        data_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(id_label, 0, 0, 1, 1)
        layout.addWidget(cmd_label, 0, 1, 1, 2)
        layout.addWidget(op_label, 0, 3, 1, 1)
        layout.addWidget(data_label, 0, 4, 1, 1)

        # ID 입력 필드 및 증감 버튼
        id_input_layout = QHBoxLayout()
        self.parent.id_input = QLineEdit()
        self.parent.id_input.setAlignment(Qt.AlignCenter)
        self.parent.id_input.setMaximumWidth(80)
        self.parent.id_input.setMaxLength(3)

        down_button = QPushButton("-")
        down_button.setMaximumWidth(40)
        down_button.clicked.connect(self.decrement_id)

        up_button = QPushButton("+")
        up_button.setMaximumWidth(40)
        up_button.clicked.connect(self.increment_id)

        id_input_layout.addWidget(down_button)
        id_input_layout.addWidget(self.parent.id_input)
        id_input_layout.addWidget(up_button)

        layout.addLayout(id_input_layout, 1, 0, 1, 1)

        # 명령어 버튼 그룹 생성 및 업데이트
        self.parent.cmd_button_group = QButtonGroup(self.parent)
        self.parent.cmd_buttons = ["ADD", "COL", "POW", "MIN", "MAX", "DBG", "INF", "D_C", "DET", "SEA", "MGS"]
        self.parent.custom_cmd_buttons = []
        self.cmd_buttons_layout = QGridLayout()  # 명령어 버튼 레이아웃 저장

        self.update_cmd_buttons_layout()

        # OP 버튼 그룹 생성
        self.op_button_group = QButtonGroup(self.parent)
        op_buttons = ["!", "?", "="]
        op_buttons_layout = QVBoxLayout()
        for op in op_buttons:
            button = QPushButton(op)
            button.setCheckable(True)
            button.clicked.connect(lambda checked, op=op: self.set_op(op))
            self.op_button_group.addButton(button)
            op_buttons_layout.addWidget(button)

        layout.addLayout(op_buttons_layout, 1, 3, len(op_buttons), 1)

        # 데이터 입력 필드 추가
        self.parent.data_input = QLineEdit()
        self.parent.data_input.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.parent.data_input, 1, 4, 1, 1)

        layout.addLayout(self.cmd_buttons_layout, 1, 1, (len(self.parent.cmd_buttons) + len(self.parent.custom_cmd_buttons)) // 2 + 1, 2)

        return layout

    # 명령어 버튼 레이아웃 업데이트
    def update_cmd_buttons_layout(self):
        # 기존 버튼 제거
        for i in reversed(range(self.cmd_buttons_layout.count())):
            widget = self.cmd_buttons_layout.itemAt(i).widget()
            if widget:
                self.cmd_buttons_layout.removeWidget(widget)
                widget.setParent(None)

        # 기본 명령어 버튼 추가
        for i, cmd in enumerate(self.parent.cmd_buttons):
            button = QPushButton(cmd)
            button.setCheckable(True)
            button.clicked.connect(lambda checked, cmd=cmd: self.set_cmd(cmd))
            self.parent.cmd_button_group.addButton(button)
            self.cmd_buttons_layout.addWidget(button, i // 2, i % 2)

        # 사용자 정의 명령어 버튼 추가
        for i, cmd in enumerate(self.parent.custom_cmd_buttons, len(self.parent.cmd_buttons)):
            button = QPushButton(cmd)
            button.setCheckable(True)
            button.clicked.connect(lambda checked, cmd=cmd: self.set_cmd(cmd))
            self.parent.cmd_button_group.addButton(button)
            self.cmd_buttons_layout.addWidget(button, i // 2, i % 2)

    # CMD 버튼 선택
    def set_cmd(self, cmd):
        for button in self.parent.cmd_button_group.buttons():
            if button.text() == cmd:
                button.setChecked(True)
                break

        self.parent.cmd_input.setText(cmd)
        self.update_len_chk()

    # OP 버튼 선택
    def set_op(self, op):
        for button in self.op_button_group.buttons():
            if button.text() == op:
                button.setChecked(True)
                break

        self.parent.op_input.setText(op)
        if op == "?":
            self.parent.data_input.setText("")  # 데이터 입력 필드 초기화
            self.parent.data_input.setReadOnly(True)
            self.parent.data_input.setStyleSheet("background-color: #e0e0e0;")  # 데이터 입력 필드를 회색으로 설정
        else:
            self.parent.data_input.setReadOnly(False)
            self.parent.data_input.setStyleSheet("")  # 데이터 입력 필드 스타일 재설정
        self.update_len_chk()

    # ID 값 증가
    def increment_id(self):
        current_text = self.parent.id_input.text()
        if current_text.isdigit():
            current_value = int(current_text)
            if current_value < 999:
                self.parent.id_input.setText(str(current_value + 1))
            else:
                self.parent.id_input.setText("0")
        else:
            self.parent.id_input.setText("1")

    # ID 값 감소
    def decrement_id(self):
        current_text = self.parent.id_input.text()
        if current_text.isdigit():
            current_value = int(current_text)
            if current_value > 0:
                self.parent.id_input.setText(str(current_value - 1))
            else:
                self.parent.id_input.setText("999")
        else:
            self.parent.id_input.setText("999")

    # 체크섬 및 길이 레이아웃 생성
    def create_len_chk_layout(self):
        len_chk_layout = QHBoxLayout()

        chk_layout = QHBoxLayout()
        chk_label = QLabel("CHK")
        self.parent.chk_value = QLineEdit()
        self.parent.chk_value.setMaximumWidth(200)
        self.parent.chk_value.setReadOnly(True)
        self.parent.chk_value.setAlignment(Qt.AlignCenter)
        chk_layout.addWidget(chk_label)
        chk_layout.addWidget(self.parent.chk_value)

        len_chk_layout.addLayout(chk_layout)

        return len_chk_layout

    # 메시지 표시 및 전송 레이아웃 생성
    def create_message_display_layout(self):
        message_display_layout = QHBoxLayout()

        self.parent.message_display = QLineEdit()
        self.parent.message_display.setObjectName("generated_message")
        self.parent.message_display.setReadOnly(True)
        self.parent.message_display.setAlignment(Qt.AlignCenter)

        send_button = QPushButton("Send")
        send_button.clicked.connect(self.parent.send_generated_message)

        message_display_layout.addWidget(self.parent.message_display)
        message_display_layout.addWidget(send_button)

        return message_display_layout

    # 빈 공간을 채우는 플레이스홀더 위젯 생성
    def create_placeholder_widget(self):
        placeholder = QTextEdit()
        placeholder.setReadOnly(True)
        placeholder.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        return placeholder

    # 길이 및 체크섬 업데이트
    def update_len_chk(self):
        id_value = self.parent.id_input.text()
        cmd_value = self.parent.cmd_input.text()
        op_value = self.parent.op_input.text()
        data_value = self.parent.data_input.text()

        # ID를 3자리 숫자로 포맷
        if id_value.isdigit():
            id_value = f"{int(id_value):03}"

        stx = self.parent.protocol_handler.STX
        etx = self.parent.protocol_handler.ETX

        # OP에 따라 메시지 내용 조정
        if op_value == "?":
            stx_and_content = f"{stx}{id_value}{cmd_value}{op_value},"
        else:
            stx_and_content = f"{stx}{id_value}{cmd_value}{op_value}{data_value},"

        chk_value = self.parent.protocol_handler.calculate_checksum(stx_and_content)

        self.parent.chk_value.setText(chk_value)

        full_message = f"{stx_and_content}{chk_value}{etx}"
        self.parent.message_display.setText(full_message)
