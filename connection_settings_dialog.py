from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton

class ConnectionSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Connection Settings")
        self.setFixedSize(500, 400)

        layout = QVBoxLayout(self)

        # Refresh Connections button at the top
        refresh_button = QPushButton("Refresh Connections")
        refresh_button.clicked.connect(self.refresh_connections)  # Connect the button to the refresh method
        layout.addWidget(refresh_button)

        # Port selection
        port_layout = QHBoxLayout()
        port_label = QLabel("Select Port:")
        self.port_combo = QComboBox()
        self.port_combo.addItems(parent.connection_manager.get_serial_ports())  # Populate with initial available ports
        port_layout.addWidget(port_label)
        port_layout.addWidget(self.port_combo)
        layout.addLayout(port_layout)

        # Baud rate selection
        baud_rate_layout = QHBoxLayout()
        baud_rate_label = QLabel("Baud Rate:")
        self.baud_rate_combo = QComboBox()
        self.baud_rate_combo.addItems(["1200", "2400", "4800", "9600", "19200", "38400", "57600", "115200", "230400", "460800", "921600"])
        self.baud_rate_combo.setCurrentText("9600")
        baud_rate_layout.addWidget(baud_rate_label)
        baud_rate_layout.addWidget(self.baud_rate_combo)
        layout.addLayout(baud_rate_layout)

        # Data bits selection
        data_bits_layout = QHBoxLayout()
        data_bits_label = QLabel("Data Bits:")
        self.data_bits_combo = QComboBox()
        self.data_bits_combo.addItems(["5", "6", "7", "8"])
        self.data_bits_combo.setCurrentText("8")
        data_bits_layout.addWidget(data_bits_label)
        data_bits_layout.addWidget(self.data_bits_combo)
        layout.addLayout(data_bits_layout)

        # Parity selection
        parity_layout = QHBoxLayout()
        parity_label = QLabel("Parity:")
        self.parity_combo = QComboBox()
        self.parity_combo.addItems(["None", "Odd", "Even"])
        self.parity_combo.setCurrentText("None")
        parity_layout.addWidget(parity_label)
        parity_layout.addWidget(self.parity_combo)
        layout.addLayout(parity_layout)

        # Stop bits selection
        stop_bits_layout = QHBoxLayout()
        stop_bits_label = QLabel("Stop Bits:")
        self.stop_bits_combo = QComboBox()
        self.stop_bits_combo.addItems(["1", "1.5", "2"])
        self.stop_bits_combo.setCurrentText("1")
        stop_bits_layout.addWidget(stop_bits_label)
        stop_bits_layout.addWidget(self.stop_bits_combo)
        layout.addLayout(stop_bits_layout)

        # Buttons (OK/Cancel)
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        # Connect buttons
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def refresh_connections(self):
        """Refresh the list of available serial ports."""
        self.port_combo.clear()  # Clear the existing items in the ComboBox
        self.port_combo.addItems(self.parent.connection_manager.get_serial_ports())  # Repopulate with the updated list of ports

    def get_settings(self):
        return {
            "port": self.port_combo.currentText(),
            "baud_rate": int(self.baud_rate_combo.currentText()),
            "data_bits": int(self.data_bits_combo.currentText()),
            "parity": self.parity_combo.currentText(),
            "stop_bits": float(self.stop_bits_combo.currentText())
        }
