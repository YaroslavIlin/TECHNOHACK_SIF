from typing import Optional
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QFileDialog, QApplication
import sys

class FileWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 300, 300)
        self.setWindowTitle("Name")
        w = QFileDialog.getOpenFileName(self)
        '''window = Window(self)
        window.exec()'''

class Window(QFileDialog):
    def __init__(self, widget):
        super().__init__(widget)

app = QApplication(sys.argv)
file_widget = FileWidget()
file_widget.show()
app.exec()