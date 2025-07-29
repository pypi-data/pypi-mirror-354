import pathlib
import subprocess  # nosec
from dataclasses import dataclass
from shutil import which

from packaging.version import parse as parse_version


@dataclass
class Process:
    returncode: int
    stdout: str
    stderr: str


def get_kicad_cli_version():
    try:
        process = subprocess.run(
            [KICAD_CLI_EXECUTABLE, "--version"], capture_output=True, check=True
        )  # nosec
        return parse_version(process.stdout.decode().strip())
    except FileNotFoundError:
        return None


KICAD_CLI_EXECUTABLE = "kicad-cli"
MIN_KICAD_CLI_VERSION = parse_version("8.0.0")
kicad_cli_version = get_kicad_cli_version()
is_kicad_cli_in_path = which(KICAD_CLI_EXECUTABLE) is not None
is_supported_kicad_cli_version = (
    kicad_cli_version and kicad_cli_version >= MIN_KICAD_CLI_VERSION
)

is_configured = is_kicad_cli_in_path and is_supported_kicad_cli_version


def kicad_cli(command: list[str | pathlib.Path]):
    if not is_configured:
        raise RuntimeError(
            f"KiCad CLI is not configured. Make sure {KICAD_CLI_EXECUTABLE} "
            f"is in your PATH and is at least version {MIN_KICAD_CLI_VERSION}"
        )

    process = subprocess.run(
        [KICAD_CLI_EXECUTABLE] + command, capture_output=True, check=True
    )  # nosec
    stderr = "\n".join(
        [
            line.decode()
            for line in process.stderr.split(b"\n")
            if
            # kicad-cli lock file errors happen when we run tests in parallel but
            # don't affect anything we are doing
            line != b""
            and b"Invalid lock file" not in line
            and b"Failed to access lock" not in line
            and b"Failed to inspect the lock file" not in line
        ]
    )
    return Process(
        returncode=process.returncode,
        stdout=process.stdout.decode(),
        stderr=stderr,
    )
