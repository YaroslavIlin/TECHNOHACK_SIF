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
import numpy as np
from matplotlib.axes import Axes
#from ui_formation_and_fluid import Ui_MainWindow
from ui_MainWindow import Ui_MainWindow
from AddWell import AddWell
from AddPort import AddPort
from AddFracture import AddFracture
from utils import SimDict
from proxy_window import ProxyWindow


from scripts.canvas import MplCanvas         

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
        
        #self.ui.tabWidget.currentChanged.connect(self.get_parameters)
        self.ui.tabWidget.currentChanged.connect(self.restart_cmb_result)

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

        self.ui.le_simulnub.setText('0')

        
        
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

        self.ui.le_comment.textChanged.connect(lambda: self.get_comment_sim(self.simdict))
        self.ui.le_simulnub.textChanged.connect(lambda: self.get_num_sim(self.simdict))

        #Привязка кнопок на открытие дополнительных окон

        self.ui.btn_addwell.clicked.connect(self.open_addwell)
        self.ui.btn_addport.clicked.connect(self.open_addport)
        self.ui.btn_addfracture.clicked.connect(self.open_addfracture)
        self.ui.btn_downoladtimer.clicked.connect(self.proxy_window)


#Вкладка конфигурации
        self.canvas_config = MplCanvas(self, width=5, height=4, dpi=100)
        self.ui.graph_config.addWidget(self.canvas_config)
        self.ui.le_X_min.setText('-200')
        self.ui.le_X_max.setText('200')
        self.ui.le_Y_min.setText('-200')
        self.ui.le_Y_max.setText('200')
        self.restart_cmb_config()
        self.ui.le_X_min.textChanged.connect(self.update_domain_borders)
        self.ui.le_X_max.textChanged.connect(self.update_domain_borders)
        self.ui.le_Y_min.textChanged.connect(self.update_domain_borders)
        self.ui.le_Y_max.textChanged.connect(self.update_domain_borders)
        self.ui.cb_well.activated.connect(self.activated_cmb_well)
        self.ui.cb_port.activated.connect(self.activated_cmb_port)  
        self.ui.cb_SIF.activated.connect(self.activated_cmb_sif)
        
        #self.ui.btn_addfracture.clicked.connect(lambda: self.testplot(self.canvas, 'testplot'))
#Вкладка сетка
        self.ui.le_dt.setText('0.4')
        self.ui.le_t_start.setText('0')
        self.ui.le_t_end.setText('10')
        self.ui.le_dt.textChanged.connect(lambda: self.get_timestep_prop(self.simdict))
        self.ui.le_t_start.textChanged.connect(lambda: self.get_timestep_prop(self.simdict))
        self.ui.le_t_end.textChanged.connect(lambda: self.get_timestep_prop(self.simdict))
        
#Вкладка расчёта
        self.ui.sldr_graph.valueChanged.connect(self.test_slider)

        self.ui.cmb_graphtype.addItem('p^p(t)')
        self.ui.cmb_graphtype.addItem('p^w(t)')
        self.ui.cmb_graphtype.addItem('Qf(t)')
        self.ui.cmb_graphtype.addItem('Qinc(t)')
        self.ui.cmb_graphtype.addItem('w(x)')
        self.ui.cmb_graphtype.addItem('p(x)')

        self.restart_cmb_result()

        self.ui.cmb_graphtype.activated.connect(self.changed_cmb_graphtype)
        self.ui.cmb_graphtype.activated.connect(self.restart_cmb_result)
        self.ui.cmb_numwell.activated.connect(self.restart_cmb_port_result)
        #self.ui.graph_result_1.addWidget(self.canvas)
        #self.ui.btn_graph_calc.clicked.connect(lambda: self.testplot(self.canvas, 'test'))

        # Вкладка "Сетка"
        self.ui.le_cell_size.setText('200')
        self.ui.le_SIHF.setText('2')
        self.ui.le_fracture.setText('5')
        self.ui.le_SIHF_min.setText('20')
        self.ui.le_SIHF_max.setText('200')
        self.ui.le_well_min.setText('20')
        self.ui.le_well_max.setText('200')
        
        self.ui.le_cell_size.textChanged.connect(self.get_mesh_properties)
        self.ui.le_SIHF.textChanged.connect(self.get_mesh_properties)
        self.ui.le_fracture.textChanged.connect(self.get_mesh_properties)
        self.ui.le_SIHF_min.textChanged.connect(self.get_mesh_properties)
        self.ui.le_SIHF_max.textChanged.connect(self.get_mesh_properties)
        self.ui.le_well_min.textChanged.connect(self.get_mesh_properties)
        self.ui.le_well_max.textChanged.connect(self.get_mesh_properties)   
        
        # Заполнить hardcode поля
        if True:
            self.simdict.set_algorithm_settings()
            self.simdict.set_elasticity_problem_settings()
            self.simdict.set_wellbore_modeling_properties()
            self.get_parameters()
            self.get_mesh_properties()
            self.update_domain_borders()
            
                    
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
        
        
    def get_mesh_properties(self):
        h_def = float(self.ui.le_cell_size.text())
        h_f   = float(self.ui.le_SIHF.text())
        h_p   = float(self.ui.le_fracture.text())
        dist_min_frac = float(self.ui.le_SIHF_min.text())
        dist_max_frac = float(self.ui.le_SIHF_max.text())
        dist_min_prod = float(self.ui.le_well_min.text())
        dist_max_prod = float(self.ui.le_well_max.text())
        self.simdict.set_mesh_properties(
            h_frac        = h_f,
            h_default     = h_def,
            h_prod        = h_p,
            dist_min_frac = dist_min_frac,
            dist_max_frac = dist_max_frac,
            dist_min_prod = dist_min_prod,
            dist_max_prod = dist_max_prod
        )
        self.simdict.write_data()
    

    def update_domain_borders(self):
        xmin = float(self.ui.le_X_min.text())
        xmax = float(self.ui.le_X_max.text())
        ymin = float(self.ui.le_Y_min.text())
        ymax = float(self.ui.le_Y_max.text())
        self.simdict.set_domain_boundaries(xmin, xmax, ymin, ymax)
        # @todo: delete later
        self.simdict.write_data()
        
        self.simdict._plot(self.canvas_config)
        self.canvas_config.draw()

    
    def open_addwell(self):
        self.w = AddWell(self.simdict, self.simdict._nwells)
        self.w.exec()
        self.restart_cmb_config()
        self.update_domain_borders()
        
        
    def open_addport(self):
        self.w = AddPort(self.simdict, self.simdict._nwells)
        self.w.exec()
        self.restart_cmb_config()
        self.update_domain_borders()


    def open_addfracture(self):
        self.w = AddFracture(self.simdict, self.simdict._nwells)
        self.w.exec()
        self.restart_cmb_config()
        self.update_domain_borders()
        
        
    def proxy_window(self):
        self.proxy = ProxyWindow(self.simdict, self.simdict._nwells)
        self.proxy.show()


    def restart_cmb_config(self):
        self.ui.cb_well.clear()
        self.ui.cb_port.clear()
        self.ui.cb_SIF.clear()
        if self.simdict._nwells == 0:
            self.ui.cb_well.setEnabled(False)
            self.ui.cb_port.setEnabled(False)
            self.ui.cb_SIF.setEnabled(False)
        else:
            self.ui.cb_well.setEnabled(True)
            for i in range(self.simdict._nwells):
                self.ui.cb_well.addItem(f"{i} ({self.simdict._welldata['wells'][f'well{i}']['name']})")
                if self.simdict._welldata['wells'][f'well{i}']['nPorts'] != 0:
                    self.ui.cb_port.setEnabled(True)
            self.activated_cmb_well()
        if self.simdict._nfracs != 0:
            self.ui.cb_SIF.setEnabled(True)
            

    def activated_cmb_sif(self):
        xleft, yleft, xright, yright = self.simdict._sim_dict['meshProperties']['fractureGeometry']['fractures'][f'fracture{self.ui.cb_SIF.currentIndex()}']['coordinates']
        self.ui.lbl_xleftfracture.setText(f'X: = {round(xleft, 1)} м')
        self.ui.lbl_yleftfracture.setText(f'Y: = {round(yleft, 1)} м')
        self.ui.lbl_xrightfracture.setText(f'X: = {round(xright,1)} м')
        self.ui.lbl_yrightfracture.setText(f'Y: = {round(yright,1)} м')

    def activated_cmb_port(self):
        #self.ui.cb_SIF.clear()
        flag = False
        for i in range (self.simdict._sim_dict['meshProperties']['fractureGeometry']['nFractures']):
            self.ui.cb_SIF.addItem(f'{i}')
            flag = True
        if flag:
            self.activated_cmb_sif()
        x, y = self.simdict._welldata['wells'][f'well{self.ui.cb_well.currentIndex()}']['ports'][f'port{self.ui.cb_port.currentIndex()}']['coordinates']
        xleftwing, yleftwing, xrightwing, yrightwing = self.simdict._welldata['wells'][f'well{self.ui.cb_well.currentIndex()}']['ports'][f'port{self.ui.cb_port.currentIndex()}']['initialFracture']['coordinates']
        kf = self.simdict._welldata['wells'][f'well{self.ui.cb_well.currentIndex()}']['ports'][f'port{self.ui.cb_port.currentIndex()}']['initialFracture']['kf']
        wf = self.simdict._welldata['wells'][f'well{self.ui.cb_well.currentIndex()}']['ports'][f'port{self.ui.cb_port.currentIndex()}']['initialFracture']['wf']
        self.ui.lbl_xcoordport.setText(f'X: = {round(x, 1)} м')
        self.ui.lbl_ycoordport.setText(f'Y: = {round(y, 1)} м')
        leftwing = abs(x - xleftwing)
        rightwing = abs(x - xrightwing)
        self.ui.lbl_leftwingport.setText(f'Левое крыло: {round(leftwing, 3)} м')
        self.ui.lbl_rightwingport.setText(f'Правое крыло: {round(rightwing, 3)} м')
        kf = kf / 9.869233e-13
        wf = wf / 1.0e-3
        self.ui.lbl_kfport.setText(f'kf:= {round(kf, 3)} Д')
        self.ui.lbl_wport.setText(f'w:= {round(wf, 3)} мм')

    def activated_cmb_well(self):
        self.ui.cb_port.clear()
        flag = False
        for i in range(self.simdict._welldata['wells'][f'well{self.ui.cb_well.currentIndex()}']['nPorts']):
            self.ui.cb_port.addItem(f"{i}")
            flag = True
        if flag:
            self.activated_cmb_port()
        if self.simdict._welldata['wells'][f'well{self.ui.cb_well.currentIndex()}']['geometryType'] == "horizontal":
            self.ui.lbl_typegeo.setText("Горизонтальная")
        elif self.simdict._welldata['wells'][f'well{self.ui.cb_well.currentIndex()}']['geometryType'] == "vertical":
            self.ui.lbl_typegeo.setText("Вертикальная")
        xbeg, ybeg, xend, yend = self.simdict._welldata['wells'][f'well{self.ui.cb_well.currentIndex()}']['coordinates']
        self.ui.lbl_xbeginwell.setText(f"X: = {round(xbeg, 1)} м")
        self.ui.lbl_ybeginwell.setText(f"Y: = {round(ybeg, 1)} м")
        self.ui.lbl_xendwell.setText(f"X: = {round(xend, 1)} м")
        self.ui.lbl_yendwell.setText(f"Y: = {round(yend, 1)} м")
        self.ui.lbl_nports.setText(f"N: = {self.simdict._welldata['wells'][f'well{self.ui.cb_well.currentIndex()}']['nPorts']}")
        #if self.simdict._welldata['wells'][f'well{self.ui.cb_well.currentIndex()}']['geometryType']
    def get_timestep_prop(self, simdict: SimDict):
        dt = float(self.ui.le_dt.text())
        t_start = float(self.ui.le_t_start.text())
        t_end = float(self.ui.le_t_end.text())
        simdict.set_timestep_properties(dt, t_start, t_end)
        self.simdict.write_data()

    def get_num_sim(self, simdict: SimDict):
        simnum = int(self.ui.le_simulnub.text())
        self.simdict.set_simID(simnum)
        self.simdict.write_data()
    
    def get_comment_sim(self, simdict: SimDict):
        simcomment = self.ui.le_comment.text()
        self.simdict.set_simComment(simcomment)
        self.simdict.write_data()

    def changed_cmb_graphtype(self):
        if self.ui.cmb_graphtype.currentIndex() <= 3:
            self.ui.lbl_numwellorfrac.setText('№ скв.')
            self.ui.lbl_numportresult.show()
            self.ui.cmb_numport.show()
        else:
            self.ui.lbl_numwellorfrac.setText('№ трещ.')
            self.ui.lbl_numportresult.hide()
            self.ui.cmb_numport.hide()

    def restart_cmb_result(self):
        self.ui.cmb_numwell.clear()
        self.ui.cmb_numport.clear()
        if self.ui.cmb_numport.isVisible():
            if self.simdict._nwells == 0:
                self.ui.cmb_numwell.setEnabled(False)
                self.ui.cmb_numport.setEnabled(False)
            else:
                self.ui.cmb_numwell.setEnabled(True)
                for i in range(self.simdict._nwells):
                    self.ui.cmb_numwell.addItem(f"{i}")
                self.restart_cmb_port_result()
                    
        else:
            if self.simdict._nfracs == 0:
                self.ui.cmb_numwell.setEnabled(False)
            else:
                self.ui.cmb_numwell.setEnabled(True)
                for i in range(self.simdict._nfracs):
                    self.ui.cmb_numwell.addItem(f"{i}")

    def restart_cmb_port_result (self):
        self.ui.cmb_numport.clear()
        if self.ui.cmb_numport.isVisible():
            for i in range(self.simdict._welldata['wells'][f'well{self.ui.cmb_numwell.currentIndex()}']['nPorts']):
                self.ui.cmb_numport.addItem(f"{i}")
                self.ui.cmb_numport.setEnabled(True)
    
    def test_slider(self):
        self.ui.lbl_t.setText(f'T: = {self.ui.sldr_graph.value()}')
        print(self.ui.sldr_graph.value())
        
    
    def testplot(self, cnv: MplCanvas, s: str):
        x = np.random.rand(10)
        y = np.random.rand(10)
        cnv.axes.cla()
        cnv.axes.plot(x, y, label=s)
        cnv.axes.legend()
        cnv.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec()