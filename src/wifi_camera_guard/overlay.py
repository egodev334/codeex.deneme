from dataclasses import dataclass


@dataclass
class OverlayStatus:
    rssi_dbm: float
    source: str
    obstacle_likely: bool


def status_from_rssi(rssi_dbm: float, source: str, threshold: float) -> OverlayStatus:
    obstacle_likely = rssi_dbm < threshold
    return OverlayStatus(rssi_dbm=rssi_dbm, source=source, obstacle_likely=obstacle_likely)
