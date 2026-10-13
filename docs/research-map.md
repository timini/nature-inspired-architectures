# Research map

[Catalogue](../README.md)

This project began with the question of whether biological evolution has produced architectures that manage complexity across levels of organisation. There is substantial relevant research, but it is distributed across fields. This is a curated introduction, not a systematic literature review or a survey of the latest work in every field.

## Questions that should be kept separate

1. **Organisation:** How do many interacting parts produce coherent behaviour?
2. **Robustness:** Which functions persist when parts fail or conditions change?
3. **Evolvability:** Which structures permit heritable change while retaining viability?
4. **Evolutionary origin:** Under what selection pressures or other processes did a structure arise?

Observing a useful structure does not establish why it evolved. A computational evolutionary model establishes a result under its assumptions, not a universal explanation. The distinction matters when using biological evidence to motivate engineering choices. [Kashtan and Alon](../references/README.md#kashtan2005) investigate modularly varying goals in models; [Gerhart and Kirschner](../references/README.md#gerhart2007) propose how properties of conserved processes facilitate viable variation.

## Across biological scales

| Scale | Research questions and mechanisms | Starting sources | Implemented examples |
| --- | --- | --- | --- |
| Molecular | How do interacting components discriminate, regulate and combine into functions? | [Hartwell et al.](../references/README.md#hartwell1999), [Alon](../references/README.md#alon2007), [Hopfield](../references/README.md#hopfield1974) | Compartments; persistence filter |
| Cellular | How are diverse inputs processed, responses regulated and internal functions stabilised? | [Csete and Doyle](../references/README.md#csete2004), [Yi et al.](../references/README.md#yi2000), [Kitano](../references/README.md#kitano2004) | Bow-tie core; integral feedback |
| Organism and development | How can stable capabilities produce varied forms and functions? | [Gerhart and Kirschner](../references/README.md#gerhart2007), [Edelman and Gally](../references/README.md#edelman2001) | Reconfigurable capabilities; diverse fallbacks |
| Populations and colonies | How do local interactions produce collective regulation? | [Prabhakar et al.](../references/README.md#prabhakar2012), [Gordon](../references/README.md#gordon2016), [Waters and Bassler](../references/README.md#waters2005) | Local worker activation; quorum signalling |
| Ecological communities | How does interaction structure affect persistence and disruption? | [Stouffer and Bascompte](../references/README.md#stouffer2011) | Compartment analogy; no ecosystem simulator |
| Transitions between levels | How do independent entities become a higher-level individual? | [West et al.](../references/README.md#west2015) | Research framing; no implemented transition model |

These levels overlap. The same general pattern can occur at different scales, while its mechanisms and constraints differ. An ecosystem is not assumed to optimise one shared objective or to be selected as a single organism.

## Foundational connections to software

**Hierarchy and near-decomposability.** [Simon (1962)](../references/README.md#simon1962) explains why stable intermediate assemblies and relatively stronger within-component interactions can matter to the formation and description of complex systems. This is a theoretical framework; it does not mean every biological interaction respects a clean layer boundary.

**Robustness and fragility.** [Csete and Doyle (2002)](../references/README.md#csete2002) compare biological and engineered organisation, including protocols, feedback and the possibility of cascading failures. [Kitano (2004)](../references/README.md#kitano2004) reviews several mechanisms supporting biological robustness. Robustness must always be specified relative to a function and a disturbance.

**New levels of individuality.** [West et al. (2015)](../references/README.md#west2015) discuss cooperation, division of labour, communication and reduced internal conflict. A possible software question is when independently managed services can operate as a coherent larger system. That analogy requires its own model of incentives and failure; deploying services together is not itself an evolutionary transition.

**Computing from local interactions.** [Abelson et al. (2000)](../references/README.md#abelson2000) and the [MIT Amorphous Computing project](../references/README.md#mitamorphous) investigate coordination among many unreliable, irregularly connected computational elements. This is an explicit bridge to biologically inspired computing, beyond metaphorical comparisons.

## Further patterns worth investigating

These directions have references but no implementation in the initial eight-pattern catalogue:

- **Kinetic proofreading:** [Hopfield (1974)](../references/README.md#hopfield1974) proposes enhanced molecular discrimination through driven reaction stages. A translation should retain the distinction between independent evidence, repeated checks and energetic or time costs; repeating the same validation is not automatically equivalent.
- **Self-organising development:** [Toda et al. (2018)](../references/README.md#toda2018) experimentally programme multicellular structures with synthetic cell signalling. A future software example could investigate local differentiation and repair. The experiment is engineered biology, not proof of a naturally selected architecture.
- **Evolving modularity:** reproduce a small version of the changing-goals experiment in [Kashtan and Alon (2005)](../references/README.md#kashtan2005), then compare evolved structure against hand-designed modular and monolithic baselines.
- **Conflict control in cooperative groups:** use [West et al. (2015)](../references/README.md#west2015) to motivate a model with explicit local and collective incentives, rather than equating cooperation with consensus.

## Interpreting the catalogue

Many translations resemble existing software techniques: bulkheads, canonical models, feedback controllers, debouncing, pipelines and fallback strategies. No novelty is claimed for those techniques. The contribution of this catalogue is to make the biological mechanism, engineering interpretation, trade-offs and testable hypotheses explicit and traceable to sources.
