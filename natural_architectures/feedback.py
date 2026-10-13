"""Integral feedback regulates a simplified service's utilisation."""

import math
from dataclasses import dataclass


@dataclass
class IntegralController:
    capacity: float = 6.0
    target: float = 0.7
    gain: float = 2.0
    minimum: float = 1.0
    maximum: float = 20.0

    def __post_init__(self) -> None:
        values = (self.capacity, self.target, self.gain, self.minimum, self.maximum)
        if not all(math.isfinite(v) for v in values):
            raise ValueError("parameters must be finite")
        if not (0 < self.minimum <= self.capacity <= self.maximum):
            raise ValueError("capacity must lie within positive bounds")
        if not (0 < self.target < 1) or self.gain <= 0:
            raise ValueError("target must be between 0 and 1; gain must be positive")

    def update(self, utilisation: float) -> float:
        if not math.isfinite(utilisation) or utilisation < 0:
            raise ValueError("utilisation must be finite and nonnegative")
        # The actuator value itself is the integral state. Clamping it avoids
        # accumulating an invisible, unbounded integral beyond actuator limits.
        self.capacity = min(self.maximum, max(
            self.minimum, self.capacity + self.gain * (utilisation - self.target)))
        return self.capacity


def simulate() -> list[dict]:
    controller = IntegralController()
    history = []
    for tick in range(240):
        demand = 3.0 if tick < 60 else 7.0
        utilisation = demand / controller.capacity
        history.append({"tick": tick, "demand": demand,
                        "capacity": controller.capacity, "utilisation": utilisation})
        controller.update(utilisation)
    return history


def demo() -> dict:
    history = simulate()
    return {"target_utilisation": 0.7,
            "samples": [{k: round(v, 4) if isinstance(v, float) else v
                         for k, v in history[i].items()} for i in (0, 59, 60, 100, 239)]}
