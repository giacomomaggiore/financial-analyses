# Global 90/60 — source availability audit

## 2026-11-09: free long-history alternatives verified

A roughly 40-year **generic global equity/government-bond leverage study is feasible with free monthly data**. This does not establish faithful historical NTSG replication. No benchmark selection or backtest implementation was changed.

### Yahoo: actual historical downloads

Checks used `helpers.data.download_yahoo_prices` and direct chart requests, not quote-page existence.

| Identifier | Verified coverage/result | Limitation |
| --- | --- | --- |
| `^990100-USD-NETR` | One observation with max-monthly and ten-year-daily requests; none for a 2000–2019 request | Quote exists, usable history not verified |
| `^990100-USD-GRTR` | One current observation | No long gross-return history verified |
| `BTSYTRUH`, `^BTSYTRUH` | HTTP 404; Yahoo search found no quotes | Actual Bloomberg identifier, not verified on Yahoo |
| `^SP500TR` | 9,786 daily observations, 1988-01-04–2026-11-06 | US total-return index, not global equities |
| `VFINX` | 11,809 observations, 1980-01-02–2026-11-06 | US S&P 500 mutual fund, embedded fees |
| `VUSTX` | 10,197 observations, 1986-05-19–2026-11-06 | Long US Treasury fund, different duration from NTSG |
| `VFITX` | 8,820 observations, 1991-10-28–2026-11-06 | Intermediate US Treasury fund |
| `VEURX`, `VPACX` | 9,165 observations each, 1990-06-18–2026-11-06 | Regional index building blocks, not a complete World replication |
| `VGTSX` | 7,682 observations, 1996-04-29–2026-11-06 | Ex-US equities including emerging markets |

US continuous Treasury futures remain available from 2000, but unverified stitched quotes are not contract-level excess returns. The complete global futures basket remains unverified. Mutual-fund distribution adjustments, historical fees and benchmark changes require validation before use. Daily history was checked because Yahoo's max-monthly sampling can differ materially from the full daily download.

The exact bond index is [Bloomberg Global Treasury Total Return Index Value Hedged USD, BTSYTRUH](https://www.bloomberg.com/professional/products/indices/quote/BTSYTRUH:IND). An identified index is not evidence of a free historical download or equivalence to NTSG futures.

### Free alternatives downloaded and saved

| File in `data/` | Levels | First–last level | Return/currency treatment |
| --- | ---: | --- | --- |
| `MSCI_WORLD_NET_USD_MONTHLY.CSV` | 681 | 1969-12-31–2026-08-31 | Curvo net-dividend index translated from EUR to USD |
| `FTSE_WGBI_DM_USD_UNHEDGED_MONTHLY.CSV` | 500 | 1985-01-31–2026-08-31 | Developed government cash-bond total return, USD unhedged |
| `FTSE_WGBI_DM_EUR_HEDGED_MONTHLY.CSV` | 500 | 1985-01-31–2026-08-31 | Developed government cash-bond total return, EUR hedged |
| `EURUSD_CURVO_MONTHLY.CSV` | 681 | 1969-12-31–2026-08-31 | USD per EUR; ECU/DEM proxies before the euro |
| `FRENCH_USD_BILL_MONTHLY.CSV` | 1,204 | 1926-06-30–2026-09-30 | Base-100 wealth index compounded from published monthly RF |
| `FRENCH_DEVELOPED_USD_MONTHLY.CSV` | 436 | 1990-06-30–2026-09-30 | Research market index compounded from its own monthly `Mkt-RF + RF` |

Actual JSON/ZIP responses were downloaded and written with `helpers.data.write_prices`; CSV schemas, positivity, finite values, unique ascending dates and monthly continuity were checked. All Curvo inputs have zero missing months. The common World/government-bond/cash panel supplies **499 monthly returns, February 1985–August 2026**; January 1985 is a starting level, not an observed January return.

Curvo's public [asset map](https://curvo.eu/backtest/data/asset-map.json) identifies the downloadable histories. Its metadata labels World `net` and government bonds `total`. Native levels are EUR: unhedged USD levels equal EUR levels times matching USD-per-EUR observations. The EUR-hedged index stays in EUR. **Spot conversion does not turn EUR hedging into USD hedging.** See [FTSE's index description](https://www.lseg.com/en/ftse-russell/indices/world-government-bond-index) for the cash-government-bond universe.

The [Curvo FAQ](https://curvo.eu/backtest/en/faq) documents ECU before 1999 and DEM before 1979. Pre-euro EUR results and historical hedged backcasts must remain explicitly synthetic; availability does not validate historical hedge fidelity. Index metadata TER is zero because these are not fund series; implementation costs must be modeled separately.

### Independent MSCI cross-check

The official public MSCI chart endpoint supplied 309 overlapping USD net-return month-end levels, December 2000–August 2026. Against Curvo World converted to USD:

- monthly-return correlation: 0.9999999997911764;
- maximum absolute monthly-return difference: 0.00001109034033630607, approximately **0.111 basis points**;
- maximum relative level difference: 0.00001050518732137462.

This corroborates the overlap and currency conversion, not pre-2000 MSCI history or the FTSE histories. Official MSCI queries before 1997 were rejected; separate 1997–1999 requests returned 12 monthly levels each, while a 2000-only request returned only December. Its public endpoint should not be assumed to supply clean continuous 30-year data.

### Kenneth French definitions

The [developed-market documentation](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/f-f_developed.html) confirms USD returns including dividends and capital gains. Recover total market return by adding RF to Mkt-RF **from the same source file**. This is not MSCI World net withholding-tax treatment.

The US factors ZIP states that RF uses Ibbotson through May 2024 and ICE BofA US 1-Month Treasury Bill Index from June 2024. RF is an ex-post bill return, not an executable borrowing quote. The US and developed files differ by one basis point in April 1995 and July 2025; the manifest records this, and the developed equity reconstruction uses its own RF. Financing spreads and timing remain explicit assumptions.

### Research choices now supported

1. **Primary NTSG-inspired 90/60 proxy:** World net total return plus FTSE WGBI Developed Markets USD-unhedged and a USD cash reference, approximately 1985–2026. It changes the original USD-hedged bond assumption and is not NTSG replication.
2. **Transparent implementation-friction scenarios:** apply specified financing/basis, scheduled-roll, execution and fund-cost assumptions to the proxy. Margin is a month-end collateral stress test only until daily settlement and margin data are sourced; do not claim historical margin survival or realized futures P&L.
3. **Hedge-policy sensitivity:** a separately specified EUR-hedged government-bond experiment. A genuine USD-hedged series requires actual hedge/forward returns or a documented synthetic rehedging model, not spot translation.
4. **Yahoo-only robustness:** US equities plus intermediate/long US Treasury fund histories allow 35–40-year studies, labelled US-only with duration and fund-fee differences visible.
5. **Live NTSG diagnostic:** validate monthly proxy behavior against NTSG only from November 2024. It can identify material tracking differences but cannot conclusively calibrate a long-run model from the short sample.

Coverage, retrieval time, source URLs, transformations and limitations are in `data/90_60_alternative_sources_manifest.json`. Existing benchmark parameters and snapshots were not replaced. Free public access is not automatically a raw-data redistribution licence: check provider rights before GitHub/blog publication and publish acquisition instructions/attributed permitted outputs rather than assuming an open-data licence.

## 2026-11-09 evening: supplemental NTSG replication research

Research and downloads only: the notebook, its parameters and all previously existing price snapshots were left unchanged. New inputs are registered in [metadata](../data/metadata.csv). See the [supplemental manifest](../outputs/pareto_superiority_90_60/research_2026-11-09/manifest.json) for exact source URLs, coverage, transformations and limitations, and [validation results](../outputs/pareto_superiority_90_60/research_2026-11-09/validation.json) for checks and outstanding issues.

### Highest-priority improvement: validate against official NAV

The public [WisdomTree product page](https://www.wisdomtree.com/ch/en/products/equities/wisdomtree-global-efficient-core-ucits-etf---usd-acc) provides View NAV History. Its public `/api/fund-history/54028991?view=navHistory` endpoint returned 507 daily observations, 2024-11-06 through 2026-11-06. Direct terminal requests returned 403; the ordinary browser same-origin request worked. The captured response is retained in the research sources directory.

Saved [NTSG_NAV_USD_WISDOMTREE.CSV](../data/NTSG_NAV_USD_WISDOMTREE.CSV). This is the accumulating USD share-class NAV, already net of expenses: do not deduct TER or add distributions again. It is fund performance, not the underlying index. The published fund inception is 2024-11-05; do not invent an initial NAV for that date because this response starts on 2024-11-06.

Using each series' last available monthly observation, December 2024–August 2026 (21 monthly returns):

- Existing uncalibrated notebook proxy versus official NAV: correlation 0.99018; annualized tracking error 1.749%; monthly RMSE 0.4935%.
- Official NAV versus the existing London adjusted market-price series: correlation 0.95703; annualized tracking error 3.574%.
- Official NAV cumulative return 28.119%; exchange-price cumulative return 28.680%.

This substantially changes the interpretation of the earlier market-price diagnostic: a material part of the apparent tracking mismatch is associated with using exchange prices rather than NAV. Do not fit a subsidy to compensate for that mismatch. The short sample still does not validate a 40-year NTSG reconstruction.

Valuation dates remain important. The last official August 2026 NAV is August 28, not August 31. Monthly resampling relabels the observation; it does not create an August 31 valuation. Retain actual source dates when reconciling fund, proxy and index returns.

### Official current holdings resolve the eight-contract snapshot

The public `/api/fund-holdings/54028991` endpoint returned 371 fund positions as of 2026-11-06, saved as [JSON](../outputs/pareto_superiority_90_60/research_2026-11-09/sources/ntsg_holdings_2026-11-06.json). The eight futures actually disclosed in this snapshot are:

| Market | Contract names | Bloomberg-style December 2026 tickers |
| --- | --- | --- |
| US | 2-year note; 10-year note; long Treasury bond | TUZ6; TYZ6; USZ6 |
| Germany | Euro-Schatz; Euro-Bund; Euro-Buxl 30-year | DUZ6; RXZ6; UBZ6 |
| UK | Long Gilt | G Z6 |
| Japan | 10-year mini JGB | BJZ6 |

Do not assume a four-contract US 2/5/10/30 ladder or a German Bobl contract: neither the US 5-year nor Bobl appears in this snapshot. These are current fund holdings, not proof that the historical index always used precisely these contracts.

The endpoint's `weight` is a market-value weight. Negative futures market values do not imply short notional exposures. Recover notional from contract counts, contract specifications and the index's notional convention; confirm the mini-JGB and US 2-year multipliers separately. The endpoint misleadingly labels cash and futures `asset_group=EQ`; do not use that field to classify exposure. A sum of market-value weights of 100% does not establish 150% gross exposure.

The [October 2025 methodology](https://www.wisdomtree.eu/-/media/eu-media-files/other-documents/research/index/wisdomtree-global-efficient-core-index-methodology.pdf) confirms quarterly resets/rolls in February, May, August and November, currency groups matched to rescaled equity-currency weights, equal contract weights within each currency, and multicurrency collateral. Its short-form exceptional-reset wording is 'more than 5%'; confirm the precise threshold convention and execution timing before calling a band implementation exact.

### Downloaded shorter-history, country-specific bond candidates

| New adjusted-price file | Currency | Saved daily coverage | Role |
| --- | --- | --- | --- |
| [SHY.CSV](../data/SHY.CSV) | USD | 2002-07-30–2026-11-06 | US short government bonds |
| [TLT.CSV](../data/TLT.CSV) | USD | 2002-07-30–2026-11-06 | US long government bonds |
| [EXHB.DE.CSV](../data/EXHB.DE.CSV) | EUR | 2008-01-02–2026-11-06 | German 1.5–2.5-year government bonds |
| [EXHD.DE.CSV](../data/EXHD.DE.CSV) | EUR | 2008-01-02–2026-11-06 | German 5.5–10.5-year government bonds |
| [EXX6.DE.CSV](../data/EXX6.DE.CSV) | EUR | 2008-01-02–2026-11-06 | German 10.5+-year government bonds |
| [IGLT.L.CSV](../data/IGLT.L.CSV) | GBP | 2008-01-02–2026-11-06 | UK conventional gilts |
| [2561.T.CSV](../data/2561.T.CSV) | JPY | 2020-02-26–2026-11-06 | Japanese government bonds |

Existing IEF supplies the US intermediate sleeve; IWDA.L/URTH supply clearly imperfect developed-equity alternatives. These seven new ETF files use Yahoo's daily adjusted-close field, not unadjusted prices or max-monthly sampling. Saved daily coverage is not necessarily fund inception. Two pre-listing observations from 2561.T were explicitly excluded against the issuer's February 2020 launch/listing dates. Its current tax-inclusive management fee is 0.066%; it is not represented as a verified historical all-in cost schedule.

These are research candidates, not certified futures or NAV total-return histories. EXHB.DE and EXHD.DE both show approximately -3.6% on 2009-05-15; investigate issuer NAV and distributions before performance use. IGLT.L's Yahoo adjusted-price 2025 return is approximately 4.73%, versus the issuer's rounded 5.1% NAV return. Do not silently repair, interpolate or winsorize discrepancies. The validation file preserves these flags.

A transparent local-bond approximation can match the correct four countries and multiple maturity segments much better than a world cash-bond aggregate. It still needs delivery-adjusted duration/DV01 comparisons: TLT and EXX6 do not automatically equal US long-bond or Buxl futures. The common Japanese-ETF history limits this particular daily panel to February 2020 onward, not 1985.

### Downloaded long-history country bond alternative

[Swinkels, Laurens (2023), Historical Data: International monthly government bond returns, v6](https://doi.org/10.25397/eur.8152748.v6), is published by Erasmus University Rotterdam under **CC BY 4.0**. The original ODS workbook and Readme PDF are retained in the research sources directory. Extracted the published cached cumulative-return columns without replacing them with a new estimation formula:

| File | First level | Last level |
| --- | --- | --- |
| [SWINKELS_US_10Y_LOCAL_MONTHLY.CSV](../data/SWINKELS_US_10Y_LOCAL_MONTHLY.CSV) | 1946-12-31 | 2022-12-31 |
| [SWINKELS_DE_10Y_LOCAL_MONTHLY.CSV](../data/SWINKELS_DE_10Y_LOCAL_MONTHLY.CSV) | 1972-09-30 | 2022-12-31 |
| [SWINKELS_JP_10Y_LOCAL_MONTHLY.CSV](../data/SWINKELS_JP_10Y_LOCAL_MONTHLY.CSV) | 1974-09-30 | 2022-12-31 |
| [SWINKELS_UK_10Y_LOCAL_MONTHLY.CSV](../data/SWINKELS_UK_10Y_LOCAL_MONTHLY.CSV) | 1970-01-31 | 2022-12-31 |

All four monthly histories are continuous and their level changes reproduce the workbook's cached monthly returns. They are yield-derived, approximately 10-year local-currency par-bond reconstructions, not traded futures or complete maturity ladders. German local returns refer to DEM before 1999 and EUR thereafter; the metadata EUR label does not imply an actual pre-1999 EUR asset. The common bond sample supplies returns from October 1974 through December 2022. Other inputs can shorten the usable portfolio sample.

Use this as a separately labelled country-matched long-history sensitivity alongside the existing 1985–2026 WGBI study. Do not silently splice post-2022 ETFs, apply today's currency weights retrospectively, or claim that a 10-year synthetic bond recreates a 2/10/30 futures ladder. A continuous extension needs a separately documented yield/return construction and overlap comparison.

### FX and funding inputs

Saved new spot series, without replacing existing Yahoo FX:

- [FRED_USD_PER_EUR_DAILY.CSV](../data/FRED_USD_PER_EUR_DAILY.CSV): 1999-01-04–2026-10-30.
- [FRED_USD_PER_GBP_DAILY.CSV](../data/FRED_USD_PER_GBP_DAILY.CSV): 1971-01-04–2026-10-30.
- [FRED_USD_PER_JPY_DAILY.CSV](../data/FRED_USD_PER_JPY_DAILY.CSV): 1971-01-04–2026-10-30, explicitly inverted from FRED's JPY per USD quote.

Federal Reserve FX fixings are not necessarily synchronized with fund NAV or ETF closes. Missing holidays were omitted, not interpolated. A daily DEM identifier returned 404; a verified pre-euro DEM month-end series is still missing. Existing Curvo ECU/EUR data is a separately labelled proxy, not an exact DEM substitute.

Downloaded raw rates into the research sources directory, **not into the positive-price data contract**: daily EFFR (2000–2026), SOFR (2018–2026), euro STR (2019–2026), monthly German/euro-area/UK three-month interbank rates, and monthly Japanese call-money/three-month interbank rates. Exact endpoint coverage is in the manifest. Some monthly histories end well before November 2026. The direct Bank of England SONIA request returned 403; the tested Japanese daily call-money identifier returned 404. Complete current daily GBP/JPY collateral remuneration remains unresolved.

Rates can be negative. They are not observed cash total returns or guaranteed borrowing costs. Apply explicit day counts, actual observation/publication lags and calendar rules before constructing cash accruals. Monthly labels are not availability dates; current vintages do not establish point-in-time inputs.

### Recommended model separation and implementation order

1. **Actual fund validation:** replace market-price calibration with uncalibrated comparison against the downloaded official accumulating NAV. Keep the market-price diagnostic separate; do not deduct the fee twice. Preserve actual valuation dates.
2. **Closer daily NTSG-inspired model, approximately 2020 onward:** global developed equity proxy; US/German maturity ladders and UK/Japanese local government bonds; currency-matched local funding; four-currency collateral; daily equity/cash accounting and futures-like P&L settled into cash. Use historical, known currency weights if available; otherwise predeclare weight scenarios and do not call them replication. Verify ETF distributions/outliers first.
3. **Long-history strategy study:** keep the existing monthly world/WGBI model explicitly generic. Add the Swinkels four-country local-bond experiment through 2022 without hidden splicing. Stress the missing maturity, currency-weight, rate and pre-euro assumptions instead of fitting them to fund returns.
4. **Official rules and uncertainty:** scheduled resets at the specified last business days; explicitly defined exceptional-reset timing; documented roll and financing assumptions; separate equity/fund/index comparisons. Monthly data cannot establish intramonth trigger or margin survival.

For a funded foreign bond, a full USD total return includes FX movement on its principal. A futures overlay does not invest that principal. Approximate futures exposure from **local-currency bond excess returns over local funding**, then translate the resulting P&L into USD; separately translate the actual collateral balances. Do not translate a fully funded foreign-bond total return and merely subtract USD bills. The new approach is still an approximation until settlements, multipliers, roll rules, basis and collateral accounting are verified.

No complete free eight-contract history, full WTNTSGN NTR series, historical ESG constituent sets or point-in-time currency weights was verified. Yahoo's tested German futures/index identifiers returned 404; US continuous futures quotes were available but were not approved as roll-accounted return inputs. The public WTNTSG page is useful for facts/current constituents, but a nearby ticker is not evidence of the required WTNTSGN NTR history.

All 15 new level/price files passed schema, finite/positive-value, ordering and duplicate checks and have matching metadata. These checks do not certify economic fidelity. Research sources and the validation JSON record the remaining gaps; at that research stage the notebook had not been modified.

## 2026-11-09: uncalibrated NAV validation and daily model

The [main notebook](../03_pareto_superiority_90_60.ipynb) now compares its uncalibrated monthly synthetic proxy with official accumulating USD NAV. The earlier fitted market-price adjustment has been removed. The 1985–2026 portfolio calculation remains unchanged: 10.47% proxy CAGR. The NAV comparison still has 21 monthly returns, December 2024–August 2026: correlation 0.9902 and annualized tracking error 1.75%. The NAV observation dates are displayed because the original indices and fund do not always have the same month-end valuation day. A 0% / 0.5% / 1% annual drag-per-bond-notional sensitivity is shown separately; it is not an estimate of actual futures costs.

### Dividend and data reconciliation

[Reconciliation details](../outputs/pareto_superiority_90_60/research_2026-11-09/etf_reconciliation.json) describe checks and unresolved items. BlackRock's official IGLT distribution table confirms one GBP 0.2025 ex-dividend event on 2024-11-14, whereas Yahoo includes the same dividend on both November 14 and November 15. The second event produced a false adjusted-return gain on November 15. The separately saved [IGLT_L_DEDUP_20241115.CSV](../data/IGLT_L_DEDUP_20241115.CSV) removes that event by scaling subsequent levels by $1-0.2025/9.9350004196167$. The original file is unchanged. Its corrected 2024 market-price return is -3.329%, consistent with the issuer's rounded -3.3% NAV return. The 2025 market-price/NAV gap remains unexplained and is not silently corrected.

German EXHB/EXHD 2009-05-15 price drops coincide with third-party reported distributions, but Yahoo returns no dividend events for that month. This is strong evidence of missing adjustments, not a completed issuer-level reconciliation. The daily model starts in 2020 and does not use those 2009 returns; do not use the original ETF series for a 2009 backtest without reconciling them. A scan of 2020–2026 Yahoo dividend events found no other closely spaced identical pairs among the eight bond candidates, which does not establish completeness or accuracy of all dividends.

Found daily Bank of England SONIA via FRED and Bank of Japan uncollateralized overnight call rate via BOJ, so the earlier statement that these histories were unavailable is superseded. Both are included as rate observations in the research sources directory, not positive-price CSVs. They are rate proxies, not verified NTSG financing or collateral rates.

### Daily country/maturity scenarios

The separate runnable [daily model](../outputs/pareto_superiority_90_60/research_2026-11-09/daily_ntsg_approximation.py) and its [scenario summary](../outputs/pareto_superiority_90_60/research_2026-11-09/daily_scenarios_summary.csv) and [daily levels](../outputs/pareto_superiority_90_60/research_2026-11-09/daily_scenarios_levels.csv) preserve the original monthly notebook as a separate generic study. Run from the repository root with `python outputs/pareto_superiority_90_60/research_2026-11-09/daily_ntsg_approximation.py`.

- Common price history is **2020-02-26–2026-10-30**, approximately 6 years and 8 months. The initial date is a starting level; the first simulated return is February 27. FRED's October 30 FX observation currently limits the end date. Returns extend to October 30 but official fund NAV comparisons start with the available November 2024 observations.
- Developed equities use IWDA.L. Eight cash-bond ETFs approximate US 2/10/long, German 2/10/long, UK gilt and Japanese government exposures. These ETF maturities and durations are not the actual contracts or their delivery-adjusted sensitivities. IGLT uses the corrected series.
- Two fixed, illustrative currency scenarios, **not historical index weights**, are A: USD/EUR/GBP/JPY 70/15/10/5 and B: 60/20/10/10. Each currency's notional is equally split between its available maturity proxies. Static assumptions must not be presented as point-in-time official weights.
- Equity is funded; approximate local futures-like P&L is local bond return minus local overnight financing, translated to USD when credited to local-currency collateral. Local notionals drift with total-return ETF proxies; real contract notional and roll accounting differ. Collateral accrues local rates and has its own FX exposure. Both positive and negative cash use the same reference rate. Current 0.25% fund cost is deducted once; component ETF returns already contain their own expenses, creating additional proxy fee drag that is not removed.
- Cash/funding proxies are EFFR, euro STR, SONIA and the BOJ call rate. Rate observations are delayed by two generic business days before use, then the preceding available rate is used for each accrual interval. USD/EUR use actual/360 and GBP/JPY actual/365, as approximations. This is not a complete historical publication calendar, a point-in-time vintage, or a verified fund collateral rate.
- Dates are daily calendar observations. Missing market/FX observations are forward-filled at most ten calendar days, with no extrapolation past the end of input coverage. This can create stale and asynchronous exposures. Scheduled resets use the last **common observed** input date in each official reset month, not a verified official holiday calendar. Exceptional resets are compared under both five-percentage-point and five-percent-relative interpretations. Weekend trigger checks are omitted, intraday moves are unavailable, and no margin-liquidation test is performed.
- Added implementation drag is a transparent 0% / 0.5% / 1% annual scenario applied to bond notional. It does not identify historical futures basis, roll, bid-ask costs, or the true fund costs. The USD bill or local funding component is already subtracted from bond exposure; do not subtract another funding charge.

For scenario A with the percentage-point trigger and zero extra drag, CAGR is **9.25%** over 2020-02-26–2026-10-30. Official NAV comparison uses 23 monthly returns, 2024-11-29–2026-10-30: correlation **0.9835**, annualized tracking error **2.32%**, monthly RMSE **0.655%**, and cumulative return **23.08%** versus NAV **24.32%**. These are in-sample diagnostics, not future evidence. Over the 21 comparable months to August 2026, this scenario's tracking error is **2.37%**, versus **1.75%** for the original monthly approximation; the valuation methods differ and the extra structural detail did not improve observed tracking. Additional positive drag lowers the scenario's cumulative return further; there is no empirical justification here for fitting a cost to make it look like NAV.

No point-in-time index currency weights, complete constituent data or contract-level settlement/roll history was recovered. Thus the daily model is an illustrative approximation, not a verified closer tracking replica. Matching the official NAV over a short interval would not prove historical or out-of-sample fidelity.
