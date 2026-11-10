# DBMF Methodology and Peer Decision

The current monthly comparison is governed by the [10 November 2026 assumption audit](realistic_backtest.md): SG CTA net returns less a hypothetical ETF fee before observed DBMF, with aggregate gross-up only as a sensitivity. The WTMF files discussed below belong to an older, separate experiment and are not inputs to that notebook.

## Status

DBMF cannot be reconstructed from public rules. `data/DBMF_proxy.csv` is a
fee-adjusted WTMF peer and must never be described as synthetic DBMF or inserted
into the model portfolio as a DBMF backfill. Use actual `data/DBMF.CSV` from the
fund's 2019-05-07 inception.

## Official Strategy

DBMF is actively managed and seeks to replicate the pre-fee performance of a
representative basket of leading managed-futures hedge funds. DBi's published
process is conceptually:

1. Observe recent returns from a representative managed-futures hedge-fund pool.
2. Add back estimated hedge-fund management and performance fees to approximate
	gross strategy returns.
3. Use a proprietary multi-factor model, the Dynamic Beta Engine, to estimate
	the aggregate exposures that explain those returns.
4. Express the estimated exposures through liquid long and short futures and
	forwards across equity indices, fixed income, currencies, and commodities.
5. Re-estimate and trade dynamically as the inferred hedge-fund exposures change.

This is factor replication of managers, not a conventional trend rule applied
independently to each market. Public materials do not provide the point-in-time
manager universe, return inputs, estimation window, regressors, constraints,
regularization, exposure caps, trade thresholds, or exact rebalance schedule.
Those omissions prevent an out-of-sample historical reconstruction.

The fund uses substantial gross notional exposure and holds Treasury bills or
cash collateral. Futures notionals must therefore be modeled as profit and loss,
not as additional funded holdings. DBMF charges 0.85% annually.

## Project Peer Series

`data/DBMF_proxy.csv` starts with WTMF adjusted prices, approximately removes
WTMF's 0.65% fee, and deducts DBMF's 0.85% fee:

$$
V_t=V_{t-1}\frac{P_t}{P_{t-1}}
\frac{(1-0.0085/365)^{d_t}}{(1-0.0065/365)^{d_t}}.
$$

This only normalizes the fee assumption. It does not transform WTMF's signals,
markets, risk allocation, collateral, or positions into DBMF's Dynamic Beta
Engine.

## Validation and Rejection as Backfill

From June 2019 through August 2026, 87 closed-month returns have only 0.279
correlation, -3.47% annualized mean peer-minus-DBMF return, and 11.32% annualized
tracking error. This evidence rejects WTMF as a historical DBMF backfill.

## Other Comparators

- The SG CTA Index is DBMF's more relevant manager benchmark because it measures
  a pool of major systematic CTAs. It is non-investable, fee-bearing manager
  performance and still does not reveal DBMF's inferred positions.
- Simplify CTA is a systematic long/short trend fund in commodity and interest-rate
  futures. It omits DBMF's broad equity and currency implementation, follows its
  own signals, and began only in March 2022. It adds no useful backfill history.
- WTMF remains useful as an investable managed-futures peer, but not as a clone.

No comparator should be selected because it happens to improve in-sample fit.
A licensed daily SG CTA history could be added as a benchmark panel, not as fund
performance.

## Sources

- [iMGP DBMF fund page](https://www.imgp.com/us/fund/us53700t8273-imgp-dbi-managed-futures-strategy-etf/)
- [DBi Managed Futures strategy](https://www.imgp.com/us/strategy/dbi-managed-futures-strategy/)
- [Simplify CTA](https://www.simplify.us/etfs/cta-simplify-managed-futures-strategy-etf)