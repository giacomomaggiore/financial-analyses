# Backtest assumption audit and implementation decisions

**Decision date:** 10 November 2026. **Scope:** the current [90/60 + managed-futures notebook](../03_pareto_superiority_90_60.ipynb), not the older WTMF or BNDW experiments. The investor confirmed access to both European UCITS funds and US-listed DBMF, realistic trading costs, and no personal capital-gains taxation. Product access is assumed, not a conclusion about citizenship, broker permissions, or tax eligibility.

## 1. Current research panel and optional comparison periods

The executable notebook parameters and calculations are the source of truth, followed by [the article](../article.md), then this document. Notebook narrative and this methodology describe those calculations; they do not override the executable configuration. There is no configuration that turns the long synthetic history into actual DBMF or NTSG performance. Selecting costs to make the historical strategy look good would be inappropriate. The adopted configuration prioritizes observable product returns, avoids crediting unverifiable fee recovery in the baseline, and charges portfolio trading costs explicitly.

1. **Current historical research panel:** January 1990–August 2026, 440 monthly returns. The managed-futures sleeve uses BTOP50 during 1990–1999, SG CTA from January 2000 through May 2019, then actual DBMF from June 2019. Other sleeves also switch from proxies to observed ETF returns at their first full return month. This is a hypothetical pre-inception implementation, not a tradable 1990 ETF portfolio.
2. **Optional 2000-start comparison:** changing `start_date` to `"2000-01-01"` removes the BTOP50 segment. This is a separate rerun, not a panel automatically displayed by the current notebook.
3. **Optional observed-ETF comparison:** changing `start_date` to `"2024-12-01"` gives 21 all-observed months through August 2026. Positions and entry costs reset for that rerun. The current notebook does not display this as a separate panel; its official-NTSG-NAV diagnostic covers the same dates but is a different comparison.
4. **Optional extended research:** set `start_date = "1985-02-01"` in the parameters cell to include AQR through 1986, then BTOP50 and SG CTA. These strategy and implementation differences make this a lower-confidence robustness exercise. AQR does not contribute to the default 1990-start portfolio.

No allocation, fee, drag, or trading-cost estimate was chosen by optimizing CAGR, Sharpe, drawdown, or the short overlap with an ETF. The assumptions are either sourced product facts, explicit modeling judgments, or display choices. Numerical sensitivity results below are diagnostics, not calibration targets.

## 2. Products: preserve the actual exposures

| Role | Selected product/reference | Verified fact | Decision and remaining difference |
| --- | --- | --- | --- |
| Capital-efficient core | WisdomTree Global Efficient Core UCITS ETF, NTSG, ISIN IE00077IIPQ8 | 0.25% TER; inception 5 November 2024; 90% developed equities, 60% government-futures notional, about 10% collateral [S1, S2] | Retain the requested global product. Use the USD London listing's adjusted total returns after its first full month. The pre-inception funded WGBI bond model cannot reproduce the futures, ESG stock selection or multicurrency collateral. |
| Managed futures | US-listed iMGP DBi Managed Futures Strategy ETF, DBMF | 0.85% expense ratio; inception 7 May 2019; replicates leading managed-futures exposures through liquid futures [S3, S4] | Actual DBMF from June 2019. Before that, SG CTA from January 2000 and BTOP50 during 1990–1999 are broad manager-basket comparators, not DBMF clones. |
| Developed-world equities | iShares MSCI World ETF, URTH | 0.24% expense ratio; MSCI World Net benchmark; inception 10 January 2012 [S5] | Actual adjusted returns from February 2012; before then MSCI World net returns with a hypothetical 0.10% annual implementation allowance. The allowance is the notebook's chosen proxy input, not URTH's actual 0.24% expense ratio or a verified historical fee schedule. |
| Unhedged global government bonds | iShares Global Govt Bond UCITS ETF, IGLO, ISIN IE00B3F81K65 | 0.20% TER; inception 6 March 2009; FTSE G7 Government Bond Index (USD); local-currency sovereign bonds [S6] | Actual USD London adjusted returns from April 2009. Before then use the existing WGBI Developed Markets USD-unhedged series with a hypothetical 0.10% annual implementation allowance, not IGLO's actual 0.20% TER. G7 is not the broader WGBI Developed Markets universe; this splice changes the benchmark and is disclosed, not called identical tracking. |
| Financing/comparison cash | Kenneth French monthly USD bill returns | One-month Treasury bill reference; source changes in June 2024 [S9] | Keep a time-varying cash reference rather than a fixed rate. It is not an executable loan or a complete multicurrency financing model. |

**Rejected substitutions:** BNDW is global aggregate and USD hedged, not unhedged developed sovereign debt. IGOV charges 0.35% and excludes US Treasuries [S7], so it is not a complete replacement for the bond benchmark. GOVT alone would be US-only. RSSB changes the equity/bond notionals and bond universe. WTMF's low prior overlap with DBMF already argues against treating it as DBMF backfill. No product is substituted solely because its fee is low or its observed performance is favorable.

The user has confirmed mixed-market access. If that assumption changes to US-listed-only, NTSG and IGLO cannot simply be relabeled as US products: the implementable strategy and benchmark construction would need to be redesigned.

## 3. Parameters and additional analysis settings

The main parameters are in the code cell beginning `# Parameters`. Bootstrap settings are defined separately in the final analysis cell and documented in section 4.

Annual rates are decimals. One basis point is 0.0001. Integer constants for monthly annualization, zero-return reference lines and numerical solver convergence are conventions, not market forecasts.

### Sample, capital and allocation

| Input | Adopted value | Rationale / evidence |
| --- | --- | --- |
| `DATA` | `Path("data")` | Existing local snapshot convention; no online downloads occur when running the notebook. |
| `start_date` | `"1990-01-01"` | Includes BTOP50 during 1990–1999, followed by SG CTA from January 2000 [S8]. SG's January return compounds daily ROR from 3 January, rather than inferring a return from the first month-end level. The default portfolio contains no AQR segment. |
| `end_date` | `None` | Latest completed month supported by all original equity/bond/cash inputs. Current bottleneck is August 2026, not the later dates of some ETF snapshots. No forward filling beyond observed fund coverage. |
| `initial_value` | `100000.0` | Convenient scalable portfolio capital. Not a return enhancer. Fractional ETF units are assumed; fixed ticket minima, whole-share rounding and idle residual cash are not modeled. A $1,000 mixed-market portfolio may be materially less implementable. |
| `rebalance_months` | `(2, 5, 8, 11)` | NTSG's published scheduled quarter ends [S2]. The two-fund allocation and 60/40 benchmark use the same schedule for comparability, not an asserted DBMF internal trading schedule. |
| `core_weight` | `2 / 3` | Corrects 66% rounding: `(2/3) × 90% = 60%` equities and `(2/3) × 60% = 40%` bond notional, plus one-third funded managed futures. This is the user's intended exposure, not an optimized allocation. |
| `core_equity_weight` / `core_bond_weight` | `0.90` / `0.60` | Published core target notionals [S1, S2]. Synthetic months use them; actual NTSG follows its own holdings. |
| `benchmark_equity_weight` / `benchmark_bond_weight` | `0.60` / `0.40` | Defines the requested 60/40 benchmark. It is not a forecast or optimized weight. |
| `exceptional_rebalance_band` | `0.05` | Approximate five-percentage-point exposure deviation checked at month-end in the synthetic core, consistent with the published exceptional-reset concept [S2]. Actual intramonth timing and the precise index convention cannot be recovered from monthly proxies. `None` disables this approximation. No extra investor transaction fee is charged for an ETF's internal reset. |

### Fees, funding and proxy implementation

| Input | Adopted value | Rationale / evidence |
| --- | --- | --- |
| `fund_ter` | `0.0025` | NTSG's current 0.25% TER [S1]. Only synthetic core months pay this modeled fee. Historical pre-launch fees did not exist. |
| `annual_drag` | `0.005` | Retain 50 bp/year per bond notional as a cautious, **unverified** funded-bond-to-futures implementation allowance. It is not a measured NTSG cost and does not repair the wrong bond/currency/duration universe. At target, direct drag is approximately `(2/3) × 0.60 × 0.005 = 0.002`, or 20 bp/year of the combined portfolio, before drift/compounding. Test 0 and 100 bp as well; do not call 50 bp uniquely accurate. |
| `equity_annual_ter` | `0.0010` | Hypothetical 0.10% annual cost applied only to the standalone World equity proxy before observed URTH. Not URTH's published 0.24% fee [S5] or a verified historical schedule. The synthetic 90/60 core uses the underlying index directly and its own `fund_ter`, not this allowance. |
| `bond_annual_ter` | `0.0010` | Hypothetical 0.10% annual cost applied only to the standalone government-bond proxy before observed IGLO. Not IGLO's published 0.20% TER [S6]. The synthetic 90/60 core uses the underlying bond index directly and its own TER/drag, not this allowance. |
| `dbmf_ter` | `0.0085` | Current 0.85% DBMF expense ratio [S3]. Deducted once from synthetic CTA months; never again from actual DBMF. No investor-level performance fee is charged. |
| `cta_management_fee` | `0.02` | Hypothetical 2% manager fee **only in the gross-up sensitivity and the candidate diagnostic**, not the portfolio baseline. Not a sourced historical constituent fee schedule. |
| `cta_performance_fee` | `0.20` | Hypothetical 20% incentive fee in the same sensitivity and candidate diagnostic, with monthly crystallization and each original index's net-NAV high-water mark from inception. Individual managers' histories and incentive allocations cannot be inferred from an aggregate index. |
| `use_cta_gross_up` | `False` | Key conservative change. SG CTA is already net of constituent fees [S8]. Aggregate 2/20 inversion cannot verify DBMF's proprietary pre-fee replication. The base proxy intentionally retains manager fees and then imposes an ETF fee: it is a conservative net-CTA-minus-fee comparator, **not an unbiased estimate of pre-inception DBMF**. The gross-up case remains visible, not discarded. |
| `aqr_annual_drag` | `0.005` | Explicit 50 bp annual transaction-cost allowance for the optional pre-1987 segment; not a measured AQR cost. AQR publishes excess, hypothetical factor returns [S10]; the downloaded definition does not verify a net-of-transaction-cost funded ETF return. No effect on the default 1990 sample; AQR remains present in the separate candidate diagnostic. Treat that allowance as an uncertain extended-history scenario. |
| `use_actual_core` | `True` | NTSG observed USD adjusted returns replace synthetic core months from December 2024. Synthetic TER/drag no longer affect those months. |
| `use_actual_benchmarks` | `True` | Prefer observed URTH and IGLO returns when available over assuming today's fee perfectly explains historical index tracking. Their adjusted returns include expenses and distributions. |
| `use_actual_dbmf` | `True` | Use observed DBMF rather than the proxy after June 2019. No gross-up, TER deduction or additional synthetic futures turnover is imposed on actual ETF returns. |

At target weights, the synthetic combined portfolio's explicit fund-fee budget is `(2/3 × 0.25%) + (1/3 × 0.85%) = 0.45%` per year. The assumed synthetic bond-notional drag contributes approximately another 0.20%, making approximately 0.65% before investor trading costs and any manager fees retained inside net CTA returns. The synthetic 60/40 fee budget is `0.60 × 0.10% + 0.40 × 0.10% = 0.10%` per year. These benchmark proxy allowances are applied multiplicatively as `(1 + index_return) × (1 − annual_ter)^(1/12) − 1`; the synthetic core instead deducts `fund_cost = 1 − (1 − fund_ter)^(1/12)` from opening NAV and `annual_drag / 12` from opening bond notional. CTA proxy TER is deducted as `dbmf_ter / 12`. These are explanatory target-weight approximations, not additional charges or constant realized tracking differences; observed ETF months use their embedded actual costs.

**Financing is not changed to a fixed percentage.** The synthetic core already has negative cash of approximately 50% of its own NAV at reset, earning/paying the monthly bill return. Adding another full borrowing rate or financing charge to the bond leg would double count that part of the approximation. Actual futures carry depends on repo, cheapest-to-deliver, contract basis and roll [S11], not just USD bills. The single-currency proxy cannot resolve this structurally. Its limitations are more important than debating a few basis points of extra drag.

### Investor trading costs

| Input | Adopted value, per dollar traded | Evidence and interpretation |
| --- | --- | --- |
| `core_trading_cost` | `0.0025` = 25 bp one way | Cautious NTSG execution/commission allowance, not a verified historical median. Official product size is materially smaller than URTH [S1, S5]. There is no reliable long-run spread series in the inputs. A single venue's quote must not be mistaken for an all-venue historical spread. |
| `equity_trading_cost` | `0.0005` = 5 bp one way | URTH issuer page reports a 0.07% **full** 30-day median bid/ask spread as of 9 November 2026 [S5]: half is 3.5 bp. The additional 1.5 bp is a judgmental execution allowance, not measured slippage. The current median is not backfilled as an observed historical spread. |
| `bond_trading_cost` | `0.0010` = 10 bp one way | Explicit IGLO execution/commission allowance. Not a product TER or an observed historical spread. Keep 0.5× and 2× sensitivity because listing, order timing and broker fees differ. |
| `mf_trading_cost` | `0.0010` = 10 bp one way | Explicit DBMF execution allowance. A primary-source historical median spread was not verified; neither an isolated Morningstar quote nor a current narrow quote is treated as its long-run spread. |
| `trading_cost_multiplier` | `1.0` | Uses the stated cost budget without performance-driven tuning. All-in proportional execution budgets include the assumed spread/slippage and proportional commission; no second commission is added. |
| `trading_cost_scenarios` | `(0.5, 1.0, 2.0)` | Declared scenario grid; the current notebook does not automatically loop over it. Section 5 reports audit reruns of `combined_returns(core_returns, managed_futures, cost_multiplier)` at these values. These are assumed multipliers, not confidence bounds; account-specific work requires actual broker minima and execution history. |
| `liquidate_at_end` | `False` | Reports the continuing invested portfolio. `True` charges selling costs at the end. Does not charge a pointless rebalance in the last month and then sell again. |

Cost accounting is self-financing. For starting capital `V`, target weights `w` and one-way cost rates `c`, initial positions total `V / (1 + w·c)`. At a reset, solve `V_after = V_before − Σ c_i |w_i V_after − holding_i|`, then set holdings to `w_i V_after`. Returns include entry cost in the first reported month. The helper iterates this contraction 20 times; allowed cost rates below 10% make numerical error negligible. Buy and sell dollars are both charged once; zero turnover has zero rebalance cost. Pure buy-and-hold equities incur entry cost but no artificial quarterly selling/rebuying.

Internal ETF transaction costs are already reflected in observed fund returns. They are not charged again. Before inception, synthetic core internal frictions are represented by `annual_drag`, while the CTA indices are manager net returns; investor trading costs remain separate. The code does not assume the ETF itself could have been bought in 1990.

### Source boundaries and diagnostics

| Input | Adopted value | Rationale / evidence |
| --- | --- | --- |
| `btop_start` | `"1987-01-31"` | First public BTOP50 return month [S12]; the default portfolio uses its 1990–1999 segment. The optional 1985 extension uses AQR before this boundary. Do not extend BTOP50 to 1980. |
| `sg_start` | `"2000-01-31"` | SG CTA inception month [S8]. Cutovers use original full source histories for fee estimation, not a reset of high-water marks at the selected portfolio start. |
| `validation_drag` | `0.0` | Keep the uncalibrated diagnostic's base case transparent. It is not the main simulation drag or a fitted subsidy. |
| `validation_drag_scenarios` | `(0.0, 0.005, 0.01)` | Uncalibrated 0/50/100 bp per bond-notional scenarios. No winner is chosen from the short NTSG overlap. |
| `drag_sensitivity_min` / `drag_sensitivity_max` | `0.0` / `0.01` | Unverified implementation-cost stress range, not measured fees. Actual NTSG months are unchanged across the range. |
| `drag_sensitivity_points` | `21` | Display resolution, giving 5 bp/year spacing across 0–100 bp. Does not change the main return series. |
| `rolling_months` | `(12, 60, 120)` | Descriptive 1/5/10-year holding periods. Overlapping windows are not independent trials; unavailable windows are skipped. |
| `correlation_months` | `6` | Six-month rolling return correlation. With only six monthly observations per window it is noisy; descriptive, not a trading signal or evidence of systematic crisis protection. |
| `regime_months` | `6` | Trailing six-month equity cumulative return, including the current month-end. Requires a full past window; it is not an ex-ante label for that month's return. |
| `bull_return_threshold` | `0.0` | Non-negative trailing equity total return is labeled bull; negative is bear. This is not the conventional 20%-drawdown definition and does not backdate labels using future troughs. |
| `histogram_bins` | `40` | Visual setting only, with common edges and axes across all three portfolios; no normality or tail-probability assumption. |

### Every source-file parameter

| Input | Value | What is and is not represented |
| --- | --- | --- |
| `equity_file` | `MSCI_WORLD_NET_USD_MONTHLY.CSV` | Historical net-dividend World index. Fund-level withholding/tracking can differ from the standardized net index; no assumption that removing personal taxes removes source withholding. |
| `bond_file` | `FTSE_WGBI_DM_USD_UNHEDGED_MONTHLY.CSV` | Developed sovereign cash-bond total return. Not futures, not USD-hedged, not exactly IGLO's G7 index. |
| `cash_file` | `FRENCH_USD_BILL_MONTHLY.CSV` | Time-varying USD cash reference, not broker financing [S9]. |
| `nav_file` | `NTSG_NAV_USD_WISDOMTREE.CSV` | Official accumulating USD NAV used for diagnostics only, not extra distributions or a second TER. |
| `managed_futures_file` | `MANAGED_FUTURES_MONTHLY.CSV` | Separate AQR excess and BTOP50/SG net monthly series, with provider retrieval metadata. |
| `dbmf_file` | `DBMF_ACTUAL.CSV` | Observed US market adjusted closes, distributions reinvested, already net of expenses. |
| `fx_file` | `EURUSD_CURVO_MONTHLY.CSV` | Spot USD per EUR. EUR wealth equals USD wealth divided by FX, rebased at the initial FX. This is reporting currency, not a hedge or repeated currency trade. |
| `core_actual_file` | `NTSG_ACTUAL_USD.CSV` | Separate refreshed USD London adjusted-close snapshot. Different from official NAV and subject to market-price/closing-time differences. |
| `equity_actual_file` | `URTH_ACTUAL.CSV` | Separate refreshed actual World ETF snapshot; do not deduct 0.24% again. |
| `bond_actual_file` | `IGLO_ACTUAL_USD.CSV` | USD London listing, not a GBP-priced series mislabeled USD. Actual cash government-bond ETF, distributions adjusted; no second 0.20% fee. |

## 4. Currency, performance metrics and omissions

- **Cash bonds versus futures:** an unhedged foreign cash-bond index includes exchange-rate changes on the entire invested principal. A foreign bond future does not automatically create the same currency position on its notional: conversion of P&L, margin flows and the currency of collateral matter. NTSG holds USD/EUR/GBP/JPY collateral, while the proxy finances unhedged cash bonds against USD bills. A constant drag cannot repair this structural currency/carry/duration mismatch. See [article Appendix A](../article.md#appendice-a--rischio-valutario-della-proxy-obbligazionaria).
- **Unhedged EUR:** month-end spot translation uses USD per EUR, with an ECU proxy before 1999. At common dates the FX factor cancels in relative wealth, necessarily preserving final-wealth and CAGR rankings; volatility, drawdowns and risk-adjusted ratios can change. There is no forward hedge or change into a EUR-funded strategy. This reporting conversion does not fix the synthetic core's cash-bond currency mismatch. The account is assumed already USD-funded; converting chart units alone creates no broker currency transaction. Actual initial/final conversion costs require broker/timing assumptions.
- **EUR Sharpe/Sortino:** the comparison cash asset is USD bills translated to EUR. It carries FX risk and is explicitly not called a EUR risk-free investment. A true EUR cash benchmark would change the risk-adjusted ratios and needs an appropriate historical cash source; it is not invented here.
- **Metric conventions:** nominal month-end total returns; CAGR compounds over `number_of_months / 12`. Volatility is sample monthly standard deviation times `sqrt(12)`. Sharpe is the monthly mean excess return divided by its sample standard deviation, times `sqrt(12)`; Sortino uses the root mean square of negative excess returns over all months as its denominator, then the same annualization. Calmar is full-sample CAGR divided by the absolute full-sample maximum drawdown. Annualization assumes monthly dependence is not material; these ratios are descriptive, not significance tests.
- **Average drawdown:** mean of each drawdown episode's worst loss, including an unrecovered final episode, per the user's choice. Not the average of monthly underwater observations.
- **Ulcer index:** root mean square of drawdowns at all sampled month-ends, including zero drawdowns but excluding the extra initial wealth observation. Reported as a percentage, without annualization. All drawdowns use a high-water mark that includes initial capital; monthly sampling does not recover intramonth losses or daily margin stress.
- **Rolling returns:** cumulative returns over 12, 60 and 120 months, not annualized multi-year returns. The separate 12-month-return dispersion is their sample standard deviation, without another annualization. Overlapping windows are not independent.
- **Relative wealth:** each portfolio's wealth divided by 60/40 wealth, initially 1. The chart shows the model and equities with a 60/40 reference at 1. A rising ratio means relative outperformance; a level above 1 means more wealth since the common start, not outperformance in every intervening period.
- **Candidate diagnostic:** June 2019–May 2026, 84 common monthly observations; AQR availability limits the common end. SG CTA, SG Trend and BTOP50 receive the hypothetical 2/20 gross-up and a 0.85%/12 proxy fee in this diagnostic regardless of baseline `use_cta_gross_up=False`. AQR receives cash, its 0.50% annual drag and the same proxy fee, but no CTA gross-up. The reported SG CTA tracking error of 5.81% belongs to this diagnostic, not the baseline net-CTA series. AQR's funded comparison starts in February 1985 because the common bill/index return panel begins then, although the raw factor starts in January 1985.
- **NTSG validation:** 21 common months, December 2024–August 2026; official NAV versus uncalibrated core with `validation_drag=0`, not the 0.50% baseline drag. Monthly correlation is 0.990 and annualized tracking error 1.75%. This short equity-dominated overlap does not verify the long-run bond/currency approximation.
- **Bootstrap:** `paired_circular_bootstrap` uses 10,000 paired circular-block resamples of the current model and 60/40 monthly portfolio returns, each with the original sample length. Defaults are block lengths `(6, 12, 24, 60)` and seed `20261110`. One generator advances through those lengths in that order. Both portfolios use identical sampled months; CAGR is recomputed from each sampled return path. The 2.5th/97.5th percentiles of the CAGR difference form an exploratory 95% interval, conditional on this model and sample, not proxy, historical-cost or structural-change uncertainty.
- **Personal taxes:** no personal capital-gains taxation is applied. Fund withholding, expenses, internal tax effects and actual distributions remain embedded in observed adjusted returns or net indices; they are not grossed up. Automatic reinvestment of distributions is assumed without separate DRIP fees.
- **No hidden optimizations:** fixed allocation and windows; no return-driven leverage scaling, no proxy volatility fit to DBMF, no changing history to erase a crisis. SG versus AQR risk-target differences remain disclosed.
- **Not modeled:** fixed/minimum commissions, whole-share rounding, trade-size market impact, historical broker currency spreads, personal income/dividend/estate/PFIC taxes, securities-lending income in synthetic pre-inception funds, bid/ask histories, point-in-time manager membership, futures contract settlement/margin or historical expense-ratio changes. A large institutional order or a very small account requires different execution assumptions.

## 5. Verified impact, not a forecast

The current January 1990–August 2026 USD panel, 440 monthly returns and 100,000 USD starting capital, reports the same results as the article:

| Portfolio | Total return | CAGR | Volatility | Max drawdown | Average drawdown | Ulcer index | Sharpe | Sortino | Calmar |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 90/60 + managed futures | 1321.61% | 7.51% | 10.35% | -32.25% | -4.91% | 7.23% | 0.49 | 0.75 | 0.23 |
| 60/40 | 950.88% | 6.63% | 9.94% | -34.24% | -4.62% | 7.90% | 0.43 | 0.62 | 0.19 |
| 100% equities | 1560.24% | 7.96% | 15.02% | -54.09% | -6.78% | 15.31% | 0.41 | 0.58 | 0.15 |

At the common end, model/60-40 wealth is 1.3528: 35.28% more ending wealth, not 35.28 percentage points of annual return. The standard deviations of overlapping 12-month cumulative returns are 10.35%, 9.97% and 15.87%, respectively.

### Assumption sensitivities on the same dates

| Hypothesis | Combined CAGR |
| --- | ---: |
| Bond-notional drag 0% | 7.71% |
| Bond-notional drag 0.50% — baseline | 7.51% |
| Bond-notional drag 1.00% | 7.31% |
| Hypothetical CTA 2/20 gross-up, baseline drag | 8.52% |

The gross-up raises CAGR by about 1.01 percentage points per year, a model-assumption effect, not measured DBMF alpha. The article's trading-cost sensitivity was independently reproduced using the notebook's `combined_returns` function: CAGR is 7.52%, 7.51% and 7.48% at 0.5×, 1× and 2× the cost budget. This grid is declared but not automatically tabulated by the current notebook. Synthetic drag and CTA fee-inversion changes leave the observed ETF sleeve returns unchanged; trading-cost changes still affect investor entry and rebalancing during observed ETF months.

### Exploratory bootstrap and interpretation

| Block length (months) | Lower 95% CAGR difference (pp/year) | Upper 95% CAGR difference (pp/year) |
| --- | ---: | ---: |
| 6 | -0.163 | +1.944 |
| 12 | -0.064 | +1.858 |
| 24 | +0.052 | +1.730 |
| 60 | +0.312 | +1.507 |

The article rounds the 12-month-block interval to [-0.06; +1.86] percentage points per year. It includes zero and changes with block length; it is not a definitive significance verdict. The model has higher historical CAGR and Sharpe and a less severe maximum drawdown than 60/40, but higher volatility and a worse episode-average drawdown. Its lower Ulcer index measures a different aspect of losses. These are trade-offs, not Pareto dominance or proof of general product superiority. The optional 2000-start and all-observed reruns are not current headline outputs.

## 6. Sources and reproducibility

Sources were checked on 10 November 2026. Fee/product pages describe current terms, not a point-in-time historical schedule. Some issuer pages restrict direct automated access; the URTH issuer page and official fact sheet were verified through indexed issuer content. No third-party live quote was promoted to a historical trading-cost estimate.

- **S1 — WisdomTree NTSG product information and factsheet:** [product page](https://www.wisdomtree.com/se/products/equities/wisdomtree-global-efficient-core-ucits-etf---usd-acc), [official factsheet](https://www.wisdomtree.com/gb/media/factsheet/ucits/eu/en-gb/ie00077iipq8/factsheet-ie00077iipq8-wisdomtree-global-efficient-core-uc). Supports 0.25%, global 90/60 design, inception, accumulation and current product size.
- **S2 — WisdomTree October 2025 index methodology:** [methodology](https://www.wisdomtree.eu/-/media/eu-media-files/other-documents/research/index/wisdomtree-global-efficient-core-index-methodology.pdf). Supports quarterly reset months, exceptional-reset concept, 90/60/10 exposures, futures/currency structure; does not validate the funded WGBI proxy or its 50 bp drag.
- **S3 — iMGP US DBMF:** [official product page](https://www.imgp.com/us/dbmf/). Supports 85 bp expense ratio, May 2019 inception and replication concept; does not support the exact historical 2/20 fee inversion used here.
- **S4 — iMGP DBi strategy description:** [managed-futures strategy](https://www.imgp.com/imgp-dbi-managed-futures-fund/). Supports representative leading-CTA pre-fee exposure replication and implementation in liquid futures, not public reconstructibility of historical holdings.
- **S5 — iShares URTH:** [issuer page](https://www.ishares.com/us/products/239696/), [official fact sheet](https://www.ishares.com/us/literature/fact-sheet/urth-ishares-msci-world-etf-fund-fact-sheet-en-us.pdf). Supports 0.24%, MSCI World Net, launch date and the current 0.07% full-spread observation. Not evidence that trading has always cost 5 bp.
- **S6 — iShares IGLO:** [issuer page](https://www.ishares.com/ch/individual/en/products/251753/ishares-global-government-bond-ucits-etf), [official fact sheet](https://www.ishares.com/ch/individual/en/literature/fact-sheet/iglo-ishares-global-govt-bond-ucits-etf-fund-fact-sheet-en-ch.pdf). Supports 0.20%, G7 government bond benchmark, March 2009 launch, USD listing and unhedged local-currency sovereign exposure. Not evidence for a 10 bp historical spread.
- **S7 — iShares IGOV:** [issuer page](https://www.ishares.com/us/products/239830/), [fact sheet](https://www.ishares.com/us/literature/fact-sheet/igov-ishares-international-treasury-bond-etf-fund-fact-sheet-en-us.pdf). Supports 0.35% and non-US developed sovereign exposure; reason it is not the whole global bond leg.
- **S8 — Société Générale CTA methodology:** [official methodology](https://wholesale.banking.societegenerale.com/fileadmin/indices_feeds/SG_CTA_Index_Methodology.pdf). Supports inception 1 January 2000, manager-basket construction and returns net of constituent fees. Data download provenance is in [the managed-futures manifest](../data/managed_futures_sources_manifest.json).
- **S9 — Kenneth French:** [factor definitions](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/f-f_factors.html). Supports the monthly RF reference and the June 2024 data-source change, not an executable borrowing rate.
- **S10 — AQR TSMOM:** [dataset description](https://www.aqr.com/Insights/Datasets/Time-Series-Momentum-Factors-Monthly), [workbook](https://www.aqr.com/-/media/AQR/Documents/Insights/Data-Sets/Time-Series-Momentum-Factors-Monthly.xlsx). Supports excess returns from January 1985 and hypothetical factor construction. No assertion is made that this download is a funded net-of-cost ETF return.
- **S11 — CME Treasury futures:** [cheapest-to-deliver and implied repo](https://www.cmegroup.com/education/courses/introduction-to-treasuries/get-to-know-treasuries-ctd), [Treasury analytics definitions](https://www.cmegroup.com/tools-information/quikstrike/quikstrike-treasury-analytics-user-guide.html). Explains why actual futures carry is not a universal bill rate plus a constant spread.
- **S12 — BarclayHedge:** [index directory](https://ionanalytics.com/barclayhedge/indices/), [BTOP50](https://portal.barclayhedge.com/cgi-bin/indices/displayHfIndex.cgi?indexCat=Barclay-Investable-Benchmarks&indexName=BTOP50-Index). Supports the optional older manager-index comparator; BarclayHedge is not Barclays Bank.

Actual prices use the existing Yahoo adjusted-close acquisition helper; these are not certified issuer NAV histories. Source files and timestamps are saved separately in [the implementation manifest](../data/realistic_backtest_sources_manifest.json). Existing price snapshots are not overwritten.

A limited calendar-return reconciliation was performed, not a complete dividend audit. URTH's downloaded 2025 adjusted-close return is 21.36%, matching the issuer fact sheet's 21.36% market-price figure [S5]; 2024 is approximately 18.66%, versus the rounded issuer market-price 18.67%. IGLO's downloaded 2025 market-price return is 7.14%, matching the price-return column of [Morningstar's IGLO performance table](https://www.morningstar.com/etfs/xlon/iglo/performance); its separate NAV column is 6.45%, a material 0.69-percentage-point difference. That secondary-source price match is not an issuer NAV reconciliation. DBMF's downloaded 2025 adjusted return is 13.844%; a primary-source full historical reconciliation was not completed. NTSG NAV-versus-market timing differences were already identified in [the source audit](../insights/pareto_superiority_90_60.md). These gaps remain visible rather than being corrected by fitting a fee or overwriting prices.

```bash
python -m helpers.download_managed_futures_data
python -m helpers.download_implementation_data
python -m unittest discover -s tests -p 'test_pareto_metrics.py'
```

Run the notebook from the repository root after installing the existing project requirements. Raw data remain excluded by the repository's existing ignore policy; the downloader and attributed methodology are the reproducible artifacts, not a claim of raw-data redistribution rights.
