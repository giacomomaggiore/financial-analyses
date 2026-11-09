import importlib.util
from pathlib import Path
import unittest
from tempfile import TemporaryDirectory

import numpy as np
import pandas as pd

PATH = Path(__file__).resolve().parents[1] / 'outputs/pareto_superiority_90_60/research_2026-11-09/daily_ntsg_approximation.py'
spec = importlib.util.spec_from_file_location('ntsg_daily_approximation', PATH)
model = importlib.util.module_from_spec(spec)
spec.loader.exec_module(model)


class DailyApproximationTests(unittest.TestCase):
    def setUp(self):
        self.dates = pd.date_range('2024-01-01', periods=2, freq='D')
        self.prices = pd.DataFrame(1.0, index=self.dates, columns=['equity', *model.BONDS, *model.CURRENCIES])
        self.rates = pd.DataFrame(0.0, index=self.dates, columns=model.CURRENCIES)
        self.weights = {'USD': 1.0, 'EUR': 0.0, 'GBP': 0.0, 'JPY': 0.0}

    def test_flat_inputs_remain_flat(self):
        result, resets = model.simulate(self.prices, self.rates, self.weights, set(), annual_fee=0)
        np.testing.assert_allclose(result, [1.0, 1.0])
        self.assertEqual(resets, [])

    def test_futures_pnl_uses_notional_not_funded_bond_value(self):
        self.prices.loc[self.dates[1], 'US2'] = 1.10
        result, _ = model.simulate(self.prices, self.rates, self.weights, set(), annual_fee=0)
        self.assertAlmostEqual(result.iloc[-1], 1.02)

    def test_foreign_fx_moves_collateral_not_full_futures_principal(self):
        self.weights = {'USD': 0.0, 'EUR': 0.0, 'GBP': 1.0, 'JPY': 0.0}
        self.prices.loc[self.dates[1], 'GBP'] = 1.1
        result, _ = model.simulate(self.prices, self.rates, self.weights, set(), annual_fee=0)
        self.assertAlmostEqual(result.iloc[-1], 1.01)

    def test_local_funding_and_collateral_are_distinct(self):
        self.rates.loc[self.dates[0], 'USD'] = 0.036
        result, _ = model.simulate(self.prices, self.rates, self.weights, set(), annual_fee=0)
        self.assertAlmostEqual(result.iloc[-1], 1 + (0.1 - 0.6) * 0.036 / 360)

    def test_relative_and_percentage_point_bands_differ(self):
        self.prices.loc[self.dates[1], 'equity'] = 1.07
        _, points = model.simulate(self.prices, self.rates, self.weights, set(), 'points', annual_fee=0)
        _, relative = model.simulate(self.prices, self.rates, self.weights, set(), 'relative', annual_fee=0)
        self.assertEqual(points, [])
        self.assertEqual(relative, [(self.dates[1], 'exceptional')])

    def test_scheduled_reset_preserves_nav(self):
        self.prices.loc[self.dates[1], 'US2'] = 1.10
        result, resets = model.simulate(self.prices, self.rates, self.weights, {self.dates[1]}, annual_fee=0)
        self.assertAlmostEqual(result.iloc[-1], 1.02)
        self.assertEqual(resets, [(self.dates[1], 'scheduled')])

    def test_drag_reduces_portfolio_once(self):
        result, _ = model.simulate(self.prices, self.rates, self.weights, set(), annual_drag=0.01, annual_fee=0)
        self.assertAlmostEqual(result.iloc[-1], 1 - 0.6 * 0.01 / 365)

    def test_non_contiguous_calendar_rejected(self):
        dates = pd.to_datetime(['2024-01-01', '2024-01-03'])
        self.prices.index = dates
        self.rates.index = dates
        with self.assertRaisesRegex(ValueError, 'every day'):
            model.simulate(self.prices, self.rates, self.weights, set())

    def test_no_extrapolation_or_excessively_stale_prices(self):
        s = pd.Series([1.0, 2.0], index=pd.to_datetime(['2024-01-01', '2024-01-20']))
        with self.assertRaisesRegex(ValueError, 'stale'):
            model.align_with_staleness(s, pd.date_range('2024-01-01', '2024-01-20'))
        with self.assertRaisesRegex(ValueError, 'extrapolate'):
            model.align_with_staleness(s, pd.date_range('2024-01-01', '2024-01-21'))

    def test_invalid_currency_weights_rejected(self):
        self.weights['USD'] = 0.9
        with self.assertRaisesRegex(ValueError, 'sum to one'):
            model.simulate(self.prices, self.rates, self.weights, set())

    def test_rate_observation_is_delayed_two_business_days(self):
        with TemporaryDirectory() as directory:
            original = model.SOURCE
            try:
                model.SOURCE = Path(directory)
                (model.SOURCE / 'rate.csv').write_text('observation_date,annual_rate_percent\n2024-01-05,3.6\n')
                rates = model.load_rate('rate.csv')
                self.assertEqual(rates.index[0], pd.Timestamp('2024-01-09'))
                self.assertAlmostEqual(rates.iloc[0], 0.036)
            finally:
                model.SOURCE = original


if __name__ == '__main__':
    unittest.main()
