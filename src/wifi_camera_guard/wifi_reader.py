import math
import shutil
import subprocess
import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class RssiSample:
    value_dbm: float
    source: str


def _parse_iw_link(output: str) -> Optional[float]:
    for line in output.splitlines():
        if "signal:" in line:
            parts = line.strip().split()
            if len(parts) >= 2:
                try:
                    return float(parts[1])
                except ValueError:
                    return None
    return None


def read_rssi_from_iw(interface: str) -> Optional[float]:
    if not shutil.which("iw"):
        return None
    try:
        result = subprocess.run(
            ["iw", "dev", interface, "link"],
            check=False,
            capture_output=True,
            text=True,
            timeout=2,
        )
    except (subprocess.SubprocessError, OSError):
        return None

    if result.returncode != 0:
        return None

    return _parse_iw_link(result.stdout)


def simulated_rssi(t: float) -> float:
    return -55.0 + 15.0 * math.sin(t / 4.0)


def sample_rssi(interface: Optional[str]) -> RssiSample:
    if interface:
        value = read_rssi_from_iw(interface)
        if value is not None:
            return RssiSample(value_dbm=value, source=f"iw:{interface}")
    simulated = simulated_rssi(time.time())
    return RssiSample(value_dbm=simulated, source="simulated")
