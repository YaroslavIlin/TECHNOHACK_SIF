from ui_AddFracture import Ui_Dialog
import sys
from PySide6.QtWidgets import QApplication, QDialog, QComboBox

from utils import SimDict

class AddFracture(QDialog):
    def __init__(self, simdict: SimDict, num=0):
        super(AddFracture, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        #n_ports = simdict._welldata['wells'][f'well{well_id}']['nPorts']

        #self.ui.cmb_scheme.addItem('')
        self.ui.cmb_scheme.addItem('Одиночный')
        self.ui.cmb_scheme.addItem('Все порты одной скважины')
        self.ui.cmb_scheme.addItem('Все порты всех скважин')
        if(num != 0):
            for i in range(num):
                self.ui.cmb_numwell.addItem(f'{i}')
            self.changed_cmb_numwell(simdict)
        else:
            self.ui.cmb_numport.setEnabled(False)
            self.ui.cmb_numwell.setEnabled(False)

        
        
        self.ui.cmb_scheme.setCurrentIndex(0)

        self.ui.cmb_scheme.activated.connect(self.changed_cmb_scheme)

        self.ui.cmb_numwell.activated.connect(lambda: self.changed_cmb_numwell(simdict))

        #self.ui.btn_access.clicked.connect(self.add_fracture_to_simdict)

        self.ui.btn_decline.clicked.connect(self.click_decline)
 
    def changed_cmb_scheme(self):
        if(self.ui.cmb_scheme.currentIndex() == 2):
            self.ui.numport.hide()
            self.ui.cmb_numport.hide()
        elif (self.ui.cmb_scheme.currentIndex() == 3):
            self.ui.numport.hide()
            self.ui.cmb_numport.hide()
            self.ui.numwell.hide()
            self.ui.cmb_numwell.hide()
        else:
            self.ui.cmb_numport.show()
            self.ui.cmb_numwell.show()
            self.ui.numwell.show()
            self.ui.numport.show()

    def add_fracture_to_simdict(self, simdict: SimDict):
        if(self.ui.cmb_scheme.currentIndex() <= 1):
            num_well = int(self.ui.cmb_numwell.currentText())
            if(self.ui.cmb_scheme.currentIndex() == 0):
                num_port = int(self.ui.cmb_numport.currentText())
        lenS = [float(self.ui.le_lenleft.text()), float(self.ui.le_lenright.text())]

    def changed_cmb_numwell(self, simdict: SimDict):
            self.ui.cmb_numport.clear()
            self.ui.cmb_numport.setEnabled(True)
            n_ports = simdict._welldata['wells'][f'well{int(self.ui.cmb_numwell.currentText())}']['nPorts']
            for i in range (n_ports):
                self.ui.cmb_numport.addItem(f'{i}')

    def click_decline(self):
        self.close()

                

        
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AddFracture()
    window.show()
    sys.exit(app.exec())