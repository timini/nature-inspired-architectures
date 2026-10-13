"""A direct signal AND a delayed signal reject short-lived activation."""

from dataclasses import dataclass, field


@dataclass
class PersistenceGate:
    required: int = 3
    streak: int = field(default=0, init=False)

    def __post_init__(self) -> None:
        if self.required < 1:
            raise ValueError("required samples must be positive")

    def sample(self, high: bool) -> bool:
        if not isinstance(high, bool):
            raise TypeError("sample must be boolean")
        self.streak = min(self.required, self.streak + 1) if high else 0
        return high and self.streak >= self.required


def demo() -> dict:
    gate = PersistenceGate(3)
    samples = [False, True, False, True, True, True, True, False]
    return {"input": samples, "output": [gate.sample(s) for s in samples]}
