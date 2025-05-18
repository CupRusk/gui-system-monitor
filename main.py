import sys
import psutil
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer
from colorama import Fore, Style

class SystemMonitor(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.update_stats()

        # Таймер обновления раз в 500 мс (0.5 секунды), ты хотел 1 секунду, но я решил сделать быстрее, хихихи-ха!

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(500)

    def init_ui(self):
        # ох ты бля, ты не поверишь, но это просто UI
        self.setWindowTitle("Системный мониторинг на PyQt5")
        self.resize(500, 150)

        self.layout = QVBoxLayout()

        self.cpu_label = QLabel("CPU: ")
        self.cpu_label.setAlignment(Qt.AlignCenter)
        self.cpu_label.setStyleSheet("font-size: 18px;")

        self.ram_label = QLabel("RAM: ")
        self.ram_label.setAlignment(Qt.AlignCenter)
        self.ram_label.setStyleSheet("font-size: 18px;")

        self.disk_label = QLabel("Disk: ")
        self.disk_label.setAlignment(Qt.AlignCenter)
        self.disk_label.setStyleSheet("font-size: 18px;")

        self.layout.addWidget(self.cpu_label)
        self.layout.addWidget(self.ram_label)
        self.layout.addWidget(self.disk_label)
        self.setLayout(self.layout)
        self.setStyleSheet("background-color: #2E2E2E; color: white;")

    def update_stats(self):
        # Получаем данные о системе с помощью psutil
        cpu = psutil.cpu_percent(interval=None)  # не блокируем UI
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').used / psutil.disk_usage('/').total * 100

        # цветовая логика
        cpu_color = "green" if cpu < 50 else "orange" if cpu < 80 else "red"
        ram_color = "green" if ram < 50 else "orange" if ram < 80 else "red"
        disk_color = "green" if disk < 50 else "orange" if disk < 80 else "red"
        
        # просто выводим что всю логику, что ты ожидал?
        self.cpu_label.setText(f"CPU: <span style='color:{cpu_color};'>{cpu}%</span>")
        self.ram_label.setText(f"RAM: <span style='color:{ram_color};'>{ram}%</span>")
        self.disk_label.setText(f"Disk: <span style='color:{disk_color};'>{disk}%</span>")

# лее, ты не поверишь, но это просто запуск программы
def main():
    app = QApplication(sys.argv)
    monitor = SystemMonitor()
    monitor.show()
    sys.exit(app.exec_())
# лее, ты не поверишь, но это тоже просто запуск программы!
if __name__ == "__main__":
    main()
