# Insights

Record material assumptions, data decisions, results, and their interpretations here as soon as they are established.

## 2026-09-29 - Historical data downloaded

- Decision: Use Yahoo Finance adjusted-close history for NTSG, COM, DBMF, GDE, TAIL, VT, and BNDW. The generated metadata is in `data/metadata.csv`.
- Finding: The UCITS version of NTSG must be requested as `NTSG.L` from Yahoo Finance, while its project data file remains `data/NTSG.CSV`.
- Result: The adjusted-price CSVs downloaded successfully. Their history ranges from 476 observations for NTSG to 4,593 for VT.
- Limitation: Different inception dates constrain any actual-ETF portfolio backtest to the latest common history. Earlier analysis requires clearly labeled synthetic reconstructions.

## 2026-09-29 - Broad correlation proxy set

- Decision: Use VT and BNDW for global equities and global bonds; PDBC for broad commodities; WTMF for managed futures; SPY for US large-cap equities; GLD for gold; and TAIL for the tail-risk strategy.
- Result: Adjusted-price histories for PDBC, WTMF, SPY, and GLD were downloaded and added to `data/metadata.csv`.
- Limitation: These proxies describe asset-class relationships and do not recreate the holdings, futures implementation, or risk profile of the portfolio ETFs. The correlation sample is limited by NTSG's November 2024 inception when using actual holdings and proxies together.

## 2026-09-29 - Synthetic NTSG proxy built

- Decision: Build `data/NTSG_proxy.csv` from 90% URTH developed-market equities, 60% BNDW global bonds, and 10% synthetic USD cash; reset target exposures quarterly and deduct NTSG's 0.25% TER.
- Result: The proxy and `data/USD_CASH.CSV` both contain 2,026 daily observations from 2018-09-06 to 2026-09-29.
- Limitation: The proxy substitutes broad bond exposure for the official basket of US, German, UK, and Japanese government-bond futures, and it uses USD cash instead of multi-currency collateral. It is therefore a synthetic analysis series, not official NTSG or index performance.
- Follow-up: Compare monthly proxy and actual NTSG returns from November 2024 onward before using the proxy in a portfolio backtest.

## 2026-09-29 - Extended NTSG proxy

- Decision: Create `data/NTSG_proxy_extended.csv` separately from the baseline proxy, using SPY, EFA, and EWC for developed equities plus IEF and BWX for government bonds.
- Result: The extended proxy has 4,771 daily observations from 2007-10-11 to 2026-09-29, compared with 2,026 observations from 2018-09-06 for `NTSG_proxy.csv`.
- Limitation: The extended series approximates the public NTSG exposures with fixed regional ETF and US/international bond weights. It is lower fidelity than the baseline proxy and must be used only for sensitivity analysis, never silently spliced into it.

## 2026-09-29 - Strategy proxy series

- Result: `GDE_proxy.csv` provides a 90% SPY, 90% GLD-return, and 10% USD-cash exposure from 2004-11-18; `COM_proxy.csv` uses the published Auspice ABCTRI series from 2000-01-01; and `DBMF_proxy.csv` is a fee-adjusted WTMF peer from 2011-01-05.
- Decision: Use `PPUT.CSV`, the Cboe S&P 500 5% Put Protection Index, as a long-run protective-put benchmark from 1986-06-30 instead of fabricating a TAIL reconstruction.
- Limitation: COM's sector-level signals and DBMF's Dynamic Beta Engine are not publicly reproducible. GLD differs from GDE's gold-futures implementation. PPUT owns equities plus a monthly 5% out-of-the-money put, so it is not equivalent to TAIL's Treasury-backed deep-tail put ladder.

## 2026-09-29 - Proxy accounting correction and validation

- Correction: Replaced gross-notional asset summation in the NTSG and GDE proxies with funded physical sleeves, cash collateral, and separately tracked futures profit and loss. The former method incorrectly multiplied NAV by gross exposure at quarterly resets.
- Correction: Cash now accrues at the latest yield known at the start of each interval. ETF fee add-backs and DBMF fee substitution now compound multiplicatively.
- Result: Corrected terminal proxy levels are 227.98 for NTSG from September 2018, 471.81 for extended NTSG from October 2007, and 5,967.10 for GDE from November 2004. All begin at 100 without artificial first-period jumps.
- Validation: These figures were superseded by the 2026-09-30 closed-month audit below.
- Decision: Keep actual ETF, synthetic sensitivity, and underlying-exposure correlations in separate common-sample panels. Never use PPUT as TAIL inside the model portfolio; it remains a separately labelled protective-put benchmark.

## 2026-09-30 - Methodology audit and proxy upgrades

- NTSG correction: The official index resets on the last business day of February, May, August, and November, not calendar-quarter ends, and also resets if equity or bond exposure differs from target by more than 5 percentage points. Both NTSG proxies now implement those rules. Closed-month validation through August 2026 is recorded below.
- COM correction: Replaced the DBC 252-day moving-average style model with Auspice's published daily collateralized `ABCTRI` levels, less COM's 0.70% fee. The new series has 9,769 observations from 2000-01-01 through 2026-09-29 and ends at 783.37. History before 2010-09-30 is issuer-labelled simulated index history.
- COM validation: Closed-month results through August 2026 are 0.989 correlation, -0.37% annualized mean active return, and 1.34% tracking error against COM. This is materially more faithful than the rejected DBC style model.
- DBMF decision: WTMF and CTA are independent managed-futures systems, not Dynamic Beta Engine reconstructions. Keep WTMF only as a fee-adjusted peer; its 0.279 closed-month correlation rejects it as a backfill. A licensed SG CTA series would be a benchmark, not DBMF performance.
- TAIL decision: Cambria discloses roughly 80%-95% in approximately 10-year Treasuries, 1-16 month SPX puts typically 5%-15% out of the money, roughly 1% of AUM spent monthly, and volatility-sensitive notional sizing. These ranges are insufficient for reconstruction. Keep PPUT only as a separate protective-put benchmark.
- GDE decision: Retain the 90% SPY, 90% GLD-return, 10% cash exposure model as a sensitivity proxy. GDE is active, live exposures drift, and no complete public rebalance or gold-futures roll rule was found.
- Limitation: Source files include a partial September 2026. Correlation and validation outputs now exclude every terminal month unless a later observation proves that month closed.

## 2026-09-30 - MSCI World price-index correlation benchmark

- Decision: Replace VT with Yahoo Finance symbol `^990100-USD-STRD`, stored as `data/MSCI_WORLD_USD.CSV`, for all rolling and monthly correlation panels. The downloaded series contains 14,017 daily observations from 1972-01-03 through 2026-09-30.
- Source: Yahoo Finance chart API, downloaded 2026-09-30.
- Limitation: This is the MSCI World standard price index, not MSCI World Net Total Return. It excludes dividends, emerging markets, and small caps; it is used deliberately to provide a much longer developed-market equity correlation benchmark.

## 2026-10-01 - Inflation correlation data

- Data: Added `data/CPIAUCSL.CSV` from the FRED Consumer Price Index for All Urban Consumers (CPIAUCSL), downloaded 2026-10-01. It contains 955 monthly index observations from 1947-01-01 through 2026-08-01.
- Method: Inflation is the year-over-year percent change in the monthly CPI index. Rolling correlations use 36 monthly observations between that rate and each asset's month-end total return.
- Series: The panels compare inflation with actual WTMF for managed futures, BWX for the longest available global-government-bond proxy, and the fee-adjusted Auspice ABCTRI proxy for commodities.
- Limitation: A correlation between monthly return and year-over-year CPI is descriptive and mixes a one-month asset-return horizon with a trailing 12-month price-change measure; it is not a causal estimate of inflation hedging.

## 2026-09-30 - Daily USD portfolio backtests

- Data decision: Replaced the NTSG source with the EUR-traded `NTSG.DE` listing and added Yahoo Finance `EURUSD=X`, stored as `data/EURUSD.CSV`. Daily NTSG USD values equal the EUR adjusted price times USD per EUR. From 2024-11-13 through 2026-09-30, NTSG returned 18.99% in EUR and 27.03% in USD.
- Cash-rate decision: Added `data/USD_CASH_EFFR.CSV`, a USD cash index compounded across each calendar gap at the prior observed FRED Effective Federal Funds Rate on an ACT/360 basis. The data is used as the daily risk-free return in Sharpe ratios.
- Method: All portfolio legs use daily adjusted prices, target capital weights of 60% NTSG, 10% COM, 15% DBMF, 10% GDE, and 5% TAIL, with month-end rebalancing, zero transaction costs, and zero capital-gains taxes. The 60/40 benchmark is 60% VT and 40% BNDW, rebalanced on the same schedule; VT is the 100% equity benchmark.
- Actual ETF result: On the common 2024-11-13 to 2026-09-30 sample, the model CAGR was 15.70%, maximum drawdown -10.68%, annualized volatility 10.86%, and EFFR-based Sharpe 1.02. The 60/40 benchmark had 11.28% CAGR and 0.72 Sharpe; VT had 17.91% CAGR and 0.87 Sharpe.
- Superseded result: The original proxy-extended run backfilled DBMF with WTMF and began in 2018. The audit rejected that substitution; current results are recorded below.

## 2026-09-30 - Audit: GDE proxy fix, NTSG validation, notebook rebuild

- GDE correction: `GDE_proxy.csv` used GLD *spot* returns as the gold-futures excess return and never subtracted cash, overstating the proxy by about 0.9 x the cash rate per year. After subtracting cash (`excess_return_index`), closed-month validation through August 2026 has +0.93% annualized proxy-minus-fund return, 0.987 correlation, and 3.56% tracking error. The terminal level fell from 5,967 to 4,181 (2004-11-18 start). `USD_CASH_LONG.CSV` was rebuilt from FRED DGS3MO (downloaded 2026-09-30) to cover 2026-09-30.
- NTSG validation correction: `NTSG.CSV` is the EUR-listed line, so validation must convert it to USD with EURUSD first. Closed-month validation through August 2026 has 0.932 correlation, +0.73% annualized tracking difference, and 4.33% tracking error over 21 months.
- Timing caveat: daily NTSG (Xetra close, EURUSD 24:00 London close) versus US-listed assets is non-synchronous. Daily correlation of actual NTSG with the USD proxy is about 0.27 and weekly about 0.81, so daily volatility, Sharpe and drawdown of the actual-ETF backtest are approximate.
- Notebook change: the synthetic-sensitivity backtest does not backfill DBMF or TAIL and uses actual COM because COM predates DBMF. The window starts at DBMF inception, 2019-05-08. Results (USD, monthly rebalancing): model CAGR 11.60%, Sharpe 0.70, max drawdown -22.4%; 60/40 CAGR 8.34%, Sharpe 0.50; VT CAGR 13.10%, Sharpe 0.60. Only NTSG and GDE contain synthetic pre-inception segments.
- Metrics: CAGR uses the full elapsed period. Volatility, Sharpe, and Sortino use the observed sample frequency rather than assuming 252 observations per year. Cumulative return, Calmar, complete-calendar-year return, and one-year rolling-return quantiles are reported.
- Correlation validation: Terminal months are excluded. Through August 2026, proxy/fund correlations are 0.932 for NTSG, 0.987 for GDE, 0.989 for COM, and 0.279 for the WTMF-based DBMF peer.
- Not yet done: EUR and CHF periodic-return reporting and TER-consistent cash rates across proxies (DGS3MO in proxies, EFFR in Sharpe).


## 2026-11-09 - 90/60 Yahoo dataset refresh

- Download timestamp: 2026-11-09T09:07:30.192638+00:00; current UTC date excluded.
- Source: Yahoo Finance chart API via `helpers.data.download_yahoo_prices`; snapshots written with `write_prices`.
- NTSG.L.CSV: 505 observations, 2024-11-08 to 2026-11-06; Yahoo NTSG.L (USD).
- IWDA.L.CSV: 4325 observations, 2009-09-25 to 2026-11-06; Yahoo IWDA.L (USD).
- URTH.CSV: 3727 observations, 2012-01-12 to 2026-11-06; Yahoo URTH (USD).
- IEF.CSV: 6109 observations, 2002-07-30 to 2026-11-06; Yahoo IEF (USD).
- IGOV.CSV: 4471 observations, 2009-01-30 to 2026-11-06; Yahoo IGOV (USD).
- BWX.CSV: 4799 observations, 2007-10-11 to 2026-11-06; Yahoo BWX (USD).
- BNDW.CSV: 2054 observations, 2018-09-06 to 2026-11-06; Yahoo BNDW (USD).
- BIL.CSV: 4893 observations, 2007-05-30 to 2026-11-06; Yahoo BIL (USD).
- EURUSD.CSV: 5951 observations, 2003-12-01 to 2026-11-06; Yahoo EURUSD=X (USD).
- GBPUSD.CSV: 5963 observations, 2003-12-01 to 2026-11-06; Yahoo GBPUSD=X (USD).
- USDJPY.CSV: 7785 observations, 1996-10-30 to 2026-11-06; Yahoo JPY=X (JPY).
- Coverage and exclusions: see `data/90_60_data_manifest.json`. Price indexes, quoted yields and unverified continuous-futures quotes were not saved as total-return inputs.
- Interpretation: these ETF proxies do not reproduce the NTSG equity selection, government-futures basket or multicurrency collateral. Current metadata TERs are not historical fee schedules.
- Existing NTSG.CSV (EUR Xetra listing), MSCI_WORLD_USD.CSV (price index), synthetic proxies and FRED cash series were not replaced. Other listed snapshots were refreshed; old notebook outputs were not recalculated.

## 2026-11-09 - 90/60 research design and reconstruction gates

- Decision: Use three separate evidence tiers: controlled identical-sleeve leverage experiment, implementation-oriented reconstruction, and live ETF validation. The output is a reproducible GitHub analysis and technical blog post, not a claim of automatic Pareto superiority.
- Theoretical control: Before costs, a period-reset 90/60 equals 1.5 times the same 60/40 excess return. Higher return alone does not establish better capital efficiency; include matched-risk comparisons.
- NTSG reference: WisdomTree Global Efficient Core Index methodology, October 2025, https://www.wisdomtree.com/eu/-/media/eu-media-files/other-documents/research/index/wisdomtree-global-efficient-core-index-methodology.pdf. It specifies physical equities, eight US/German/UK/Japanese government futures, multicurrency collateral and February/May/August/November resets. Exact contract mapping, historical weights and exceptional-trigger semantics remain validation gates.
- Accounting: Separate the financed cash-index approximation from actual futures P&L. Do not double-count financing, collateral, roll return or ETF expenses. Remove the unsupported 0.05% annual roll-cost baseline; use documented cost scenarios. The presentation derives the one-rate approximation from 90% funded equities, 10% cash and 60% futures excess return, and adds Tobin (1958) plus CME cheapest-to-deliver/conversion-factor references. Duration/DV01 and yield-curve buckets must be validated, not just notional.
- Coverage result: Yahoo ^990100-USD-NETR returned one current-day point, not usable historical net total returns. ^IRX is a quoted yield, not an adjusted-price index. Tested non-US futures candidates failed; the exact Bloomberg USD-hedged government index was not verified. Do not replace these with the long MSCI price index or unverified continuous-futures percentage returns.
- Practical scope: The downloaded IWDA/IEF/IGOV/BIL/FX panel supports a shorter sensitivity study from September 2009, not a faithful NTSG reconstruction. BNDW adds credit exposure and shortens history to September 2018; live NTSG begins in November 2024. Government-ETF weights and FX/duration treatment must be specified before use.
- Validation: Require self-financing accounting tests, common-sample and FX checks, monthly live tracking diagnostics, dependence-aware uncertainty intervals and explicit data/implementation limitations. Never tune proxy weights and validate them on the same short live window.
- Publication: Check provider redistribution rights before publishing raw data. Keep long-history, proxy and live evidence separate; no new performance results have been calculated by this revision.

## 2026-11-09 - Free long-history alternatives verified

- Follow-up audit: `insights/pareto_superiority_90_60.md` records direct Yahoo checks, free Curvo index downloads and Kenneth French return definitions. `data/90_60_alternative_sources_manifest.json` records identifiers, sources, transformations, coverage and limitations.
- Result: Saved six candidate histories using the existing CSV helpers, without replacing earlier snapshots or changing benchmark parameters. World net total returns, developed-government bonds and USD bill returns permit a 499-return monthly panel from February 1985 through August 2026.
- Validation: Curvo World converted to USD agrees with 309 official MSCI month-end levels over December 2000–August 2026; maximum monthly-return difference is about 0.111 basis points. This does not independently validate the older history or FTSE series.
- Important distinction: Available FTSE candidates are USD-unhedged or EUR-hedged; neither establishes the original USD-hedged bond series or NTSG's futures basket. A currency-policy decision remains necessary. Pre-euro FX is explicitly synthetic.
- Yahoo result: Long US alternatives are verified, including ^SP500TR from 1988, VFINX from 1980, VUSTX from 1986 and VFITX from 1991. MSCI net/gross quotes still returned one point, and the exact Bloomberg identifier BTSYTRUH was not found on Yahoo.
- Data quality: Published French RF columns differ by one basis point in April 1995 and July 2025; the developed equity reconstruction uses RF from its own source. All new CSVs and monthly continuity are validated; no performance result is claimed.
