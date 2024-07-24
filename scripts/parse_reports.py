import re
import pandas as pd
import vivado_report_parser as vrp
from pathlib import Path
from globals import PROJECT_ROOT, CONFIG
import argparse

def first_float(s: str) -> float:
    match = re.search('[0-9]+(?:.[0-9]+)?', s)
    if match is None:
        raise Exception("float not found")
    else:
        return float(match[0])
    
def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f',
        default="data.hdf",
        help="specify a filename for the resulting hdf (default: /data.hdf)",
        metavar="file"
    )
    parser.add_argument(
        '-d',
        default="rpt",
        help="specify an rpt directory (default: /rpt)",
        metavar="dir"
    )
    args = parser.parse_args()
    indir = args.d
    outfile = args.f

    # startup tasks
    rpt_dir : Path = PROJECT_ROOT / indir

    # file parsing
    rows = []
    for rpt in rpt_dir.iterdir():
        param_str, rpt_type = rpt.stem.split('-')
        datatype, operation, width = param_str.split('_')
        row : dict[str, str | int | float] = {
            'datatype' : datatype,
            'operation' : operation,
            'width' : int(width),
        }
        with rpt.open() as f:
            raw_contents : str = f.read()
            match rpt_type:
                case "utilization":
                    row['primitives'] = vrp.parse_vivado_report(raw_contents)["Primitives"]
                case "power":
                    summary_dict : dict = vrp.parse_vivado_report(raw_contents)["Summary"]
                    try:
                        row['power_total']   = first_float(summary_dict['Total On-Chip Power (W)'])
                        row['power_static']  = first_float(summary_dict['Device Static (W)'])
                        row['power_dynamic'] = first_float(summary_dict['Dynamic (W)'])
                    except Exception:
                        print(f"power not parsed correctly in {rpt}")
                case "timing":
                    match = re.search(r"^\s*Data Path Delay:\s*([0-9\.]*)ns\s*\(logic ([0-9\.]*)ns [0-9\.%\(\)]*  route ([0-9\.]*)ns", raw_contents, re.MULTILINE)
                    if match is None:
                        print(f"timing not parsed correctly in {rpt}")
                    else:
                        row['delay_total'] = float(match[1])
                        row['delay_logic'] = float(match[2])
                        row['delay_route'] = float(match[3])
        rows.append(row)
    
    # pandas dataframe setup
    df: pd.DataFrame = pd.DataFrame(rows)
    df = df.groupby(['datatype', 'operation', 'width']).aggregate("first").reset_index()
    df.to_hdf(PROJECT_ROOT / outfile, key='df')


if __name__ == "__main__":
    main()