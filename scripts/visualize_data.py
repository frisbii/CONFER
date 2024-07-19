
import matplotlib.pyplot as plt
import pandas as pd

from globals import PROJECT_ROOT

df: pd.DataFrame = pd.read_hdf(PROJECT_ROOT / 'data.hdf', key='df') # type: ignore
df['width'] = [int(x) for x in df['width']]
df = df.set_index(['datatype', 'operation', 'width'])



num_datatypes = len(set([i[0] for i in df.index]))
num_operations = len(set([i[1] for i in df.index]))

fig, axs = plt.subplots(3 * num_operations, num_datatypes, layout='constrained')

axes_lookup = {}
for j, datatype in enumerate(set([i[0] for i in df.index])):
    if datatype not in axes_lookup: axes_lookup[datatype] = {}
    for i, operation in enumerate(set([i[1] for i in df.index])):
        if operation not in axes_lookup[datatype]: axes_lookup[datatype][operation] = {}
        axes_lookup[datatype][operation]['utilization'] = (i*3, j)
        axes_lookup[datatype][operation]['timing'] = (i*3 + 1, j)
        axes_lookup[datatype][operation]['power'] = (i*3 + 2, j)

def make_plots(datatype, operation):
    table = df.loc[pair, :]

    # primitives
    table['primitives_total'] = [sum(int(y['Used']) for y in x) for x in table['primitives']]
    print(table)
    
    r, c = axes_lookup[datatype][operation]['utilization']
    ax = axs[r][c].plot(table.index, table['primitives_total'])


    # timing
    r, c = axes_lookup[datatype][operation]['timing']
    axs[r][c].text(0.5, 0.5, f'{datatype}, {operation}', transform=axs[r][c].transAxes)


    # power
    r, c = axes_lookup[datatype][operation]['power']
    axs[r][c].text(0.5, 0.5, f'{datatype}, {operation}', transform=axs[r][c].transAxes)

pairs = {i[0:2] for i in df.index}

for pair in pairs:
    make_plots(*pair)

plt.show()