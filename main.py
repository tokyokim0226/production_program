import sys
from PyQt5.QtWidgets import QApplication
from serial_port_monitor import SerialPortMon

# 스타일 시트를 로드하는 함수
def load_stylesheet(app):
    """애플리케이션의 스타일 시트를 로드."""
    with open("style.qss", "r") as file:  # 'style.qss' 파일을 읽어서
        app.setStyleSheet(file.read())  # 애플리케이션에 스타일 시트 적용

# 메인 애플리케이션 시작 부분
if __name__ == '__main__':
    app = QApplication(sys.argv)  # PyQt 애플리케이션 객체 생성

    # 스타일 시트 로드
    load_stylesheet(app)  # 스타일 시트를 로드하여 애플리케이션에 적용

    ex = SerialPortMon()  # SerialPortMon 클래스 인스턴스 생성 (메인 윈도우)
    ex.show()  # 메인 윈도우 표시
    sys.exit(app.exec_())  # 애플리케이션 이벤트 루프 실행 및 정상 종료 시 프로그램 종료
