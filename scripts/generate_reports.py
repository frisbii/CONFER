from datetime import datetime
from pathlib import Path
import subprocess
from globals import PROJECT_ROOT, CONFIG
import os


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

    def process_paramaterization(self, datatype: str, operation: str, width: int):
        param_str = f"{datatype}_{operation}_{width}"

        # Extend the existing environment
        env = os.environ | {
            "PRJ_DIR": self.prj_dir.as_posix(),
            "PRJ_NAME": param_str,
            "SRC_FILE": Path.as_posix(PROJECT_ROOT / "src" / f"{datatype}.cpp"),
            "HEADER_FILE": Path.as_posix(PROJECT_ROOT / "src" / "params.hpp"),
            "CFLAGS": " ".join(
                CONFIG["cflags"] + [f"-D{operation}", f"-DWIDTH={width}"]
            ),
            "PART": CONFIG["part"],
            "CLOCK_PERIOD": "10",
        }

        subprocess.run(
            [
                CONFIG["vhls_install_path"],
                "-f",
                str(PROJECT_ROOT / "scripts" / "vhls_generate_ip.tcl"),
                "-l",
                str(self.log_dir / f"{param_str}-vhls.log"),
            ],
            env=env,
        )


ReportGenerator().process_paramaterization("uint", "ADD", 4)
