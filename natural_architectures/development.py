"""Immutable recipes recombine a conserved set of processing capabilities."""

from collections.abc import Callable
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Document:
    text: str
    words: int | None = None


Documents = tuple[Document, ...]
Stage = Callable[[Documents], Documents]


def normalise(documents: Documents) -> Documents:
    # Any edit invalidates a previously derived word count.
    return tuple(replace(d, text=" ".join(d.text.split()), words=None) for d in documents)


def drop_empty(documents: Documents) -> Documents:
    return tuple(d for d in documents if d.text.strip())


def count_words(documents: Documents) -> Documents:
    return tuple(replace(d, words=len(d.text.split())) for d in documents)


def longest_first(documents: Documents) -> Documents:
    if any(d.words is None for d in documents):
        raise ValueError("count_words must precede longest_first")
    return tuple(sorted(documents, key=lambda d: d.words, reverse=True))


@dataclass(frozen=True)
class Recipe:
    name: str
    stages: tuple[str, ...]

    def run(self, documents: Documents, registry: dict[str, Stage]) -> Documents:
        # Validate the whole plan before any stage executes.
        unknown = set(self.stages) - registry.keys()
        if unknown:
            raise ValueError(f"unknown stages: {sorted(unknown)}")
        for stage in self.stages:
            documents = registry[stage](documents)
        return documents


def demo() -> dict:
    from dataclasses import asdict

    registry = {fn.__name__: fn for fn in (normalise, drop_empty, count_words, longest_first)}
    documents = (Document("  small  "), Document(""), Document("a longer document"))
    recipes = [Recipe("preview-v1", ("normalise", "drop_empty")),
               Recipe("index-v1", ("normalise", "drop_empty", "count_words", "longest_first"))]
    return {r.name: [asdict(d) for d in r.run(documents, registry)] for r in recipes}
