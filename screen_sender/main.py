import datetime
import keyboard
import os
import time
import sys

from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import *
from PIL import ImageGrab


class ScreenshotWorker(QObject):
    capture_screenshot_signal = pyqtSignal()

    @pyqtSlot()
    def capture_screenshot(self):
        self.capture_screenshot_signal.emit()


class ScreenshotThread(QThread):
    screenshot_saved_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        self.capture_screenshot()

    @pyqtSlot()
    def capture_screenshot(self):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        time.sleep(0.2)

        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        name, _ = QFileDialog.getSaveFileName(
            None, 'Сохранить файл', '', 'Images (*.png *.jpg)', options=options)
        time.sleep(0.2)

        if name:
            screenshot = ImageGrab.grab()
            screenshot_path = os.path.splitext(
                name)[0] + '_' + timestamp + '.jpg'
            screenshot.save(screenshot_path)
            self.screenshot_saved_signal.emit(screenshot_path)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(QSize(500, 200))
        self.setWindowTitle('Screen sender')
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(
            QLabel('1. Чтобы сделать скриншот экрана, нажмите ctrl+alt+s.\n'
                   '2. Чтобы убрать программу в трей, кликните ниже.', self))

        self.hide_button = QPushButton('Спрячь меня')
        self.hide_button.setFixedSize(100, 25)
        central_layout.addWidget(self.hide_button)
        central_layout.addItem(QSpacerItem(
            0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding))

        # directory section
        dir_layout = QHBoxLayout()
        self.dir_name_edit = QLineEdit()
        dir_layout.addWidget(QLabel('Путь:'))
        dir_layout.addWidget(self.dir_name_edit)

        dir_btn = QPushButton('Обзор')
        dir_btn.clicked.connect(self.open_dir_dialog)
        dir_btn.setFixedSize(70, 25)

        dir_layout.addWidget(dir_btn)
        central_layout.addLayout(dir_layout)

        version_label = QLabel('ver. 1.0.0')
        version_label.setAlignment(QtCore.Qt.AlignRight)
        central_layout.addWidget(version_label)

        self.show()

        # настроки иконок
        icon_path = (
            r'C:\Users\adm03\Desktop\work\programming\click_click_screen\icon\icon_.png')
        # иконка приложения
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(icon_path),
                       QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.setWindowIcon(icon)
        # иконка трея
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(
            QIcon(icon_path))

        show_action = QAction('☐   Открыть', self)
        hide_action = QAction('▼   Свернуть', self)
        quit_action = QAction('✕   Закрыть click click screen', self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(QApplication.instance().quit)
        # меню трея
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        self.screenshot_thread = ScreenshotThread()
        self.screenshot_thread.screenshot_saved_signal.connect(
            self.screenshot_saved)

        # обработчик изменения состояния кнопки
        self.hide_button.clicked.connect(self.handle_hide_button_click)

        keyboard.add_hotkey(
            'ctrl+alt+s', self.capture_and_save_screenshot)
        self.screenshot_worker = ScreenshotWorker()
        self.screenshot_worker.capture_screenshot_signal.connect(
            self.screenshot_thread.capture_screenshot)

    def capture_and_save_screenshot(self):
        self.screenshot_worker.capture_screenshot()

    def screenshot_saved(self, screenshot_path):
        print(f'Screenshot saved at {screenshot_path}')

    def handle_hide_button_click(self):
        if self.isHidden():
            self.show()
        else:
            self.hide()

    def open_dir_dialog(self):
        dir_name = QFileDialog.getExistingDirectory(self, 'Выберите папку')
        if dir_name:
            path = Path(dir_name)
            self.dir_name_edit.setText(str(path))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    mw = MainWindow()
    mw.hide()
    sys.exit(app.exec_())
