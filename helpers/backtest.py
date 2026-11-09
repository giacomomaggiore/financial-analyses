"""Backward-compatible portfolio utilities for financial analysis notebooks."""

from pathlib import Path

import numpy as np
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_prices(filename: str, name: str | None = None) -> pd.Series:
    prices = pd.read_csv(DATA_DIR / filename, parse_dates=["date"], index_col="date")["adjusted_price"]
    return prices.sort_index().rename(name or Path(filename).stem)


def weekly_returns(filename: str, name: str) -> pd.Series:
    # Friday sampling reduces non-synchronous closing-time noise across markets.
    prices = load_prices(filename, name).resample("W-FRI").last().dropna()
    if prices.index[-1] > load_prices(filename).index[-1]:
        prices = prices.iloc[:-1]
    return prices.pct_change()


def load_ntsg_usd() -> pd.Series:
    # NTSG trades in EUR but tracks a USD index: EUR price x USD per EUR gives the USD series
    ntsg_eur = load_prices("NTSG.CSV", "NTSG")
    eurusd = load_prices("EURUSD.CSV").reindex(ntsg_eur.index, method="ffill")
    return (ntsg_eur * eurusd).rename("NTSG")


def splice_proxy_to_actual(proxy_filename: str, actual: pd.Series) -> pd.Series:
    # Proxy before the ETF inception, actual ETF afterwards, rescaled so the level is continuous
    proxy = load_prices(proxy_filename)
    start = actual.index.min()
    scaled_actual = actual / actual.iloc[0] * proxy.loc[:start].iloc[-1]
    return pd.concat([proxy[proxy.index < start], scaled_actual]).rename(actual.name)


def align_prices(prices: pd.DataFrame) -> pd.DataFrame:
    # Fill short market-holiday gaps, but reject longer stale-price gaps.
    return prices.sort_index().ffill(limit=5).dropna(how="any")


def monthly_rebalanced_returns(prices: pd.DataFrame, weights: pd.Series) -> pd.Series:
    asset_returns = prices[weights.index].pct_change().fillna(0.0)
    months = asset_returns.index.to_series().dt.month
    is_month_end = (months != months.shift(-1)).to_numpy()
    holdings = weights.astype(float)
    portfolio_returns = []
    for (_, returns), reset in zip(asset_returns.iterrows(), is_month_end):
        holdings = holdings * (1 + returns)
        total = holdings.sum()
        portfolio_returns.append(total - 1)
        # Reset to target weights at month end, otherwise let weights drift
        holdings = weights.astype(float) if reset else holdings / total
    return pd.Series(portfolio_returns, index=asset_returns.index, name="return")


def summary_metrics(returns: pd.Series, cash_prices: pd.Series) -> pd.Series:
    # The first zero return anchors wealth at 1.0 on the common start date.
    wealth = (1 + returns).cumprod()
    years = (returns.index[-1] - returns.index[0]).days / 365.25
    returns = returns.iloc[1:]
    cash_returns = cash_prices.reindex(wealth.index).ffill().pct_change().fillna(0.0).iloc[1:]
    excess = returns - cash_returns
    periods_per_year = len(returns) / years
    drawdown = wealth / wealth.cummax() - 1
    trough = drawdown.idxmin()
    peak = wealth.loc[:trough].idxmax()
    cagr = wealth.iloc[-1] ** (1 / years) - 1
    downside_deviation = np.sqrt((excess.clip(upper=0) ** 2).mean())
    annual_groups = returns.groupby(returns.index.year)
    complete_years = [
        year
        for year, values in annual_groups
        if values.index[0].month == 1 and values.index[-1].month == 12
    ]
    complete_returns = returns[returns.index.year.isin(complete_years)]
    calendar_returns = (1 + complete_returns).groupby(complete_returns.index.year).prod() - 1
    worst_year = calendar_returns.idxmin() if not calendar_returns.empty else np.nan
    rolling_year = (1 + returns).rolling(round(periods_per_year)).apply(np.prod, raw=True) - 1
    return pd.Series({
        "Cumulative return": wealth.iloc[-1] - 1,
        "CAGR": cagr,
        "Volatility": returns.std(ddof=1) * np.sqrt(periods_per_year),
        "Max drawdown": drawdown.min(),
        "Max drawdown period": f"{peak:%Y-%m-%d} to {trough:%Y-%m-%d}",
        "Sharpe": excess.mean() / excess.std(ddof=1) * np.sqrt(periods_per_year),
        "Sortino": excess.mean() / downside_deviation * np.sqrt(periods_per_year),
        "Calmar": cagr / -drawdown.min(),
        "Worst calendar year": worst_year,
        "Worst calendar year return": calendar_returns.min() if not calendar_returns.empty else np.nan,
        "1Y rolling return (5th percentile)": rolling_year.quantile(0.05),
        "1Y rolling return (median)": rolling_year.median(),
        "1Y rolling return (95th percentile)": rolling_year.quantile(0.95),
    })
