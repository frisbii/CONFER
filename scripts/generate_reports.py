from datetime import datetime
from pathlib import Path
import subprocess
from time import sleep
from globals import PROJECT_ROOT, CONFIG, Parameters
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from progress.bar import IncrementalBar
import shutil





class ReportGenerator:
    def __init__(self):
        now: datetime = datetime.now()
        self.timestamp: str = (
            f"{now.year}-{now.month}-{now.day}_{now.hour}-{now.minute}-{now.second}"
        )

        self.run_dir: Path = PROJECT_ROOT / "saved" / self.timestamp
        self.log_dir: Path = self.run_dir / "log"
        self.prj_dir: Path = self.run_dir / "prj"
        self.rpt_dir: Path = self.run_dir / "rpt"

        for dir in [self.run_dir, self.log_dir, self.prj_dir, self.rpt_dir]:
            dir.mkdir()

    def process_paramaterization(self, params: Parameters):
        # Extend the existing environment in preparation for the VHLS script
        env = os.environ | {
            "PRJ_DIR": self.prj_dir.as_posix(),
            "PRJ_NAME": str(params),
            "SRC_FILE": Path.as_posix(PROJECT_ROOT / "src" / f"{params.datatype}.cpp"),
            "HEADER_FILE": Path.as_posix(PROJECT_ROOT / "src" / "params.hpp"),
            "CFLAGS": " ".join(
                CONFIG.cflags + [f"-D{params.operation}", f"-DWIDTH={params.width}"]
            ),
            "PART": params.part,
            "CLK_PERIOD": str(params.period)
        }

        subprocess.run(
            [
                CONFIG.vhls_install_path,
                "-f",
                str(PROJECT_ROOT / "scripts" / "vhls_generate_ip.tcl"),
                "-l",
                str(self.log_dir / f"{str(params)}---vhls.log"),
            ],
            env=env,
            stdout=subprocess.DEVNULL,
            check=True
        )

        env = os.environ | {
            "XPR_FILE" : str(self.prj_dir / str(params) / "solution1" / "impl" / "verilog" / "project.xpr"),
            "UTIL_FILE" : str(self.rpt_dir / f"{str(params)}---utilization.rpt"),
            "TIME_FILE" : str(self.rpt_dir / f"{str(params)}---timing.rpt"),
            "POWER_FILE" : str(self.rpt_dir / f"{str(params)}---power.rpt")
        }

        subprocess.run(
            [
                CONFIG.vivado_install_path,
                "-journal",
                str(self.log_dir / f"{str(params)}---vivado.jou"),
                "-log",
                str(self.log_dir / f"{str(params)}---vivado.log"),
                "-mode",
                "batch",
                "-source",
                str(PROJECT_ROOT / "scripts" / "vivado_generate_reports.tcl")
            ],
            env=env,
            stdout=subprocess.DEVNULL,
            check=True
        )
    
    def process_paramaterizations(self, paramaterizations):
        bar = IncrementalBar("Report Generation", max=len(paramaterizations), suffix='%(elapsed_td)s | %(index)s / %(max)s')
        bar.update()
        with ThreadPoolExecutor(CONFIG.max_processes) as executor:
            futures = [executor.submit(self.process_paramaterization, params) for params in paramaterizations]
            for future in as_completed(futures):
                bar.next()
        bar.finish()
        for rpt in self.rpt_dir.iterdir():
            shutil.copy(rpt, PROJECT_ROOT / 'rpt')


def main():

    ReportGenerator().process_paramaterizations(CONFIG.generate_paramaterizations())


if __name__ == "__main__":
    main()

