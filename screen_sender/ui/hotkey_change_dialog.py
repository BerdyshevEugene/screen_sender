from PyQt5.QtWidgets import *


class HotkeyChangeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Изменить комбинацию для скриншота')

        layout = QVBoxLayout(self)
        layout.addWidget(
            QLabel('Введите новую комбинацию клавиш для скриншота:'))

        self.input_widgets = []

        for i in range(3):
            input_widget = QLineEdit()
            self.input_widgets.append(input_widget)
            layout.addWidget(input_widget)

        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(button_box)

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

    def get_new_hotkeys(self):
        return [input_widget.text() for input_widget in self.input_widgets]
