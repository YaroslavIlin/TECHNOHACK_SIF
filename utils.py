import sys
import os
import json
import numpy as np

from math import sqrt
from itertools import chain

_repository_dir = os.path.abspath(os.getcwd())
sys.path.append(_repository_dir)


# coo = [xmin, ymin, xmax, ymax]
def _is_point_in_rectangle(p: list, coo: list):
    return coo[0] < p[0] and p[0] < coo[2] and coo[1] < p[1] and p[1] < coo[3]

def _is_segment_in_rectangle(seg: list, coo: list):
    return _is_point_in_rectangle([seg[0], seg[1]], coo) and _is_point_in_rectangle([seg[2], seg[3]], coo)

# ports in the segments centers
def _get_ports_coords_centers(well_coord, n_ports):
    xmin, ymin, xmax, ymax = well_coord
    dx = (xmax-xmin) / n_ports
    dy = (ymax-ymin) / n_ports
    return [[xmin + dx/2 + dx * ip, ymin + dy/2 + dy * ip] for ip in range(n_ports)]

# ports in the segments borders
def _get_ports_coords_borders(well_coord, n_ports):
    xmin, ymin, xmax, ymax = well_coord
    if n_ports == 1:
        return [[(xmax + xmin) / 2, (ymax + ymin) / 2]]
    dx = (xmax-xmin) / (n_ports - 1)
    dy = (ymax-ymin) / (n_ports - 1)
    return [[xmin + dx*ip, ymin + dy*ip] for ip in range(n_ports)]

def _is_point_in_segment(point: list, seg_start: list, seg_end: list):
    [x1, y1], [x2, y2], [x3, y3] = seg_start, seg_end, point
    return abs(sqrt((x3 - x1)**2 + (y3 - y1)**2)
               + sqrt((x3 - x2)**2 + (y3 - y2)**2)
               - sqrt((x2 - x1)**2 + (y2 - y1)**2)) < 1.0e-6

def _fracture_from_wings(point: list, wings: list):
    xleft, yleft, xright, yright = point[0] - wings[0], point[1], point[0] + wings[1], point[1]
    return [xleft, yleft, xright, yright]

# ports to the nearest well point according to given coords
def _fix_ports_coordinates(well_coord, port_coords, iw):
    xmin, ymin, xmax, ymax = well_coord
    A = xmax - xmin;  B = ymax - ymin # guide vector
    ans, error_message = [], ''
    for i in range(len(port_coords)):
        # read given coordinate
        xp, yp = port_coords[i]
        # correct given coordinate and transfer it to well line
        if A**2 + B**2 > 0.0:
            t = ((xp - xmin)*A + (yp - ymin)*B) / (A**2 + B**2)
        else:
            t = 0.0
        if t < 0.0 or t > 1.0:
            error_message = f'\tНа скважине №{iw} не удалось скорректировать положения портов, задайте их точнее\n'
        x_cor = xmin + A*t
        y_cor = ymin + B*t
        ans.append([x_cor, y_cor])
    return ans, error_message



class SimDict:
    def __init__(self):
        self._sim_dict = dict()
        self._welldata = dict()
        
        self._sim_dict['simID'] = 0
        
        self._fracs_on_wells = dict()
        
        self._sim_dict['inputVersion'] = '1.0'
        
        self._welldata['wells'] = dict()
        self._nwells = 0
        self._sim_dict['meshProperties'] = dict()
        self._sim_dict['meshProperties']['fractureGeometry'] = dict()
        self._sim_dict['meshProperties']['fractureGeometry']['fractures'] = dict()
        self._nfracs = 0
        self._sim_dict['gmshProperties'] = dict()
        self._sim_dict['settingsProperties'] = dict()
        self._sim_dict['timestepProperties'] = dict()
        self._sim_dict['reservoirProperties'] = dict()
        self._sim_dict['elasticityProperties'] = dict()
        self._sim_dict['wellmoduleProperties'] = dict()
        
        self._sim_dict['twoPhase'] = dict()
        
        self._sim_dict['filtrationProperties'] = dict()
        self._sim_dict['lubricationProperties'] = dict()
        
        # Default field value if corresponding method is never called 
        # todo: add dictionary with all required fields and check if they are filled or not yet
        self._sim_dict['simComment'] = ''
    
    
    def set_simID(self, simID):
        self._sim_dict['simID'] = simID
        
        self._sim_dict['simDir'] = _repository_dir + f'/simulations/simID{simID}'
        self._sim_dict['meshProperties']['meshPath'] = _repository_dir + f'/simulations/simID{simID}/mesh.vtk'
    
    
    def set_simComment(self, simComment):
        try:            
            self._sim_dict['simComment'] = str(simComment)
        except:
            self._sim_dict['simComment'] = ''
            
    
    def set_domain_boundaries(self, xmin, xmax, ymin, ymax):
        self._sim_dict['meshProperties']['xmin'] = float(xmin)
        self._sim_dict['meshProperties']['xmax'] = float(xmax)
        self._sim_dict['meshProperties']['ymin'] = float(ymin)
        self._sim_dict['meshProperties']['ymax'] = float(ymax)
        self._sim_dict['meshProperties']['zmin'] = -5.0
        self._sim_dict['meshProperties']['zmax'] = 5.0
    
    
    def set_mesh_properties(self, h_frac, h_default, h_prod,
                            dist_min_frac, dist_max_frac,
                            dist_min_prod, dist_max_prod):
        params = [h_frac, h_default, h_prod, dist_min_frac, dist_max_frac, dist_min_prod, dist_max_prod]
        dict_keys = ['hFrac', 'hDefault', 'hProd', 'distMinFrac', 'distMaxFrac', 'distMinProd', 'distMaxProd']
        
        for key, val in zip(dict_keys, params):
            self._sim_dict['gmshProperties'][key] = float(val)
    
    
    # hardcode
    def set_algorithm_settings(self):
        self._sim_dict['settingsProperties']['domainType']                   = 'full'
        self._sim_dict['settingsProperties']['isDebug']                      = True
        self._sim_dict['settingsProperties']['isNonOrthogonalCorrection']    = True
        self._sim_dict['settingsProperties']['lubricationTolerance']         = 1.0e-5
        self._sim_dict['settingsProperties']['linearSolver']                 = 'inner_ilu2'
        self._sim_dict['settingsProperties']['optionsDatabasePath']          = './options/database.xml'
        self._sim_dict['settingsProperties']['fractureMaxWidth']             = 3.0e-3
        self._sim_dict['settingsProperties']['outputSaveRate']               = 1 
        self._sim_dict['lubricationProperties']['LUBRICATION_FLUX_LIMITER']  = 1.0e-13
        self._sim_dict['lubricationProperties']['LUBRICATION_CUT_OFF']       = 1.0e-14
        self._sim_dict['timestepProperties']['outputSaveRate']               = 1
    
    
    def set_timestep_properties(self, dt, t_start, t_end):
        self._sim_dict['timestepProperties']['dt']        = float(dt)
        self._sim_dict['timestepProperties']['startTime'] = float(t_start)
        self._sim_dict['timestepProperties']['endTime']   = float(t_end)
    
    
    def set_reservoir_properties(self, E, nu, alpha_elast, alpha_filtr, kr, phi, M,
                                 mu, sigma_min, sigma_max, pres_init):
        params = [E, nu, alpha_elast, alpha_filtr, kr, phi, M,
                  mu, mu, sigma_min, sigma_max, pres_init]
        dict_keys = ['E', 'nu', 'alphaE', 'alphaF', 'kr', 'phi', 'M',
                     'mu', 'muf', 'SMin', 'SMax', 'p0']
        for key, val in zip(dict_keys, params):
            self._sim_dict['reservoirProperties'][key] = float(val)
    
    
    # hardcode
    def set_elasticity_problem_settings(self):
        self._sim_dict['elasticityProperties']['BC']           = 'neumann'
        self._sim_dict['elasticityProperties']['shiftInitial'] = False
    
    
    # hardcode
    def set_wellbore_modeling_properties(self):
        self._sim_dict['wellmoduleProperties']['rateSplitType'] = 'poiseuille'
        self._sim_dict['wellmoduleProperties']['perfFriction']  = 'ON'
    
    
    def _set_submodels_properties(self):
        reservoir   = 'reservoirProperties'
        elasticity  = 'elasticityProperties'
        filtration  = 'filtrationProperties'
        lubrication = 'lubricationProperties'
        twophase    = 'twoPhase'
        
        self._sim_dict[elasticity]['E']      = self._sim_dict[reservoir]['E']
        self._sim_dict[elasticity]['nu']     = self._sim_dict[reservoir]['nu']
        self._sim_dict[elasticity]['alphaE'] = self._sim_dict[reservoir]['alphaE']
        self._sim_dict[elasticity]['SMin']   = self._sim_dict[reservoir]['SMin']
        self._sim_dict[elasticity]['SMax']   = self._sim_dict[reservoir]['SMax']
        self._sim_dict[elasticity]['p0']     = self._sim_dict[reservoir]['p0']
        
        self._sim_dict[filtration]['mu']     = self._sim_dict[reservoir]['mu']
        self._sim_dict[filtration]['k']      = self._sim_dict[reservoir]['kr']
        self._sim_dict[filtration]['alphaF'] = self._sim_dict[reservoir]['alphaF']
        self._sim_dict[filtration]['p0']     = self._sim_dict[reservoir]['p0']
        self._sim_dict[filtration]['phi']    = self._sim_dict[reservoir]['phi']
        self._sim_dict[filtration]['M']      = self._sim_dict[reservoir]['M']
        
        if 'nw' in self._sim_dict[twophase].keys():
            self._sim_dict[twophase]['mu']     = self._sim_dict[reservoir]['mu']
            self._sim_dict[twophase]['k']      = self._sim_dict[reservoir]['kr']
            self._sim_dict[twophase]['alphaF'] = self._sim_dict[reservoir]['alphaF']
            self._sim_dict[twophase]['p0']     = self._sim_dict[reservoir]['p0']
            self._sim_dict[twophase]['phi']    = self._sim_dict[reservoir]['phi']
            self._sim_dict[twophase]['M']      = self._sim_dict[reservoir]['M']
            self._sim_dict[twophase]['mu_w']   = self._sim_dict[reservoir]['mu']
        
        self._sim_dict[lubrication]['muf']   = self._sim_dict[reservoir]['muf']
        self._sim_dict[lubrication]['k']     = self._sim_dict[reservoir]['kr']
    
    
    def add_well(self, geometry_type, well_type, is_initial_hf,
                 start_point: list, end_point=None,
                 control: str='flowrate', has_bean=False,
                 name=None):
        # todo: message that end_point is not needed for vertical well
        end_point = start_point if geometry_type == 'vertical' else end_point
        
        coordinates = [float(coo) for coo in list(chain.from_iterable([start_point, end_point]))]
        
        # if well_type != 'production':
        self._fracs_on_wells[f'well{self._nwells}'] = dict()
        self._fracs_on_wells[f'well{self._nwells}']['nfracs'] = 0
        self._fracs_on_wells[f'well{self._nwells}']['is_fractured'] = dict()
        
        
        # Set default name here
        well = dict()
        well['name']         = name if name else f'скв. №{self._nwells}'
        well['geometryType'] = geometry_type
        well['wellType']     = well_type
        well['coordinates']  = coordinates
        well['isInitialHF']  = is_initial_hf
        well['controlType']  = control
        
        self._welldata['wells'][f'well{self._nwells}'] = well
        self._welldata['wells'][f'well{self._nwells}']['ports'] = dict()
        self._welldata['wells'][f'well{self._nwells}']['nPorts'] = 0
        
        self._nwells += 1
        
    
    def set_well_schedule(self, well_id, flowrate, schedule):
        flowrate = [flowrate] if not isinstance(flowrate, list) else flowrate
        schedule = [schedule] if not isinstance(schedule, list) else schedule
        
        t_start = self._sim_dict['timestepProperties']['startTime']
        t_end = self._sim_dict['timestepProperties']['endTime']

        # Assume zero flowrate before start time
        # todo: add warning
        if schedule[0] > t_start:
            schedule = np.insert(schedule, 0, t_start)
            flowrate = np.insert(flowrate, 0, 0.0)
        
        self._welldata['wells'][f'well{well_id}']['flowrate'] = [float(f) for f in flowrate]
        self._welldata['wells'][f'well{well_id}']['schedule'] = [float(s) for s in schedule]


    # hardcode
    def set_well_friction_all(self):
        for iw in range(self._nwells):
            self._welldata['wells'][f'well{iw}']['C_poiseuille'] = 0.001
    
    
    def add_port_to_well(self, well_id, port_point, names=None, force_push=True):
        well_coord = self._welldata['wells'][f'well{well_id}']['coordinates']
        n_ports = 1
        ip = self._welldata['wells'][f'well{well_id}']['nPorts'] - 1
        
        names = [] if names == None else names
        names = [names] if not isinstance(names, list) else names
        
        ppoints = [[float(port_point[0]), float(port_point[1])]]
            
        self._fracs_on_wells[f'well{well_id}']['nfracs'] += n_ports
        self._fracs_on_wells[f'well{well_id}']['is_fractured'][f'port{ip}'] = False
        
        if force_push:
            # todo: add warning if port positions were corrected
            ppoints, err_msg = _fix_ports_coordinates(well_coord, ppoints, well_id)
        
        self._welldata['wells'][f'well{well_id}']['nPorts'] += n_ports
        # print(f"in dict {self._welldata['wells'][f'well{well_id}']['nPorts']}")
        # ports = dict()
        if not names:
            names_default = []
            names_default.append(f'скв. №{well_id}, порт №{ip}')
        else:
            names_default = names
        port = dict()
        # Set default name here
        port['name'] = names_default[0]
        port['coordinates'] = ppoints[0]
        self._welldata['wells'][f'well{well_id}']['ports'][f'port{ip}'] = port
    
    
    def add_ports_to_well_segment_centers(self, well_id, n_ports, names=None):
        names = [] if names == None else names
        names = [names] if not isinstance(names, list) else names
        
        geometry_type = self._welldata['wells'][f'well{well_id}']['geometryType']
        if geometry_type == 'vertical' and n_ports > 1:
            n_ports = 1
            
        self._fracs_on_wells[f'well{well_id}']['nfracs'] = n_ports
        self._fracs_on_wells[f'well{well_id}']['is_fractured'] = dict()
        for ip in range(n_ports):
            self._fracs_on_wells[f'well{well_id}']['is_fractured'][f'port{ip}'] = False
        
        coo = self._welldata['wells'][f'well{well_id}']['coordinates']
        pp = _get_ports_coords_centers(coo, n_ports)
        
        self._welldata['wells'][f'well{well_id}']['nPorts'] = n_ports
        if not names:
            names_default = []
            for ip in range(n_ports):
                names_default.append(f'скв. №{well_id}, порт №{ip}')
        else:
            names_default = names
        for ip in range(n_ports):
            port = dict()
            # Set default name here
            port['name'] = names_default[ip]
            port['coordinates'] = pp[ip]
            self._welldata['wells'][f'well{well_id}']['ports'][f'port{ip}'] = port
            # print(port)
            # print(self._welldata['wells'][f'well{well_id}']['ports'][f'port{ip}'])
            
    
    def add_ports_to_well_segment_borders(self, well_id, n_ports, names=None):
        names = [] if names == None else names
        names = [names] if not isinstance(names, list) else names
        
        geometry_type = self._welldata['wells'][f'well{well_id}']['geometryType']
        if geometry_type == 'vertical' and n_ports > 1:
            n_ports = 1
            
        self._fracs_on_wells[f'well{well_id}']['nfracs'] = n_ports
        self._fracs_on_wells[f'well{well_id}']['is_fractured'] = dict()
        for ip in range(n_ports):
            self._fracs_on_wells[f'well{well_id}']['is_fractured'][f'port{ip}'] = False
        
        coo = self._welldata['wells'][f'well{well_id}']['coordinates']
        pp = _get_ports_coords_borders(coo, n_ports)
        
        self._welldata['wells'][f'well{well_id}']['nPorts'] = n_ports
        if not names:
            names_default = []
            for ip in range(n_ports):
                names_default.append(f'скв. №{well_id}, порт №{ip}')
        else:
            names_default = names
        for ip in range(n_ports):
            port = dict()
            # Set default name here
            port['name'] = names_default[ip]
            port['coordinates'] = pp[ip]
            self._welldata['wells'][f'well{well_id}']['ports'][f'port{ip}'] = port
    
    
    # hardcode
    def set_perforation_friction_all_ports_all_wells(self):
        for well_id in range(self._nwells):
            n_ports = self._welldata['wells'][f'well{well_id}']['nPorts']
            for port_id in range(n_ports):
                self._welldata['wells'][f'well{well_id}']['ports'][f'port{port_id}']['C_perforation'] = 1.0e11

    
    def set_initial_fracture(self, well_id, port_id, initial_fracture_wings, kf, wf):
        # n_ports = self._welldata['wells'][f'well{well_id}']['nPorts']
        # print(f"in dict initfrac {self._welldata['wells'][f'well{well_id}']['nPorts']}")
        # print(port_id)
        pcoords = self._welldata['wells'][f'well{well_id}']['ports'][f'port{port_id}']['coordinates']
        
        initfrac = dict()
        initfrac['norm'] = [0.0, 1.0]   # set normal vector for fracture
        initfrac['kf'] = float(kf)
        initfrac['wf'] = float(wf)
        initfrac['coordinates'] = _fracture_from_wings(pcoords, initial_fracture_wings)
        self._welldata['wells'][f'well{well_id}']['ports'][f'port{port_id}']['initialFracture'] = initfrac
    
    
    def set_initial_fractures_all_ports_on_well(self, well_id, initial_fracture_wings, kf, wf):
        n_ports = self._welldata['wells'][f'well{well_id}']['nPorts']
        for port_id in range(n_ports):
            pcoords = self._welldata['wells'][f'well{well_id}']['ports'][f'port{port_id}']['coordinates']
            initfrac = dict()
            initfrac['norm'] = [0.0, 1.0]   # set normal vector for fracture
            initfrac['kf'] = float(kf)
            initfrac['wf'] = float(wf)
            initfrac['coordinates'] = _fracture_from_wings(pcoords, initial_fracture_wings)
            self._welldata['wells'][f'well{well_id}']['ports'][f'port{port_id}']['initialFracture'] = initfrac
    
    
    def set_potential_fracture(self, well_id, port_id, potential_fracture_wings):
        pcoords = self._welldata['wells'][f'well{well_id}']['ports'][f'port{port_id}']['coordinates']
        self._fracs_on_wells[f'well{well_id}']['is_fractured'][f'port{port_id}'] = True
        potentfrac = dict()
        potentfrac['norm'] = [0.0, 1.0]   # set normal vector for fracture
        potentfrac['coordinates'] = _fracture_from_wings(pcoords, potential_fracture_wings)
        self._sim_dict['meshProperties']['fractureGeometry']['fractures'][f'fracture{self._nfracs}'] = potentfrac
        self._nfracs += 1
    
    
    def set_potential_fractures_all_ports_on_well(self, well_id, potential_fracture_wings):
        n_ports = self._welldata['wells'][f'well{well_id}']['nPorts']
        for port_id in range(n_ports):
            pcoords = self._welldata['wells'][f'well{well_id}']['ports'][f'port{port_id}']['coordinates']
            self._fracs_on_wells[f'well{well_id}']['is_fractured'][f'port{port_id}'] = True
            potentfrac = dict()
            potentfrac['norm'] = [0.0, 1.0]   # set normal vector for fracture
            potentfrac['coordinates'] = _fracture_from_wings(pcoords, potential_fracture_wings)
            self._sim_dict['meshProperties']['fractureGeometry']['fractures'][f'fracture{self._nfracs}'] = potentfrac
            self._nfracs += 1
    
    
    def set_potential_fractures_all_ports_all_wells(self, potential_fracture_wings):
        for well_id in range(self._nwells):
            n_ports = self._welldata['wells'][f'well{well_id}']['nPorts']
            for port_id in range(n_ports):
                pcoords = self._welldata['wells'][f'well{well_id}']['ports'][f'port{port_id}']['coordinates']
                self._fracs_on_wells[f'well{well_id}']['is_fractured'][f'port{port_id}'] = True
                potentfrac = dict()
                potentfrac['norm'] = [0.0, 1.0]   # set normal vector for fracture
                potentfrac['coordinates'] = _fracture_from_wings(pcoords, potential_fracture_wings)
                self._sim_dict['meshProperties']['fractureGeometry']['fractures'][f'fracture{self._nfracs}'] = potentfrac
                self._nfracs += 1

    
    def write_data(self):
        if self._sim_dict['simID'] == 0:
            self.set_simID(0)
            
        self._welldata['nWells'] = self._nwells
        self._sim_dict['meshProperties']['fractureGeometry']['nFractures'] = self._nfracs
        self._sim_dict['wellData'] = self._welldata
        
        sim_dir = self._sim_dict['simDir']
        if not os.path.exists(sim_dir):
            os.makedirs(sim_dir)
        
        input_file = sim_dir + '/input.json'
        # print(f'simdict input file = {input_file}')
        with open(input_file, 'w', encoding='utf8') as f:
            json.dump(self._sim_dict, f, indent=4, ensure_ascii=False)
        
        # runner_file = _repository_dir + '/runner.json'
        # with open(runner_file, 'w') as f:
        #     runnerDict = {
        #         'input_path' : os.path.abspath(sim_dir + '/input.json')
        #     }
        #     json.dump(runnerDict, f, indent=4)
        
        # generate_mesh(input_file, plot_mesh)
    