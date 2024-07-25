from dataclasses import dataclass
import itertools
from pathlib import Path
from typing import Any
import tomllib


class Config:
    vhls_install_path: str
    vivado_install_path: str
    cflags: list[str]

    max_processes: int

    datatypes: list[str]
    operations: list[str]
    widths: list[int]
    parts: list[str]
    periods: list[int]

    def __init__(self):
        with open(PROJECT_ROOT / "config.toml", "rb") as f:
            config_dict: dict[str, Any] = tomllib.load(f)

            self.vhls_install_path = config_dict['vhls_install_path']
            self.vivado_install_path = config_dict['vivado_install_path']
            self.cflags = config_dict['cflags']

            self.max_processes = config_dict['max_processes']

            self.datatypes = config_dict['datatypes']
            self.operations = config_dict['operations']
            self.parts = config_dict['parts']
            self.periods = config_dict['periods']
            
            if isinstance(config_dict["widths"], str):
                start, end = [int(x) for x in config_dict['widths'].split('-')]
                self.widths = list(range(start, end))
            else:
                self.widths = config_dict["widths"]
    
    def generate_paramaterizations(self):
        return [Parameters(*x) for x in itertools.product(self.datatypes, self.operations, self.widths, self.parts, self.periods)]

@dataclass
class Parameters:
    datatype: str
    operation: str
    width: int
    part: str
    period: int

    def __str__(self):
        return f"{self.datatype}_{self.operation}_{self.width}_{self.part}_{self.period}"


PROJECT_ROOT: Path = Path(__file__).parent.parent
CONFIG: Config = Config()


for dir in ["saved", "rpt", "plots"]:
    Path.mkdir(PROJECT_ROOT / dir, exist_ok=True)