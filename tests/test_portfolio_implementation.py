from pathlib import Path
import ast
import json
import unittest

import numpy as np
import pandas as pd

from helpers.portfolio_implementation import rebalance_portfolio, splice_actual_returns


class PortfolioImplementationTests(unittest.TestCase):
    def setUp(self):
        self.dates = pd.date_range("2020-01-31", periods=3, freq="ME")

    def test_flat_assets_charge_entry_once_not_every_month(self):
        inputs = pd.DataFrame(0.0, index=self.dates, columns=["stocks", "bonds"])
        result = rebalance_portfolio(inputs, [0.6, 0.4], [0.001, 0.002], (2,))
        expected_entry = 1 / (1 + 0.6 * 0.001 + 0.4 * 0.002) - 1
        np.testing.assert_allclose(result, [expected_entry, 0, 0], atol=1e-12)

    def test_single_asset_buy_and_hold_has_no_quarterly_turnover(self):
        inputs = pd.DataFrame({"stock": [0.1, -0.2, 0.05]}, index=self.dates)
        result = rebalance_portfolio(inputs, [1.0], [0.001], (1, 2, 3))
        expected = inputs["stock"].copy()
        expected.iloc[0] = 1.1 / 1.001 - 1
        np.testing.assert_allclose(result, expected, atol=1e-12)

    def test_rebalance_cost_satisfies_post_cost_targets(self):
        inputs = pd.DataFrame({"stock": [0.1, 0, 0], "bond": [-0.1, 0, 0]}, index=self.dates)
        result = rebalance_portfolio(inputs, [0.6, 0.4], [0.01, 0.02], (2,))
        high = 0.6 * 1.1 / 1.014
        low = 0.4 * 0.9 / 1.014
        before = high + low
        after = (before - 0.01 * high + 0.02 * low) / 1.002
        self.assertAlmostEqual(result.iloc[1], after / before - 1, places=12)
        self.assertAlmostEqual((1 + result).prod(), after, places=12)

    def test_liquidation_charged_once_without_final_rebalance(self):
        inputs = pd.DataFrame({"stock": [0.1, 0, 0], "bond": [-0.1, 0, 0]}, index=self.dates)
        result = rebalance_portfolio(inputs, [0.6, 0.4], [0.01, 0.02], (3,), liquidate=True)
        expected = (0.6 * 1.1 * 0.99 + 0.4 * 0.9 * 0.98) / 1.014
        self.assertAlmostEqual((1 + result).prod(), expected)

    def test_zero_costs_preserve_quarterly_drift(self):
        inputs = pd.DataFrame({"stock": [1.0, 0.1, 0.1], "mf": [0, 0, 0]}, index=self.dates)
        result = rebalance_portfolio(inputs, [0.66, 0.34], [0, 0], (2,))
        np.testing.assert_allclose(result, [0.66, 1.32 / 1.66 * 0.1, 0.066])

    def test_higher_trading_cost_reduces_flat_portfolio_wealth(self):
        inputs = pd.DataFrame(0.0, index=self.dates, columns=["stock", "bond"])
        low = rebalance_portfolio(inputs, [0.6, 0.4], [0.001, 0.002], (2,))
        high = rebalance_portfolio(inputs, [0.6, 0.4], [0.002, 0.004], (2,))
        self.assertLess((1 + high).prod(), (1 + low).prod())

    def test_invalid_inputs_rejected(self):
        inputs = pd.DataFrame(0.0, index=self.dates, columns=["stock", "bond"])
        for weights, costs in [([0.6, 0.3], [0, 0]), ([1.1, -0.1], [0, 0]),
                               ([0.6, 0.4], [0, -0.01]), ([0.6, 0.4], [0, 0.1])]:
            with self.assertRaises(ValueError):
                rebalance_portfolio(inputs, weights, costs, (2,))

    def test_actual_returns_replace_without_fee_adjustment(self):
        proxy = pd.Series([0.01, 0.02, 0.03], index=self.dates)
        actual = pd.Series([0.04, 0.05], index=self.dates[1:])
        result = splice_actual_returns(proxy, actual)
        np.testing.assert_allclose(result, [0.01, 0.04, 0.05])
        pd.testing.assert_series_equal(splice_actual_returns(proxy, actual, False), proxy)

    def test_actual_gap_or_stale_end_rejected(self):
        proxy = pd.Series(0.0, index=self.dates)
        with self.assertRaises(ValueError):
            splice_actual_returns(proxy, pd.Series(0.1, index=self.dates[[0, 2]]))
        with self.assertRaises(ValueError):
            splice_actual_returns(proxy, pd.Series([0.1], index=self.dates[1:2]))

    def test_two_thirds_core_matches_sixty_forty_notionals(self):
        notebook = json.loads((Path(__file__).resolve().parents[1] / "03_pareto_superiority_90_60.ipynb").read_text())
        namespace = {}
        exec("".join(notebook["cells"][1]["source"]), namespace)
        self.assertAlmostEqual(namespace["core_weight"] * namespace["core_equity_weight"], 0.6)
        self.assertAlmostEqual(namespace["core_weight"] * namespace["core_bond_weight"], 0.4)
        self.assertFalse(namespace["use_cta_gross_up"])
        for cell in notebook["cells"]:
            if cell["cell_type"] == "code":
                ast.parse("".join(cell["source"]))


if __name__ == "__main__":
    unittest.main()
