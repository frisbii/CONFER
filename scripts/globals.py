from pathlib import Path
from typing import Any
import tomllib


PROJECT_ROOT: Path = Path(__file__).parent.parent


with open(PROJECT_ROOT / "config.toml", "rb") as f:
    CONFIG: dict[str, Any] = tomllib.load(f)
    
    if isinstance(CONFIG["widths"], str):
        start, end = [int(x) for x in CONFIG['widths'].split('-')]
        CONFIG['widths'] = list(range(start, end))

for dir in ["saved", "rpt", "plots"]:
    Path.mkdir(PROJECT_ROOT / dir, exist_ok=True)
