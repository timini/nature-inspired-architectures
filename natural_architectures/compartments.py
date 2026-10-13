"""Bounded compartments isolate overload and expected processing failures."""

from collections import deque
from collections.abc import Callable
from dataclasses import dataclass, field


class RejectedJob(Exception):
    """An expected per-job failure, rather than a programming error."""


@dataclass
class Compartment:
    capacity: int
    handler: Callable[[str], str]
    pending: deque[str] = field(default_factory=deque, init=False)
    completed: list[str] = field(default_factory=list, init=False)
    failed: list[str] = field(default_factory=list, init=False)
    rejected: int = field(default=0, init=False)

    def __post_init__(self) -> None:
        if self.capacity < 1:
            raise ValueError("capacity must be positive")

    def submit(self, job: str) -> bool:
        if len(self.pending) >= self.capacity:
            self.rejected += 1
            return False
        self.pending.append(job)
        return True

    def tick(self) -> None:
        """Spend at most one unit of this compartment's execution budget."""
        if self.pending:
            job = self.pending.popleft()
            try:
                self.completed.append(self.handler(job))
            except RejectedJob:
                self.failed.append(job)


def demo() -> dict:
    def process(job: str) -> str:
        if job == "bad":
            raise RejectedJob(job)
        return job.upper()

    billing = Compartment(2, process)
    analytics = Compartment(2, process)
    for job in ["bad", "report", "overflow"]:
        analytics.submit(job)
    billing.submit("invoice")
    for _ in range(2):
        billing.tick()
        analytics.tick()
    return {"billing": billing.completed, "analytics": analytics.completed,
            "failed": analytics.failed, "overload_rejections": analytics.rejected}
