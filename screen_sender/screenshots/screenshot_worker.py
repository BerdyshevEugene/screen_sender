import datetime
import time
import os

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PIL import ImageGrab


class ScreenshotWorker(QObject):
    capture_screenshot_signal = pyqtSignal()

    @pyqtSlot()
    def capture_screenshot(self):
        self.capture_screenshot_signal.emit()


class ScreenshotThread(QThread):
    screenshot_saved_signal = pyqtSignal(str)

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
