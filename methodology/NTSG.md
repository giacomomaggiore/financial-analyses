# NTSG Historical Proxy

The current monthly comparison is governed by the [10 November 2026 assumption audit](realistic_backtest.md): a generic historical World/WGBI core followed by observed NTSG returns, with explicit investor execution costs. The URTH/BNDW files discussed below describe an earlier, separate proxy and are not the current notebook's historical input basket.

## Status

`data/NTSG_proxy.csv` is a transparent synthetic proxy, not the official
WisdomTree Global Efficient Core Index or NTSG ETF. Use actual `data/NTSG.CSV`
from the UCITS fund's 2024 history whenever possible. Every output using either
synthetic series must say so.

## Official Strategy

The UCITS ETF tracks the WisdomTree Global Efficient Core Index (NTR), Bloomberg
ticker `WTNTSGN`, in USD, and charges 0.25%. The October 2025 index construction
document specifies 90% physical developed-market equities, 60% government-bond
futures notional, and roughly 10% multi-currency cash collateral.

### Equity sleeve

The eligible universe covers listed companies from the United States, Canada,
Japan, Australia, Hong Kong, Singapore, Israel, and specified developed European
countries. Eligible securities include common stocks, REITs, tracking stocks,
and holding companies, subject to at least $100,000 three-month median daily
trading volume. The index:

1. Selects the top 1,500 eligible companies by market capitalization.
2. Applies WisdomTree ESG exclusions, including UN Global Compact, controversial
	weapons, tobacco, thermal coal, unconventional oil and gas, and small arms.
3. Weights by free-float market capitalization.
4. Caps a single stock at 10% and applies a liquidity adjustment requiring at
	least $400 million of median daily volume per unit of index weight.

Equity constituent weights are reviewed annually in December.

### Bond-futures sleeve

Eligible contracts reference government bonds issued by the United States,
Germany, Japan, and the United Kingdom and require at least $100 million of
average daily volume and/or open interest. The current methodology uses eight
contracts spanning approximately 2- to 30-year maturities.

Futures are grouped by USD, EUR, JPY, and GBP. Each currency group's weight is
matched to the rescaled corresponding equity-currency weight, and contracts are
equal-weighted within each currency group. The front contract rolls to the second
near contract over one day on the last business day of February, May, August,
and November.

### Cash and rebalancing

Cash is spread across USD, EUR, JPY, and GBP in the same currency weights as the
bond sleeve. The whole index resets to 90/60/10 on the last business day of
February, May, August, and November. It also performs an exceptional reset if
the equity or bond exposure deviates by more than 5 percentage points from target.

## Proxy Inputs

| Component | Weight | Series | Treatment |
| --- | ---: | --- | --- |
| Developed-market equities | 90% | `data/URTH.CSV` | Add back URTH's 0.24% annual TER approximately. |
| Global bond futures | 60% notional | `data/BNDW.CSV` | Add back BNDW's 0.05% annual TER, then subtract synthetic cash returns to approximate a futures excess-return index. |
| USD cash collateral | 10% funded | `data/USD_CASH.CSV` | Build a cash index from FRED DGS3MO using the rate known at the start of each interval. |
| Proxy fee | -0.25% | NTSG TER | Deduct daily from net asset value. |

URTH is a practical developed-equity proxy. BNDW is a practical global-bond proxy, but it is not a basket of rolling sovereign-bond futures.

## Calculation

At the first common observation, set NAV to 100. At each official scheduled or
exceptional reset, invest 90% of NAV in the equity proxy, retain 10% as cash,
and set bond-futures notional to 60%. Bond notional is not a funded asset.

Because BNDW is a funded total-return ETF, first approximate a bond-futures excess return:

$$
r_{b,t}^{excess}=\frac{1+r_{BNDW,t}}{1+r_{cash,t}}-1.
$$

Between rebalances, physical equity and cash units remain invested while changes in the bond excess-return index generate futures profit or loss that settles into cash. At target weights, the one-period approximation is:

$$
r_{proxy,t}\approx0.90r_{equity,t}+0.60r_{b,t}^{excess}+0.10r_{cash,t}-fee_t.
$$

The implementation tracks sleeve drift between resets, applies the published
February/May/August/November schedule, interprets the 5% exceptional threshold as
5 percentage points, and deducts the 0.25% annual fee multiplicatively.

## Limitations

- URTH cannot reproduce the official ESG screens, top-1,500 selection, caps,
	liquidity adjustment, or historical constituent weights.
- BNDW is a USD-hedged funded global aggregate bond ETF containing government,
	agency, and credit exposure. It differs from the eight sovereign futures in
	duration, country and currency weights, leverage, and roll return.
- Dividing BNDW total return by USD cash is only an approximation of futures
	excess return.
- The cash series uses one USD Treasury rate rather than a USD/EUR/JPY/GBP
	collateral basket.
- TER add-backs are approximations because ETF expense accrual and tracking differences are not directly observable.
- The proxy begins at the first common date of URTH and BNDW, not at the index inception date.

## Validation

From December 2024 through August 2026, 21 closed-month returns, with NTSG
converted from its EUR listing to USD, have 0.932 correlation, 0.73% annualized
mean proxy-minus-fund return, and 4.33% annualized tracking error. This short
sample supports only provisional validation; weights must not be tuned to it.

## Extended Proxy

`data/NTSG_proxy_extended.csv` extends the synthetic history back to the first common observation of its ETF inputs. It is deliberately separate from `NTSG_proxy.csv` because its inputs are less faithful to the official index.

| Exposure | Extended input | Overall target weight |
| --- | --- | ---: |
| US developed equities | SPY | 63.0% |
| Developed equities excluding North America | EFA | 24.3% |
| Canadian equities | EWC | 2.7% |
| US government bonds | IEF | 30.0% |
| International government bonds | BWX | 30.0% |
| USD cash | USD_CASH | 10.0% |

The equity weights approximate a 70% US, 27% developed ex-US, and 3% Canadian developed-market sleeve. The bond weights use an equal US/international split because the public NTSG materials identify the four government-futures markets but do not publish their historical target weights.

The extended proxy treats SPY, EFA, and EWC as funded equity holdings. It converts
IEF and BWX total returns to approximate excess returns over synthetic cash before
applying 30% futures notionals. It uses the official reset schedule and 5-point
band and deducts the 0.25% TER. It remains lower fidelity and must never be
silently spliced into the baseline proxy.

RSSB is not used as an input. It targets approximately 100% global equities plus
100% U.S. Treasuries, began in December 2023, includes emerging markets, and uses
only U.S. Treasury exposure. Those differences outweigh its superficial
capital-efficient similarity and it adds no earlier history than NTSG.

## Sources

- [WisdomTree Global Efficient Core Index Methodology](https://www.wisdomtree.eu/-/media/eu-media-files/other-documents/research/index/wisdomtree-global-efficient-core-index-methodology.pdf)
- [NTSG fund factsheet](https://dataspanapi.wisdomtree.com/pdr/documents/FACTSHEET/UCITS/EU/EN-GB/IE00077IIPQ8/)
- [RSSB product page](https://www.returnstackedetfs.com/rssb-return-stacked-global-stocks-bonds/)