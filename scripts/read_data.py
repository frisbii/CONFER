import argparse
import itertools
import pandas as pd
from globals import PROJECT_ROOT
import seaborn as sns
import matplotlib.pyplot as plt

pd.options.mode.chained_assignment = None


        
def generate_plots():
    global df

    # define total design space (operation, datatype, part, period)
    operations = ['ADD', 'MUL']
    datatypes = ['uint', 'sint', 'ufxp', 'sfxp', 'float', 'posit']
    parts = ['xc7k160tfbg484-1', 'xc7s50csga324-1']
    periods = [3, 10, 1000000]

    specified_params = [['MUL'], None, ['xc7k160tfbg484-1'], [3]]

    parameters = list(itertools.product(
        specified_params[0] if specified_params[0] is not None else operations, 
        specified_params[1] if specified_params[1] is not None else datatypes, 
        specified_params[2] if specified_params[2] is not None else parts, 
        specified_params[3] if specified_params[3] is not None else periods, 
        ))
    num_plots = len(parameters)

    fig = plt.figure()
    sfigs = fig.subfigures(1, num_plots)

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
        d = df.loc[*p].loc[:, ['power_static', 'power_dynamic']].copy() # type: ignore
        bottom_values = [0] * len(d)
        for col in d.columns:
            # plot each column on top of each other
            axs[2].bar(d.index, d[col], bottom=bottom_values, label=col, width=2)
            # add the new values to the bottom_values baseline to prepare for the next column
            bottom_values = [i+j for i, j in zip(bottom_values, d[col])]
        axs[2].legend()
    
    plt.show()


def main():
    global df

    # Set seaborn matplotlib theme
    #sns.set_theme()
    # Set legend size to x-small for space
    plt.rc('legend', fontsize='x-small')

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

    # Load dataframe
    df = pd.read_hdf(PROJECT_ROOT / infile, key='df')

    # Generates comparison plots for specified parameters
    generate_plots()


if __name__ == '__main__':
    main()