"""Many input formats share a small, versioned canonical event."""

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Temperature:
    sensor: str
    celsius: float
    version: int = 1

    def __post_init__(self) -> None:
        if not isinstance(self.sensor, str) or not self.sensor.strip():
            raise ValueError("sensor must have a nonempty identifier")
        if self.version != 1 or not math.isfinite(self.celsius):
            raise ValueError("unsupported schema or non-finite temperature")


def from_celsius(payload: dict) -> Temperature:
    return Temperature(payload["sensor"], float(payload["celsius"]))


def from_fahrenheit(payload: dict) -> Temperature:
    return Temperature(payload["device"], (float(payload["fahrenheit"]) - 32) * 5 / 9)


def alert(event: Temperature) -> dict:
    return {"sensor": event.sensor, "overheating": event.celsius >= 30}


def display(event: Temperature) -> str:
    return f"{event.sensor}: {event.celsius:.1f} C"


def demo() -> dict:
    events = [from_celsius({"sensor": "rack-a", "celsius": 35}),
              from_fahrenheit({"device": "rack-b", "fahrenheit": 95})]
    return {"alerts": [alert(e) for e in events], "display": [display(e) for e in events]}
