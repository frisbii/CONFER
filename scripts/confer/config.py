import itertools
from pathlib import Path
import tomllib
from typing import Any

from .design import Design


class Dependencies:
    vhls_path: str
    vivado_path: str
    cflags: list[str]


class Generation:
    max_processes: int
    datatypes: list[str]
    operations: list[str]
    widths: list[int]
    parts: list[str]
    periods: list[int]

    def product(self):
        return itertools.product(
                self.datatypes, self.operations, self.widths, self.parts, self.periods
            )


class Visualization:
    parameters_order:list[str]
    categorical: bool
    show_annotation: bool
    datatypes: list[str]
    operations: list[str]
    widths: list[int]
    parts: list[str]
    periods: list[int]


class Config:
    dependencies: Dependencies
    generation: Generation
    visualization: Visualization

    def parse_widths(self, width: str) -> list[int]:
        if '-' in width:
            start, end = [int(x) for x in width.split('-')]
            return list(range(start, end))
        elif ',' in width:
            return [int(x.strip()) for x in width.split(',')]
        else:
            return [int(width)]

    def __init__(self, config_path: Path):
        self.dependencies = Dependencies()
        self.generation = Generation()
        self.visualization = Visualization()

        with open(config_path, "rb") as f:
            config_dict: dict[str, Any] = tomllib.load(f)

        self.dependencies.vhls_path = config_dict["dependencies"]["vhls_path"]
        self.dependencies.vivado_path = config_dict["dependencies"]["vivado_path"]
        self.dependencies.cflags = config_dict["dependencies"]["cflags"]

        self.generation.max_processes = config_dict["generation"]["max_processes"]
        self.generation.datatypes = config_dict["generation"]["datatypes"]
        self.generation.operations = config_dict["generation"]["operations"]
        self.generation.parts = config_dict["generation"]["parts"]
        self.generation.periods = config_dict["generation"]["periods"]
        self.generation.widths = self.parse_widths(config_dict["generation"]["widths"])

        self.visualization.parameters_order = config_dict["visualization"]["parameters_order"]
        self.visualization.categorical = config_dict["visualization"]["categorical"]
        self.visualization.show_annotation = config_dict["visualization"]["show_annotation"]
        self.visualization.datatypes = config_dict["visualization"]["datatypes"]
        self.visualization.operations = config_dict["visualization"]["operations"]
        self.visualization.widths = self.parse_widths(config_dict["visualization"]["widths"])
        self.visualization.parts = config_dict["visualization"]["parts"]
        self.visualization.periods = config_dict["visualization"]["periods"]

    def generate_designs(self):
        return [
            Design(*x)
            for x in self.generation.product()
        ]
