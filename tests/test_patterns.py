import math
import random
import unittest

from natural_architectures.bow_tie import Temperature, alert, from_celsius, from_fahrenheit
from natural_architectures.compartments import Compartment, RejectedJob
from natural_architectures.development import (
    Document, Recipe, count_words, drop_empty, longest_first, normalise,
)
from natural_architectures.degeneracy import (
    SolverUnavailable, fewest_hops, route, valid_route, weighted_route,
)
from natural_architectures.feedback import IntegralController, simulate as control_simulate
from natural_architectures.persistence import PersistenceGate
from natural_architectures.quorum import SignalField
from natural_architectures.swarm import simulate as swarm_simulate


class CompartmentTests(unittest.TestCase):
    def test_overload_and_expected_failure_are_contained(self):
        def reject(job):
            raise RejectedJob(job)
        broken, healthy = Compartment(1, reject), Compartment(1, str.upper)
        self.assertTrue(broken.submit("bad"))
        self.assertFalse(broken.submit("overflow"))
        healthy.submit("invoice")
        broken.tick()
        healthy.tick()
        self.assertEqual(healthy.completed, ["INVOICE"])
        self.assertEqual(broken.failed, ["bad"])
        self.assertEqual(len(broken.pending), 0)

    def test_programming_errors_are_visible(self):
        def bug(job):
            raise TypeError("bug")
        compartment = Compartment(1, bug)
        compartment.submit("x")
        with self.assertRaises(TypeError):
            compartment.tick()

    def test_capacity_reopens_after_processing(self):
        compartment = Compartment(1, str.upper)
        compartment.submit("a")
        compartment.tick()
        self.assertTrue(compartment.submit("b"))


class BowTieTests(unittest.TestCase):
    def test_equivalent_inputs_have_identical_downstream_meaning(self):
        c = from_celsius({"sensor": "a", "celsius": 35})
        f = from_fahrenheit({"device": "a", "fahrenheit": 95})
        self.assertEqual(c, f)
        self.assertEqual(alert(c), alert(f))

    def test_boundary_validation(self):
        for value in (math.nan, math.inf, -math.inf):
            with self.assertRaises(ValueError):
                Temperature("a", value)
        with self.assertRaises(ValueError):
            Temperature("a", 20, version=2)
        with self.assertRaises(ValueError):
            Temperature(" ", 20)


class FeedbackTests(unittest.TestCase):
    def test_recovers_after_demand_step(self):
        history = control_simulate()
        self.assertGreater(history[60]["utilisation"], 1)
        self.assertAlmostEqual(history[59]["utilisation"], 0.7, places=4)
        self.assertAlmostEqual(history[-1]["utilisation"], 0.7, places=4)
        self.assertTrue(all(1 <= row["capacity"] <= 20 for row in history))

    def test_saturation_does_not_hide_unbounded_integral(self):
        controller = IntegralController()
        for _ in range(100):
            controller.update(100)
        self.assertEqual(controller.capacity, controller.maximum)
        controller.update(0)
        self.assertLess(controller.capacity, controller.maximum)

    def test_invalid_measurements_rejected(self):
        for value in (-1, math.nan, math.inf):
            with self.assertRaises(ValueError):
                IntegralController().update(value)


class PersistenceTests(unittest.TestCase):
    def test_glitches_reset_and_shutdown_is_immediate(self):
        gate = PersistenceGate(3)
        values = [True, False, True, True, True, False]
        self.assertEqual([gate.sample(v) for v in values],
                         [False, False, False, False, True, False])

    def test_exhaustive_short_sequences(self):
        import itertools
        for samples in itertools.product((False, True), repeat=7):
            gate = PersistenceGate(3)
            for i, sample in enumerate(samples):
                expected = i >= 2 and all(samples[i-2:i+1])
                self.assertEqual(gate.sample(sample), expected)


class DevelopmentTests(unittest.TestCase):
    def test_recomposition_without_mutating_inputs(self):
        original = (Document("  a b  "), Document(" "), Document("c"))
        registry = {f.__name__: f for f in (normalise, drop_empty, count_words, longest_first)}
        result = Recipe("index-v1", tuple(registry)).run(original, registry)
        self.assertEqual(result, (Document("a b", 2), Document("c", 1)))
        self.assertEqual(original[0], Document("  a b  "))

    def test_unknown_stages_rejected_before_execution(self):
        calls = []
        with self.assertRaises(ValueError):
            Recipe("bad", ("first", "unknown")).run((), {"first": lambda d: calls.append(d)})
        self.assertEqual(calls, [])

    def test_invalid_order_and_stale_derived_values(self):
        with self.assertRaises(ValueError):
            longest_first((Document("a"),))
        self.assertIsNone(normalise((Document("a", 999),))[0].words)


class DegeneracyTests(unittest.TestCase):
    def setUp(self):
        self.graph = {"a": {"b": 1, "d": 10}, "b": {"c": 1}, "c": {"d": 1}, "d": {}}

    def test_diverse_solvers_trade_quality_for_availability(self):
        normal = route(self.graph, "a", "d")
        fallback = route(self.graph, "a", "d", (fewest_hops,))
        self.assertEqual(normal["cost"], 3)
        self.assertEqual(fallback["cost"], 10)
        for result in (normal, fallback):
            self.assertTrue(valid_route(self.graph, result["path"], "a", "d"))

    def test_expected_failure_and_invalid_output_trigger_fallback(self):
        def offline(*args):
            raise SolverUnavailable()
        def invalid(*args):
            return ["a", "missing", "d"]
        for failed in (offline, invalid):
            result = route(self.graph, "a", "d", (failed, fewest_hops))
            self.assertEqual(result["solver"], "fewest_hops")

    def test_no_path_and_invalid_graph_fail_explicitly(self):
        with self.assertRaises(SolverUnavailable):
            route(self.graph, "d", "a")
        for graph in ({"a": {"b": 1}}, {"a": {"a": -1}}, {"a": {"a": math.nan}}):
            with self.assertRaises(ValueError):
                route(graph, "a", "a")

    def test_weighted_route_against_exhaustive_small_graphs(self):
        # Compare against exhaustive simple paths, not another Dijkstra copy.
        rng = random.Random(19)
        for _ in range(30):
            graph = {str(i): {} for i in range(5)}
            for a in graph:
                for b in graph:
                    if a != b and rng.random() < 0.45:
                        graph[a][b] = rng.randrange(0, 8)
            costs = []
            def enumerate_paths(node, seen, cost):
                if node == "4":
                    costs.append(cost)
                else:
                    for other, weight in graph[node].items():
                        if other not in seen:
                            enumerate_paths(other, seen | {other}, cost + weight)
            enumerate_paths("0", {"0"}, 0)
            if costs:
                self.assertEqual(route(graph, "0", "4", (weighted_route,))["cost"], min(costs))
            else:
                with self.assertRaises(SolverUnavailable):
                    route(graph, "0", "4")


class SwarmTests(unittest.TestCase):
    def test_reproducible_and_resource_bounded(self):
        first = swarm_simulate(0.5)
        self.assertEqual(first, swarm_simulate(0.5))
        self.assertLessEqual(first["successes"], first["launches"])
        self.assertLessEqual(first["peak_busy"], 20)

    def test_richer_environment_increases_departures_across_seeds(self):
        scarce = sum(swarm_simulate(0.01, seed=s)["launches"] for s in range(10))
        abundant = sum(swarm_simulate(0.5, seed=s)["launches"] for s in range(10))
        self.assertGreater(abundant, scarce * 2)

    def test_no_success_preserves_exploration_without_false_completions(self):
        result = swarm_simulate(0)
        self.assertEqual(result["successes"], 0)
        self.assertGreater(result["launches"], 0)


class QuorumTests(unittest.TestCase):
    def test_density_response_and_decay_after_departure(self):
        field = SignalField(12)
        for _ in range(40):
            field.step([True] + [False] * 11)
        self.assertLess(sum(field.active), 12)
        for _ in range(40):
            field.step([True] * 12)
        self.assertTrue(all(field.active))
        self.assertTrue(all(0 <= value <= 5 for value in field.signal))
        for _ in range(40):
            field.step([False] * 12)
        self.assertFalse(any(field.active))

    def test_local_signal_does_not_immediately_reach_distant_nodes(self):
        field = SignalField(12)
        field.step([True] + [False] * 11)
        field.step([False] * 12)
        self.assertGreater(field.signal[1], 0)
        self.assertEqual(field.signal[6], 0)

    def test_hysteresis_retains_state_between_thresholds(self):
        field = SignalField(3, decay=0.5, diffusion=0)
        field.signal = [3.0, 3.0, 3.0]
        field.active = [True, False, True]
        self.assertEqual(field.step([False] * 3), [True, False, True])

    def test_bad_inputs_do_not_modify_state(self):
        field = SignalField(3)
        with self.assertRaises(ValueError):
            field.step([True])
        self.assertEqual(field.signal, [0, 0, 0])


if __name__ == "__main__":
    unittest.main()
