import sys
from typing import Optional
from PySide6.QtCore import Qt
import pandas as pd
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QTableWidget,
    QTableWidgetItem
    )
from PySide6.QtUiTools import QUiLoader

class TableWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 700, 500)
        self.setWindowTitle("Предпросмотр входных данных")
        table = Table(self)

class Table(QTableWidget):
    def __init__(self, widget):
        super().__init__(widget)
        self.setGeometry(0, 0, 700, 500)
        file_path = "src/sched_206.xlsx"
        df = pd.read_excel(file_path)
        row_count = len(df.index)
        col_count = len(df.columns)
        self.setRowCount(row_count)
        self.setColumnCount(col_count)

        self.setHorizontalHeaderLabels(df.columns)
        for i in range(row_count):
            for j in range(col_count):
                self.setItem(i, j, ElementOfTable(str(df.iloc[i, j])))
        self.resizeColumnsToContents()

class ElementOfTable(QTableWidgetItem):
    def __init__(self, element):
        super().__init__(element)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    table_widget = TableWidget()
    table_widget.show()
    app.exec()
