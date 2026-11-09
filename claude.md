# Financial and Investment Analysis

## Purpose

This repository is a shared workspace for independent financial and investment analyses. Each analysis is an executable Jupyter notebook that uses the same market-data contract, reusable helpers, and output conventions. No portfolio, benchmark, currency, asset class, or investment thesis is assumed globally.

## Repository Structure

- Store each analysis notebook in the repository root as `<analysis-name>.ipynb`.
- Store shared, reusable Python utilities only in `helpers/`.
- Store source market data in `data/` and analysis-specific deliverables in `outputs/<analysis-name>/`.
- Record material assumptions, data decisions, results, and interpretations in `insights/<analysis-name>.md`.
- Keep visual assets that belong to an analysis in `outputs/<analysis-name>/images/`.

Create the analysis-specific output and insight directories before writing results. Do not overwrite another analysis's outputs or notes.

## Data Contract

- Store every price, index, FX, rate, or economic time series in `data/` as a CSV with exactly `date` and `adjusted_price` columns.
- Use an unambiguous file name, typically `<TICKER>.CSV` or `<SERIES_NAME>.CSV`.
- `date` must be unique, ascending, and ISO-8601; `adjusted_price` must be positive.
- Treat `adjusted_price` as a total-return level only when the source confirms that distributions are included. Otherwise, state that it is price return.
- Maintain `data/metadata.csv` with exactly `ticker`, `asset_name`, `ter`, and `currency`. TER is an annual decimal; use `0` only where no fund-level fee applies.
- For every new or replaced series, record the provider, source identifier, download date, currency, total-return treatment, and known limitations in that analysis's insight file.
- Prefer directly investable total-return history. Clearly label all indexes, proxies, synthetic reconstructions, and backfilled series.

## Analysis Rules

- State the investment question, universe, date range, reference currency, sampling frequency, and rebalancing rule before reporting results.
- Align returns by date and calculate correlations from aligned periodic returns.
- Convert each periodic return with the matching FX return series when reporting another currency; never convert only terminal wealth.
- For portfolio work, show capital allocations, any embedded or derivative exposures, gross exposure, financing assumptions, and benchmark definitions.
- For proxies, document inputs, methodology, fee treatment, start date, and limitations. Futures reconstructions must address collateral and roll return unless already included in the selected series.
- Exclude taxes, bid-ask spreads, commissions, and financing or margin costs unless the analysis explicitly models them.
- Present assumptions and data limitations beside the relevant tables and charts.

## Standard Reporting

When relevant, report cumulative return, CAGR, annualized volatility, maximum drawdown, Sharpe ratio, Sortino ratio, Calmar ratio, worst calendar year, and rolling-return distributions. Define the risk-free series, annualization convention, and any incomplete-period exclusions.

Use clear tables and charts. Every result must identify its date range, currency, return type, and whether it uses investable data, an index, a proxy, or a synthetic reconstruction.

## Shared Helpers

- `helpers/data.py` validates the shared CSV and metadata contracts, aligns prices, converts prices with FX, and downloads Yahoo Finance adjusted closes.
- `helpers/correlations.py` calculates periodic returns, common samples, and correlation matrices.
- `helpers/proxies.py` provides transparent fee, excess-return, proxy-index, and rebalanced-return calculations.
- `helpers/backtest.py` remains for compatibility with existing notebooks; new analyses should use the focused shared modules above.

Keep helpers generic and data-source agnostic. Put analysis-specific parameters, instrument lists, transformations, plots, and interpretations in the owning notebook rather than adding named portfolio logic to `helpers/`.

## Code Principles

- Prefer simple, linear algorithms and clear data structures over performance-oriented complexity.
- Keep modules focused on data loading, return construction, portfolio calculation, or reporting.
- Validate inputs and fail explicitly rather than silently guessing financial assumptions.
- Add short English comments only for material design choices or non-obvious financial assumptions.
