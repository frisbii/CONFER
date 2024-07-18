import datetime
from pathlib import Path
import subprocess
from globals import PROJECT_ROOT, CONFIG

TIME : str

RUN_FOLDER : Path
LOG_FOLDER : Path
RPT_FOLDER : Path
PRJ_FOLDER : Path

now  : datetime.datetime = datetime.datetime.now()
TIME = f"{now.year}-{now.month}-{now.day}_{now.hour}-{now.minute}-{now.second}"

RUN_FOLDER = PROJECT_ROOT / 'saved' / TIME
LOG_FOLDER = RUN_FOLDER / 'log'
RPT_FOLDER = RUN_FOLDER / 'rpt'
PRJ_FOLDER = RUN_FOLDER / 'prj'

Path.mkdir(RUN_FOLDER)
Path.mkdir(LOG_FOLDER)
Path.mkdir(RPT_FOLDER)
Path.mkdir(PRJ_FOLDER)



def process_paramaterization(
    d: str,
    o: str,
    w: int
):
    
    dow = f'{d}_{o}_{w}'

    # Environment variable strings
    env = {
        'PRJ_FOLDER' : Path.as_posix(PRJ_FOLDER),
        'PRJ_NAME' : dow,
        'SRC_FILE' : Path.as_posix(PROJECT_ROOT / 'src' / f'{d}.cpp'),
        'HEADER_FILE' : Path.as_posix(PROJECT_ROOT / 'src' / 'params.hpp'),
        'CFLAGS' : ' '.join(CONFIG['cflags'] + [f'-D{o}', f'-DWIDTH={w}']), 
        'PART' : CONFIG['part'],
        'CLOCK_PERIOD' : '10'
    }

    subprocess.run(
        [
            CONFIG['vivadohls_install_path'],
            '-f', str(PROJECT_ROOT / 'scripts' / 'vhls_generate_ip.tcl'),
            '-l', str(LOG_FOLDER / f'{dow}_vhls.log')
        ]
    )


process_paramaterization('uint', 'ADD', 4)