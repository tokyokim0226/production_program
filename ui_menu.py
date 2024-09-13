from PyQt5.QtWidgets import QAction, QInputDialog, QMessageBox, QWidget

# UIMenu 클래스: 메뉴바에서 커맨드(명령어)를 추가, 수정, 삭제하는 기능을 관리
class UIMenu(QWidget):  # QWidget을 상속하여 메뉴 인터페이스 생성
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent  # parent는 주로 메인 애플리케이션을 참조
        self.initUI()  # UI 생성 메서드 호출

    # UI 생성 메서드
    def initUI(self):
        menubar = self.parent.menuBar()  # 메인 윈도우에서 메뉴바 가져오기
        self.parent.setMenuBar(menubar)  # 메뉴바 설정
        self.create_menu()  # 메뉴 생성 메서드 호출

    # 메뉴 생성 메서드
    def create_menu(self):
        # 'Command'라는 이름의 메뉴 생성
        command_menu = self.parent.menuBar().addMenu("Command")

        # 'Add Command' 액션 생성 및 연결
        add_cmd_action = QAction("Add Command", self.parent)
        add_cmd_action.triggered.connect(self.add_custom_command)  # 'Add Command' 클릭 시 호출될 메서드 연결
        command_menu.addAction(add_cmd_action)  # 'Add Command' 메뉴에 추가

        # 'Edit Command' 액션 생성 및 연결
        edit_cmd_action = QAction("Edit Command", self.parent)
        edit_cmd_action.triggered.connect(self.edit_custom_command)  # 'Edit Command' 클릭 시 호출될 메서드 연결
        command_menu.addAction(edit_cmd_action)  # 'Edit Command' 메뉴에 추가

        # 'Delete Command' 액션 생성 및 연결
        delete_cmd_action = QAction("Delete Command", self.parent)
        delete_cmd_action.triggered.connect(self.delete_custom_command)  # 'Delete Command' 클릭 시 호출될 메서드 연결
        command_menu.addAction(delete_cmd_action)  # 'Delete Command' 메뉴에 추가

    # 사용자 정의 명령어 추가 메서드
    def add_custom_command(self):
        if len(self.parent.custom_cmd_buttons) < 3:  # 최대 3개의 명령어만 추가 가능
            # 사용자에게 3자리 명령어 입력받기
            cmd, ok = QInputDialog.getText(self.parent, "Add Command", "Enter 3-character CMD:")
            if ok and len(cmd) == 3:  # 사용자가 입력을 확인하고, 명령어가 3자리인지 확인
                if cmd in self.parent.cmd_buttons or cmd in self.parent.custom_cmd_buttons:
                    # 명령어가 이미 존재하는 경우 경고 메시지 표시
                    QMessageBox.warning(self.parent, "Input Error", "CMD already exists.")
                else:
                    # 새 명령어를 사용자 정의 명령어 목록에 추가
                    self.parent.custom_cmd_buttons.append(cmd)
                    self.parent.ui_right_generator.update_cmd_buttons_layout()  # 명령어 버튼 레이아웃 업데이트
            elif len(cmd) != 3:
                # 명령어가 3자리가 아니면 경고 메시지 표시
                QMessageBox.warning(self.parent, "Input Error", "CMD must be 3 characters long.")
        else:
            # 사용자 정의 명령어가 이미 3개인 경우 경고 메시지 표시
            QMessageBox.warning(self.parent, "Limit Reached", "You can only add up to 3 custom commands.")

    # 사용자 정의 명령어 수정 메서드
    def edit_custom_command(self):
        """기존 사용자 정의 명령어를 수정합니다."""
        if not self.parent.custom_cmd_buttons:  # 수정할 사용자 정의 명령어가 없으면 정보 메시지 표시
            QMessageBox.information(self.parent, "Info", "No custom commands to edit.")
            return

        # 수정할 명령어를 선택
        cmd_to_edit, ok = QInputDialog.getItem(self.parent, "Edit Command", "Select command to edit:", self.parent.custom_cmd_buttons, 0, False)

        if ok and cmd_to_edit:
            # 새 명령어 입력
            new_cmd, ok = QInputDialog.getText(self.parent, "Edit Command", "Enter new 3-character CMD:")

            if ok and len(new_cmd) == 3:
                if new_cmd not in self.parent.cmd_buttons + self.parent.custom_cmd_buttons:
                    # 기존 명령어를 새 명령어로 대체
                    index = self.parent.custom_cmd_buttons.index(cmd_to_edit)
                    self.parent.custom_cmd_buttons[index] = new_cmd
                    self.parent.ui_right_generator.update_cmd_buttons_layout()  # 명령어 버튼 레이아웃 업데이트
                else:
                    # 새 명령어가 이미 존재하면 경고 메시지 표시
                    QMessageBox.warning(self.parent, "Error", "New command already exists or is invalid.")
            else:
                # 새 명령어가 3자리가 아니면 경고 메시지 표시
                QMessageBox.warning(self.parent, "Error", "Command must be exactly 3 characters.")

    # 사용자 정의 명령어 삭제 메서드
    def delete_custom_command(self):
        """기존 사용자 정의 명령어를 삭제합니다."""
        if not self.parent.custom_cmd_buttons:  # 삭제할 사용자 정의 명령어가 없으면 정보 메시지 표시
            QMessageBox.information(self.parent, "Info", "No custom commands to delete.")
            return

        # 삭제할 명령어 선택
        cmd_to_delete, ok = QInputDialog.getItem(self.parent, "Delete Command", "Select command to delete:", self.parent.custom_cmd_buttons, 0, False)

        if ok and cmd_to_delete:
            # 선택한 명령어 삭제
            self.parent.custom_cmd_buttons.remove(cmd_to_delete)
            self.parent.ui_right_generator.update_cmd_buttons_layout()  # 명령어 버튼 레이아웃 업데이트
