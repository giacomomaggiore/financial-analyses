# Daily futures data research



## Deliverables

- [Data directory](../data/trend_following_futures/): **111 time-series CSVs**, 976,069 observations in the validated local snapshot, separated by instrument, provider and series type. This includes overlapping sources, not 111 independent markets.
- [Catalog](../data/trend_following_futures/catalog.csv): exact per-file coverage, observation counts, nonpositive levels, weekend observations, longest calendar gap and staleness.
- [Download manifest](../data/trend_following_futures/sources_manifest.json): provider identifiers, complete URLs, pinned archive revisions, download timestamps, currencies, return treatment, limitations and SHA-256 hashes; failed requests are retained too.
- [Source research](../data/trend_following_futures/source_research.json): successful sources, inaccessible/rejected alternatives and an explicit entry for every named manager program.
- [Shared metadata](../data/metadata.csv): registered the new series without replacing existing datasets.
- [Downloader](../helpers/download_trend_following_data.py): reproducible acquisition and offline validation. All dependencies are declared in [requirements](../requirements.txt).

The data directory remains covered by the existing Git ignore. Downloads are persistent local files, not committed market-data redistributions.

## Sources and selection

| Source | Downloaded | What it supplies | Important boundary |
|---|---:|---|---|
| Yahoo Finance / yfinance | 29 | Futures Close, cash indices, spot FX, distribution-adjusted URTH | Futures Close/Adj Close must not be presumed roll-adjusted. Most futures start around 2000. |
| pysystemtrade pinned current sample | 54 | 27 chains, each Panama-adjusted and unadjusted active-contract prices | Sample ends **2024-03-28**, not the download date. Contracts are provider-selected, not necessarily front month. |
| pysystemtrade Eurodollar archive | 2 | Removed EDOLLAR adjusted/unadjusted histories | Through **2023-06-23**, including potentially stale terminal observations. |
| pysystemtrade earlier sample archive | 5 | Earlier Bund, Euro Stoxx and copper samples | Earlier starts, but earlier end dates; two legacy adjustment methods remain unverified. |
| FRED | 12 | Energy spot, FX, policy rates, Treasury yields | Yields are not bond prices or total returns. DFF is calendar daily. |
| EIA | 4 | Official energy spot prices | These are the originating series also republished by FRED, not independent data. |
| CIRO | 2 | Canadian BA 1-month and 3-month cash yields | **Not BAX futures**; ends **2024-07-31**. |
| MSCI public chart API | 3 | Official World USD price, net TR and gross TR | Price starts **1997-01-01**; both TR variants start **2000-12-29**. |

Maximum returned history was requested for each successful source. Sources were **not spliced** to manufacture a longer continuous history. This is the longest accessible history found in this research, not proof that no longer licensed or public archive exists.

### Futures coverage

“Panama start” includes the earlier pinned adjusted archives where these extend the initial date. It is not a claim that the entire date span uses today's exact contract specification.

| Guide instrument | Earliest Panama-adjusted start | Yahoo continuation start | Specific qualification |
|---|---|---|---|
| S&P 500 / ES | 1982-09-14 | 2000-09-18 | Pre-E-mini history belongs to older S&P contracts. |
| Micro S&P 500 / MES | 1982-09-14 | 2019-05-03 | Pre-2019 PST history is a larger-contract backfill, not historical MES trading. |
| Nasdaq-100 / NQ | 1999-12-14 | 2000-09-18 | Not the Nasdaq Composite. |
| Euro Stoxx 50 / FESX | 2013-12-12 | Unavailable | Additional **unverified-adjustment** legacy sample starts 2013-03-19. |
| SOFR / SR3 lineage | 1984-03-23 | One quote only; excluded | PST SOFR contains pre-launch rate-futures history; not pure SOFR since 1984. |
| Eurodollar / ED | 1984-03-23 | Unavailable | Archived separately from the SOFR lineage. |
| US 10-year note / ZN | 1982-08-30 | 2000-09-21 | Not a 10-year cash yield or an Ultra 10-year future. |
| US 2-year note / ZT | 2000-03-02 | 2000-06-02 | Not a 2-year cash yield. |
| US Treasury bond / ZB | 1978-05-31 | 2000-09-21 | PST US20 selected; **not US30/Ultra Bond**. |
| Euro-Bund / FGBL | 2006-09-01 | Unavailable | Earlier adjusted archive ends in 2019; newer sample begins 2006-12-01. |
| Canadian bankers acceptance / BAX | Unavailable | Unavailable | CIRO BA yields supplied separately; no invented BAX chain. |
| Federal funds / ZQ | 1990-03-13 | 2000-09-01 | Separate from the effective fed funds cash rate. |
| Euro FX / 6E | 1999-06-15 | 2000-09-12 | USD per EUR; separate spot-FX histories supplied. |
| Japanese yen / 6J | 1977-06-14 | Not acquired | USD per JPY; added from the same pinned futures sample. |
| British pound / 6B | 1975-12-16 | Not acquired | USD per GBP; added from the same pinned futures sample. |
| WTI crude / CL | 1990-10-16 | 2000-08-23 | PST **CRUDE_W is a winter-contract chain**. |
| Brent crude | 1989-08-11 | 2007-07-30 | PST **BRENT_W is a summer-contract chain**. |
| Henry Hub natural gas / NG | 1990-07-26 | 2000-08-30 | Provider-selected contract; not assumed to match Yahoo's contract. |
| Heating oil / HO | 1980-02-19 | 2000-09-01 | Historical heating-oil / ULSD specification changes matter. |
| Gold / GC | 1975-04-01 | 2000-08-30 | Futures, not London spot fixing. |
| Copper / HG | 1995-02-28 | 2000-08-30 | Additional **unverified-adjustment** legacy sample starts 1993-05-05. |
| Silver / SI | 1970-06-15 | 2000-08-30 | PST SILVER config has a 1,000 point multiplier, not standard SI's 5,000. |
| Corn / ZC | 1972-10-18 | 2000-07-17 | Quote-unit / point-value consistency is essential. |
| Soybeans / ZS | 1985-09-20 | 2000-09-15 | Additive-adjusted history contains nonpositive levels. |
| Coffee C / KC | 2007-02-20 | 2000-01-03 | Yahoo is longer here, but is not verified roll-adjusted. |
| Sugar No. 11 / SB | 1970-02-16 | 2000-03-01 | Oldest futures history acquired. |
| Cotton No. 2 / CT | 1970-03-10 | 2000-01-03 | PST COTTON2, not the differently scaled COTTON instrument. |
| Lean hogs / HE | 1974-07-22 | 2000-12-15 | Historical contract/underlying definitions may change. |
| Live cattle / LE | 1971-10-21 | 2001-03-01 | Not feeder cattle. |

The guide's illustrative June/July 2009 positions define underlying markets, not a request to pretend a single expired contract traded for decades. The downloads are continuations for those markets; the original individual 2009 contracts were not recovered as separate full contract histories. “Livestock” is represented by the explicitly named live cattle and lean hog markets; no unrelated basket was silently added.

### Index, cash and FX comparisons

- S&P 500 **price** history starts **1927-12-30**; Nasdaq-100 starts **1985-10-01**; Yahoo Euro Stoxx 50 starts **2007-03-30**.
- Yahoo MSCI World **price** history starts **1972-01-03**. Do not call this the guide's MSCI World TR benchmark.
- Official MSCI World USD **STRD / NETR / GRTR** were acquired independently. The public API rejected pre-1997 request parameters; valid 1997 requests still returned no TR observations before 2000-12-29. No inference of pre-2000 daily TR was made from monthly data.
- URTH is a separate, expense-bearing, adjusted-price ETF proxy from **2012-01-12**, not a renamed MSCI World gross-return series. Its distributions are included in Yahoo's adjusted prices; do not deduct the TER twice.
- EUR/USD spot begins **1999-01-04** at FRED. USD/CHF begins **1971-01-04** at FRED. Quote directions are **USD per EUR** and **CHF per USD**, respectively.
- Daily 3-month bill yields begin **1954-01-04** and effective fed funds rates **1954-07-01**. SOFR cash rates begin **2018-04-03**. These remain **rates**, not pre-compounded collateral wealth indices.
- Energy spot histories are retained from EIA and FRED separately. They exclude futures carry/roll and cannot substitute for a futures P&L series without changing the research question.
- All source yields are stored in **percent per annum**, including CIRO, whose decimal rates were multiplied by 100. Treasury bill discount yields need an appropriate convention before constructing cash returns. CIRO uses a calculation waterfall; some observations derive from other tenors, BAX movements or prior rates rather than same-day BA transactions.

## Backtest-critical limitations

### Native levels and the CSV schema

Every time-series CSV has exactly `date,adjusted_price` for compatibility with the repository's column names. **The field name does not certify adjustment, total return, investability or positivity.** The manifest's `series_type` is authoritative.

This collection makes an intentional exception to the shared positive-price assumption: negative WTI observations and negative/zero additive-adjusted futures levels are preserved. No absolute values, arbitrary shifts, clipping, log transformations or row deletion were used to make them pass an ETF-oriented validator. The existing shared `load_prices` / `write_prices` functions reject nonpositive values; use `pandas.read_csv` and the dedicated downloader validation for this collection. Existing ETF files/helpers were not changed.

### Futures P&L is not percentage change of an adjusted level

PST's source [adjustment implementation](https://github.com/pst-group/pysystemtrade/blob/bbf5cf823e16be1cca27493a94099eb8cf33f6e7/sysobjects/adjusted_prices.py) uses additive/Panama back-adjustment, adding the contemporaneous forward-minus-current price differential to earlier observations when rolling. Its price level is therefore arbitrary and revises when the adjustment anchor changes.

- Prefer differences in a correctly adjusted price series for point-P&L research, with the correct contract scale and position size. Do **not** apply the guide's simple percentage-return formula to an arbitrary additive-adjusted level.
- An unadjusted chain contains roll jumps: ordinary close-to-close percentage changes are not investable returns.
- A roll-price gap is not itself an execution fee or automatically an equivalent cash loss. Roll/carry economics, actual contract transitions, spreads, commissions and collateral treatment require a coherent futures P&L model.
- There is no futures total-return index, collateral accrual, contract count, margin, spread, fee or execution model embedded in these price files. Metadata TER=0 for futures/indices/rates does not mean costless trading.
- Never append Yahoo raw prices directly to the 2024 PST back-adjusted series. The contract, roll date and adjustment basis can differ. Preserve separate samples or reconstruct with actual matching contract data.

### Contract identity and sampling

PST config and [data documentation](https://github.com/pst-group/pysystemtrade/blob/bbf5cf823e16be1cca27493a94099eb8cf33f6e7/docs/data.md) explicitly allow non-front contracts; SOFR can be held several years out. The original [instrument configuration](https://github.com/pst-group/pysystemtrade/blob/bbf5cf823e16be1cca27493a94099eb8cf33f6e7/data/futures/csvconfig/instrumentconfig.csv) and [roll configuration](https://github.com/pst-group/pysystemtrade/blob/bbf5cf823e16be1cca27493a94099eb8cf33f6e7/data/futures/csvconfig/rollconfig.csv) are pinned references. Pre-launch ES/MES/SOFR history and provider-specific silver sizing are not evidence that the exact modern contracts existed earlier.

Source intraday samples are reduced to the **last nonmissing observation per source calendar date**. No missing dates are inserted and no values are forward-filled. This does not guarantee an official exchange settlement: some source days contain only intraday observations. Source calendar labels are retained rather than guessing exchange-session shifts.

The catalog explicitly flags weekend observations and long gaps. These are **not exchange-calendar-cleaned, execution-ready data**. For example, Yahoo returned a 2026-11-14 Saturday-labelled MSCI/CHF snapshot, and PST contains historical weekend-labelled updates. Inspect calendars, repeated/stale values, time zones and holiday treatment before signals/returns. Do not forward-fill the entire panel across an instrument's unavailable history. DFF's legitimate calendar-day observations should not be mistaken for exchange trading sessions.

The files are **close/level-only**. They support close-based volatility and trend research, not a faithful high/low-based ATR calculation; acquire OHLC or individual-contract bars for that later step.

## Unavailable data and alternatives researched

No unrestricted machine-readable daily histories were verified for **Chesapeake Classic, Dunn WMA, Eckhardt Evolution, EMC Classic, Estlander Alpha, Fort Global Diversified, ISAM Systematic Trend or Mulvaney Global Markets**. Each has its own evidence/source entry in the research JSON. A manager website being reachable is not proof that historical daily NAVs can be downloaded. Monthly factsheets were not interpolated; different mutual funds or generic CTA benchmarks were not silently substituted.

Other results:

- Clenow's free-data page redirected to a suspended-hosting page.
- Stooq's tested CSV endpoint returned browser-verification HTML; the ES futures historical browser page supplied no verified CSV link. No challenge solving was attempted.
- Nasdaq/Quandl CHRIS test download returned HTTP 403. Even if accessible, an unadjusted CHRIS chain should not automatically be called back-adjusted.
- [Norgate](https://norgatedata.com/futurespackage.php) documents arithmetic-adjusted and unadjusted histories, but requires a paid subscription, outside scope. No free full-history no-login Barchart export was verified.
- STOXX's historical text-file endpoint redirected to login. ECB's verified long Euro Stoxx history is a monthly average series; tested daily candidates did not return data.
- DataHub gold histories are monthly/annual, including repeated annual-average observations in early years; they were rejected for daily backtesting. Tested DBnomics LBMA candidates returned 404.
- Removed FRED London gold fixing and USD LIBOR IDs returned 404. Those missing cash series were not synthesized from monthly values or futures rates.
- No verified public full-history ratio-adjusted futures or collateral-inclusive futures return index was acquired. The adjusted and unadjusted types actually obtained are clearly distinguished.

## Reproduction and validation

From the repository root, after installing the declared requirements:

```bash
python -m helpers.download_trend_following_data
python -m helpers.download_trend_following_data --validate-only
python -m unittest discover -s tests -p 'test_trend_following_data.py' -v
```

Existing successful downloads are reused unless `--refresh` is specified; `--provider` restricts acquisition. Immutable PST revisions make source selection reproducible, not current. Live vendor data can revise on refresh. Failed optional candidates remain visible in the manifest and do not masquerade as downloaded files.

Validation checks the two-column schema, parseable unique ascending dates, finite numeric values, manifest row counts/date boundaries, and SHA-256 hashes. It preserves and reports nonpositive observations, computes calendar-gap/weekend/staleness flags, and generates the catalog. This verifies download integrity, **not economic correctness or source accuracy**.

## Rights and attribution

Sources remain attributable to Yahoo, Rob Carver / pst-group and their underlying vendors, the Federal Reserve Bank of St Louis and originating agencies, EIA, CIRO and MSCI. Discovery of MSCI's public chart API was aided by the [msci-data reference](https://pypi.org/project/msci-data/); the downloader calls the official API directly without installing that package.

Personal local research only. Public accessibility, the yfinance software license and pysystemtrade's GPL software license are **not blanket grants of exchange/index market-data redistribution rights**. Keep provider notices and terms in mind before publishing data, derived products or commercial backtests. No account credentials, access-control bypass, paid endpoints or API keys were used.
