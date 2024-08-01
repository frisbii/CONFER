from argparse import ArgumentParser
from pathlib import Path

from .project_root import PROJECT_ROOT


def add_config_path(parser: ArgumentParser) -> None:
    parser.add_argument(
        "--config", dest="config_path", default=PROJECT_ROOT / "config.toml", type=Path
    )
