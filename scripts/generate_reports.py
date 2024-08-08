import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import os
from pathlib import Path
import shutil
import subprocess

from progress.bar import IncrementalBar

from confer import add_config_path, Config, Design, PROJECT_ROOT


class ReportGenerator:
    def __init__(self, config: Config):
        now: datetime = datetime.now()
        # timestamp is used to mark the output folder for this set of runs
        self.timestamp: str = (
            f"{now.year}-{now.month}-{now.day}_{now.hour}-{now.minute}-{now.second}"
        )

        self.config: Config = config

        self.run_dir: Path = PROJECT_ROOT / "saved" / self.timestamp
        self.log_dir: Path = self.run_dir / "log"
        self.prj_dir: Path = self.run_dir / "prj"
        self.rpt_dir: Path = self.run_dir / "rpt"

        # create output folders
        for dir in [self.run_dir, self.log_dir, self.prj_dir, self.rpt_dir]:
            dir.mkdir(parents=True)

    def process_design(self, design: Design):
        # Extend the existing environment in preparation for the VHLS script
        # The tcl scripts read these as environment variables
        env = os.environ | {
            "PRJ_DIR": self.prj_dir.as_posix(),
            "PRJ_NAME": str(design),
            "SRC_FILE": Path.as_posix(PROJECT_ROOT / "src" / f"{design.datatype}.cpp"),
            "HEADER_FILE": Path.as_posix(PROJECT_ROOT / "src" / "params.hpp"),
            "CFLAGS": " ".join(
                self.config.cflags
                + [f"-D{design.operation}", f"-DWIDTH={design.width}"]
            ),
            "PART": design.part,
            "CLK_PERIOD": str(design.period),
        }

        subprocess.run(
            [
                self.config.vhls_install_path,
                "-f",
                str(PROJECT_ROOT / "scripts" / "tcl" / "vhls_generate_ip.tcl"),
                "-l",
                str(self.log_dir / f"{str(design)}---vhls.log"),
            ],
            env=env,
            stdout=subprocess.DEVNULL,
            check=True,
        )

        env = os.environ | {
            "XPR_FILE": str(
                self.prj_dir
                / str(design)
                / "solution1"
                / "impl"
                / "verilog"
                / "project.xpr"
            ),
            "UTIL_FILE": str(self.rpt_dir / f"{str(design)}---utilization.rpt"),
            "TIME_FILE": str(self.rpt_dir / f"{str(design)}---timing.rpt"),
            "POWER_FILE": str(self.rpt_dir / f"{str(design)}---power.rpt"),
        }

        subprocess.run(
            [
                self.config.vivado_install_path,
                "-journal",
                str(self.log_dir / f"{str(design)}---vivado.jou"),
                "-log",
                str(self.log_dir / f"{str(design)}---vivado.log"),
                "-mode",
                "batch",
                "-source",
                str(PROJECT_ROOT / "scripts" / "tcl" / "vivado_generate_reports.tcl"),
            ],
            env=env,
            stdout=subprocess.DEVNULL,
            check=True,
        )

    def process_designs(self, designs):
        bar = IncrementalBar(
            "Report Generation",
            max=len(designs),
            suffix="%(elapsed_td)s | %(index)s / %(max)s",
        )
        bar.update()

        with ThreadPoolExecutor(self.config.max_processes) as executor:
            futures = [
                executor.submit(self.process_design, design) for design in designs
            ]

            for future in as_completed(futures):
                bar.next()
        bar.finish()

        latest_rpt_dir = PROJECT_ROOT / "rpt"
        latest_rpt_dir.mkdir(exist_ok=True)
        for rpt in self.rpt_dir.iterdir():
            shutil.copy(rpt, latest_rpt_dir)


def main():
    parser = argparse.ArgumentParser()
    add_config_path(parser)
    args = parser.parse_args()

    config = Config(args.config_path)

    ReportGenerator(config).process_designs(config.generate_designs())


if __name__ == "__main__":
    main()
