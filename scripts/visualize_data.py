import itertools
import matplotlib.pyplot as plt
import pandas as pd

from globals import PROJECT_ROOT, CONFIG

df: pd.DataFrame = pd.read_hdf(PROJECT_ROOT / 'data.hdf', key='df') # type: ignore

df = df.set_index(['datatype', 'operation', 'width'])

datatypes = CONFIG['datatypes']
operations = CONFIG['operations']

fig, axs = plt.subplots(3 * len(operations), len(datatypes), layout='constrained', sharex=True, sharey='row')
axes_lookup = {}
for i, datatype in enumerate(datatypes):
    if datatype not in axes_lookup:
        axes_lookup[datatype] = {}

    for j, operation in enumerate(operations):
        if operation not in axes_lookup[datatype]:
            axes_lookup[datatype][operation] = {}

        axes_lookup[datatype][operation]['utilization'] = (j*3, i)
        axes_lookup[datatype][operation]['timing'] = (j*3 + 1, i)
        axes_lookup[datatype][operation]['power'] = (j*3 + 2, i)

def make_plots(datatype, operation):
    table = df.loc[(datatype, operation), :]

    # primitives
    total_primitives = [sum(int(y['Used']) for y in x) for x in table['primitives']]
    r, c = axes_lookup[datatype][operation]['utilization']
    ax = axs[r][c]
    ax.scatter(table.index, total_primitives)
    ax.set_title(f"{datatype}, {operation}")
    if c == 0:
        ax.set_ylabel('Primitives')

    # timing
    r, c = axes_lookup[datatype][operation]['timing']
    ax = axs[r][c]
    ax.scatter(table.index, table['delay_total'])
    if c == 0:
        ax.set_ylabel('Delay (ns)')

    # power
    r, c = axes_lookup[datatype][operation]['power']
    ax = axs[r][c]
    ax.scatter(table.index, table['power_total'])
    if c == 0:
        ax.set_ylabel('Power (W)')


for d, o in itertools.product(datatypes, operations):
    make_plots(d, o)

plt.show()
