import ast
import json
from pathlib import Path
import unittest

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = json.loads((ROOT / "03_pareto_superiority_90_60.ipynb").read_text())
namespace = {"np": np, "pd": pd}
for cell in NOTEBOOK["cells"]:
    if cell["cell_type"] != "code":
        continue
    definitions = [node for node in ast.parse("".join(cell["source"])).body
                   if isinstance(node, ast.FunctionDef)
                   and node.name in {"summary_metrics", "format_summary", "paired_circular_bootstrap"}]
    exec(compile(ast.Module(body=definitions, type_ignores=[]), "notebook", "exec"), namespace)


class ParetoMetricsTests(unittest.TestCase):
    def setUp(self):
        self.dates = pd.date_range("2020-01-31", periods=4, freq="ME")

    def test_drawdown_metrics_use_all_months_but_not_initial_date(self):
        wealth = pd.Series([0.9, 0.8, 1.0, 0.7], index=self.dates)
        previous = pd.Series([1.0, 0.9, 0.8, 1.0], index=self.dates)
        returns = (wealth / previous - 1).to_frame("test")
        metrics = namespace["summary_metrics"](returns, pd.Series(0.0, index=self.dates))
        expected = np.sqrt((0.1 ** 2 + 0.2 ** 2 + 0.0 ** 2 + 0.3 ** 2) / 4)
        self.assertAlmostEqual(metrics.loc["test", "Ulcer index"], expected)
        self.assertAlmostEqual(metrics.loc["test", "Average drawdown"], -0.15)
        self.assertEqual(namespace["format_summary"](metrics).loc["test", "Average drawdown"], "-15.00%")
        self.assertAlmostEqual(metrics.loc["test", "Max drawdown"], -0.3)
        self.assertEqual(namespace["format_summary"](metrics).loc["test", "Ulcer index"], "18.71%")

    def test_ulcer_index_is_zero_for_monotonic_wealth(self):
        returns = pd.DataFrame({"test": [0.01, 0.02, 0.0, 0.03]}, index=self.dates)
        metrics = namespace["summary_metrics"](returns, pd.Series(0.0, index=self.dates))
        self.assertEqual(metrics.loc["test", "Ulcer index"], 0.0)
        self.assertEqual(metrics.loc["test", "Average drawdown"], 0.0)

    def test_average_drawdown_weights_months_not_episodes(self):
        dates = pd.date_range("2020-01-31", periods=6, freq="ME")
        wealth = pd.Series([0.9, 0.8, 0.7, 1.0, 0.9, 0.8], index=dates)
        previous = wealth.shift(1, fill_value=1.0)
        returns = (wealth / previous - 1).to_frame("test")
        metrics = namespace["summary_metrics"](returns, pd.Series(0.0, index=dates))
        self.assertAlmostEqual(metrics.loc["test", "Average drawdown"], -0.15)

    def test_bootstrap_preserves_pairing_and_is_reproducible(self):
        values = [0.1, -0.1, 0.2, -0.2]
        paired = pd.DataFrame({"model": values, "benchmark": values}, index=self.dates)
        result = namespace["paired_circular_bootstrap"](paired, 100, (1, 2), 7)
        np.testing.assert_allclose(result, 0.0)
        paired["benchmark"] = 0.0
        first = namespace["paired_circular_bootstrap"](paired, 100, (1, 2), 7)
        second = namespace["paired_circular_bootstrap"](paired, 100, (1, 2), 7)
        pd.testing.assert_frame_equal(first, second)

    def test_bootstrap_constant_returns_have_known_cagr_difference(self):
        paired = pd.DataFrame({"model": 0.01, "benchmark": 0.005}, index=self.dates)
        result = namespace["paired_circular_bootstrap"](paired, 100, (1, 3), 7)
        np.testing.assert_allclose(result, 1.01 ** 12 - 1.005 ** 12)

    def test_bootstrap_rejects_missing_or_invalid_returns_and_parameters(self):
        paired = pd.DataFrame({"model": 0.01, "benchmark": 0.005}, index=self.dates)
        for invalid in [paired.assign(model=np.nan), paired.assign(model=-1), paired[["model"]]]:
            with self.assertRaises(ValueError):
                namespace["paired_circular_bootstrap"](invalid, 100, (1,), 7)
        for resamples, blocks in [(0, (1,)), (100, (0,)), (100, (5,)), (100, ())]:
            with self.assertRaises(ValueError):
                namespace["paired_circular_bootstrap"](paired, resamples, blocks, 7)

    def test_relative_wealth_uses_common_initial_capital(self):
        returns = pd.DataFrame({"model": [0.1, -0.1, 0.2, 0.0],
                                "60/40": [0.05, -0.05, 0.1, 0.0]}, index=self.dates)
        wealth = 100000 * (1 + returns).cumprod()
        wealth.loc[self.dates[0] - pd.offsets.MonthEnd(1)] = 100000
        wealth = wealth.sort_index()
        relative = wealth.div(wealth["60/40"], axis=0)
        np.testing.assert_allclose(relative["60/40"], 1.0)
        self.assertEqual(relative["model"].iloc[0], 1.0)
        expected = (1 + returns["model"]).prod() / (1 + returns["60/40"]).prod()
        self.assertAlmostEqual(relative["model"].iloc[-1], expected)


if __name__ == "__main__":
    unittest.main()
