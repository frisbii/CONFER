import datetime
import tomllib
from pathlib import Path


PROJECT_ROOT : Path = Path(__file__).parent.parent


with open(PROJECT_ROOT/'config.toml', 'rb') as f:
    CONFIG = tomllib.load(f)
    

tlds = [
    'saved',
    'rpt'
    'plots',
]
for tld in tlds:
    Path.mkdir(PROJECT_ROOT/tld, exist_ok=True)
    
