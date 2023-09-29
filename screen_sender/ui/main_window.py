import keyboard
import os
import time

from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from .hotkey_change_dialog import HotkeyChangeDialog
from screenshots.screenshot_worker import ScreenshotWorker, ScreenshotThread

from dotenv import load_dotenv


load_dotenv()
APP_ICON = os.getenv('APP_ICON')


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(QSize(500, 200))
        self.setWindowTitle('Screen sender')
        self.icon_path = APP_ICON
        self.hotkey_combinations = ['ctrl', 'alt', 's']

        self.setup_ui()
        self.setup_tray_icon()
        self.setup_screenshot_thread()
        self.setup_keyboard_shortcut()

        # Установка иконки приложения
        app_icon = QIcon(APP_ICON)
        self.setWindowIcon(app_icon)

    def setup_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        central_layout = QVBoxLayout(central_widget)

        hotkey_label_text = (
            '1. Чтобы сделать скриншот экрана, нажмите {0}.\n'
            '2. Чтобы убрать программу в трей, нажмите на "✕".\n'
            '3. Чтобы назначить свою комбинацию клавиш для скриншота, нажмите на кнопку ниже:'
        ).format('+'.join(self.hotkey_combinations))

        self.hotkey_label = QLabel(hotkey_label_text, self)
        central_layout.addWidget(self.hotkey_label)

        self.change_hotkey_button = QPushButton(
            'Изменить комбинацию для скриншота', self)
        self.change_hotkey_button.setFixedSize(300, 25)
        self.change_hotkey_button.clicked.connect(self.change_hotkey)
        central_layout.addWidget(self.change_hotkey_button)

        central_layout.addItem(QSpacerItem(
            0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding))

        dir_layout = QHBoxLayout()
        self.dir_name_edit = QLineEdit()
        dir_layout.addWidget(QLabel('Путь:'))
        dir_layout.addWidget(self.dir_name_edit)

        dir_btn = QPushButton('Обзор')
        dir_btn.clicked.connect(self.open_dir_dialog)
        dir_btn.setFixedSize(70, 25)

        dir_layout.addWidget(dir_btn)
        central_layout.addLayout(dir_layout)

        version_label = QLabel('ver. 1.1.0')
        version_label.setAlignment(Qt.AlignRight)
        central_layout.addWidget(version_label)

    def setup_tray_icon(self):
        self.tray_icon = TrayIcon(self, APP_ICON)
        self.tray_icon.show()

    def setup_screenshot_thread(self):
        self.screenshot_thread = ScreenshotThread()
        self.screenshot_thread.screenshot_saved_signal.connect(
            self.screenshot_saved)

    def setup_keyboard_shortcut(self):
        self.update_hotkey_label()
        self.register_hotkey()
        self.screenshot_worker = ScreenshotWorker()
        self.screenshot_worker.capture_screenshot_signal.connect(
            self.screenshot_thread.capture_screenshot)

    def update_hotkey_label(self):
        hotkey_text = (
            '1. Чтобы сделать скриншот экрана, нажмите {0}.\n'
            '2. Чтобы убрать программу в трей, нажмите на "✕".\n'
            '3. Чтобы назначить свою комбинацию клавиш для скриншота, нажмите на кнопку ниже:'
        ).format('+'.join(self.hotkey_combinations))

        self.hotkey_label.setText(hotkey_text)

    def register_hotkey(self):
        new_hotkey = '+'.join(self.hotkey_combinations)
        keyboard.add_hotkey(new_hotkey, self.capture_and_save_screenshot)

    def capture_and_save_screenshot(self):
        self.screenshot_worker.capture_screenshot()

    def screenshot_saved(self, screenshot_path):
        print(f'Screenshot saved at {screenshot_path}')

    def open_dir_dialog(self):
        dir_name = QFileDialog.getExistingDirectory(self, 'Выберите папку')
        if dir_name:
            path = Path(dir_name)
            self.dir_name_edit.setText(str(path))

    def change_hotkey(self):
        dialog = HotkeyChangeDialog(self)
        result = dialog.exec_()

        if result == QDialog.Accepted:
            new_hotkeys = dialog.get_new_hotkeys()
            # Фильтруем пустые строки
            self.hotkey_combinations = [key for key in new_hotkeys if key]
            self.update_hotkey_label()
            try:
                keyboard.unhook_all_hotkeys()
                self.register_hotkey()
            except Exception as e:
                QMessageBox.critical(
                    self, 'Ошибка', f'Не удалось назначить клавишу: {str(e)}, настройте другую комбинацию')


class TrayIcon(QSystemTrayIcon):
    def __init__(self, main_window, app_icon):
        super().__init__(main_window)
        self.main_window = main_window
        self.setIcon(QIcon(app_icon))

        show_action = QAction('☐   Открыть', main_window)
        hide_action = QAction('▼   Свернуть', main_window)
        quit_action = QAction('✕   Закрыть click click screen', main_window)

        show_action.triggered.connect(main_window.show)
        hide_action.triggered.connect(main_window.hide)
        quit_action.triggered.connect(QApplication.instance().quit)

        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.setContextMenu(tray_menu)
