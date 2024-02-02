from ui_AddWell import Ui_Dialog
import sys
from PySide6.QtWidgets import QApplication, QDialog, QComboBox

from utils import SimDict

class AddWell(QDialog):
    def __init__(self, simdict: SimDict, num=0):
        super(AddWell, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        # self.simdict = simdict

        self.ui.le_namewell.setText(f'скв. №{num}') 
        
        # self.ui.cmb_typegeo.addItem('')
        self.ui.cmb_typegeo.addItem('Горизонтальная')
        self.ui.cmb_typegeo.addItem('Вертикальная')

        # self.ui.cmb_typewell.addItem('')
        self.ui.cmb_typewell.addItem('Только добыча')
        self.ui.cmb_typewell.addItem('Добыча и закачка')
        self.ui.cmb_typewell.addItem('Только закачка')
        
        self.ui.cmb_typegeo.setCurrentIndex(0)
        self.ui.cmb_typewell.setCurrentIndex(0)
 
        self.ui.cmb_typegeo.activated.connect(self.changed_cmb_typegeo)
        
        self.ui.btn_accept.clicked.connect(lambda: self.add_well_to_simdict(simdict))
        
    
    def changed_cmb_typegeo(self, index):
        if(self.ui.cmb_typegeo.currentIndex() == 1):
            self.ui.end.hide()
            self.ui.xend.hide()
            self.ui.yend.hide()
            self.ui.le_xend.hide()
            self.ui.le_yend.hide()
        else:
            self.ui.end.show()
            self.ui.xend.show()
            self.ui.yend.show()
            self.ui.le_xend.show()
            self.ui.le_yend.show()
    
    
    def add_well_to_simdict(self, simdict: SimDict):
        if self.ui.cmb_typegeo.currentIndex() == 0: # 'Горизонтальная'
            geom_type = 'horizontal'
        else:   # 'Вертикальная'
            geom_type = 'vertical'
        
        if self.ui.cmb_typewell.currentIndex() == 0: # 'Только добыча'
            w_type = 'production'
        else:   # 'Добыча и закачка' или 'Только закачка'
            w_type = 'injection'
                    
        start = [
            float(self.ui.le_xbegin.text()),
            float(self.ui.le_ybegin.text()),
        ]
        end = [
            float(self.ui.le_xend.text()),
            float(self.ui.le_yend.text()),
        ]
        name = self.ui.le_namewell.text()
        if name == '':
            name = None
         
        # hardcode
        is_hf = True
        
        simdict.add_well(
            geometry_type = geom_type,
            well_type     = w_type,
            is_initial_hf = is_hf,
            start_point   = start,
            end_point     = end,
            name          = name
        )
        
        # @todo: delete this line later
        simdict.write_data()
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AddWell()
    window.show()
    sys.exit(app.exec())
