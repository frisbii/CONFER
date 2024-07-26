import argparse
import itertools
import pandas as pd
from globals import PROJECT_ROOT
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.container import BarContainer
import mplcursors

def show_annotation(sel: mplcursors.Selection):
    if type(sel.artist) == BarContainer:
        bar = sel.artist[sel.index]
        sel.annotation.set_text(f'{sel.artist.get_label()}: {bar.get_height():.3f}')
        sel.annotation.xy = (bar.get_x() + bar.get_width() / 2, bar.get_y() + bar.get_height() / 2)
        sel.annotation.get_bbox_patch().set_alpha(0.8)
        
def generate_plots():
    global df
    # define total design space (operation, datatype, part, period)
    operations = ['ADD', 'MUL']
    datatypes = ['uint', 'sint', 'ufxp', 'sfxp', 'float', 'posit']
    parts = ['xc7k160tfbg484-1', 'xc7s50csga324-1']
    periods = [3, 10, 1000000]
    # choose which parameters to hold fixed for this run
    specified_params = [
        ['ADD'], 
        ['uint', 'float', 'posit'], 
        ["xc7s50csga324-1"], 
        [3]
    ]
    # fill the list of desired plots for this run
    parameters = list(itertools.product(
        specified_params[0] if specified_params[0] is not None else operations, 
        specified_params[1] if specified_params[1] is not None else datatypes, 
        specified_params[2] if specified_params[2] is not None else parts, 
        specified_params[3] if specified_params[3] is not None else periods, 
        ))
    # create figure and prepare subfigures
    fig = plt.figure()
    sfigs = fig.subfigures(1, len(parameters))

    # VISUALIZATION
    for i, p in enumerate(parameters):
        # Create figure and axes
        subfig = sfigs[i]
        axs = sfigs[i].subplots(3, 1, sharex=True)

        #################
        # SUPER STYLING
        subfig.suptitle('\n'.join([str(x) for x in p]) + 'ns')
        # If this is the leftmost subfigure, add y-labels
        if i == 0:
            axs[0].set_ylabel("Primitives count")
            axs[1].set_ylabel("Delay (ns)")
            axs[2].set_ylabel("Power usage (W)")
        axs[2].set_xlabel("Bit width")

        ##############
        # PRIMITIVES
        # create specific table
        try:
            d = df.loc[*p].drop(['delay_route', 'delay_logic', 'power_static', 'power_dynamic'], axis=1).copy() # type: ignore
        except:
            continue
        # bottom_values necessary to keep track of stacked baselines
        bottom_values = [0] * len(d)
        for col in d.columns:
            # plot each column on top of each other
            axs[0].bar(d.index, d[col], bottom=bottom_values, label=col, width=2)
            # add the new values to the bottom_values baseline to prepare for the next column
            bottom_values = [i+j for i, j in zip(bottom_values, d[col])]
        # styling
        axs[0].legend()

        ##########
        # TIMING
        d = df.loc[*p].loc[:, ['delay_route', 'delay_logic']].copy() # type: ignore
        bottom_values = [0] * len(d)
        for col in d.columns:
            # plot each column on top of each other
            axs[1].bar(d.index, d[col], bottom=bottom_values, label=col, width=2)
            # add the new values to the bottom_values baseline to prepare for the next column
            bottom_values = [i+j for i, j in zip(bottom_values, d[col])]
        axs[1].legend()

        #########
        # POWER
        d = df.loc[*p].loc[:, ['power_dynamic']].copy() # type: ignore
        bottom_values = [0] * len(d)
        for col in d.columns:
            # plot each column on top of each other
            axs[2].bar(d.index, d[col], bottom=bottom_values, label=col, width=2)
            # add the new values to the bottom_values baseline to prepare for the next column
            bottom_values = [i+j for i, j in zip(bottom_values, d[col])]
        axs[2].legend()
    
    cursor = mplcursors.cursor(hover=True)
    cursor.connect('add', show_annotation)  

    plt.show()


def main():
    global df
    ####################
    # ARGUMENT PARSING
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f',
        default="data.hdf",
        help="specify a filename for the input hdf (default: /data.hdf)",
        metavar="file"
    )
    args = parser.parse_args()
    infile = args.f
    ####################

    ####################
    # PLOT STYLING
    # Set seaborn matplotlib theme
    sns.set_theme()
    sns.set_context(rc = {'patch.linewidth': 0.0})
    # Set legend size to x-small for space
    plt.rc('legend', fontsize='x-small')
    ####################

    # Load dataframe
    df = pd.read_hdf(PROJECT_ROOT / infile, key='df')
    # Generates comparison plots for specified parameters
    generate_plots()


if __name__ == '__main__':
    main()