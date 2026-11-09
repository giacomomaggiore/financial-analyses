"""Illustrative daily NTSG-inspired country and maturity proxy, not index replication."""

from pathlib import Path
import sys

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from helpers.data import load_prices

SOURCE = Path(__file__).parent / 'sources'
BONDS = {
    'US2': ('SHY.CSV', 'USD'),
    'US10': ('IEF.CSV', 'USD'),
    'US30': ('TLT.CSV', 'USD'),
    'DE2': ('EXHB.DE.CSV', 'EUR'),
    'DE10': ('EXHD.DE.CSV', 'EUR'),
    'DE30': ('EXX6.DE.CSV', 'EUR'),
    'UK10': ('IGLT_L_DEDUP_20241115.CSV', 'GBP'),
    'JP10': ('2561.T.CSV', 'JPY'),
}
FX = {'EUR': 'FRED_USD_PER_EUR_DAILY.CSV', 'GBP': 'FRED_USD_PER_GBP_DAILY.CSV', 'JPY': 'FRED_USD_PER_JPY_DAILY.CSV'}
RATES = {
    'USD': 'FRED_EFFR_RATE.csv', 'EUR': 'FRED_ECBESTRVOLWGTTRMDMNRT_RATE.csv',
    'GBP': 'FRED_IUDSOIA_RATE.csv', 'JPY': 'BOJ_STRDCLUCON_RATE.csv',
}
CURRENCIES = ['USD', 'EUR', 'GBP', 'JPY']
DAY_COUNT = pd.Series({'USD': 360, 'EUR': 360, 'GBP': 365, 'JPY': 365})
SCENARIOS = {
    'illustrative_A': {'USD': 0.70, 'EUR': 0.15, 'GBP': 0.10, 'JPY': 0.05},
    'illustrative_B': {'USD': 0.60, 'EUR': 0.20, 'GBP': 0.10, 'JPY': 0.10},
}


def align_with_staleness(series, calendar, max_stale_days=10):
    series = series.sort_index()
    if not series.index.is_unique or series.isna().any() or not np.isfinite(series).all():
        raise ValueError('Inputs must be finite, nonmissing and unique')
    if series.index.max() < calendar.max():
        raise ValueError('Cannot extrapolate beyond the last observation')
    aligned = series.reindex(series.index.union(calendar)).sort_index().ffill().reindex(calendar)
    observed = pd.Series(series.index, index=series.index).reindex(series.index.union(calendar)).sort_index().ffill().reindex(calendar)
    age = (pd.Series(calendar, index=calendar) - observed).dt.days
    if aligned.isna().any() or (age > max_stale_days).any():
        raise ValueError(f'Missing or stale observations: {series.name}')
    return aligned


def load_rate(filename):
    frame = pd.read_csv(SOURCE / filename, parse_dates=['observation_date'])
    rates = pd.Series(frame.annual_rate_percent.to_numpy(dtype=float) / 100, index=pd.DatetimeIndex(frame.observation_date), name=filename)
    # A conservative two-business-day publication delay avoids using same-day fixings.
    rates.index = rates.index + pd.offsets.BDay(2)
    return rates


def load_panel():
    prices = {'equity': load_prices('IWDA.L.CSV')}
    prices.update({name: load_prices(filename) for name, (filename, _) in BONDS.items()})
    prices.update({ccy: load_prices(filename) for ccy, filename in FX.items()})
    rates = {ccy: load_rate(filename) for ccy, filename in RATES.items()}
    # Actual price and FX coverage, not future-dated publication availability, bounds the study.
    start = max(s.index.min() for s in prices.values())
    end = min(s.index.max() for s in prices.values())
    calendar = pd.date_range(start, end, freq='D')
    aligned_prices = {name: align_with_staleness(s, calendar) for name, s in prices.items()}
    aligned_rates = {name: align_with_staleness(s, calendar) for name, s in rates.items()}
    price_frame = pd.DataFrame(aligned_prices)
    price_frame['USD'] = 1.0
    rate_frame = pd.DataFrame(aligned_rates)
    common = set.intersection(*(set(s.index) for s in prices.values()))
    reset_dates = pd.DatetimeIndex(sorted(d for d in common if d.month in (2, 5, 8, 11)))
    reset_dates = set(pd.Series(reset_dates, index=reset_dates).groupby(reset_dates.to_period('M')).last())
    return price_frame, rate_frame, reset_dates


def simulate(prices, rates, currency_weights, reset_dates, threshold='points', annual_drag=0.0, annual_fee=0.0025):
    if threshold not in ('points', 'relative'):
        raise ValueError('threshold must be points or relative')
    weights = pd.Series(currency_weights, dtype=float).reindex(CURRENCIES)
    if weights.isna().any() or (weights < 0).any() or not np.isclose(weights.sum(), 1):
        raise ValueError('Currency weights must be nonnegative and sum to one')
    if annual_drag < 0 or not 0 <= annual_fee < 1:
        raise ValueError('Costs must be nonnegative and fee less than one')
    if not prices.index.equals(rates.index) or len(prices) < 2:
        raise ValueError('Aligned price and rate panels with at least two days required')
    counts = pd.Series({ccy: sum(c == ccy for _, c in BONDS.values()) for ccy in CURRENCIES})
    bond_weights = pd.Series({name: 0.6 * weights[ccy] / counts[ccy] for name, (_, ccy) in BONDS.items()})
    currency_for_bond = pd.Series({name: ccy for name, (_, ccy) in BONDS.items()})
    first = prices.iloc[0]
    equity = 0.9
    cash = 0.1 * weights / first[CURRENCIES].astype(float)
    notionals = bond_weights / first[currency_for_bond.to_list()].to_numpy(dtype=float)
    values = [1.0]
    rebalances = []
    for i in range(1, len(prices)):
        date = prices.index[i]
        previous, row = prices.iloc[i - 1], prices.iloc[i]
        if (date - prices.index[i - 1]).days != 1:
            raise ValueError('Simulation calendar must contain every day')
        nav_start = equity + (cash * previous[CURRENCIES].astype(float)).sum()
        equity *= row['equity'] / previous['equity']
        cash *= 1 + rates.iloc[i - 1].reindex(CURRENCIES) / DAY_COUNT
        for name, (_, ccy) in BONDS.items():
            bond_return = row[name] / previous[name] - 1
            funding = rates.iloc[i - 1][ccy] / DAY_COUNT[ccy]
            cash[ccy] += notionals[name] * (bond_return - funding)
            notionals[name] *= 1 + bond_return
        fee = nav_start * (1 - (1 - annual_fee) ** (1 / 365))
        bond_usd = notionals * row[currency_for_bond.to_list()].to_numpy(dtype=float)
        cash['USD'] -= fee + annual_drag * bond_usd.sum() / 365
        nav = equity + (cash * row[CURRENCIES].astype(float)).sum()
        if nav <= 0:
            raise ValueError(f'Nonpositive NAV on {date.date()}')
        equity_weight = equity / nav
        bond_weight = bond_usd.sum() / nav
        if threshold == 'points':
            exceptional = abs(equity_weight - 0.9) > 0.05 or abs(bond_weight - 0.6) > 0.05
        else:
            exceptional = abs(equity_weight / 0.9 - 1) > 0.05 or abs(bond_weight / 0.6 - 1) > 0.05
        # Scheduled reset dates are last dates in the month with all inputs observed.
        if date in reset_dates or (date.weekday() < 5 and exceptional):
            rebalances.append((date, 'scheduled' if date in reset_dates else 'exceptional'))
            equity = 0.9 * nav
            cash = 0.1 * nav * weights / row[CURRENCIES].astype(float)
            notionals = nav * bond_weights / row[currency_for_bond.to_list()].to_numpy(dtype=float)
        values.append(nav)
    return pd.Series(values, index=prices.index, name='proxy'), rebalances


def metrics(proxy, nav):
    both = pd.concat([proxy.rename('proxy'), nav.rename('nav')], axis=1).dropna()
    # Observations are retained at their actual dates, not relabelled NAV month-ends.
    last_dates = both.groupby(both.index.to_period('M')).tail(1).index
    monthly = both.loc[last_dates].pct_change(fill_method=None).dropna()
    difference = monthly['proxy'] - monthly['nav']
    if len(monthly) < 2:
        raise ValueError('Insufficient matching monthly NAV observations')
    return {'first_comparison_date': str(both.loc[last_dates].index[0].date()),
            'last_comparison_date': str(both.loc[last_dates].index[-1].date()),
            'months': len(monthly), 'monthly_correlation': monthly.corr().iloc[0, 1],
            'annualized_tracking_error': difference.std(ddof=1) * np.sqrt(12),
            'monthly_rmse': np.sqrt((difference ** 2).mean()),
            'proxy_cumulative': (1 + monthly['proxy']).prod() - 1,
            'nav_cumulative': (1 + monthly['nav']).prod() - 1}


def main():
    prices, rates, reset_dates = load_panel()
    nav = load_prices('NTSG_NAV_USD_WISDOMTREE.CSV')
    results = []
    all_values = {}
    for scenario, weights in SCENARIOS.items():
        for threshold in ('points', 'relative'):
            for drag in (0.0, 0.005, 0.01):
                proxy, rebalances = simulate(prices, rates, weights, reset_dates, threshold, drag)
                label = f'{scenario}_{threshold}_drag_{drag:.3f}'
                all_values[label] = proxy
                summary = metrics(proxy, nav)
                summary.update(scenario=scenario, threshold=threshold, annual_drag_per_bond_notional=drag,
                               first_price_date=str(proxy.index[0].date()), last_price_date=str(proxy.index[-1].date()),
                               cagr=proxy.iloc[-1] ** (365.25 / (proxy.index[-1] - proxy.index[0]).days) - 1,
                               scheduled_resets=sum(kind == 'scheduled' for _, kind in rebalances),
                               exceptional_resets=sum(kind == 'exceptional' for _, kind in rebalances))
                results.append(summary)
    directory = Path(__file__).parent
    pd.DataFrame(results).to_csv(directory / 'daily_scenarios_summary.csv', index=False)
    pd.DataFrame(all_values).rename_axis('date').to_csv(directory / 'daily_scenarios_levels.csv', float_format='%.10f')
    print(pd.DataFrame(results).to_string(index=False))


if __name__ == '__main__':
    main()
