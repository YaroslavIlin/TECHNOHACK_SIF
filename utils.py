import sys
import os
import json

_repository_dir = os.path.abspath(os.getcwd())
sys.path.append(_repository_dir)


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
    
    
    def set_algorithm_settings(self):
        pass
    
    
    def set_timestep_properties(self, dt, t_start, t_end):
        pass
    
    
    def set_reservoir_properties(self, E, nu, alpha_elast, alpha_filtr, kr, phi, M,
                                 mu, sigma_min, sigma_max, pres_init):
        params = [E, nu, alpha_elast, alpha_filtr, kr, phi, M,
                  mu, mu, sigma_min, sigma_max, pres_init]
        dict_keys = ['E', 'nu', 'alphaE', 'alphaF', 'kr', 'phi', 'M',
                     'mu', 'muf', 'SMin', 'SMax', 'p0']
        for key, val in zip(dict_keys, params):
            self._sim_dict['reservoirProperties'][key] = float(val)
    
    
    def set_elasticity_problem_settings(self):
        pass
    
    
    def write_data(self):
        if self._sim_dict['simID'] == 0:
            self.set_simID(0)
            
        self._welldata['nWells'] = self._nwells
        # self._sim_dict['meshProperties']['fractureGeometry']['nFractures'] = self._nfracs
        self._sim_dict['wellData'] = self._welldata
        
        sim_dir = self._sim_dict['simDir']
        if not os.path.exists(sim_dir):
            os.makedirs(sim_dir)
        
        input_file = sim_dir + '/input.json'
        print(f'simdict input file = {input_file}')
        with open(input_file, 'w') as f:
            json.dump(self._sim_dict, f, indent=4)
        
        # runner_file = _repository_dir + '/runner.json'
        # with open(runner_file, 'w') as f:
        #     runnerDict = {
        #         'input_path' : os.path.abspath(sim_dir + '/input.json')
        #     }
        #     json.dump(runnerDict, f, indent=4)
        
        # generate_mesh(input_file, plot_mesh)
    