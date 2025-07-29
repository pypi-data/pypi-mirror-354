"""
Test that parses as many KiCad schematic and PCB files as we could find.

SPDX-License-Identifier: EUPL-1.2
"""

import os

import pytest

from edea.kicad._parse import MisconfiguredProjectError
from edea.kicad.common import VersionError
from edea.kicad.parser import from_str
from edea.kicad.pcb import Pcb
from edea.kicad.schematic import Schematic

test_folder = os.path.dirname(os.path.realpath(__file__))
kicad_folder = os.path.join(test_folder, "kicad_projects/kicad-test-files")


kicad_sch_files = []
kicad_pcb_files = []
for root, dirs, files in os.walk(kicad_folder):
    for file in files:
        path = os.path.join(root, file)
        if file.endswith(".kicad_sch"):
            kicad_sch_files.append(path)
        elif file.endswith(".kicad_pcb"):
            kicad_pcb_files.append(path)


@pytest.mark.parametrize("sch_path", kicad_sch_files)
@pytest.mark.long_running
def test_parse_all_sch(sch_path):
    with open(sch_path, encoding="utf-8") as f:
        try:
            sch = from_str(f.read())
        except (VersionError, MisconfiguredProjectError, EOFError) as e:
            pytest.skip(f"skipping {sch_path} due to: {e}")
        else:
            assert isinstance(sch, Schematic)


@pytest.mark.parametrize("pcb_path", kicad_pcb_files)
@pytest.mark.long_running
def test_parse_all_pcb(pcb_path):
    with open(pcb_path, encoding="utf-8") as f:
        try:
            pcb = from_str(f.read())
        except (VersionError, MisconfiguredProjectError, EOFError) as e:
            pytest.skip(f"skipping {pcb_path} due to: {e}")
        else:
            assert isinstance(pcb, Pcb)
