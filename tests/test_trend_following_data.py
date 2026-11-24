import ast
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np
import pandas as pd

from helpers.download_trend_following_data import daily_values, save_series, validate


class DailyFuturesDataTests(unittest.TestCase):
    def test_last_observed_quote_per_source_date(self):
        result = daily_values(
            ["2020-04-21 23:00", "2020-04-20 12:00", "2020-04-20 23:00", "2020-04-22 23:00"],
            [0, 10, -37.63, None],
        )
        self.assertEqual(list(result.index), ["2020-04-20", "2020-04-21"])
        self.assertEqual(list(result.values), [-37.63, 0])

    def test_missing_observations_not_forward_filled(self):
        result = daily_values(["2000-01-01", "2000-01-03", "2000-01-05"], [1, ".", 3])
        self.assertEqual(list(result.index), ["2000-01-01", "2000-01-05"])

    def test_empty_data_rejected(self):
        with self.assertRaises(ValueError):
            daily_values(["2000-01-01"], [None])

    def test_infinity_rejected(self):
        with self.assertRaises(ValueError):
            daily_values(["2000-01-01"], [float("inf")])

    def test_invalid_download_does_not_replace_existing_file(self):
        with tempfile.TemporaryDirectory() as name:
            directory = Path(name)
            save_series(directory, "EXISTING", ["2000-01-01"], [10])
            path = directory / "EXISTING.CSV"
            original = path.read_bytes()
            with self.assertRaises(ValueError):
                save_series(directory, "EXISTING", ["2000-01-01"], [None])
            self.assertEqual(path.read_bytes(), original)
            self.assertFalse(list(directory.glob("*.tmp")))

    def test_csv_round_trip_and_manifest_validation(self):
        with tempfile.TemporaryDirectory() as name:
            directory = Path(name)
            summary = save_series(directory, "CL_TEST", ["2020-04-20", "2020-04-21"], [-37.63, 10])
            record = dict(key="CL_TEST", instrument="CL", provider="test", series_type="futures", **summary)
            (directory / "sources_manifest.json").write_text(json.dumps({"series": [record]}))
            catalog = validate(directory)
            self.assertEqual(catalog.iloc[0].nonpositive_rows, 1)
            frame = pd.read_csv(directory / "CL_TEST.CSV")
            self.assertEqual(list(frame.columns), ["date", "adjusted_price"])
            self.assertEqual(frame.adjusted_price.tolist(), [-37.63, 10])
            (directory / "CL_TEST.CSV").write_text("date,adjusted_price\n2020-04-20,1\n2020-04-21,10\n")
            with self.assertRaises(AssertionError):
                validate(directory)


class TrendSignalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = Path(__file__).resolve().parents[1] / '05_trend_following_futures.ipynb'
        notebook = json.loads(path.read_text())
        cell = next(cell for cell in notebook['cells'] if cell['id'] == '4fce3aac')
        cls.signals = {'pd': pd}
        exec(''.join(cell['source']), cls.signals)

    def test_filter_warmup_tie_and_sma(self):
        trend = self.signals['trend_filter']
        prices = pd.Series([1., 5., 3., 3.5])
        ema_trend = trend(prices, 1, 3)
        self.assertTrue(pd.isna(ema_trend.iloc[1]))
        self.assertEqual(ema_trend.iloc[2:].tolist(), [-1, 1])
        self.assertEqual(trend(prices, 1, 3, ma_type='sma').iloc[-1], -1)

    def test_inclusive_breakouts_fill_next_close_and_do_not_reverse(self):
        position = self.signals['position']
        prices = pd.Series([10., 11., 11., 13., 12., 12., 9., 8.])
        expected = [0, 0, 0, 1, 1, 1, 0, -1]
        self.assertEqual(position(prices, 1, 2, 2, 2).tolist(), expected)
        self.assertEqual(position(-prices, 1, 2, 2, 2).tolist(), [-value for value in expected])
        self.assertEqual(position(prices, 1, 2, 2, 2, long_only=True).iloc[-1], 0)
        self.assertEqual(position(prices, 1, 2, 2, 2, short_only=True).iloc[3], 0)

    def test_filter_flip_does_not_exit_and_pending_entry_cannot_cross_gap(self):
        position = self.signals['position']
        prices = pd.Series([10., 11., 11., 15., 14., 13., 9., 8., 7.])
        self.assertEqual(self.signals['trend_filter'](prices, 1, 2).iloc[5], -1)
        self.assertEqual(position(prices, 1, 2, 2, 3).tolist(), [0, 0, 0, 1, 1, 1, 1, 0, -1])
        self.assertEqual(position(prices, 1, 2, 2, 3, segment=pd.Series([0] * 3 + [1] * 6),
                                  eligible=pd.Series([False, False, True, False, False, True, True, True, True])).tolist(),
                         [0, 0, 0, 0, 0, 0, -1, -1, -1])


class TrendComparisonTests(unittest.TestCase):
    def setUp(self):
        dates = pd.to_datetime(['2020-01-01', '2020-01-02', '2020-01-03', '2020-01-04',
                                '2020-01-05', '2020-01-06', '2020-01-10', '2020-01-20',
                                '2020-01-21'])
        a_dates = dates.delete(6)
        a = pd.DataFrame({'adjusted': [100., 101., 103., 104., 105., 106., 116., 117.],
                          'active': [100., 101., 103., 104., 105., 106., 116., 117.],
                          'segment': [0, 0, 0, 0, 0, 0, 1, 1],
                          'eligible_at_close': [True] * 6 + [False, False]}, index=a_dates)
        b = pd.DataFrame({'adjusted': [200., 201., 203., 204., 205., 206., 207., 208., 209.],
                          'active': [200., 201., 203., 204., 205., 206., 207., 208., 209.],
                          'segment': 0, 'eligible_at_close': True}, index=dates)
        self.dates = dates
        self.directions = {'A': pd.Series([0, 0, 0, 1, 1, 1, 0, 0], index=a_dates),
                           'B': pd.Series(0, index=dates)}
        self.env = {
            'pd': pd, 'np': np, 'futures': {'A': a, 'B': b},
            'contracts': pd.DataFrame({'point_value': [1., 1.], 'currency': ['USD', 'USD']},
                                      index=['A', 'B']),
            'benchmark': pd.Series([100., 101., 103.02, 104., 105., 106., 107., 108., 109.],
                                   index=dates),
            'audit': pd.DataFrame({'first_eligible_close': [dates[0], dates[0]]}, index=['A', 'B']),
            'load_level': lambda *args: pd.Series(0., index=dates),
            'signal_directions': lambda *args: self.directions,
            'SIZING_METHOD': 'volatility', 'INSTRUMENT_RISK_LOOKBACK_SESSIONS': 2,
            'BENCHMARK_RISK_LOOKBACK_SESSIONS': 2, 'CASH_RATE_SERIES': 'cash',
            'INITIAL_NAV_USD': 100_000, 'MA_TYPE': 'ema', 'MA_FAST_SESSIONS': 1,
            'MA_SLOW_SESSIONS': 2, 'ENTRY_LOOKBACK_SESSIONS': 2, 'EXIT_LOOKBACK_SESSIONS': 1,
            'REBALANCY_FREQ_DAYS': 100, 'TARGET_RISK_MULTIPLIER': 1.,
            'TRANSACTION_COST_RATE_BP': .001, 'ANNUAL_ROLL_COST_RATE': 0.,
            'CASH_RATE_MULTIPLIER': 1., 'display': lambda *args: None, 'print': lambda *args: None,
        }
        path = Path(__file__).resolve().parents[1] / '05_trend_following_futures.ipynb'
        notebook = json.loads(path.read_text())
        parameters_cell = next(cell for cell in notebook['cells'] if cell['id'] == 'e7ccc257')
        benchmark_cell = next(cell for cell in notebook['cells'] if cell['id'] == '40363c06')
        backtest_cell = next(cell for cell in notebook['cells'] if cell['id'] == '28c72f90')
        parameters = {}
        exec(''.join(parameters_cell['source']), parameters)
        self.env['EQUITY_BENCHMARK_TER'] = parameters['EQUITY_BENCHMARK_TER']
        exec(''.join(benchmark_cell['source']), self.env)
        self.backtest_source = ''.join(backtest_cell['source'])
        exec(self.backtest_source, self.env)

    def test_risk_ready_start_does_not_depend_on_direction(self):
        comparison = self.env['comparison']
        self.assertEqual(comparison.index[0], self.dates[2])
        np.testing.assert_allclose(comparison.iloc[0], [100., 100.])
        self.assertEqual(self.env['cash_start_comparison'].index[0], self.dates[0])
        self.directions['A'][:] = 0
        args = ('ema', 1, 2, 2, 1, 100, 1., .001, 0., 1.)
        self.assertEqual(self.env['run_comparison'](*args).index[0], self.dates[2])

    def test_equity_comparison_matches_the_index_without_a_fee(self):
        for key in ('comparison', 'cash_start_comparison'):
            comparison = self.env[key]
            index = self.env['benchmark'].loc[comparison.index]
            np.testing.assert_allclose(comparison['MSCI World Net Return USD'], index / index.iloc[0] * 100)

    def test_gap_books_held_pnl_then_exit_cost_at_next_mark(self):
        trend = self.env['comparison']['Futures Trend Following']
        self.assertAlmostEqual(trend.loc['2020-01-04'], 99.896)
        self.assertAlmostEqual(trend.loc['2020-01-06'], 101.896)
        self.assertAlmostEqual(trend.loc['2020-01-10'], 101.896)
        self.assertAlmostEqual(trend.loc['2020-01-20'], 111.78)
        self.assertAlmostEqual(trend.loc['2020-01-21'], 111.78)
        exit_row = self.env['gap_exits'].iloc[0]
        self.assertEqual(exit_row['market'], 'A')
        self.assertAlmostEqual(exit_row['contracts'], 1_000.)
        self.assertAlmostEqual(exit_row['estimated_pnl_usd'], 10_000.)
        self.assertAlmostEqual(exit_row['exit_cost_usd'], 116.)
        self.assertEqual(self.env['daily_risk_moves'][7, 0], 0.)

    def test_short_gap_pnl_and_exit_cost_are_signed_correctly(self):
        self.directions['A'] *= -1
        args = ('ema', 1, 2, 2, 1, 100, 1., .001, 0., 1.)
        levels, exits = self.env['run_comparison'](*args, return_gap_exits=True)
        self.assertAlmostEqual(levels.loc['2020-01-20', 'Futures Trend Following'], 87.78)
        self.assertAlmostEqual(exits.iloc[0]['estimated_pnl_usd'], -10_000.)
        self.assertAlmostEqual(exits.iloc[0]['exit_cost_usd'], 116.)

    def test_annual_roll_proxy_accrues_on_prior_open_notional(self):
        args = ('ema', 1, 2, 2, 1, 100, 1., .001)
        without = self.env['run_comparison'](*args, 0., 1.)['Futures Trend Following']
        with_roll = self.env['run_comparison'](*args, .002, 1.)['Futures Trend Following']
        self.assertEqual(with_roll.loc['2020-01-04'], without.loc['2020-01-04'])
        expected_drag = 1_000 * 104 * .002 / 365 / 100_000 * 100
        self.assertAlmostEqual(without.loc['2020-01-05'] - with_roll.loc['2020-01-05'], expected_drag)
        self.assertEqual(with_roll.loc['2020-01-21'], with_roll.loc['2020-01-20'])

    def test_attribution_books_gap_pnl_and_exit_cost_to_the_held_side(self):
        args = ('ema', 1, 2, 2, 1, 100, 1., .001, .002, 1.)
        levels, ledger = self.env['run_comparison'](*args, return_attribution=True)
        self.assertAlmostEqual(ledger.loc['2020-01-20', ('A', 'Long', 'Futures P&L')], 10.)
        self.assertAlmostEqual(ledger.loc['2020-01-20', ('A', 'Long', 'Trading costs')], -.116)
        self.assertAlmostEqual(ledger.loc['2020-01-20', ('A', 'Long', 'Roll drag')],
                               -1_000 * 106 * .002 * 10 / 365 / 1_000)
        self.assertFalse(ledger.xs('Short', level='Side', axis=1).to_numpy().any())
        np.testing.assert_allclose(ledger.sum(axis=1), levels.iloc[:, 0].diff().dropna(), atol=1e-12)

    def test_attribution_splits_a_reversal_and_keeps_cash_unallocated(self):
        self.directions['A'].loc['2020-01-05':'2020-01-06'] = -1
        self.env['load_level'] = lambda *args: pd.Series(3.6, index=self.dates)
        exec(self.backtest_source, self.env)
        args = ('ema', 1, 2, 2, 1, 100, 1., .001, .002, 1.)
        levels, ledger = self.env['run_comparison'](*args, return_attribution=True)
        reversal = ledger.loc['2020-01-05']
        self.assertGreater(reversal['A', 'Long', 'Futures P&L'], 0)
        self.assertEqual(reversal['A', 'Short', 'Futures P&L'], 0)
        self.assertLess(reversal['A', 'Long', 'Trading costs'], 0)
        self.assertLess(reversal['A', 'Short', 'Trading costs'], 0)
        self.assertLess(ledger.loc['2020-01-20', ('A', 'Short', 'Futures P&L')], 0)
        self.assertAlmostEqual(ledger.iloc[0][('Portfolio', 'Unallocated', 'Cash interest')], .01)
        np.testing.assert_allclose(ledger.sum(axis=1), levels.iloc[:, 0].diff().dropna(), atol=1e-12)

    def test_start_and_returns_do_not_depend_on_later_data(self):
        expected = self.env['comparison'].loc[:'2020-01-06'].copy()
        for market in self.env['futures']:
            self.env['futures'][market] = self.env['futures'][market].loc[:'2020-01-06']
            self.directions[market] = self.directions[market].loc[:'2020-01-06']
        self.env['benchmark'] = self.env['benchmark'].loc[:'2020-01-06']
        exec(self.backtest_source, self.env)
        pd.testing.assert_frame_equal(self.env['comparison'], expected)

    def test_holding_remains_open_if_no_later_mark_arrives(self):
        self.env['futures']['A'] = self.env['futures']['A'].loc[:'2020-01-06']
        self.directions['A'] = self.directions['A'].loc[:'2020-01-06']
        exec(self.backtest_source, self.env)
        args = ('ema', 1, 2, 2, 1, 100, 1., .001, .365, 1.)
        levels, exits = self.env['run_comparison'](*args, return_gap_exits=True)
        self.assertTrue(exits.empty)
        self.assertLess(levels.loc['2020-01-21', 'Futures Trend Following'],
                        levels.loc['2020-01-10', 'Futures Trend Following'])


class InteractiveTrendTests(unittest.TestCase):
    def setUp(self):
        import matplotlib.pyplot as plt

        self.calls = []
        self.displayed = []

        def run_comparison(**parameters):
            self.calls.append(parameters)
            return pd.DataFrame({'Futures Trend Following': [100., 100. + parameters['risk_multiplier']],
                                 'MSCI World Net Return USD': [100., 101.]},
                                index=pd.to_datetime(['2020-01-01', '2020-01-02']))

        self.env = {
            'pd': pd, 'plt': plt, 'run_comparison': run_comparison,
            'STRATEGY_COLORS': {'Futures Trend Following': 'green', 'MSCI World Net Return USD': 'purple'},
            'comparison_summary': lambda levels: pd.DataFrame({'Trend': [levels.iloc[-1, 0]]}),
            'format_summary': lambda summary: summary, 'annotate_events': lambda ax: None,
            'display': self.displayed.append,
            'MA_TYPE': 'ema', 'MA_FAST_SESSIONS': 50, 'MA_SLOW_SESSIONS': 100,
            'ENTRY_LOOKBACK_SESSIONS': 100, 'EXIT_LOOKBACK_SESSIONS': 50,
            'REBALANCY_FREQ_DAYS': 1, 'TARGET_RISK_MULTIPLIER': 1.,
            'TRANSACTION_COST_RATE_BP': .0005, 'ANNUAL_ROLL_COST_RATE': .002,
            'CASH_RATE_MULTIPLIER': 1.,
        }
        path = Path(__file__).resolve().parents[1] / '05_trend_following_futures.ipynb'
        notebook = json.loads(path.read_text())
        cell = next(cell for cell in notebook['cells'] if cell['id'] == 'c5087939')
        exec(''.join(cell['source']), self.env)

    def test_slider_updates_one_chart_without_creating_pyplot_figures(self):
        import matplotlib.pyplot as plt

        self.assertEqual(len(self.displayed), 1)
        chart = self.env['chart_image']
        initial = chart.value
        figures = plt.get_fignums()
        self.env['controls']['risk_multiplier'].value = 1.25
        self.assertIs(chart, self.env['chart_image'])
        self.assertNotEqual(initial, chart.value)
        self.assertEqual(len(self.calls), 2)
        self.assertEqual(self.calls[-1]['risk_multiplier'], 1.25)
        self.assertEqual(self.calls[-1]['transaction_rate'], .0005)
        self.assertEqual(self.calls[-1]['annual_roll_rate'], .002)
        self.assertEqual(plt.get_fignums(), figures)

    def test_invalid_inputs_report_error_without_recomputing(self):
        self.env['controls']['fast'].value = 100
        self.assertEqual(len(self.calls), 1)
        self.assertIn('Fast MA must be shorter', self.env['update_status'].value)

    def test_backtest_errors_are_visible_and_previous_result_is_retained(self):
        def fail(**parameters):
            raise ValueError('Bad <input>')

        previous = self.env['chart_image'].value
        self.env['run_comparison'] = fail
        self.env['controls']['risk_multiplier'].value = 1.25
        self.assertEqual(self.env['chart_image'].value, previous)
        self.assertIn('Bad &lt;input&gt;', self.env['update_status'].value)
        self.assertIn('Previous results', self.env['update_status'].value)


class TrendSensitivityTests(unittest.TestCase):
    def test_grid_varies_one_parameter_and_uses_matching_benchmark_metrics(self):
        from unittest.mock import patch

        import matplotlib.pyplot as plt
        from matplotlib.ticker import PercentFormatter

        calls = []
        benchmark = {'CAGR': .07, 'Volatility': .16, 'Sharpe ratio': .4}
        sg_benchmark = {'CAGR': .05, 'Volatility': .13, 'Sharpe ratio': .33}
        monthly_calls = []
        baseline_dates = pd.date_range('2020-01-31', periods=3, freq='ME')

        def run_comparison(**parameters):
            calls.append(parameters)
            return parameters

        def sg_monthly_comparison(levels, cash, returns, equity):
            monthly_calls.append((levels, cash, returns, equity))
            return levels, 'matched cash'

        def monthly_comparison_summary(levels, cash):
            self.assertEqual(cash, 'matched cash')
            if isinstance(levels, pd.DataFrame):
                strategy = {'CAGR': .09, 'Volatility': .17, 'Sharpe ratio': .5}
            else:
                strategy = {'CAGR': levels['annual_roll_rate'] + levels['cash_multiplier'],
                            'Volatility': levels['risk_multiplier'] / 10,
                            'Sharpe ratio': levels['rebalance_days'] / 100}
            return pd.DataFrame({'Futures Trend Following': strategy,
                                 'MSCI World Net Return USD': benchmark,
                                 'SG Trend (net)': sg_benchmark})

        env = {'pd': pd, 'np': np, 'plt': plt, 'PercentFormatter': PercentFormatter,
               'STRATEGY_COLORS': {'Futures Trend Following': 'green', 'MSCI World Net Return USD': 'purple',
                                   'SG Trend (net)': 'olive'},
               'run_comparison': run_comparison, 'monthly_comparison_summary': monthly_comparison_summary,
               'sg_monthly_comparison': sg_monthly_comparison, 'sg_comparison': pd.DataFrame(index=baseline_dates),
               'sg_cash': 'matched cash', 'cash_growth': 'daily cash', 'sg_returns': 'SG returns',
               'benchmark': 'equity index', 'MA_TYPE': 'ema', 'MA_FAST_SESSIONS': 50,
               'MA_SLOW_SESSIONS': 100, 'ENTRY_LOOKBACK_SESSIONS': 100,
               'EXIT_LOOKBACK_SESSIONS': 50, 'REBALANCY_FREQ_DAYS': 1,
               'TARGET_RISK_MULTIPLIER': 1., 'TRANSACTION_COST_RATE_BP': .0005,
               'ANNUAL_ROLL_COST_RATE': .002, 'CASH_RATE_MULTIPLIER': 1.}
        path = Path(__file__).resolve().parents[1] / '05_trend_following_futures.ipynb'
        notebook = json.loads(path.read_text())
        cell = next(cell for cell in notebook['cells'] if cell['id'] == 'sensitivity-grid')
        with patch.object(plt, 'show'):
            exec(''.join(cell['source']), env)

        axes = env['sensitivity_axes']
        self.assertEqual(axes.shape, (4, 3))
        self.assertEqual(len(calls), 25)
        self.assertEqual(monthly_calls, [(parameters, 'daily cash', 'SG returns', 'equity index')
                                         for parameters in calls])
        call_index = 0
        for row, (parameter, _, values, scale) in enumerate(env['sensitivity_specs']):
            values = sorted(set(values + [env['sensitivity_baseline'][parameter]]))
            results = env['sensitivity_results'][parameter]
            for value in values:
                self.assertEqual(calls[call_index], {**env['sensitivity_baseline'], parameter: value})
                call_index += 1
            np.testing.assert_allclose(results.index, values)
            for column, metric in enumerate(env['sensitivity_metrics']):
                trend_line, benchmark_line, sg_line, baseline_line = axes[row, column].lines
                np.testing.assert_allclose(trend_line.get_xdata(), np.array(values) * scale)
                np.testing.assert_allclose(trend_line.get_ydata(), results[metric])
                np.testing.assert_allclose(benchmark_line.get_ydata(), [benchmark[metric]] * 2)
                np.testing.assert_allclose(sg_line.get_ydata(), [sg_benchmark[metric]] * 2)
                np.testing.assert_allclose(baseline_line.get_xdata(),
                                           [env['sensitivity_baseline'][parameter] * scale] * 2)
        plt.close(env['sensitivity_fig'])


class SGTrendComparisonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = Path(__file__).resolve().parents[1] / '05_trend_following_futures.ipynb'
        notebook = json.loads(path.read_text())
        names = {'drawdown', 'cagr', 'ulcer_index', 'average_drawdown_duration', 'max_drawdown',
                 'sg_monthly_comparison', 'monthly_comparison_summary'}
        cls.env = {'pd': pd, 'np': np}
        for cell in notebook['cells']:
            if cell['cell_type'] == 'code':
                tree = ast.parse(''.join(cell['source']))
                definitions = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in names]
                exec(compile(ast.Module(body=definitions, type_ignores=[]), str(path), 'exec'), cls.env)

    def setUp(self):
        dates = pd.to_datetime(['2020-01-15', '2020-01-31', '2020-02-28', '2020-03-31', '2020-04-28'])
        self.levels = pd.DataFrame({'Trend': [90., 100., 110., 99., 120.],
                                    'Equity': [90., 100., 105., 110., 120.]}, index=dates)
        self.cash = pd.Series([1., 1., 1.01, 1.02, 1.03], index=dates)
        self.sg = pd.Series([0.5, 0.1, -0.2, 0.5],
                            index=pd.to_datetime(['2020-01-31', '2020-02-29', '2020-03-31', '2020-04-30']))
        self.benchmark = pd.Series(1., index=pd.to_datetime(['2020-04-28', '2020-04-30', '2020-05-01']))

    def test_common_returns_and_partial_terminal_month(self):
        levels, cash = self.env['sg_monthly_comparison'](self.levels, self.cash, self.sg, self.benchmark)
        self.assertEqual(levels.index.tolist(), list(pd.to_datetime(['2020-01-31', '2020-02-29', '2020-03-31'])))
        np.testing.assert_allclose(levels['Trend'], [100, 110, 99])
        np.testing.assert_allclose(levels['SG Trend (net)'], [100, 110, 88])
        np.testing.assert_allclose(cash, [1, 1.01, 1.02])
        summary = self.env['monthly_comparison_summary'](levels, cash)
        self.assertAlmostEqual(summary.loc['Volatility', 'SG Trend (net)'], np.std([0.1, -0.2], ddof=1) * np.sqrt(12))
        self.assertAlmostEqual(summary.loc['Max drawdown', 'SG Trend (net)'], -0.2)

    def test_missing_sg_month_is_not_bridged(self):
        sg = self.sg.drop(pd.Timestamp('2020-03-31'))
        with self.assertRaisesRegex(ValueError, 'Missing observations'):
            self.env['sg_monthly_comparison'](self.levels, self.cash, sg, self.benchmark)

    def test_complete_terminal_month_is_included(self):
        levels = self.levels.rename(index={pd.Timestamp('2020-04-28'): pd.Timestamp('2020-04-30')})
        cash = self.cash.rename(index={pd.Timestamp('2020-04-28'): pd.Timestamp('2020-04-30')})
        result, _ = self.env['sg_monthly_comparison'](levels, cash, self.sg, self.benchmark)
        self.assertEqual(result.index[-1], pd.Timestamp('2020-04-30'))


if __name__ == "__main__":
    unittest.main()
