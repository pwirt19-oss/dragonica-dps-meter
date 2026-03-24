import sys
import socket
from PyQt5 import QtWidgets, QtGui, QtCore

class DPSTracker(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.total_damage = 0
        self.damage_history = []
        self.dps = 0
        self.start_time = QtCore.QDateTime.currentDateTime()

    def initUI(self):
        # Set layout and widgets
        self.setWindowTitle('DPS Meter')
        self.setGeometry(100, 100, 400, 300)

        self.dps_label = QtWidgets.QLabel('DPS: 0', self)
        self.total_damage_label = QtWidgets.QLabel('Total Damage: 0', self)
        self.stats_label = QtWidgets.QLabel('Statistics:', self)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.dps_label)
        self.layout.addWidget(self.total_damage_label)
        self.layout.addWidget(self.stats_label)
        self.setLayout(self.layout)

        # Start UDP listener
        self.udp_thread = UDPReceiver(self)
        self.udp_thread.damage_received.connect(self.update_damage)
        self.udp_thread.start()

    def update_damage(self, damage):
        self.total_damage += damage
        self.damage_history.append(damage)
        elapsed_time = self.start_time.secsTo(QtCore.QDateTime.currentDateTime())
        if elapsed_time > 0:
            self.dps = self.total_damage / elapsed_time
        self.update_labels()

    def update_labels(self):
        self.dps_label.setText(f'DPS: {self.dps:.2f}')
        self.total_damage_label.setText(f'Total Damage: {self.total_damage}')
        self.stats_label.setText(f'Statistics:
Damage History: {self.damage_history}')

class UDPReceiver(QtCore.QThread):
    damage_received = QtCore.pyqtSignal(int)

    def run(self):
        # UDP socket setup
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('0.0.0.0', 12345))  # Listen on port 12345
        while True:
            data, _ = sock.recvfrom(1024)
            damage = int(data.decode('utf-8'))  # Assuming damage data is sent as a string
            self.damage_received.emit(damage)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = DPSTracker()
    window.show()
    sys.exit(app.exec_())
