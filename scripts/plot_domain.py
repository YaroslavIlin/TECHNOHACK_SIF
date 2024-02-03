import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.widgets import Button
# import matplotlib

from .canvas import MplCanvas    


SMALL_SIZE = 20
MEDIUM_SIZE = 25
BIGGER_SIZE = 25
LEGEND_SIZE = 14
# rc('text', usetex=True)
rc('font', size=SMALL_SIZE)          # controls default text sizes
rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
rc('axes', labelsize=SMALL_SIZE)    # fontsize of the x and y labels
rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
rc('legend', fontsize=LEGEND_SIZE)    # legend fontsize
rc('figure', titlesize=SMALL_SIZE)  # fontsize of the figure title

# matplotlib.rcParams['text.latex.preamble']= \
#     r"\usepackage[utf8]{inputenc} \usepackage[russian]{babel} \usepackage{amsmath} \usepackage{amssymb}"
# matplotlib.rcParams['font.family'] = 'serif'

def plot_wells_fractures_domain(canvas: MplCanvas,
                                well_labels, well_coords, is_hf,
                                well_port_coords, well_port_labels, init_frac_coords,
                                frac_coords, domain_coords,
                                show_well_labels, show_port_labels):
    xmin, ymin, xmax, ymax = domain_coords
    xlimits = [xmin, xmax]
    ylimits = [ymin, ymax]
    # fig, ax = plt.subplots(1, 1, figsize=(10, 10*(ymax-ymin)/(xmax-xmin)))
    for iw in range(len(well_coords)):
        well_coo = well_coords[iw]
        color = 'blue' if is_hf[iw] == 0 else 'red'
        canvas.axes.plot([well_coo[0], well_coo[2]], [well_coo[1], well_coo[3]], linewidth=5, color=color, zorder=10)
        
        port_coo = well_port_coords[iw]
        port_name = well_port_labels[iw]
        X = [port[0] for port in port_coo]
        Y = [port[1] for port in port_coo]
        S = [8**2 for n in range(len(port_coo))]
        canvas.axes.scatter(X, Y, S, color='black', zorder=25)
        
        init_frac_coo = init_frac_coords[iw]
        [canvas.axes.plot([pfr_coord[0], pfr_coord[2]], [pfr_coord[1], pfr_coord[3]], 
                 linewidth=3, color='green', alpha=1, zorder=15, ls='-') for pfr_coord in frac_coords]
        [canvas.axes.plot([ifr_coord[0], ifr_coord[2]], [ifr_coord[1], ifr_coord[3]], 
                 linewidth=4, color='orange', alpha=1, zorder=20) for ifr_coord in init_frac_coo]
        x_center = 0.5 * (well_coo[0] + well_coo[2])
        y_center = 0.5 * (well_coo[1] + well_coo[3])
        
        # well label
        if show_well_labels:
            canvas.axes.text(x_center+40, y_center+110*(well_coo[0]!=well_coo[2] or well_coo[1]!=well_coo[3]),
                    str(well_labels[iw]),
                    horizontalalignment='center', verticalalignment='center',
                    fontsize=12,
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=1, pad=0.2),
                    zorder=30)
        
        # port label
        if show_port_labels:
            [canvas.axes.text(xp-40, yp, str(pn),
                    horizontalalignment='center', verticalalignment='center',
                    fontsize=9,
                    bbox=dict(boxstyle='round', facecolor='palegreen', alpha=1, pad=0.2),
                    zorder=30) for xp, yp, pn in zip(X, Y, port_name)]
        
    canvas.axes.set_xlabel('$x$, м')
    canvas.axes.set_ylabel('$y$, м')
    # canvas.axes.set_aspect('equal')
    canvas.axes.set_xlim(xlimits)
    canvas.axes.set_ylim(ylimits)
    canvas.axes.grid()
    canvas.fig.tight_layout()
    # plt.show()


def save_pdf(pdf_final_filename):
    pdf_ext = '.pdf'
    pdf_final_filename_with_ext = pdf_final_filename + pdf_ext
    plt.savefig(pdf_final_filename_with_ext, bbox_inches='tight', pad_inches=0)


def save_png(png_final_filename):
    png_ext = '.png'
    png_final_filename_with_ext = png_final_filename + png_ext
    plt.savefig(png_final_filename_with_ext, dpi=300, bbox_inches='tight', pad_inches=0)
    

def save_eps(eps_final_filename):
    eps_ext = '.eps'
    eps_final_filename_with_ext = eps_final_filename + eps_ext
    plt.savefig(eps_final_filename_with_ext)   


def create_save_button(file_path):
    ax_button = plt.axes([0.7, 0.05, 0.2, 0.075])

    def call(event):
        print("button clicked")
        ax_button.set_visible(False)
        save_pdf(file_path)
        save_png(file_path)
        # save_eps(file_path)
    button = Button(ax_button, 'Save image')
    button.on_clicked(call)
    return button