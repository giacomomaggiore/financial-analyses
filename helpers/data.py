"""Shared market-data loading, validation, and currency-conversion utilities."""

from datetime import UTC, datetime
import csv
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
REQUIRED_PRICE_COLUMNS = ("date", "adjusted_price")
REQUIRED_METADATA_COLUMNS = ("ticker", "asset_name", "ter", "currency")


def load_prices(filename: str | Path, data_dir: Path = DATA_DIR, name: str | None = None) -> pd.Series:
    """Load one two-column adjusted-price CSV as a date-indexed series."""
    path = data_dir / filename
    frame = pd.read_csv(path, parse_dates=["date"])
    if tuple(frame.columns) != REQUIRED_PRICE_COLUMNS:
        raise ValueError(f"{path} must contain exactly: {', '.join(REQUIRED_PRICE_COLUMNS)}.")
    if frame["date"].isna().any() or frame["adjusted_price"].isna().any():
        raise ValueError(f"{path} contains missing dates or adjusted prices.")
    if frame["date"].duplicated().any() or not frame["date"].is_monotonic_increasing:
        raise ValueError(f"{path} must have unique, ascending dates.")
    if (frame["adjusted_price"] <= 0).any():
        raise ValueError(f"{path} contains non-positive adjusted prices.")
    return frame.set_index("date")["adjusted_price"].rename(name or path.stem)


def load_metadata(data_dir: Path = DATA_DIR) -> pd.DataFrame:
    """Load and validate the shared instrument metadata table."""
    path = data_dir / "metadata.csv"
    metadata = pd.read_csv(path)
    if tuple(metadata.columns) != REQUIRED_METADATA_COLUMNS:
        raise ValueError(f"{path} must contain exactly: {', '.join(REQUIRED_METADATA_COLUMNS)}.")
    if metadata["ticker"].duplicated().any():
        raise ValueError(f"{path} contains duplicate tickers.")
    if metadata[["ticker", "asset_name", "currency"]].isna().any().any():
        raise ValueError(f"{path} contains required empty metadata values.")
    if (metadata["ter"] < 0).any():
        raise ValueError(f"{path} contains negative TER values.")
    return metadata.set_index("ticker")


def align_prices(prices: pd.DataFrame, max_stale_periods: int = 5) -> pd.DataFrame:
    """Align price histories while limiting stale-price forward fills."""
    if max_stale_periods < 0:
        raise ValueError("max_stale_periods must be non-negative.")
    if prices.empty:
        raise ValueError("No price series were supplied.")
    return prices.sort_index().ffill(limit=max_stale_periods).dropna(how="any")


def convert_prices(prices: pd.Series, fx_prices: pd.Series, quote_per_base: bool = True) -> pd.Series:
    """Convert prices using an FX series quoted as target per source currency by default."""
    aligned = pd.concat([prices, fx_prices], axis=1).sort_index().ffill().dropna()
    converted = aligned.iloc[:, 0] * aligned.iloc[:, 1] if quote_per_base else aligned.iloc[:, 0] / aligned.iloc[:, 1]
    return converted.rename(prices.name)


def download_yahoo_prices(ticker: str, start: datetime | None = None) -> pd.Series:
    """Download Yahoo Finance adjusted closes for one identifier."""
    period1 = 0 if start is None else int(start.replace(tzinfo=UTC).timestamp())
    query = urlencode({"period1": period1, "period2": int(datetime.now(UTC).timestamp()), "interval": "1d"})
    request = Request(
        f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?{query}",
        headers={"User-Agent": "financial-investment-analysis/1.0"},
    )
    with urlopen(request, timeout=30) as response:
        result = json.load(response)["chart"]["result"][0]
    values = {
        datetime.fromtimestamp(timestamp, UTC).date(): value
        for timestamp, value in zip(result["timestamp"], result["indicators"]["adjclose"][0]["adjclose"], strict=True)
        if value is not None
    }
    if not values:
        raise ValueError(f"Yahoo Finance returned no adjusted prices for {ticker}.")
    return pd.Series(values, name=ticker, dtype=float).rename_axis("date")


def write_prices(prices: pd.Series, filename: str | Path, data_dir: Path = DATA_DIR) -> Path:
    """Write a validated adjusted-price series to the shared CSV contract."""
    path = data_dir / filename
    if prices.empty or prices.isna().any() or (prices <= 0).any():
        raise ValueError("Prices must be non-empty, positive, and complete.")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as file:
        writer = csv.writer(file, lineterminator="\n")
        writer.writerow(REQUIRED_PRICE_COLUMNS)
        writer.writerows((pd.Timestamp(timestamp).date().isoformat(), f"{value:.10f}") for timestamp, value in prices.sort_index().items())
    return path
