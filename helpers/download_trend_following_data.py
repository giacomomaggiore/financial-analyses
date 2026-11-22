"""Download daily futures research inputs without mixing providers or roll methods."""

import argparse
from datetime import datetime, timezone
import hashlib
from io import BytesIO
import json
from pathlib import Path
import subprocess
import time
from urllib.parse import quote
from urllib.request import urlopen

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DESTINATION = ROOT / "data" / "trend_following_futures"
PST_REPO = "https://raw.githubusercontent.com/pst-group/pysystemtrade"
PST_REVISION = "bbf5cf823e16be1cca27493a94099eb8cf33f6e7"
LEGACY_REVISION = "10120f2f6bab6eecade36455d9203751cbe02539"

# Guide instruments; provider chains are explicitly not assumed to be front-month.
# instrument, name, currency, Yahoo identifier, pysystemtrade identifier
MARKETS = [
    ("ES", "S&P 500 futures (legacy full-size history in PST)", "USD", "ES=F", "SP500"),
    ("MES", "Micro E-mini S&P 500 (PST backfilled with larger contracts)", "USD", "MES=F", "SP500_micro"),
    ("NQ", "Nasdaq-100 futures", "USD", "NQ=F", "NASDAQ"),
    ("FESX", "Euro Stoxx 50 futures", "EUR", "FESX=F", "EUROSTX"),
    ("SR3_ED_CHAIN", "SOFR chain with pre-launch rate-futures backfill", "USD", "SR3=F", "SOFR"),
    ("ED", "Eurodollar futures (discontinued)", "USD", "GE=F", "EDOLLAR"),
    ("ZN", "10-year US Treasury note futures", "USD", "ZN=F", "US10"),
    ("ZT", "2-year US Treasury note futures", "USD", "ZT=F", "US2"),
    ("ZB", "US Treasury bond futures (not Ultra Bond)", "USD", "ZB=F", "US20"),
    ("FGBL", "Euro-Bund futures", "EUR", "FGBL=F", "BUND"),
    ("BAX", "Canadian bankers acceptance futures (discontinued)", "CAD", "BAX=F", None),
    ("ZQ", "30-day federal funds futures", "USD", "ZQ=F", "FED"),
    ("6E", "Euro FX futures", "USD", "6E=F", "EUR"),
    ("6J", "Japanese yen futures", "USD", None, "JPY"),
    ("6B", "British pound futures", "USD", None, "GBP"),
    ("CL", "WTI crude oil futures (PST winter chain)", "USD", "CL=F", "CRUDE_W"),
    ("BRENT", "Brent crude oil futures (PST summer chain)", "USD", "BZ=F", "BRENT_W"),
    ("NG", "Henry Hub natural gas futures", "USD", "NG=F", "GAS_US"),
    ("HO", "Heating oil / NY Harbor ULSD futures", "USD", "HO=F", "HEATOIL"),
    ("GC", "Gold futures", "USD", "GC=F", "GOLD"),
    ("HG", "Copper futures", "USD", "HG=F", "COPPER"),
    ("SI", "Silver futures (PST contract specification differs)", "USD", "SI=F", "SILVER"),
    ("ZC", "Corn futures", "USD", "ZC=F", "CORN"),
    ("ZS", "Soybean futures", "USD", "ZS=F", "SOYBEAN"),
    ("KC", "Coffee C futures", "USD", "KC=F", "COFFEE"),
    ("SB", "Sugar No. 11 futures", "USD", "SB=F", "SUGAR11"),
    ("CT", "Cotton No. 2 futures", "USD", "CT=F", "COTTON2"),
    ("HE", "Lean hog futures", "USD", "HE=F", "LEANHOG"),
    ("LE", "Live cattle futures", "USD", "LE=F", "LIVECOW"),
]
YAHOO_PROXIES = [
    ("SP500_INDEX", "S&P 500 price index", "USD", "^GSPC"),
    ("NASDAQ100_INDEX", "Nasdaq-100 price index", "USD", "^NDX"),
    ("EUROSTOXX50_INDEX", "Euro Stoxx 50 price index", "EUR", "^STOXX50E"),
    ("MSCI_WORLD_PRICE", "MSCI World USD price index", "USD", "^990100-USD-STRD"),
    ("MSCI_WORLD_TR_CANDIDATE", "Unverified MSCI World gross return identifier", "USD", "^990100-USD-GR"),
    ("URTH_PROXY", "iShares MSCI World ETF adjusted-price proxy, not MSCI World TR", "USD", "URTH"),
    ("EURUSD_SPOT", "USD per EUR spot rate", "USD", "EURUSD=X"),
    ("USDCHF_SPOT", "CHF per USD spot rate", "CHF", "CHF=X"),
]
FRED_SERIES = [
    ("WTI_SPOT", "Cushing WTI spot price", "USD", "DCOILWTICO", "spot"),
    ("BRENT_SPOT", "Europe Brent spot price", "USD", "DCOILBRENTEU", "spot"),
    ("HENRY_HUB_SPOT", "Henry Hub natural gas spot price", "USD", "DHHNGSP", "spot"),
    ("HEATING_OIL_SPOT", "NY Harbor heating oil spot price", "USD", "DHOILNYH", "spot"),
    ("GOLD_LONDON_AM", "London gold AM fixing (discontinued)", "USD", "GOLDAMGBD228NLBM", "spot"),
    ("GOLD_LONDON_PM", "London gold PM fixing (discontinued)", "USD", "GOLDPMGBD228NLBM", "spot"),
    ("EURUSD_SPOT", "USD per EUR spot rate", "USD", "DEXUSEU", "spot_fx"),
    ("USDCHF_SPOT", "CHF per USD spot rate", "CHF", "DEXSZUS", "spot_fx"),
    ("USD_LIBOR_3M", "3-month USD LIBOR fixing, percent per annum", "USD", "USD3MTD156N", "yield_percent"),
    ("SOFR_RATE", "Secured overnight financing rate, percent per annum", "USD", "SOFR", "yield_percent"),
    ("FED_FUNDS_RATE", "Effective federal funds rate, percent per annum", "USD", "DFF", "yield_percent"),
    ("TREASURY_2Y_YIELD", "2-year Treasury constant maturity yield, percent per annum", "USD", "DGS2", "yield_percent"),
    ("TREASURY_10Y_YIELD", "10-year Treasury constant maturity yield, percent per annum", "USD", "DGS10", "yield_percent"),
    ("TREASURY_30Y_YIELD", "30-year Treasury constant maturity yield, percent per annum", "USD", "DGS30", "yield_percent"),
    ("USD_BILL_3M_YIELD", "3-month Treasury bill secondary market discount rate, percent", "USD", "DTB3", "yield_percent"),
]
EIA_SERIES = [
    ("WTI_SPOT", "Cushing WTI spot price", "RWTCd"),
    ("BRENT_SPOT", "Europe Brent spot price", "RBRTEd"),
    ("HENRY_HUB_SPOT", "Henry Hub natural gas spot price", "RNGWHHDd"),
    ("HEATING_OIL_SPOT", "NY Harbor heating oil spot price", "EER_EPD2F_PF4_Y35NY_DPGd"),
]


def fetch(url):
    for attempt in range(2):
        try:
            with urlopen(url, timeout=25) as response:
                return response.read()
        except Exception:
            if attempt == 1:
                raise
            time.sleep(1)


def daily_values(dates, values):
    """Keep the last observed value per provider calendar date, including negatives."""
    frame = pd.DataFrame({"timestamp": pd.to_datetime(dates), "value": pd.to_numeric(values, errors="coerce")})
    frame = frame.dropna().sort_values("timestamp", kind="stable")
    if not np.isfinite(frame["value"]).all():
        raise ValueError("Non-finite observations")
    frame["date"] = frame["timestamp"].dt.strftime("%Y-%m-%d")
    result = frame.groupby("date", sort=True)["value"].last()
    if result.empty:
        raise ValueError("No numeric observations")
    return result


def save_series(directory, key, dates, values):
    result = daily_values(dates, values)
    path = directory / f"{key}.CSV"
    temporary = path.with_suffix(".CSV.tmp")
    result.rename("adjusted_price").to_csv(temporary, float_format="%.10f")
    temporary.replace(path)
    return {
        "file": path.name, "rows": len(result), "start": result.index[0], "end": result.index[-1],
        "nonpositive_rows": int((result <= 0).sum()),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def acquire(directory=DESTINATION, refresh=False, only=None):
    directory.mkdir(parents=True, exist_ok=True)
    manifest_path = directory / "sources_manifest.json"
    previous = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    records = {item["key"]: item for item in previous.get("series", [])}
    failures = {item["key"]: item for item in previous.get("failed_downloads", [])}

    def persist_manifest():
        manifest = dict(created_at_utc=datetime.now(timezone.utc).isoformat(), frequency="daily observations; no filling",
                        schema="date,adjusted_price; native levels, not necessarily adjusted or positive",
                        pst_revision=PST_REVISION, legacy_revision=LEGACY_REVISION,
                        series=list(records.values()), failed_downloads=list(failures.values()))
        temporary = manifest_path.with_suffix(".json.tmp")
        temporary.write_text(json.dumps(manifest, indent=2) + "\n")
        temporary.replace(manifest_path)

    def attempt(key, instrument, name, currency, provider, identifier, series_type, url, loader, notes=""):
        if only and provider not in only:
            return
        old = records.get(key)
        if not refresh and old and old["source_url"] == url and (directory / old["file"]).exists():
            old.update(asset_name=name, currency=currency, notes=notes)
            return
        try:
            dates, values = loader()
            result = daily_values(dates, values)
            if provider in {"Yahoo", "pysystemtrade", "pysystemtrade_legacy"} and len(result) < 100:
                raise ValueError(f"Only {len(result)} daily observations; insufficient for the guide's 100-day signal")
            summary = save_series(directory, key, result.index, result.to_numpy())
            records[key] = dict(key=key, instrument=instrument, asset_name=name, currency=currency,
                                provider=provider, identifier=identifier, series_type=series_type,
                                source_url=url, downloaded_at_utc=datetime.now(timezone.utc).isoformat(),
                                total_return=series_type in {"etf_adjusted_price", "net_total_return_index", "gross_total_return_index"}, notes=notes, **summary)
            failures.pop(key, None)
            print(f"OK {key}: {summary['start']} to {summary['end']} ({summary['rows']})", flush=True)
        except Exception as error:
            failures[key] = dict(key=key, provider=provider, identifier=identifier, source_url=url,
                                 checked_at_utc=datetime.now(timezone.utc).isoformat(), error=str(error)[:500])
            print(f"UNAVAILABLE {key}: {error}", flush=True)
        persist_manifest()

    if only is None or "Yahoo" in only:
        import yfinance as yf
        for instrument, name, currency, yahoo, _ in MARKETS:
            if yahoo is None:
                continue
            url = f"https://finance.yahoo.com/quote/{quote(yahoo, safe='')}/history/"
            def yahoo_loader(symbol=yahoo):
                frame = yf.Ticker(symbol).history(period="max", auto_adjust=False)
                if frame.empty:
                    raise ValueError("Yahoo returned no daily history")
                return frame.index.tz_localize(None), frame["Close"].to_numpy()
            attempt(f"{instrument}__YAHOO_CLOSE", instrument, name, currency, "Yahoo", yahoo,
                    "futures_continuation_unverified_roll", url, yahoo_loader,
                    "Raw Yahoo Close, not a verified roll-adjusted or total-return series. No generic Adj Close roll adjustment assumed.")
        for instrument, name, currency, yahoo in YAHOO_PROXIES:
            url = f"https://finance.yahoo.com/quote/{quote(yahoo, safe='')}/history/"
            def proxy_loader(symbol=yahoo):
                frame = yf.Ticker(symbol).history(period="max", auto_adjust=False)
                if frame.empty:
                    raise ValueError("Yahoo returned no daily history")
                column = "Adj Close" if symbol == "URTH" else "Close"
                return frame.index.tz_localize(None), frame[column].to_numpy()
            attempt(f"{instrument}__YAHOO", instrument, name, currency, "Yahoo", yahoo,
                    "etf_adjusted_price" if yahoo == "URTH" else "spot_or_price_index", url, proxy_loader,
                    "Not a futures return series. URTH includes fund expenses and distributions; index Close is price return only.")

    for instrument, name, currency, _, pst in MARKETS:
        if pst is None:
            continue
        revision = LEGACY_REVISION if instrument == "ED" else PST_REVISION
        provider = "pysystemtrade_legacy" if instrument == "ED" else "pysystemtrade"
        for folder, column, kind in [("adjusted_prices_csv", "price", "panama_back_adjusted"),
                                     ("multiple_prices_csv", "PRICE", "unadjusted_active_contract")]:
            url = f"{PST_REPO}/{revision}/data/futures/{folder}/{pst}.csv"
            def pst_loader(source=url, value_column=column):
                frame = pd.read_csv(BytesIO(fetch(source)))
                return frame["DATETIME"], frame[value_column]
            attempt(f"{instrument}__PST_{kind.upper()}", instrument, name, currency, provider, pst, kind, url, pst_loader,
                    "Last nonmissing observation per source calendar date; may include intraday samples. Provider-selected contract/roll, not necessarily front month. Additive adjustments can be negative. No collateral or trading costs. SOFR includes pre-2018 backfill; ES includes pre-E-mini history; CL/BRENT seasonal chains; verify native units, notably SILVER.")

    archive_revision = "693eef674f65b2b422ac64bdf9b528c0c398b4b6"
    for instrument, name, currency, pst, folder, column in [
        ("FGBL", "Euro-Bund archived continuation", "EUR", "BUND", "adjusted_prices_csv", "price"),
        ("FESX", "Euro Stoxx 50 archived continuation", "EUR", "EUROSTX", "adjusted_prices_csv", "price"),
        ("HG", "Copper archived continuation", "USD", "COPPER", "adjusted_prices_csv", "price"),
        ("HG", "Copper legacy price sample, adjustment not verified", "USD", "COPPER", "legacycsv", "PRICE"),
        ("FESX", "Euro Stoxx 50 legacy price sample, adjustment not verified", "EUR", "EUROSTX", "legacycsv", "PRICE"),
    ]:
        suffix = f"{pst}_price.csv" if folder == "legacycsv" else f"{pst}.csv"
        url = f"{PST_REPO}/{archive_revision}/data/futures/{folder}/{suffix}"
        def archive_loader(source=url, value_column=column):
            frame = pd.read_csv(BytesIO(fetch(source)))
            return frame["DATETIME"], frame[value_column]
        kind = "legacy_adjustment_unverified" if folder == "legacycsv" else "panama_back_adjusted"
        attempt(f"{instrument}__PST_ARCHIVE2019_{folder.upper()}", instrument, name, currency, "pysystemtrade_archive",
                pst, kind, url, archive_loader,
                "Archived sample selected because it starts earlier than the 2024 snapshot. May be sparse; no cross-snapshot splice. Legacycsv adjustment is not independently verified. Do not treat its percentage changes as futures returns.")

    for instrument, name, currency, fred, kind in FRED_SERIES:
        url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={fred}"
        def fred_loader(source=url):
            frame = pd.read_csv(BytesIO(fetch(source)))
            return frame.iloc[:, 0], frame.iloc[:, 1]
        attempt(f"{instrument}__FRED_{fred}", instrument, name, currency, "FRED", fred, kind, url, fred_loader,
                "Missing source observations omitted, not filled. Yields are percent per annum, not prices or total returns. Calendar-day DFF retained at native frequency.")

    for instrument, name, code in EIA_SERIES:
        url = f"https://www.eia.gov/dnav/pet/hist_xls/{code}.xls" if instrument != "HENRY_HUB_SPOT" else f"https://www.eia.gov/dnav/ng/hist_xls/{code}.xls"
        def eia_loader(source=url):
            frame = pd.read_excel(BytesIO(fetch(source)), sheet_name="Data 1", skiprows=2)
            return frame.iloc[:, 0], frame.iloc[:, 1]
        attempt(f"{instrument}__EIA", instrument, name, "USD", "EIA", code, "spot", url, eia_loader,
                "Physical spot prices, not futures; often same originating series as FRED. No synthetic extension or splice.")

    for tenor, column in [("1M", 1), ("3M", 8)]:
        url = "https://www.ciro.ca/sites/default/files/epubs/BARate/BA%20Rate%20History.xls"
        def ciro_loader(source=url, value_column=column):
            content = subprocess.check_output(["curl", "--fail", "--location", "--silent", "--show-error", "--max-time", "30", source])
            frame = pd.read_excel(BytesIO(content), sheet_name="BA Rate History", header=None, skiprows=7)
            dates = pd.to_datetime(frame.iloc[:, 0], errors="coerce")
            values = pd.to_numeric(frame.iloc[:, value_column], errors="coerce") * 100
            return dates, values
        attempt(f"CAD_BA_{tenor}__CIRO", "BAX_SPOT_PROXY", f"Canadian bankers acceptance {tenor} rate, percent per annum",
                "CAD", "CIRO", f"BA Rate History {tenor}", "yield_percent", url, ciro_loader,
                "Underlying cash-market rate, not BAX futures. Source decimal rates multiplied by 100. Calculation waterfall can use other tenors, BAX movements or prior rates; not all days are transaction-based.")

    for variant, kind in [("STRD", "price_index"), ("NETR", "net_total_return_index"), ("GRTR", "gross_total_return_index")]:
        today = datetime.now(timezone.utc).strftime("%Y%m%d")
        url = ("https://app2.msci.com/products/service/index/indexmaster/getLevelDataForGraph"
               f"?index_codes=990100&currency_symbol=USD&index_variant={variant}&data_frequency=DAILY"
               f"&start_date=19970101&end_date={today}")
        def msci_loader(source=url, expected=variant):
            data = json.loads(fetch(source))
            if data.get("index_variant_type") != expected or data.get("ISO_currency_symbol") != "USD":
                raise ValueError(f"Unexpected MSCI response: {str(data)[:200]}")
            frame = pd.DataFrame(data["indexes"]["INDEX_LEVELS"])
            return pd.to_datetime(frame["calc_date"].astype(str), format="%Y%m%d"), frame["level_eod"]
        attempt(f"MSCI_WORLD_{variant}__MSCI", "MSCI_WORLD", f"MSCI World USD {kind}", "USD", "MSCI", "990100/" + variant,
                kind, url, msci_loader,
                "Official public chart endpoint; no account/key. Earliest returned observation may be later than requested. NETR includes net dividends; GRTR includes gross dividends. Index not investable. No prehistory manufactured.")

    persist_manifest()
    # Metadata stays compatible with the shared table, while the manifest carries semantic detail.
    metadata_path = ROOT / "data" / "metadata.csv"
    metadata = pd.read_csv(metadata_path)
    additions = pd.DataFrame([dict(ticker=r["key"], asset_name=r["asset_name"],
                                   ter=0.0024 if r["instrument"] == "URTH_PROXY" else 0.0,
                                   currency=r["currency"]) for r in records.values()])
    if not additions.empty:
        metadata = pd.concat([metadata[~metadata.ticker.isin(additions.ticker)], additions], ignore_index=True)
        metadata.to_csv(metadata_path, index=False)
    return list(records.values()), list(failures.values())


def validate(directory=DESTINATION):
    manifest = json.loads((directory / "sources_manifest.json").read_text())
    rows = []
    for record in manifest["series"]:
        path = directory / record["file"]
        frame = pd.read_csv(path)
        assert list(frame.columns) == ["date", "adjusted_price"], path
        dates = pd.to_datetime(frame.date, format="%Y-%m-%d", errors="raise")
        assert dates.is_unique and dates.is_monotonic_increasing, path
        assert np.isfinite(frame.adjusted_price).all(), path
        assert len(frame) == record["rows"], path
        assert frame.date.iloc[0] == record["start"] and frame.date.iloc[-1] == record["end"], path
        assert hashlib.sha256(path.read_bytes()).hexdigest() == record["sha256"], path
        row = {key: record[key] for key in ["key", "instrument", "provider", "series_type", "start", "end", "rows", "nonpositive_rows", "file"]}
        row["weekend_rows"] = int((dates.dt.dayofweek >= 5).sum())
        row["maximum_gap_calendar_days"] = int(dates.diff().dt.days.max()) if len(dates) > 1 else 0
        row["stale_calendar_days"] = (pd.Timestamp.now().normalize() - dates.iloc[-1]).days
        rows.append(row)
    catalog = pd.DataFrame(rows)
    catalog.to_csv(directory / "catalog.csv", index=False)
    print(f"Validated {len(rows)} series, {catalog.rows.sum():,} observations; negative/zero levels retained.")
    return catalog


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh", action="store_true")
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--provider", action="append", choices=["Yahoo", "pysystemtrade", "pysystemtrade_legacy", "pysystemtrade_archive", "FRED", "EIA", "CIRO", "MSCI"])
    args = parser.parse_args()
    if not args.validate_only:
        acquire(refresh=args.refresh, only=args.provider)
    validate()
