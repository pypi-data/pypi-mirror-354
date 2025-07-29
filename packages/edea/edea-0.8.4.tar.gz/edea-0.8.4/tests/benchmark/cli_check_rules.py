"""Monitor checking design and electrical rules via the CLI."""

from pathlib import Path

from edea.cli import check

pcb_path = Path(__file__).parent.parent.joinpath(
    "kicad_projects", "benchmarks", "pcb", "Desktop_50_Pin_TopConn.kicad_pcb"
)

sch_path = Path(__file__).parent.parent.joinpath(
    "kicad_projects", "benchmarks", "sch", "JumperlessRev3point1.kicad_sch"
)


def target():
    check(pcb_path)
    check(sch_path)


if __name__ == "__main__":
    target()
