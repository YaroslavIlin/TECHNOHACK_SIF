from ui_AddPort import Ui_Dialog
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

        self.ui.btn_decline.clicked.connect(self.click_decline)
        
        self.ui.btn_access.clicked.connect(lambda: self.add_ports_to_simdict(simdict))
        
 
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
        w_id = int(self.ui.cmb_numwell.currentText())
        len_wing_left  = float(self.ui.le_lenwingleft.text())
        len_wing_right = float(self.ui.le_lenwingright.text())
        initfrac = [len_wing_left, len_wing_right]
        kf = 9.869233e-13*float(self.ui.le_translatability.text())
        wf = 1.0e-3*float(self.ui.le_crackfracture.text())
        
        if self.ui.cmb_scheme.currentIndex() == 0:   # 'Одиночный'
            point = [float(self.ui.le_x.text()), float(self.ui.le_y.text())]
        else:
            nports = int(self.ui.le_x.text())
        
        if self.ui.cmb_scheme.currentIndex() == 0:   # 'Одиночный'
            simdict.add_port_to_well(
                well_id = w_id,
                port_point = point
            )
            # last added port index
            p_id = simdict._welldata['wells'][f'well{w_id}']['nPorts'] - 1
            simdict.set_initial_fracture(w_id, p_id, initfrac, kf, wf)
        else:
            if self.ui.cmb_scheme.currentIndex() == 1:    # 'По краям отрезков'
                simdict.add_ports_to_well_segment_borders(
                    well_id = w_id,
                    n_ports = nports
                )
            else:   # 'По центрам отрезков'
                simdict.add_ports_to_well_segment_centers(
                    well_id = w_id,
                    n_ports = nports
                )
            simdict.set_initial_fractures_all_ports_on_well(
                w_id, initfrac, kf, wf
            )
            
        # @todo: delete this line later
        simdict.write_data()
        self.close()

    def click_decline(self):
        self.close()
    
'''
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AddPort()
    window.show()
    sys.exit(app.exec())
'''