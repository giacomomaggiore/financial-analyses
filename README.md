# Model Portfolio Analytics

Personal financial analysis projects by [Giacomo Maggiore](https://giacomomaggiore.com).

Made for personal interest only. This is not financial advice.

## 90/60 + managed futures

[The comparison notebook](03_pareto_superiority_90_60.ipynb) uses two-thirds in the global 90/60 core and one-third in managed futures, rebalanced quarterly. All source files, comparison dates, allocations, fees, drags, proxy boundaries and analysis windows are configured in cell 2; edit that cell and Run All. Comparison dates do not truncate source validation or historical CTA high-water marks. It includes USD and unhedged EUR comparisons, drawdowns, return distributions, and rolling correlation with equity bull/bear regimes.

Refresh the public managed-futures inputs after installing [requirements](requirements.txt):

```bash
python -m helpers.download_managed_futures_data
python -m helpers.download_implementation_data
```

The default research sample starts in 2000 with SG CTA; AQR from 1985 and BTOP50 from 1987 remain optional extended-history inputs. Aggregate 2/20 gross-up is OFF by default and shown as a sensitivity. Observed NTSG, URTH, IGLO and DBMF returns replace synthetic sleeves when available, without a second TER. Entry and rebalance trading costs are modeled separately. A short all-observed ETF panel is displayed alongside the long hypothetical study.

[The assumption audit](methodology/realistic_backtest.md) documents every configuration choice, product source, cost allowance and limitation. Mixed access to UCITS and US ETFs is assumed. No pre-1985 history or historical ETF investability is fabricated.

Cheers!
