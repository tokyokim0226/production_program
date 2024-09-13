from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt

# Logger 클래스: 메시지를 테이블에 기록하고, 로그를 관리하는 클래스
class Logger:
    def __init__(self, log_table: QTableWidget):
        self.log_table = log_table  # 로그를 표시할 QTableWidget 객체 참조

    # 메시지를 테이블에 기록하는 메서드
    def log_message(self, message_type, message, time_taken=""):
        """로그 테이블에 메시지를 기록합니다."""
        row_position = self.log_table.rowCount()  # 현재 테이블의 행 수를 가져옴
        self.log_table.insertRow(row_position)  # 새로운 행 추가

        # 각 셀에 QTableWidgetItem 생성 및 편집 비활성화
        for i, text in enumerate([message_type, message, time_taken]):
            item = QTableWidgetItem(text)  # 각 메시지 항목을 QTableWidgetItem으로 생성
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # 셀 편집 비활성화
            self.log_table.setItem(row_position, i, item)  # 테이블의 각 셀에 항목 설정

    # 로그 테이블을 비우는 메서드
    def clear_log(self):
        """로그 테이블의 모든 행을 삭제합니다."""
        self.log_table.setRowCount(0)  # 테이블의 행 수를 0으로 설정하여 초기화
