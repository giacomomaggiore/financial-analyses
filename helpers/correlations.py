"""Reusable return alignment and correlation helpers."""

import pandas as pd


def periodic_returns(prices: pd.DataFrame | pd.Series, frequency: str = "ME") -> pd.DataFrame | pd.Series:
    """Calculate period-end total returns from adjusted-price histories."""
    if prices.empty:
        raise ValueError("No prices were supplied.")
    return prices.sort_index().resample(frequency).last().pct_change().dropna(how="all")


def aligned_returns(returns: pd.DataFrame, min_observations: int = 2) -> pd.DataFrame:
    """Keep only periods common to every supplied return series."""
    aligned = returns.dropna(how="any")
    if len(aligned) < min_observations:
        raise ValueError(f"At least {min_observations} aligned return observations are required.")
    return aligned


def correlation_matrix(returns: pd.DataFrame, min_observations: int = 2) -> pd.DataFrame:
    """Calculate a Pearson correlation matrix from a common return sample."""
    return aligned_returns(returns, min_observations).corr()
