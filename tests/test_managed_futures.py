import ast
import json
from pathlib import Path
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd

from helpers.download_managed_futures_data import aqr_returns, barclay_monthly_returns, sg_monthly_returns
from helpers.portfolio_implementation import rebalance_portfolio

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = json.loads((ROOT / "03_pareto_superiority_90_60.ipynb").read_text())
FUNCTIONS = {"gross_up_cta", "summary_metrics"}
namespace = {"np": np, "pd": pd}
exec("".join(NOTEBOOK["cells"][1]["source"]), namespace)
for cell in NOTEBOOK["cells"]:
    if cell["cell_type"] == "code":
        tree = ast.parse("".join(cell["source"]))
        definitions = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in FUNCTIONS]
        exec(compile(ast.Module(body=definitions, type_ignores=[]), "notebook", "exec"), namespace)


class ManagedFuturesTests(unittest.TestCase):
    def setUp(self):
        self.dates = pd.date_range("2020-01-31", periods=4, freq="ME")

    def test_gross_up_inverts_monthly_fees_and_high_water_mark(self):
        gross = pd.Series([0.10, -0.20, 0.10, 0.30], index=self.dates)
        nav = high_water_mark = 1.0
        net = []
        for value in gross:
            before_incentive = nav * (1 + value - 0.02 / 12)
            end_nav = before_incentive - 0.20 * max(before_incentive - high_water_mark, 0)
            net.append(end_nav / nav - 1)
            nav = end_nav
            high_water_mark = max(high_water_mark, nav)
        actual = namespace["gross_up_cta"](pd.Series(net, index=self.dates))
        np.testing.assert_allclose(actual, gross, atol=1e-12)

    def test_no_incentive_fee_below_high_water_mark(self):
        net = pd.Series([-0.20, 0.05], index=self.dates[:2])
        np.testing.assert_allclose(namespace["gross_up_cta"](net), net + 0.02 / 12)

    def test_zero_fees_leave_returns_unchanged(self):
        net = pd.Series([0.10, -0.20, 0.05, 0.30], index=self.dates)
        np.testing.assert_allclose(namespace["gross_up_cta"](net, 0, 0), net)

    def test_invalid_fee_or_return_rejected(self):
        for values in ([0.1, np.nan], [0.1, -1.0], [0.1, np.inf]):
            with self.assertRaises(ValueError):
                namespace["gross_up_cta"](pd.Series(values))
        with self.assertRaises(ValueError):
            namespace["gross_up_cta"](pd.Series([0.1]), performance_fee=1)

    def test_blend_drifts_then_rebalances_at_february_end(self):
        core = pd.Series([1.0, 0.1, 0.1, 0], index=self.dates)
        mf = pd.Series(0.0, index=self.dates)
        actual = rebalance_portfolio(pd.concat([core, mf], axis=1), [0.66, 0.34], [0, 0], (2, 5, 8, 11))
        np.testing.assert_allclose(actual, [0.66, 1.32 / 1.66 * 0.1, 0.066, 0])

    def test_blend_allocation_endpoints(self):
        core = pd.Series([0.1, -0.2, 0.05, 0], index=self.dates)
        mf = pd.Series([0, 0.1, -0.1, 0.05], index=self.dates)
        assets = pd.concat([core, mf], axis=1)
        np.testing.assert_allclose(rebalance_portfolio(assets, [1, 0], [0, 0], (2, 5, 8, 11)), core)
        np.testing.assert_allclose(rebalance_portfolio(assets, [0, 1], [0, 0], (2, 5, 8, 11)), mf)

    def test_unaligned_or_invalid_sleeves_rejected(self):
        core = pd.Series(0.0, index=self.dates)
        with self.assertRaises(ValueError):
            rebalance_portfolio(pd.concat([core, core.iloc[1:]], axis=1), [0.66, 0.34], [0, 0], (2,))
        with self.assertRaises(ValueError):
            rebalance_portfolio(pd.concat([core, core], axis=1), [1.1, -0.1], [0, 0], (2,))
        with self.assertRaises(ValueError):
            rebalance_portfolio(pd.concat([core, core * np.nan], axis=1), [0.66, 0.34], [0, 0], (2,))

    def test_summary_episode_average_includes_unrecovered_drawdown(self):
        wealth = pd.Series([0.9, 0.8, 1.0, 0.7], index=self.dates)
        monthly = wealth / pd.Series([1.0, 0.9, 0.8, 1.0], index=self.dates) - 1
        summary = namespace["summary_metrics"](monthly.to_frame("test"), monthly * 0)
        self.assertAlmostEqual(summary.loc["test", "Max drawdown"], -0.3)
        self.assertAlmostEqual(summary.loc["test", "Average drawdown"], -0.25)

    def test_monthly_export_does_not_read_vami_as_returns(self):
        table = pd.DataFrame([[None] * 13, [None] * 13,
                              [1987, 0.1, -0.02] + [None] * 10,
                              [None] * 13, [1987, 1100, 1078] + [None] * 10])
        with patch("helpers.download_managed_futures_data.pd.read_excel", return_value=table):
            series = barclay_monthly_returns(b"")
        np.testing.assert_allclose(series, [0.1, -0.02])
        self.assertEqual(series.index[0], pd.Timestamp("1987-01-31"))

    def test_sg_daily_compounding_includes_first_month(self):
        table = pd.DataFrame([[None, None], ["Dstamp", "ROR"],
                              [pd.Timestamp("2000-01-03"), 0.1],
                              [pd.Timestamp("2000-01-04"), -0.1],
                              [pd.Timestamp("2000-02-01"), 0.05]])
        with patch("helpers.download_managed_futures_data.pd.read_excel", return_value=table):
            series = sg_monthly_returns(b"", "SG CTA")
        np.testing.assert_allclose(series, [-0.01, 0.05], atol=1e-12)
        self.assertEqual(series.index[0], pd.Timestamp("2000-01-31"))

    def test_aqr_dates_normalized_without_scaling(self):
        table = pd.DataFrame([[None, "TSMOM"], [pd.Timestamp("2026-05-29"), 0.02]])
        with patch("helpers.download_managed_futures_data.pd.read_excel", return_value=table):
            series = aqr_returns(b"")
        self.assertEqual(series.index[0], pd.Timestamp("2026-05-31"))
        self.assertEqual(series.iloc[0], 0.02)


if __name__ == "__main__":
    unittest.main()
