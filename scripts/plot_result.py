from .canvas import MplCanvas
from .fracture_data import FractureData

def plot_result_frac_1(canvas: MplCanvas, fd: FractureData,
                       timestep, ifrac, datatype: str):
    x = fd.get_timestep_data(timestep)[f'fracture{ifrac}']["x"]
    # print(x)
    canvas.axes.set_xlabel('x, м')
    # print(f'datatype={datatype}')
    if datatype == 'p(x)':
        yp = 1.0e-6*fd.get_timestep_data(timestep)[f'fracture{ifrac}']["pressure"]
        canvas.axes.set_ylabel('Давление, МПа')
        canvas.axes.plot(x, yp, lw=4)
        canvas.axes.set_ylim([0.95*1.0e-6*fd.pmin, 1.05*1.0e-6*fd.pmax])
    elif datatype == 'w(x)':
        # print('here w')
        yw = 1.0e3*fd.get_timestep_data(timestep)[f'fracture{ifrac}']["width"]
        canvas.axes.set_ylabel('Раскрытие, мм')
        canvas.axes.plot(x, yw, lw=4)
        canvas.axes.set_ylim([max(1.0e3*fd.wmin, 0), 1.05*1.0e3*fd.wmax])
        # print(yw)
    canvas.axes.grid(visible=True)
    canvas.fig.tight_layout()