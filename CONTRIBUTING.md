# Contributing a pattern

1. Identify a biological mechanism and primary or authoritative sources. State whether the evidence is experimental, theoretical, computational or a synthesis.
2. Add stable reference keys to all three files in `references/`. Record what each source supports and any important limitations.
3. Use an existing pattern page as the template: biological basis, problem, mapping, diagram, implementation, use cases, trade-offs, limits and validation.
4. Add a small standard-library implementation in `natural_architectures/`, with a `demo()` returning JSON-serialisable data. Register it in `__main__.py` and `catalogue.json`.
5. Add meaningful tests of the mechanism and its failure modes. Prefer invariants and comparisons against independent baselines to snapshots of internal implementation details.
6. Add a Mermaid source and rendered SVG using the [diagram instructions](diagrams/README.md). Dotted analogy edges must not be presented as biological causal claims.
7. Update the README catalogue and captured example output. Run the commands below.

```sh
python3 -m unittest discover -s tests -v
python3 -m natural_architectures all > examples/output.json
python3 scripts/check_docs.py
```

Keep evidence separate from engineering inference. Do not describe a simulator as a production service, a chemical quorum as consensus, or a mechanism’s usefulness as proof of its evolutionary origin. Avoid claiming novelty for established software techniques.
