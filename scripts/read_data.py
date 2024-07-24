import argparse
import pandas as pd
from globals import PROJECT_ROOT

def process_utilization(util_dict):
    capture = {'Flop & Latch': 'Reg', 'LUT': 'LUTx', 'CarryLogic': 'CARRY'}
    categories = {key: 0 for key in capture.values()}

    for primitive_type in util_dict:
        if (primitive_type['Functional Category'] in capture):
            categories[capture[primitive_type['Functional Category']]] += int(primitive_type['Used'])
        else:
            if (primitive_type['Ref Name'] in categories):
                categories[primitive_type['Ref Name']] += int(primitive_type['Used'])
            else:
                categories[primitive_type['Ref Name']] = int(primitive_type['Used'])

    return categories
    


    

def main():
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
    # ====================

    # Load dataframe
    df = pd.read_hdf(PROJECT_ROOT / infile, key='df')

    existing_primitives = set()
    # For each row of the dataframe
    for i in range(len(df)):
        # Get a dictionary of primitive usage for these paramaters
        categories = process_utilization(df['primitives'].iloc[i])
        # For each of the primitives found
        for cat in categories:
            # If this primitive is not currently tabulated, add to the dataframe
            if cat not in df:
                df[cat] = 0 # Initialize with zeroes
            # Assign the value processed
            df[cat][i] = categories[cat]
            
            existing_primitives.add(cat)
    
    print(
        df
        .set_index(['operation', 'datatype', 'width'])
        .sort_index()
        .loc[:, ['power_total', 'delay_total'] + list(existing_primitives)]
        .to_html('temp.html')
        )

main()