"""Reusable utilities for transparent financial-instrument proxy construction."""

import numpy as np
import pandas as pd


def fee_adjusted_returns(returns: pd.Series, annual_fee: float, periods_per_year: float = 252) -> pd.Series:
    """Apply an annual fund fee to periodic returns."""
    if annual_fee < 0 or periods_per_year <= 0:
        raise ValueError("annual_fee must be non-negative and periods_per_year must be positive.")
    return (1 + returns) * (1 - annual_fee) ** (1 / periods_per_year) - 1


def proxy_from_returns(returns: pd.Series, annual_fee: float = 0.0, periods_per_year: float = 252, base_value: float = 100.0) -> pd.Series:
    """Compound periodic returns into a fee-adjusted proxy index."""
    if base_value <= 0:
        raise ValueError("base_value must be positive.")
    adjusted_returns = fee_adjusted_returns(returns.fillna(0.0), annual_fee, periods_per_year)
    return (base_value * (1 + adjusted_returns).cumprod()).rename(returns.name)


def excess_returns(total_returns: pd.Series, cash_returns: pd.Series) -> pd.Series:
    """Remove collateral return from total returns to approximate futures excess returns."""
    aligned = pd.concat([total_returns, cash_returns], axis=1).dropna()
    return ((1 + aligned.iloc[:, 0]) / (1 + aligned.iloc[:, 1]) - 1).rename(total_returns.name)


def weighted_returns(returns: pd.DataFrame, weights: pd.Series, rebalance_frequency: str = "ME") -> pd.Series:
    """Calculate a periodically rebalanced weighted return series."""
    if not weights.index.is_unique or set(weights.index) != set(returns.columns):
        raise ValueError("weights must uniquely match the return columns.")
    if not np.isclose(weights.sum(), 1.0):
        raise ValueError("weights must sum to 1.0.")
    rebalance_dates = set(
        returns.groupby(pd.Grouper(freq=rebalance_frequency)).apply(lambda period: period.index[-1]).tolist()
    )
    holdings = weights.reindex(returns.columns).astype(float)
    values = []
    for timestamp, row in returns.fillna(0.0).iterrows():
        holdings *= 1 + row
        portfolio_return = holdings.sum() - 1
        values.append(portfolio_return)
        holdings = weights.reindex(returns.columns).astype(float) if timestamp in rebalance_dates else holdings / holdings.sum()
    return pd.Series(values, index=returns.index, name="return")
