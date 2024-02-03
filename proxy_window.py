from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QFileDialog
)
import pandas as pd

class ProxyWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 888, 555)
        self.setWindowTitle("Предпросмотр входных данных")

        self.table_widget =  QTableWidget(self)
        self.table_widget.setGeometry(5, 5, 620, 545)

        self.explore = QPushButton(self)
        self.explore.setObjectName(u"explore")
        self.explore.setGeometry(640, 10, 240, 28)
        self.explore.setText("Обзор...")
        self.explore.clicked.connect(self.open_schedule)

        self.ok = QPushButton(self)
        self.ok.setObjectName(u"ok")
        self.ok.setGeometry(640, 90, 240, 28)
        self.ok.setText("OK")
        self.ok.clicked.connect(self.send_data)

        # table = Table(self, file_path)
    
    def open_schedule(self):
        filter = "Excel files (*.xlsx *.xls *.csv)"
        path_to_file, _ = QFileDialog.getOpenFileName(self,
                                                      "Открыть файл с расписанием закачки",
                                                      "",
                                                      filter,
                                                      filter)
        
        if path_to_file:
            self.df = pd.read_excel(path_to_file)
            self.row_count = len(self.df.index)
            self.col_count = len(self.df.columns)
            self.table_widget.setRowCount(self.row_count)
            self.table_widget.setColumnCount(self.col_count)
            self.table_widget.setHorizontalHeaderLabels(self.df.columns)

            for i in range(self.row_count):
                for j in range(self.col_count):
                    self.table_widget.setItem(i, j, ElementOfTable(str(self.df.iloc[i, j])))
    
    def send_data(self):
        self.t = self.df.iloc[:,0].to_list()
        self.Q = self.df.iloc[:,1].to_list()
        self.dict_to_json = {"t": self.t,
                             "Q": self.Q}
        print(self.t)
        print(self.Q)
        print(type(self.t))
        print("OK")
        print(self.dict_to_json)

class ElementOfTable(QTableWidgetItem):

    def __init__(self, element):
        super().__init__(element)
