from ui_AddWell import Ui_Dialog
import sys
from PySide6.QtWidgets import QApplication, QDialog, QComboBox

class AddWell(QDialog):
    def __init__(self, num=0):
        super(AddWell, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.le_namewell.setText(f'скв. №{num}') 
        
        self.ui.cmb_typegeo.addItem('')
        self.ui.cmb_typegeo.addItem('Горизонтальная')
        self.ui.cmb_typegeo.addItem('Вертикальная')

        self.ui.cmb_typewell.addItem('')
        self.ui.cmb_typewell.addItem('Только добыча')
        self.ui.cmb_typewell.addItem('Добыча и закачка')
        
        self.ui.cmb_typegeo.setCurrentIndex(0)
        self.ui.cmb_typewell.setCurrentIndex(0)
 
        self.ui.cmb_typegeo.activated.connect(self.changed_cmb_typegeo)
        
        
 
    def changed_cmb_typegeo(self, index):
        if(self.ui.cmb_typegeo.currentIndex() == 2):
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AddWell()
    window.show()
    sys.exit(app.exec())
