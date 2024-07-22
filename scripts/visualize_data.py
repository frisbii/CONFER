
import matplotlib.pyplot as plt
import pandas as pd

from globals import PROJECT_ROOT

df: pd.DataFrame = pd.read_hdf(PROJECT_ROOT / 'data.hdf', key='df') # type: ignore
datatype_order = [
    'uint', 'sint',
    'ufxp', 'sfxp'
]
operation_order = [
    'ADD',
    'MUL'
]
df = df.set_index(['datatype', 'operation', 'width'])
#print(df.index.get_level_values('datatype'))
#df = df.sort_index(level='datatype', key=lambda x: datatype_order.index(x.str)).sort_index(level='operation', key=lambda x: operation_order.index(x.str)).sort_index(level='width')

num_datatypes = len(set([i[0] for i in df.index]))
num_operations = len(set([i[1] for i in df.index]))

fig, axs = plt.subplots(3 * num_operations, num_datatypes, layout='constrained', sharex=True, )
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
    total_primitives = [sum(int(y['Used']) for y in x) for x in table['primitives']]
    r, c = axes_lookup[datatype][operation]['utilization']
    ax = axs[r][c]
    ax.scatter(table.index, total_primitives)
    ax.set_title(f"{datatype}, {operation}")


    # timing
    r, c = axes_lookup[datatype][operation]['timing']
    ax = axs[r][c].scatter(table.index, table['delay_total'])


    # power
    r, c = axes_lookup[datatype][operation]['power']
    ax = axs[r][c].scatter(table.index, table['power_total'])

pairs = {i[0:2] for i in df.index}

for pair in pairs:
    make_plots(*pair)

plt.show()