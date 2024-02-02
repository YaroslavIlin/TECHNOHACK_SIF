
import sys
from typing import Optional
from PySide6.QtCore import QFile, QSize, Qt
from PySide6.QtGui import QAction, QPalette, QColor
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QLineEdit,
    QVBoxLayout,
    QMessageBox,
    QWidget,
    QTabWidget
)
#from ui_formation_and_fluid import Ui_MainWindow
from ui_MainWindow import Ui_MainWindow
from AddWell import AddWell
from AddPort import AddPort
from utils import SimDict

class Parameters():
    data_E      = 0.0
    data_nu     = 0.0
    data_alphaE = 0.0
    data_alphaF = 0.0
    data_kr     = 0.0
    data_poro   = 0.0
    data_M      = 0.0
    data_mu     = 0.0
    data_sMin   = 0.0
    data_sMax   = 0.0
    data_p0     = 0.0
    
    def print_console(self):
        print(f'E      = {self.data_E}')
        print(f'nu     = {self.data_nu}')
        print(f'alphaE = {self.data_alphaE}')
        print(f'alphaF = {self.data_alphaF}')
        print(f'kr     = {self.data_kr}')
        print(f'poro   = {self.data_poro}')
        print(f'M      = {self.data_M}')
        print(f'mu     = {self.data_mu}')
        print(f'sMin   = {self.data_sMin}')
        print(f'sMax   = {self.data_sMax}')
        print(f'p0     = {self.data_p0}')
        

class MainWindow(QMainWindow):
    param = Parameters()
    
    simdict = SimDict()
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # default params
        self.ui.le_E.setText('20')
        self.ui.le_nu.setText('0.22')
        self.ui.le_alphaE.setText('0')
        self.ui.le_alphaF.setText('0')
        self.ui.le_kr.setText('10')
        self.ui.le_poro.setText('0.15')
        self.ui.le_M.setText('10')
        self.ui.le_mu.setText('0.001')
        self.ui.le_sMin.setText('25')
        self.ui.le_sMax.setText('45')
        self.ui.le_p0.setText('20')
        
        #При изменениии числа в line edit автоматически заполняет все параметры
        self.ui.le_E.textChanged.connect(self.get_parameters)
        self.ui.le_nu.textChanged.connect(self.get_parameters)
        self.ui.le_alphaE.textChanged.connect(self.get_parameters)
        self.ui.le_alphaF.textChanged.connect(self.get_parameters)
        self.ui.le_kr.textChanged.connect(self.get_parameters)
        self.ui.le_poro.textChanged.connect(self.get_parameters)
        self.ui.le_M.textChanged.connect(self.get_parameters)
        self.ui.le_mu.textChanged.connect(self.get_parameters)
        self.ui.le_sMin.textChanged.connect(self.get_parameters)
        self.ui.le_sMax.textChanged.connect(self.get_parameters)
        self.ui.le_p0.textChanged.connect(self.get_parameters)

        #Привязка кнопок на открытие дополнительных окон

        self.ui.btn_addwell.clicked.connect(self.open_addwell)
        self.ui.btn_addport.clicked.connect(self.open_addport)
        
    def get_parameters(self):
        #Преобразует текст из line edit в переменные класса параметров
        #Также автоматически преобразует в СИ
        self.param.data_E      = 1.0e9*float(self.ui.le_E.text())
        self.param.data_nu     = float(self.ui.le_nu.text())
        self.param.data_alphaE = float(self.ui.le_alphaE.text())
        self.param.data_alphaF = float(self.ui.le_alphaF.text())
        self.param.data_kr     = 9.869233e-16*float(self.ui.le_kr.text())
        self.param.data_poro   = float(self.ui.le_poro.text())
        self.param.data_M      = 1.0e9*float(self.ui.le_M.text())
        self.param.data_mu     = float(self.ui.le_mu.text())
        self.param.data_sMin   = 1.0e6*float(self.ui.le_sMin.text())
        self.param.data_sMax   = 1.0e6*float(self.ui.le_sMax.text())
        self.param.data_p0     = 1.0e6*float(self.ui.le_p0.text())
        
        self.simdict.set_reservoir_properties(
            #Создание списка из переменных
            self.param.data_E,
            self.param.data_nu,
            self.param.data_alphaE,
            self.param.data_alphaF,
            self.param.data_kr,
            self.param.data_poro,
            self.param.data_M,
            self.param.data_mu,
            self.param.data_sMin,
            self.param.data_sMax,
            self.param.data_p0
        )
        self.simdict.write_data()
    def open_addwell(self):
        self.w = AddWell(self.simdict, self.simdict._nwells)
        self.w.show()
    def open_addport(self):
        self.w = AddPort(self.simdict, self.simdict._nwells)
        self.w.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec()
    