"""Self-financing ETF allocation returns including investor-level trading costs."""

import numpy as np
import pandas as pd


def rebalance_portfolio(asset_returns, weights, trading_costs, rebalance_months, liquidate=False):
    weights = np.asarray(weights, dtype=float)
    costs = np.asarray(trading_costs, dtype=float)
    if (asset_returns.empty or asset_returns.isna().any().any()
            or not np.isfinite(asset_returns).all().all() or (asset_returns <= -1).any().any()):
        raise ValueError("Invalid asset returns")
    if (len(weights) != asset_returns.shape[1] or costs.shape != weights.shape
            or not np.isfinite(weights).all() or (weights < 0).any() or not np.isclose(weights.sum(), 1)
            or not np.isfinite(costs).all() or (costs < 0).any() or (costs >= 0.1).any()):
        raise ValueError("Invalid portfolio weights or one-way trading costs")
    if any(month not in range(1, 13) for month in rebalance_months):
        raise ValueError("Invalid rebalance months")

    # Initial purchases are paid out of the initial capital, not added externally.
    balances = weights / (1 + weights @ costs)
    previous_nav = 1.0
    monthly_returns = []
    for position, (date, row) in enumerate(asset_returns.iterrows()):
        balances *= 1 + row.to_numpy()
        nav = balances.sum()
        last_month = position == len(asset_returns) - 1
        if last_month and liquidate:
            balances *= 1 - costs
        elif date.month in rebalance_months and not last_month:
            # Solve NAV after costs because the target purchases depend on those costs.
            post_cost_nav = nav
            for _ in range(20):
                post_cost_nav = nav - np.abs(post_cost_nav * weights - balances) @ costs
            balances = post_cost_nav * weights
        ending_nav = balances.sum()
        monthly_returns.append(ending_nav / previous_nav - 1)
        previous_nav = ending_nav
    return pd.Series(monthly_returns, index=asset_returns.index)


def splice_actual_returns(proxy, actual, enabled=True):
    """Use full observed ETF months without a second fee or post-inception gap filling."""
    if not enabled:
        return proxy.copy()
    if actual.empty or not actual.index.equals(pd.date_range(actual.index[0], actual.index[-1], freq="ME")):
        raise ValueError("Missing or non-contiguous actual ETF return history")
    result = proxy.copy()
    observed_dates = result.index[result.index >= actual.index[0]]
    result.loc[observed_dates] = actual.reindex(observed_dates)
    if result.isna().any():
        raise ValueError("Actual ETF history does not cover the requested proxy dates")
    return result
