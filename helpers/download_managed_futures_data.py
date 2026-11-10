"""Download public managed-futures research inputs without changing existing snapshots."""

from datetime import UTC, datetime
from hashlib import sha256
from io import BytesIO
import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import pandas as pd

from helpers.data import DATA_DIR, download_yahoo_prices, write_prices

AQR_URL = "https://www.aqr.com/-/media/AQR/Documents/Insights/Data-Sets/Time-Series-Momentum-Factors-Monthly.xlsx"
BARCLAY_URL = "https://portal.barclayhedge.com/cgi-bin/barclay_stats/bcndx.cgi"


def fetch(url, form=None):
    request = Request(url, data=urlencode(form).encode() if form else None,
                      headers={"User-Agent": "financial-investment-analysis/1.0"})
    with urlopen(request, timeout=60) as response:
        return response.read()


def aqr_returns(content):
    table = pd.read_excel(BytesIO(content), sheet_name="TSMOM Factors", header=None)
    first = table.index[table.iloc[:, 1].eq("TSMOM")][0] + 1
    table = table.iloc[first:, :2].dropna()
    dates = pd.to_datetime(table.iloc[:, 0]).dt.to_period("M").dt.to_timestamp("M")
    return pd.Series(table.iloc[:, 1].astype(float).to_numpy(), index=dates, name="aqr_excess")


def barclay_monthly_returns(content):
    table = pd.read_excel(BytesIO(content), header=None)
    records = {}
    for row in table.iloc[2:].itertuples(index=False, name=None):
        if pd.isna(row[0]):
            break  # The second table contains VAMI levels, not returns.
        year = int(row[0])
        for month, value in enumerate(row[1:13], 1):
            if pd.notna(value):
                records[pd.Timestamp(year, month, 1) + pd.offsets.MonthEnd(0)] = float(value)
    return pd.Series(records, name="btop50_net", dtype=float)


def sg_monthly_returns(content, name):
    table = pd.read_excel(BytesIO(content), header=None).iloc[2:, :2].dropna()
    daily = pd.Series(table.iloc[:, 1].astype(float).to_numpy(), index=pd.to_datetime(table.iloc[:, 0]))
    if daily.index.has_duplicates or not daily.index.is_monotonic_increasing:
        raise ValueError("Invalid SG daily dates")
    return ((1 + daily).resample("ME").prod(min_count=1) - 1).rename(name)


def download_managed_futures_data():
    now = datetime.now(UTC)
    cutoff = pd.Timestamp(now.date()).to_period("M").to_timestamp()
    inputs = {}
    sources = []
    specifications = [
        ("aqr_excess", AQR_URL, None, aqr_returns),
        ("btop50_net", BARCLAY_URL, {"dump": "excel", "prog_cod": "BTOP50"}, barclay_monthly_returns),
        ("sg_cta_net", BARCLAY_URL, {"dump": "excelDaily", "prog_cod": "calyon", "return_option": "since_inception"},
         lambda data: sg_monthly_returns(data, "sg_cta_net")),
        ("sg_trend_net", BARCLAY_URL, {"dump": "excelDaily", "prog_cod": "FT90004127", "return_option": "since_inception"},
         lambda data: sg_monthly_returns(data, "sg_trend_net")),
    ]
    for name, url, form, parse in specifications:
        content = fetch(url, form)
        series = parse(content).loc[lambda values: values.index < cutoff]
        if series.empty or series.index.has_duplicates or series.isna().any() or (series <= -1).any():
            raise ValueError(f"Invalid returns: {name}")
        if not series.index.equals(pd.date_range(series.index[0], series.index[-1], freq="ME")):
            raise ValueError(f"Missing monthly returns: {name}")
        inputs[name] = series
        sources.append({"series": name, "url": url, "form": form, "sha256": sha256(content).hexdigest(),
                        "first": str(series.index[0].date()), "last": str(series.index[-1].date()),
                        "observations": len(series)})
    actual = download_yahoo_prices("DBMF")
    actual.index = pd.to_datetime(actual.index)
    actual = actual.loc[actual.index < cutoff]
    if len(actual) < 2:
        raise ValueError("Insufficient DBMF adjusted prices")
    panel = pd.concat(inputs, axis=1).sort_index().rename_axis("date")
    panel.to_csv(DATA_DIR / "MANAGED_FUTURES_MONTHLY.CSV", float_format="%.12f")
    write_prices(actual, "DBMF_ACTUAL.CSV")
    manifest = {
        "retrieved_at_utc": now.isoformat(), "exclusive_month_cutoff": str(cutoff.date()),
        "sources": sources,
        "dbmf": {"url": "https://finance.yahoo.com/quote/DBMF/history/", "file": "DBMF_ACTUAL.CSV",
                 "first": str(actual.index[0].date()), "last": str(actual.index[-1].date()),
                 "expense_ratio": 0.0085, "expense_source": "https://www.imgp.com/us/dbmf/",
                 "return_type": "Adjusted market close total return, net of expenses; not official NAV."},
        "selection": "SG CTA is the closest conceptual fit to DBMF's broad leading-CTA replication. BTOP50 extends the manager-index history to 1987; AQR TSMOM extends it to 1985.",
        "methodology_sources": [
            "https://www.aqr.com/Insights/Datasets/Time-Series-Momentum-Factors-Monthly",
            "https://www.aqr.com/Insights/Research/Journal-Article/A-Century-of-Evidence-on-Trend-Following-Investing",
            "https://ionanalytics.com/barclayhedge/indices/",
            "https://portal.barclayhedge.com/cgi-bin/indices/displayHfIndex.cgi?indexCat=Barclay-Investable-Benchmarks&indexName=BTOP50-Index",
            "https://wholesale.banking.societegenerale.com/fileadmin/indices_feeds/SG_CTA_Index_Methodology.pdf",
            "https://www.imgp.com/imgp-dbi-managed-futures-fund/",
        ],
        "limitations": [
            "AQR downloadable TSMOM starts in January 1985, not 1980. The century paper does not supply a verified monthly download here.",
            "AQR supplies hypothetical excess returns, not a funded total-return ETF; USD bill returns must be added. Transaction-cost deductions are not verified in this workbook.",
            "BTOP50 and SG returns are net manager returns; aggregate 2/20 fee inversion cannot recover individual managers' actual gross returns.",
            "SG monthly export exposes only recent years; daily since-inception ROR is compounded instead. Daily data begin in January 2000.",
            "Gross-up assumes monthly incentive crystallization, management fee of 2%/12 on opening NAV and a net-NAV high-water mark from each source inception.",
            "The stitched series mixes different strategies, risk targets and index constituents. It is a research proxy, not pre-inception DBMF performance.",
            "Candidate comparison uses the observed DBMF overlap for diagnostics only; no parameters are fitted to that overlap.",
        ],
    }
    (DATA_DIR / "managed_futures_sources_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(panel.count().to_string())
    print(f"DBMF adjusted prices: {actual.index[0]:%Y-%m-%d} to {actual.index[-1]:%Y-%m-%d}")


if __name__ == "__main__":
    download_managed_futures_data()
