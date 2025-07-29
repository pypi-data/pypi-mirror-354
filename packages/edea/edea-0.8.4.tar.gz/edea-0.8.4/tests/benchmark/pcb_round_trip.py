from pathlib import Path

from edea.kicad.parser import from_str
from edea.kicad.pcb import Pcb
from edea.kicad.serializer import to_str

benchmarks_dir = Path(__file__).parent.parent / "kicad_projects" / "benchmarks" / "pcb"
files_content = [p.read_text() for p in sorted(benchmarks_dir.iterdir())]


def target():
    for content in files_content:
        pcb = from_str(content)
        assert isinstance(pcb, Pcb)
        to_str(pcb)


if __name__ == "__main__":
    target()
