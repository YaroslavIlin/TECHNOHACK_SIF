import json
import h5py
import numpy as np
import fnmatch, os


def hdf5_read_single(h5file, key):
    if key in h5file.keys():
        data_h5 = h5file[key]
        if (data_h5.size == 1):
            return float(np.array(data_h5))
    return None


def hdf5_read_array(h5file, key):
    if key in h5file.keys():
        data_h5 = h5file[key]
        return np.array(data_h5)
    return None


class FractureData:
    def __init__(self, sim_path: str) -> None:
        self.sim_path = sim_path
        self.input_path = sim_path + "/input.json"
        self.data_dir = sim_path + "/sol1d"
        self.ntimesteps = len(fnmatch.filter(os.listdir(self.data_dir), '*.h5'))
        self.input = json.load(open(self.input_path))
        self.indxs_frac = []
        
        self.wmin, self.wmax = 10.0, -1.0
        self.pmin, self.pmax = 100.0e6, -1.0
        
        self.IS_FIRST = True
        self.PRELOAD = False
        
    def get_timestep_data(self, timestep: int):
        if self.PRELOAD:
            return self.data[timestep]
        filepath = self.data_dir + "/data_" + str(timestep) + ".h5"
        data = h5py.File(filepath, 'r')
        keys = list(data.keys())
        result = {}
        x = hdf5_read_array(data, "/x")
        y = hdf5_read_array(data, "/y")
        w = hdf5_read_array(data, "/width")
        p = hdf5_read_array(data, "/pressure")
        uv = hdf5_read_array(data, "/uv")
        time = hdf5_read_single(data, "/time")
        fid = hdf5_read_array(data, "/fracture_id")
        ifid = hdf5_read_array(data, "/initial_fracture_id")
        result["time"] = time
        
        if self.IS_FIRST:
            self.nf = max(fid) + 1
            self.init_nf = max(ifid) + 1
            for i in range(self.nf):
                indxs = np.flatnonzero(fid == i)
                xx = x[indxs]
                order = np.argsort(xx)
                indxs = indxs[order]
                self.indxs_frac.append(indxs)
            self.IS_FIRST = False
        
        wmin, wmax = 0.0, 0.0
        pmin, pmax = 0.0, 0.0
        for i in range(self.nf):
            frac = {}
            indxs = self.indxs_frac[i]
            frac["x"] = x[indxs]
            frac["y"] = y[indxs]
            frac["width"] = w[indxs]
            wmin = min(wmin, np.min(w[indxs]))
            wmax = max(wmax, np.max(w[indxs]))
            frac["pressure"] = p[indxs]
            pmin = min(pmin, np.min(p[indxs]))
            pmax = max(pmax, np.max(p[indxs]))
            frac["uv"] = uv[indxs]
            result[f"fracture{i}"] = frac
        self.wmin = min(self.wmin, wmin)
        self.wmax = max(self.wmax, wmax)
        self.pmin = min(self.pmin, pmin)
        self.pmax = max(self.pmax, pmax)
        return result
    
    def preload_data(self):
        self.data = [self.get_timestep_data(i) for i in range(self.ntimesteps)]
        self.PRELOAD = True