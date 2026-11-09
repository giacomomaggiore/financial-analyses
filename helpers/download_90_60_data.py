"""Download Yahoo inputs and record the limits of the 90/60 research dataset."""

from datetime import UTC, datetime
import json
from pathlib import Path

import pandas as pd

from helpers.data import DATA_DIR, PROJECT_ROOT, download_yahoo_prices, load_metadata, write_prices


# These are research inputs, not an approved NTSG replication basket.
DATASETS = (
    ("NTSG.L", "NTSG.L", "WisdomTree Global Efficient Core UCITS ETF USD Acc (London USD listing)", 0.0025, "USD", "live validation", "Exchange adjusted close, not official fund NAV; London close differs from US closes."),
    ("IWDA.L", "IWDA.L", "iShares Core MSCI World UCITS ETF USD Acc", 0.0020, "USD", "developed equity proxy", "ETF returns include fund expenses and fund-level withholding; not the NTSG ESG equity basket."),
    ("URTH", "URTH", "iShares MSCI World ETF", 0.0024, "USD", "US-listed equity sensitivity", "Shorter history than IWDA.L; different fund domicile and closing time."),
    ("IEF", "IEF", "iShares 7-10 Year Treasury Bond ETF", 0.0015, "USD", "US government bond sensitivity", "Cash bonds in one maturity segment, not the US futures ladder."),
    ("IGOV", "IGOV", "iShares International Treasury Bond ETF", 0.0035, "USD", "international government bond sensitivity", "Unhedged developed ex-US cash bonds; different currency, country and duration weights from NTSG."),
    ("BWX", "BWX", "SPDR Bloomberg International Treasury Bond ETF", 0.0035, "USD", "longer international bond sensitivity", "Unhedged ex-US cash bonds including emerging markets; not a USD-hedged futures sleeve."),
    ("BNDW", "BNDW", "Vanguard Total World Bond ETF", 0.0005, "USD", "broad aggregate bond sensitivity", "Includes non-government bonds and differs from NTSG government futures."),
    ("BIL", "BIL", "State Street SPDR Bloomberg 1-3 Month T-Bill ETF", 0.001353, "USD", "investable USD cash proxy", "Net-of-fee bill ETF total return, not a borrowing rate or multicurrency collateral model."),
    ("EURUSD", "EURUSD=X", "EUR/USD exchange rate (USD per EUR)", 0.0, "USD", "EUR translation and collateral FX", "Spot only; no forward points or hedge return; Yahoo history begins in 2003."),
    ("GBPUSD", "GBPUSD=X", "GBP/USD exchange rate (USD per GBP)", 0.0, "USD", "GBP collateral FX", "Spot only; does not supply GBP cash interest or financing."),
    ("USDJPY", "JPY=X", "USD/JPY exchange rate (JPY per USD)", 0.0, "JPY", "JPY collateral FX", "Invert to value JPY cash in USD; does not supply JPY cash interest."),
)

PROBES = (
    ("^990100-USD-NETR", "MSCI World net total return", "Do not substitute the MSCI price index if net-return history is insufficient."),
    ("^990100-USD-STRD", "MSCI World price index", "Price only: excludes dividends and is ineligible for the performance backtest."),
    ("^IRX", "13-week Treasury bill yield", "Quoted yield, not a price or total-return index; zero/negative values are legitimate rate observations."),
    ("ZT=F", "US 2-year Treasury continuous futures quote", "Diagnostic quotes only: no verified roll accounting, contract multipliers or collateral return."),
    ("ZF=F", "US 5-year Treasury continuous futures quote", "Diagnostic quotes only: not a tradable contract-level excess-return history."),
    ("ZN=F", "US 10-year Treasury continuous futures quote", "Diagnostic quotes only: not a tradable contract-level excess-return history."),
    ("ZB=F", "US Treasury bond continuous futures quote", "Diagnostic quotes only: not a tradable contract-level excess-return history."),
    ("FGBL=F", "candidate German Bund futures identifier", "Candidate lookup only; failure does not establish absence under every Yahoo identifier."),
    ("FGBM=F", "candidate German Bobl futures identifier", "Candidate lookup only; failure does not establish absence under every Yahoo identifier."),
    ("FGBS=F", "candidate German Schatz futures identifier", "Candidate lookup only; failure does not establish absence under every Yahoo identifier."),
    ("G=F", "candidate UK gilt futures identifier", "Candidate lookup only; not an official NTSG contract mapping."),
    ("JGB=F", "candidate Japanese government bond futures identifier", "Candidate lookup only; not an official NTSG contract mapping."),
    ("^SPEUBDP", "S&P Euro-Bund Futures Excess Return index", "An index quote is not evidence of a downloadable historical series or an NTSG replication."),
)


def download_research_data(data_dir: Path = DATA_DIR, as_of: datetime | None = None) -> dict:
    """Refresh eligible snapshots; exclude the current UTC date and audit unsuitable inputs."""
    timestamp = as_of or datetime.now(UTC)
    if timestamp.tzinfo is None:
        raise ValueError("as_of must be timezone-aware.")
    cutoff = pd.Timestamp(timestamp.astimezone(UTC).date())
    snapshots = []
    manifest = {
        "retrieved_at_utc": timestamp.astimezone(UTC).isoformat(),
        "exclusive_date_cutoff": cutoff.date().isoformat(),
        "source": "Yahoo Finance chart API; adjusted-close field",
        "scope": "Tiered research: usable ETF/FX snapshots; long-history and faithful NTSG reconstruction remain gated.",
        "datasets": [],
        "coverage_probes": [],
        "unverified_requirements": [
            "Long-history MSCI World USD net total-return levels.",
            "Precisely identified Bloomberg Global Treasury USD-hedged total-return index and licensed history.",
            "Official eight-contract mapping, point-in-time currency weights, contract settlements and roll specifications.",
            "USD/EUR/GBP/JPY collateral and financing histories; historical margin and execution assumptions.",
            "EUR/USD observations before Yahoo coverage and official NTSG NAV for live validation.",
        ],
        "fee_sources": {
            "NTSG.L": "https://dataspanapi.wisdomtree.com/pdr/documents/FACTSHEET/UCITS/EU/EN-GB/IE00077IIPQ8/",
            "IWDA.L": "https://www.ishares.com/uk/individual/en/products/251882/ishares-msci-world-ucits-etf-acc-fund",
            "IGOV": "https://www.ishares.com/us/products/239830/",
            "BIL": "https://www.ssga.com/library-content/products/factsheets/etfs/us/factsheet-us-en-bil.pdf",
        },
        "fee_note": "Current documented annual fees, not historical fee schedules. ETF adjusted prices are already net of fund expenses; do not deduct TER again.",
    }
    for ticker, symbol, asset_name, ter, currency, role, limitation in DATASETS:
        prices = download_yahoo_prices(symbol)
        prices = prices.loc[pd.to_datetime(prices.index) < cutoff]
        if len(prices) < 2 or prices.isna().any() or (prices <= 0).any():
            raise ValueError(f"Insufficient valid completed-date prices for {symbol}.")
        snapshots.append((ticker, prices, asset_name, ter, currency))
        manifest["datasets"].append({
            "ticker": ticker, "yahoo_symbol": symbol, "file": f"{ticker}.CSV",
            "asset_name": asset_name, "ter": ter, "currency": currency,
            "observations": len(prices), "first": str(prices.index[0]), "last": str(prices.index[-1]),
            "role": role, "limitation": limitation,
            "source_url": f"https://finance.yahoo.com/quote/{symbol}/history/",
        })
    for symbol, description, limitation in PROBES:
        entry = {"symbol": symbol, "description": description, "limitation": limitation}
        try:
            prices = download_yahoo_prices(symbol)
            completed = prices.loc[pd.to_datetime(prices.index) < cutoff]
            entry.update({
                "status": "insufficient_history" if len(completed) < 2 else "available_not_approved",
                "observations_returned": len(prices), "completed_date_observations": len(completed),
                "first_returned": str(prices.index[0]), "last_returned": str(prices.index[-1]),
            })
        except Exception as error:
            entry.update({"status": "lookup_failed", "error": f"{type(error).__name__}: {error}"})
        manifest["coverage_probes"].append(entry)

    # Fetch and validate every required snapshot before replacing shared files.
    metadata = load_metadata(data_dir)
    for ticker, prices, asset_name, ter, currency in snapshots:
        write_prices(prices, f"{ticker}.CSV", data_dir)
        metadata.loc[ticker, ["asset_name", "ter", "currency"]] = [asset_name, ter, currency]
    metadata.to_csv(data_dir / "metadata.csv", lineterminator="\n")
    (data_dir / "90_60_data_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


def main() -> None:
    manifest = download_research_data()
    lines = []
    for row in manifest["datasets"]:
        line = f"{row['file']}: {row['observations']} observations, {row['first']} to {row['last']}; Yahoo {row['yahoo_symbol']} ({row['currency']})."
        lines.append(f"- {line}")
        print(line)
    note = (
        f"\n\n## {manifest['exclusive_date_cutoff']} - 90/60 Yahoo dataset refresh\n\n"
        f"- Download timestamp: {manifest['retrieved_at_utc']}; current UTC date excluded.\n"
        "- Source: Yahoo Finance chart API via `helpers.data.download_yahoo_prices`; snapshots written with `write_prices`.\n"
        + "\n".join(lines)
        + "\n- Coverage and exclusions: see `data/90_60_data_manifest.json`. Price indexes, quoted yields and unverified continuous-futures quotes were not saved as total-return inputs.\n"
        "- Interpretation: these ETF proxies do not reproduce the NTSG equity selection, government-futures basket or multicurrency collateral. Current metadata TERs are not historical fee schedules.\n"
        "- Existing NTSG.CSV (EUR Xetra listing), MSCI_WORLD_USD.CSV (price index), synthetic proxies and FRED cash series were not replaced. Other listed snapshots were refreshed; old notebook outputs were not recalculated.\n"
    )
    with (PROJECT_ROOT / "insights.md").open("a") as file:
        file.write(note)


if __name__ == "__main__":
    main()
