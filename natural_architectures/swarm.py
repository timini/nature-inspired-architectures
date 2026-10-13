"""Local success contacts regulate departures in a seeded worker simulation."""

from dataclasses import dataclass
import random


@dataclass
class Worker:
    remaining: int = 0
    signal: float = 0.0

    def contact(self) -> None:
        self.signal = min(1.0, self.signal + 0.5)

    def wants_work(self, rng: random.Random) -> bool:
        # Baseline exploration prevents silence becoming permanent inactivity.
        return rng.random() < min(1.0, 0.03 + self.signal)


def simulate(success_probability: float, seed: int = 7, ticks: int = 600,
             population: int = 20) -> dict:
    if not 0 <= success_probability <= 1 or ticks < 1 or population < 2:
        raise ValueError("invalid environment or simulation size")
    rng = random.Random(seed)
    workers = [Worker() for _ in range(population)]
    launches = successes = peak_busy = 0
    for _ in range(ticks):
        contacts = []
        for index, worker in enumerate(workers):
            worker.signal *= 0.7
            if worker.remaining:
                worker.remaining -= 1
                if rng.random() < success_probability:
                    worker.remaining = 0
                    successes += 1
                    # The simulator delivers local encounters; workers cannot
                    # inspect the environment probability or a global counter.
                    other = rng.randrange(population - 1)
                    contacts.append(other if other < index else other + 1)
            elif worker.wants_work(rng):
                worker.remaining = 8
                launches += 1
        for index in contacts:
            workers[index].contact()
        peak_busy = max(peak_busy, sum(w.remaining > 0 for w in workers))
    return {"launches": launches, "successes": successes, "peak_busy": peak_busy}


def demo() -> dict:
    return {"scarce": simulate(0.01), "abundant": simulate(0.5),
            "no_success": simulate(0.0)}
