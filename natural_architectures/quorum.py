"""A local, decaying signal field gates collective activity; not consensus."""

import math


class SignalField:
    def __init__(self, population: int, decay: float = 0.2, diffusion: float = 0.4,
                 on: float = 2.0, off: float = 1.0):
        if population < 3 or not all(math.isfinite(v) for v in (decay, diffusion, on, off)):
            raise ValueError("need at least three nodes and finite parameters")
        if not (0 < decay <= 1 and 0 <= diffusion <= 1 and 0 <= off < on):
            raise ValueError("invalid decay, diffusion or hysteresis thresholds")
        self.decay, self.diffusion, self.on, self.off = decay, diffusion, on, off
        self.signal = [0.0] * population
        self.active = [False] * population

    def step(self, emitting: list[bool]) -> list[bool]:
        n = len(self.signal)
        if len(emitting) != n or any(not isinstance(e, bool) for e in emitting):
            raise ValueError("one boolean emission state per node is required")
        old = self.signal
        # Synchronous update: every node sees the preceding tick's neighbours.
        self.signal = [(1 - self.decay) * (
            (1 - self.diffusion) * old[i]
            + self.diffusion * (old[(i - 1) % n] + old[(i + 1) % n]) / 2
        ) + float(emitting[i]) for i in range(n)]
        self.active = [value > self.off if active else value >= self.on
                       for value, active in zip(self.signal, self.active)]
        return self.active.copy()


def demo() -> dict:
    field = SignalField(12)
    phases = {}
    for label, emitting in [("sparse", [True] + [False] * 11),
                            ("dense", [True] * 12), ("departed", [False] * 12)]:
        for _ in range(40):
            field.step(emitting)
        phases[label] = {"active_nodes": sum(field.active),
                         "mean_signal": round(sum(field.signal) / 12, 3)}
    return phases
