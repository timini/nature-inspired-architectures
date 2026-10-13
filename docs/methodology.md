# Methodology

[Catalogue](../README.md)

## Three distinct claims

| Claim | Required support | Example |
| --- | --- | --- |
| A mechanism exists in biology | A source describing the observation, experiment or model, with its scope stated | Harvester-ant contacts affect departures |
| A mechanism can be represented in software | A precise mapping and an implementation | Local success contacts affect simulated worker activation |
| The software design improves an outcome | A baseline, workload, metric and comparative experiment | Higher throughput at the same cost under a specified failure model |

The initial catalogue supplies references and runnable demonstrations for the first two claims. Behavioural tests establish properties of the included examples. They do not establish production superiority, evolutionary origin or biological fidelity. Suggested comparative experiments are labelled as proposals, not completed benchmarks.

## Pattern selection

Choose a mechanism that can be stated without anthropomorphising evolution. Identify the units, their state, their interaction rules, the information they can access and the constraints they face. Name the function that remains useful under change. Prefer a small executable example that exposes the mechanism to a large framework that obscures it.

Distinguish topology from dynamics: the same connectivity can behave differently under different parameters, timing or interaction signs. Distinguish a hypothesis for evolutionary origin from evidence that a mechanism functions today. Do not infer that increasing complexity or global optimality is evolution’s objective.

## Citation policy

Every biological claim in a pattern must be traceable to a citation key in [references](../references/README.md). Keep the author list, title, year, venue, DOI when available, and a usable source URL in [metadata](../references/metadata.json) and [BibTeX](../references/references.bib). Do not invent a DOI for a source that lacks one.

Each reference includes its evidence type and what it supports here. Label conceptual syntheses, computational models, experiments and further reading distinctly. Preserve foundational references even when a pattern is reorganised. External tool documentation is linked in the development instructions separately from the biological bibliography.

The bibliography is metadata plus original annotations; it does not redistribute research papers, copied figures or article text. Diagram labels and mappings are original work. Accessed and checked dates refer to bibliographic records and accessible source material, not a claim of complete full-text review.

## Validation

The examples use fixed seeds and no remote services. Tests include overload and expected-failure injection, input rejection, exhaustive short signal sequences, route optimality against enumerated paths, demand-step recovery, local signal propagation and decay, and worker behaviour across multiple seeds.

The documentation checker validates local links, citation keys, catalogue coverage and diagram-source consistency. Mermaid CLI renders the editable sources into SVG; rendering and visual review are separate from Python tests. GitHub Actions runs Python tests and documentation checks on 3.11–3.14.

For a real deployment, extend the experiment to include resource limits, actual message transport, delays, loss, restart behaviour and the application’s correctness requirements. Derive these requirements from the use case rather than assuming that the biological analogy supplies them.
