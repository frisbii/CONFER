import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import sys
import itertools

from globals import PROJECT_ROOT, CONFIG

df_path = PROJECT_ROOT / "data.hdf"
if sys.argv[1]:
    df_path = sys.argv[1]

df: pd.DataFrame = pd.read_hdf(df_path, key="df")
# df = df.sort_index(axis=1)

# df = df.set_index(['datatype', 'operation', 'width'])
print(df)

datatypes = CONFIG["datatypes"]
operations = CONFIG["operations"]

df["primitives_total"] = [sum(int(y["Used"]) for y in x) for x in df["primitives"]]


def split_utilization(df: pd.DataFrame):
    '''Return a utilization DataFrame indexed by width where each column is a primitive'''
    return (
        df["primitives"]
        .apply(
            lambda primitives: pd.Series(
                {
                    primitive["Ref Name"]: int(primitive["Used"])
                    for primitive in primitives
                }
            )
        )
        .sort_index(axis=1)
        .fillna(0)
    )

def aggregate_lut_utilization(utilization: pd.DataFrame):
    '''Combine the LUTx columns of a utilization DataFrame into one column'''
    lut_columns = list(filter(lambda label: label.startswith('LUT'), utilization.columns))
    lutx_column = utilization.apply(lambda row: row[lut_columns].sum(), axis='columns')
    return utilization.drop(columns=lut_columns).assign(LUTx=lutx_column)
    


sns.set_theme()

# sns.relplot(data=df, kind='scatter',
#            x='width', y ='primitives_total', col='datatype', hue='operation')


# https://stackoverflow.com/questions/68734050/seaborn-rows-and-x-vars-at-the-same-time
def paired_column_facets(
    df: pd.DataFrame, y_vars: list[str], other_vars: dict[str, str], **kwargs
) -> sns.FacetGrid:
    g = (
        df.melt(list(other_vars.values()), y_vars)
        .pipe(
            (sns.relplot, "data"),
            **other_vars,
            y="value",
            row="variable",
            facet_kws=dict(sharey="row", margin_titles=True),
            **kwargs,
        )
        .set_titles(col_template="{col_var} = {col_name}", row_template="")
    )
    for (row_name, _), ax in g.axes_dict.items():
        ax.set_ylabel(row_name)
    return g

def plot_utilization(datatype: str, operation: str, *, aggregate_luts=True):
    data = (
        df.set_index(["datatype", "operation"]).loc[(datatype, operation), :].set_index("width")
    )
    utilization = split_utilization(data)
    if aggregate_luts:
        utilization = aggregate_lut_utilization(utilization)
    utilization.plot(kind='bar', stacked=True, width=1, title=f'{datatype}_{operation}')

for pair in itertools.product(['float', 'posit'], ['ADD', 'MUL']):
    plot_utilization(*pair)

plt.show()

# Stacked Line Plot
# data = (
#     df.set_index(["datatype", "operation"]).loc[("uint", "MUL"), :].set_index("width")
# )
# utilization = get_split_utilization(data)
# print(utilization)
# plt.stackplot(
#     utilization.index.values,
#     utilization.reset_index().drop(columns=["width"]).T,
#     labels=utilization.columns,
# )
# plt.legend(loc="upper left")
# plt.show()

# Single operation grid
# data = df[df['operation'] == 'ADD']
#
# paired_column_facets(
#     data=data, kind='line',
#     y_vars=["primitives_total", "delay_total", "power_total"],
#     other_vars={"x": "width", "col": "datatype"},
# )

# plt.show()
