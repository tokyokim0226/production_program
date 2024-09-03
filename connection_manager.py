import serial
from PyQt5.QtWidgets import QMessageBox, QDialog
from connection_settings_dialog import ConnectionSettingsDialog
from serial.tools import list_ports

class ConnectionManager:
    def __init__(self, parent):
        self.parent = parent

    def get_serial_ports(self):
        ports = [port.device for port in list_ports.comports()]
        return ports if ports else ["No COM ports"]

    def connect_serial(self):
        if self.parent.serial_port and self.parent.serial_port.is_open:
            self.close_serial()
        else:
            dialog = ConnectionSettingsDialog(self.parent)
            result = dialog.exec_()

            if result == QDialog.Accepted:
                settings = dialog.get_settings()
                port = settings['port']
                try:
                    self.parent.serial_port = serial.Serial(
                        port,
                        baudrate=settings["baud_rate"],
                        bytesize=settings["data_bits"],
                        parity=self.get_parity(settings["parity"]),
                        stopbits=settings["stop_bits"],
                        timeout=0.1
                    )
                    self.parent.logger.log_message("Connect", f"Connected to {port}")
                    self.parent.communication_manager.start_reading_thread()
                    self.parent.connect_button.setText("Close")

                except Exception as e:
                    QMessageBox.critical(self.parent, "Connection Error", f"Could not connect to {port}: {str(e)}")
                    self.parent.serial_port = None

    def close_serial(self):
        if self.parent.serial_port and self.parent.serial_port.is_open:
            port = self.parent.serial_port.port
            self.parent.communication_manager.stop_reading_thread()
            self.parent.serial_port.close()
            self.parent.logger.log_message("Disconnect", f"Disconnected from {port}")
            self.parent.connect_button.setText("Connect")
        else:
            self.parent.logger.log_message("Info", "No open serial port to disconnect.")

    def get_parity(self, parity_str):
        parity_dict = {
            "None": serial.PARITY_NONE,
            "Odd": serial.PARITY_ODD,
            "Even": serial.PARITY_EVEN
        }
        return parity_dict.get(parity_str, serial.PARITY_NONE)
