import sys
import os
import platform
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QMessageBox
from PyQt5.QtCore import Qt, QTimer
import psutil

class SystemMonitor(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.update_stats()

        # Таймерчик наш — обновляет цифры каждую полсекунды, чтобы всё было свежачком
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(500)

    def init_ui(self):
        # Заголовок окна — ты же знаешь, что это просто окно
        self.setWindowTitle("Системный мониторинг на PyQt5")
        self.resize(500, 200)  # чуть побольше сделал, чтобы кнопка нормально влезла

        self.layout = QVBoxLayout()

        # Метки для отображения загруженности процессора, оперативки и диска
        self.cpu_label = QLabel("CPU: ")
        self.cpu_label.setAlignment(Qt.AlignCenter)
        self.cpu_label.setStyleSheet("font-size: 18px;")

        self.ram_label = QLabel("RAM: ")
        self.ram_label.setAlignment(Qt.AlignCenter)
        self.ram_label.setStyleSheet("font-size: 18px;")

        self.disk_label = QLabel("Disk: ")
        self.disk_label.setAlignment(Qt.AlignCenter)
        self.disk_label.setStyleSheet("font-size: 18px;")

        # Вот она — кнопка выключения! Нажмёшь — компьютер скажет "пока-пока"
        self.shutdown_button = QPushButton("Выключить компьютер")
        self.shutdown_button.setStyleSheet("font-size: 16px; background-color: #d9534f; color: white;")
        self.shutdown_button.clicked.connect(self.confirm_shutdown)

        # Собираем всё в кучу
        self.layout.addWidget(self.cpu_label)
        self.layout.addWidget(self.ram_label)
        self.layout.addWidget(self.disk_label)
        self.layout.addWidget(self.shutdown_button)

        self.setLayout(self.layout)
        self.setStyleSheet("background-color: #2E2E2E; color: white;")  # тёмная тема, как ты любишь

    def update_stats(self):
        # Забираем данные про систему, без тормозов UI
        cpu = round(psutil.cpu_percent(interval=None), 1)
        ram = round(psutil.virtual_memory().percent, 1)
        disk_usage = psutil.disk_usage('/')
        disk = round(disk_usage.used / disk_usage.total * 100, 1)

        # Логика цвета: зелёный — кайф, жёлтый — осторожно, красный — пиши завещание
        cpu_color = "green" if cpu < 50 else "orange" if cpu < 80 else "red"
        ram_color = "green" if ram < 50 else "orange" if ram < 80 else "red"
        disk_color = "green" if disk < 50 else "orange" if disk < 80 else "red"

        # Обновляем метки с цветом — чтобы глаз радовался
        self.cpu_label.setText(f"CPU: <span style='color:{cpu_color};'>{cpu}%</span>")
        self.ram_label.setText(f"RAM: <span style='color:{ram_color};'>{ram}%</span>")
        self.disk_label.setText(f"Disk: <span style='color:{disk_color};'>{disk}%</span>")

    def confirm_shutdown(self):
        # Вот это попап, чтобы случайно не убить комп — спрашиваем, уверен ли ты, бро?
        reply = QMessageBox.question(
            self,
            'Подтверждение',
            "Ты уверен, что хочешь выключить компьютер?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.shutdown_pc()  # если да — вперёд, к выключению!

    def shutdown_pc(self):
        # Тут магия в зависимости от ОС — выключаем комп командой из терминала
        system = platform.system()
        if system == "Windows":
            os.system("shutdown /s /t 1")  # Windows style
        elif system == "Linux" or system == "Darwin":  # MacOS тоже Darwin
            os.system("shutdown now")  # Linux & Mac style
        else:
            # Если ОС крутая и непонятная — просто сообщаем, что команда не поддерживается
            QMessageBox.warning(self, "Ошибка", "Неизвестная ОС, команда выключения не поддерживается.")

def main():
    # Запуск программы — ничего сложного, просто PyQt магия
    app = QApplication(sys.argv)
    monitor = SystemMonitor()
    monitor.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
# леее, всё, я сдедал. пойду теперь поем, а то тут уже голодный сидел полчаса 
# и код писал, и комменты, и всё такое. Надеюсь, тебе понравится!
# да, пока кто читает это на гитхабе.
