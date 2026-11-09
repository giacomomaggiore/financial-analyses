from datetime import UTC, datetime
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import pandas as pd

from helpers.data import load_metadata, load_prices
from helpers.download_90_60_data import download_research_data


class ResearchDownloadTests(unittest.TestCase):
    def setUp(self) -> None:
        self.as_of = datetime(2026, 11, 9, 10, tzinfo=UTC)
        self.prices = pd.Series(
            [100.0, 101.0, 102.0],
            index=pd.to_datetime(["2026-11-05", "2026-11-06", "2026-11-09"]),
        )
        self.dataset = (("TEST", "TEST=X", "Test FX rate", 0.0, "JPY", "FX", "Spot only."),)
        self.probes = (("^RATE", "Yield", "Not a price."), ("MISSING", "Candidate", "Unverified."))

    def prepare_directory(self, directory: str) -> Path:
        path = Path(directory)
        (path / "metadata.csv").write_text(
            "ticker,asset_name,ter,currency\nEXISTING,Unrelated ETF,0.001,EUR\n"
        )
        return path

    def test_download_preserves_metadata_and_excludes_current_day(self) -> None:
        def download(symbol: str) -> pd.Series:
            if symbol == "MISSING":
                raise ValueError("No chart data")
            if symbol == "^RATE":
                return pd.Series([-0.1, 0.0], index=self.prices.index[:2])
            return self.prices

        with TemporaryDirectory() as directory:
            path = self.prepare_directory(directory)
            with (
                patch("helpers.download_90_60_data.DATASETS", self.dataset),
                patch("helpers.download_90_60_data.PROBES", self.probes),
                patch("helpers.download_90_60_data.download_yahoo_prices", side_effect=download),
            ):
                manifest = download_research_data(path, self.as_of)
            prices = load_prices("TEST.CSV", path)
            metadata = load_metadata(path)
            self.assertEqual(len(prices), 2)
            self.assertEqual(prices.index[-1], pd.Timestamp("2026-11-06"))
            self.assertEqual(metadata.loc["EXISTING", "currency"], "EUR")
            self.assertEqual(metadata.loc["TEST", "currency"], "JPY")
            self.assertEqual(manifest["coverage_probes"][0]["status"], "available_not_approved")
            self.assertEqual(manifest["coverage_probes"][1]["status"], "lookup_failed")
            self.assertEqual(manifest["datasets"][0]["yahoo_symbol"], "TEST=X")
            self.assertTrue((path / "90_60_data_manifest.json").is_file())
            self.assertFalse((path / "^RATE.CSV").exists())

    def test_insufficient_history_does_not_replace_snapshots(self) -> None:
        with TemporaryDirectory() as directory:
            path = self.prepare_directory(directory)
            target = path / "TEST.CSV"
            target.write_text("date,adjusted_price\n2025-01-01,50\n")
            original_metadata = (path / "metadata.csv").read_text()
            with (
                patch("helpers.download_90_60_data.DATASETS", self.dataset),
                patch("helpers.download_90_60_data.download_yahoo_prices", return_value=self.prices.iloc[-1:]),
            ):
                with self.assertRaisesRegex(ValueError, "Insufficient"):
                    download_research_data(path, self.as_of)
            self.assertIn("2025-01-01,50", target.read_text())
            self.assertEqual((path / "metadata.csv").read_text(), original_metadata)
            self.assertFalse((path / "90_60_data_manifest.json").exists())

    def test_naive_timestamp_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "timezone-aware"):
            download_research_data(as_of=datetime(2026, 11, 9))


if __name__ == "__main__":
    unittest.main()
