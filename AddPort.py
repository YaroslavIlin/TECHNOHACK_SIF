from TECHNOHACK_SIF.ui_AddPort import Ui_Dialog
import sys
from PySide6.QtWidgets import QApplication, QDialog

from utils import SimDict

class AddPort(QDialog):
    def __init__(self, simdict: SimDict, num=0):
        super(AddPort, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        #self.ui.cmb_scheme.addItem('')
        self.ui.cmb_scheme.addItem('Одиночный')
        self.ui.cmb_scheme.addItem('По краям отрезков')
        self.ui.cmb_scheme.addItem('По центрам отрезков')
        for i in range(num):
            self.ui.cmb_numwell.addItem(f'{i}')
        
        self.ui.cmb_scheme.setCurrentIndex(0)
 
        self.ui.cmb_scheme.activated.connect(self.changed_cmb_scheme)
        
        
 
    def changed_cmb_scheme(self, index):
        if(self.ui.cmb_scheme.currentIndex() != 0):
            self.ui.param_x.hide()
            self.ui.param_y.hide()
            self.ui.le_y.hide()
            self.ui.nports.setText('Количество портов:')
        else:
            self.ui.param_x.show()
            self.ui.param_y.show()
            self.ui.le_y.show()
            self.ui.nports.setText('Координаты порта:')

    def add_ports_to_simdict(self, simdict: SimDict):
        num_well = int(self.ui.cmb_numwell.currentText())
        len_wing_left = float(self.ui.le_lenwingleft.text())
        len_wing_right = float(self.ui.le_lenwingright.text())
        kf = float(self.ui.le_translatability.text())
        wf = float(self.ui.le_crackfracture.text())
        if(self.ui.cmb_scheme.currentIndex == 0):
            point = [float(self.ui.le_x.text()), float(self.ui.le_y.text())]
        else:
            nports = int(self.ui.le_x.text())


    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AddPort()
    window.show()
    sys.exit(app.exec())