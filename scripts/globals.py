from pathlib import Path
from typing import Any
import tomllib


PROJECT_ROOT: Path = Path(__file__).parent.parent


with open(PROJECT_ROOT / "config.toml", "rb") as f:
    CONFIG: dict[str, Any] = tomllib.load(f)
    CONFIG["widths"] = list(range(CONFIG["widths"][0], CONFIG["widths"][1])
)

for dir in ["saved", "rpt", "plots"]:
    Path.mkdir(PROJECT_ROOT / dir, exist_ok=True)
