from pathlib import Path
import tomllib


PROJECT_ROOT: Path = Path(__file__).parent.parent


with open(PROJECT_ROOT / "config.toml", "rb") as f:
    CONFIG: dict[str, any] = tomllib.load(f)


for dir in ["saved", "rpt", "plots"]:
    Path.mkdir(PROJECT_ROOT / dir, exist_ok=True)
