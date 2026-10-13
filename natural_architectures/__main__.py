"""Run one reference example, or the whole catalogue, without dependencies."""

import argparse
import importlib
import json

PATTERNS = ("compartments", "bow_tie", "feedback", "persistence", "development",
            "degeneracy", "swarm", "quorum")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pattern", choices=("all", *PATTERNS), nargs="?", default="all")
    args = parser.parse_args()
    selected = PATTERNS if args.pattern == "all" else (args.pattern,)
    output = {name: importlib.import_module(f"natural_architectures.{name}").demo()
              for name in selected}
    print(json.dumps(output, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
