"""Refresh separate actual-ETF snapshots used by the implementation-cost audit."""

from datetime import UTC, datetime
import json

import pandas as pd

from helpers.data import DATA_DIR, download_yahoo_prices, write_prices


DATASETS = (
    ("NTSG.L", "NTSG_ACTUAL_USD.CSV", "https://www.wisdomtree.com/se/products/equities/wisdomtree-global-efficient-core-ucits-etf---usd-acc"),
    ("URTH", "URTH_ACTUAL.CSV", "https://www.ishares.com/us/products/239696/"),
    ("IGLO.L", "IGLO_ACTUAL_USD.CSV", "https://www.ishares.com/ch/individual/en/products/251753/ishares-global-government-bond-ucits-etf"),
)


def download_implementation_data():
    cutoff = pd.Timestamp.today().to_period("M").start_time
    snapshots = []
    entries = []
    for symbol, filename, issuer in DATASETS:
        prices = download_yahoo_prices(symbol)
        prices.index = pd.to_datetime(prices.index)
        prices = prices.loc[prices.index < cutoff]
        if len(prices) < 2 or prices.isna().any() or (prices <= 0).any():
            raise ValueError(f"Invalid adjusted prices for {symbol}")
        snapshots.append((filename, prices))
        entries.append({"symbol": symbol, "file": filename, "first": str(prices.index[0].date()),
                        "last": str(prices.index[-1].date()), "source": f"https://finance.yahoo.com/quote/{symbol}/history/",
                        "issuer": issuer, "type": "USD adjusted close total return; already net of fund expenses"})
    for filename, prices in snapshots:
        write_prices(prices, filename)
    manifest = {"retrieved_at_utc": datetime.now(UTC).isoformat(), "exclusive_month_cutoff": str(cutoff.date()),
                "datasets": entries, "limitations": [
                    "Market-close prices are not official NAV. London and US closing times differ.",
                    "IGLO tracks FTSE G7 Government Bond, not the pre-inception WGBI Developed Markets proxy.",
                    "Current product access to both UCITS and US ETFs is assumed; personal taxes are not modeled."]}
    (DATA_DIR / "realistic_backtest_sources_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(pd.DataFrame(entries)[["symbol", "first", "last"]].to_string(index=False))


if __name__ == "__main__":
    download_implementation_data()
