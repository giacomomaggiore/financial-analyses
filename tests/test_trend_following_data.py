import json
from pathlib import Path
import tempfile
import unittest

import pandas as pd

from helpers.download_trend_following_data import daily_values, save_series, validate


class DailyFuturesDataTests(unittest.TestCase):
    def test_last_observed_quote_per_source_date(self):
        result = daily_values(
            ["2020-04-21 23:00", "2020-04-20 12:00", "2020-04-20 23:00", "2020-04-22 23:00"],
            [0, 10, -37.63, None],
        )
        self.assertEqual(list(result.index), ["2020-04-20", "2020-04-21"])
        self.assertEqual(list(result.values), [-37.63, 0])

    def test_missing_observations_not_forward_filled(self):
        result = daily_values(["2000-01-01", "2000-01-03", "2000-01-05"], [1, ".", 3])
        self.assertEqual(list(result.index), ["2000-01-01", "2000-01-05"])

    def test_empty_data_rejected(self):
        with self.assertRaises(ValueError):
            daily_values(["2000-01-01"], [None])

    def test_infinity_rejected(self):
        with self.assertRaises(ValueError):
            daily_values(["2000-01-01"], [float("inf")])

    def test_invalid_download_does_not_replace_existing_file(self):
        with tempfile.TemporaryDirectory() as name:
            directory = Path(name)
            save_series(directory, "EXISTING", ["2000-01-01"], [10])
            path = directory / "EXISTING.CSV"
            original = path.read_bytes()
            with self.assertRaises(ValueError):
                save_series(directory, "EXISTING", ["2000-01-01"], [None])
            self.assertEqual(path.read_bytes(), original)
            self.assertFalse(list(directory.glob("*.tmp")))

    def test_csv_round_trip_and_manifest_validation(self):
        with tempfile.TemporaryDirectory() as name:
            directory = Path(name)
            summary = save_series(directory, "CL_TEST", ["2020-04-20", "2020-04-21"], [-37.63, 10])
            record = dict(key="CL_TEST", instrument="CL", provider="test", series_type="futures", **summary)
            (directory / "sources_manifest.json").write_text(json.dumps({"series": [record]}))
            catalog = validate(directory)
            self.assertEqual(catalog.iloc[0].nonpositive_rows, 1)
            frame = pd.read_csv(directory / "CL_TEST.CSV")
            self.assertEqual(list(frame.columns), ["date", "adjusted_price"])
            self.assertEqual(frame.adjusted_price.tolist(), [-37.63, 10])
            (directory / "CL_TEST.CSV").write_text("date,adjusted_price\n2020-04-20,1\n2020-04-21,10\n")
            with self.assertRaises(AssertionError):
                validate(directory)


class TrendSignalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = Path(__file__).resolve().parents[1] / '05_trend_following_futures.ipynb'
        notebook = json.loads(path.read_text())
        cell = next(cell for cell in notebook['cells'] if cell['id'] == '4fce3aac')
        cls.signals = {'pd': pd}
        exec(''.join(cell['source']), cls.signals)

    def test_filter_warmup_tie_and_sma(self):
        trend = self.signals['trend_filter']
        prices = pd.Series([1., 5., 3., 3.5])
        ema_trend = trend(prices, 1, 3)
        self.assertTrue(pd.isna(ema_trend.iloc[1]))
        self.assertEqual(ema_trend.iloc[2:].tolist(), [-1, 1])
        self.assertEqual(trend(prices, 1, 3, ma_type='sma').iloc[-1], -1)

    def test_inclusive_breakouts_fill_next_close_and_do_not_reverse(self):
        position = self.signals['position']
        prices = pd.Series([10., 11., 11., 13., 12., 12., 9., 8.])
        expected = [0, 0, 0, 1, 1, 1, 0, -1]
        self.assertEqual(position(prices, 1, 2, 2, 2).tolist(), expected)
        self.assertEqual(position(-prices, 1, 2, 2, 2).tolist(), [-value for value in expected])
        self.assertEqual(position(prices, 1, 2, 2, 2, long_only=True).iloc[-1], 0)
        self.assertEqual(position(prices, 1, 2, 2, 2, short_only=True).iloc[3], 0)

    def test_filter_flip_does_not_exit_and_pending_entry_cannot_cross_gap(self):
        position = self.signals['position']
        prices = pd.Series([10., 11., 11., 15., 14., 13., 9., 8., 7.])
        self.assertEqual(self.signals['trend_filter'](prices, 1, 2).iloc[5], -1)
        self.assertEqual(position(prices, 1, 2, 2, 3).tolist(), [0, 0, 0, 1, 1, 1, 1, 0, -1])
        self.assertEqual(position(prices, 1, 2, 2, 3, segment=pd.Series([0] * 3 + [1] * 6),
                                  eligible=pd.Series([False, False, True, False, False, True, True, True, True])).tolist(),
                         [0, 0, 0, 0, 0, 0, -1, -1, -1])


if __name__ == "__main__":
    unittest.main()
