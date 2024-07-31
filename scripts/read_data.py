import argparse
import itertools
import pandas as pd
from globals import PROJECT_ROOT, CONFIG
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
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

    # defines the order and available variables
    variables = ['operation', 'part', 'datatype', 'width', 'period'] # last one is x-axis
    variable_values = {
        'operation': ['MUL'],
        'datatype': ['float'],
        'part': ['xc7s50csga324-1'],
        'width': [16],
        'period': [3, 10, 100, 1000]
    }
    # where empty means use every available value (in dataframe? or in given ordered list?)

    # Compute the list of full parameterizations to visualize this run.
    # TODO: parameterizations is the wrong word for this purpose.
    # TODO: the getattr() call is a janky hack.
    parameterizations = list(itertools.product(
        *[variable_values.get(var, getattr(CONFIG, var + 's')) for var in variables[:-1]]
    ))

    # create figure and prepare subfigures
    fig = plt.figure()
    sfigs = fig.subfigures(1, len(parameterizations), squeeze=False)[0]

    df = df.reset_index().set_index(variables)

    # VISUALIZATION
    for i, p in enumerate(parameterizations):
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
        axs[2].set_xlabel(variables[-1])

        # Utilization
        stack_bars(axs[0], df.loc[p].drop(['delay_route', 'delay_logic', 'power_static', 'power_dynamic'], axis=1).copy())
        # Timing
        stack_bars(axs[1], df.loc[p].loc[:, ['delay_route', 'delay_logic']].copy())
        # Power
        stack_bars(axs[2], df.loc[p].loc[:, ['power_dynamic']].copy())
    
    cursor = mplcursors.cursor(hover=True)
    cursor.connect('add', show_annotation)  

    plt.show()


def stack_bars(ax: Axes, df: pd.DataFrame):
    bottom_values = [0] * len(df)
    for col in df.columns:
        # plot each column on top of each other
        ax.bar(range(len(df.index)), df[col], bottom=bottom_values, label=col, width=1)
        ax.set_xticks(range(len(df.index)), df.index)
        # add the new values to the bottom_values baseline to prepare for the next column
        bottom_values = [i+j for i, j in zip(bottom_values, df[col])]
    ax.legend()


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
