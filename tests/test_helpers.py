from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import pandas as pd

from helpers.correlations import aligned_returns, correlation_matrix, periodic_returns
from helpers.data import load_prices, write_prices
from helpers.proxies import excess_returns, proxy_from_returns, weighted_returns


class HelperTests(unittest.TestCase):
    def setUp(self) -> None:
        self.index = pd.to_datetime(["2024-01-30", "2024-01-31", "2024-02-29", "2024-03-29"])
        self.prices = pd.Series([100.0, 110.0, 121.0, 133.1], index=self.index.rename("date"), name="TEST")

    def test_price_round_trip_uses_shared_contract(self) -> None:
        with TemporaryDirectory() as directory:
            path = write_prices(self.prices, "TEST.CSV", Path(directory))
            actual = load_prices(path.name, Path(directory))
        pd.testing.assert_series_equal(actual, self.prices.rename("TEST"), check_freq=False)

    def test_periodic_returns_and_correlations_use_common_sample(self) -> None:
        returns = periodic_returns(pd.concat([self.prices, self.prices * 2], axis=1))
        aligned = aligned_returns(returns)
        self.assertEqual(len(aligned), 2)
        self.assertEqual(correlation_matrix(aligned).shape, (2, 2))

    def test_proxy_and_weighted_returns_apply_returns_correctly(self) -> None:
        returns = pd.Series([0.10, -0.10], index=self.index[:2], name="proxy")
        self.assertAlmostEqual(proxy_from_returns(returns, periods_per_year=2).iloc[-1], 99.0)
        self.assertAlmostEqual(excess_returns(returns, pd.Series([0.0, 0.0], index=returns.index)).iloc[0], 0.10)
        assets = pd.DataFrame({"A": [0.10, 0.0], "B": [0.0, 0.10]}, index=returns.index)
        result = weighted_returns(assets, pd.Series({"A": 0.5, "B": 0.5}))
        self.assertAlmostEqual(result.iloc[0], 0.05)
        self.assertAlmostEqual(result.iloc[1], 0.04761904761904767)


if __name__ == "__main__":
    unittest.main()
