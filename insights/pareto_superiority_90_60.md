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
