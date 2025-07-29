import os
import shutil
from pathlib import Path
from tempfile import TemporaryDirectory

from edea.cli.add import module

cwd = Path.cwd()


if __name__ == "__main__":
    with TemporaryDirectory() as tmpdir:
        d = os.path.join(tmpdir, "ferret")
        shutil.copytree(
            "tests/kicad_projects/benchmarks/pro/data-center-dram-tester", d
        )
        os.chdir(d)
        module(local_path=cwd.joinpath(Path("tests/kicad_projects/leako")))
        os.chdir(cwd)
