"""Synthetic, offline unit tests. No real trades, prices, accounts or alpha claims."""
import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest
from decimal import Decimal

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


m = load('finance_math')
checker = load('check_package')
BASE = dict(nav=1000000, entry=20, stress_exit=17, risk_budget_pct='0.5',
            position_cap_pct=10, theme_remaining_pct=8, cash=100000,
            liquidity_cap=60000, roundtrip_cost_bps=20, lot=100,
            existing_shares=0, currency='CNY')


class FinanceTests(unittest.TestCase):
    def test_decimal(self):
        self.assertEqual(m.decimal('0.1'), Decimal('0.1'))

    def test_scenario(self):
        v = m.pe_scenario(price=100, eps=5, pe=25, horizon_years=1, dividends=2)
        self.assertEqual(Decimal(v['terminal_price']), 125)
        self.assertEqual(Decimal(v['cumulative_return_pct']), 27)
        self.assertEqual(Decimal(v['implied_eps_at_assumed_pe']), 4)

    def test_no_annualization(self):
        v = m.pe_scenario(price=100, eps=5, pe=25, horizon_years=2)
        self.assertEqual(Decimal(v['cumulative_return_pct']), 25)

    def test_loss_scenario(self):
        v = m.pe_scenario(price=100, eps=2, pe=25, horizon_years=1)
        self.assertEqual(Decimal(v['cumulative_return_pct']), -50)

    def test_risk_example(self):
        v = m.risk_ceiling(**BASE)
        self.assertEqual(v['share_ceiling'], 1600)
        self.assertLessEqual(Decimal(v['stress_loss']), Decimal(v['risk_budget']))

    def test_cash_zero(self):
        self.assertEqual(m.risk_ceiling(**{**BASE, 'cash': 0})['share_ceiling'], 0)

    def test_risk_zero(self):
        self.assertEqual(m.risk_ceiling(**{**BASE, 'risk_budget_pct': 0})['share_ceiling'], 0)

    def test_theme_zero(self):
        self.assertEqual(m.risk_ceiling(**{**BASE, 'theme_remaining_pct': 0})['share_ceiling'], 0)

    def test_liquidity_cap(self):
        self.assertEqual(m.risk_ceiling(**{**BASE, 'liquidity_cap': 10000})['share_ceiling'], 500)

    def test_cash_includes_cost(self):
        self.assertEqual(m.risk_ceiling(**{**BASE, 'cash': 2000})['share_ceiling'], 0)

    def test_total_loss_stress(self):
        self.assertEqual(m.risk_ceiling(**{**BASE, 'stress_exit': 0})['share_ceiling'], 200)

    def test_constraints_grid(self):
        for cash in (0, 2000, 10000, 100000):
            for risk in ('0', '0.1', '0.5', '2'):
                v = m.risk_ceiling(**{**BASE, 'cash': cash, 'risk_budget_pct': risk})
                self.assertLessEqual(Decimal(v['cash_required']), cash)
                self.assertLessEqual(Decimal(v['stress_loss']), Decimal(v['risk_budget']))
                self.assertEqual(v['share_ceiling'] % 100, 0)

    def test_future_evidence(self):
        self.assertFalse(m.evidence_available(first_available_at='2025-12-26T10:00:00+08:00', decision_at='2024-12-18T10:00:00+08:00'))

    def test_timezone_equal(self):
        self.assertTrue(m.evidence_available(first_available_at='2026-01-01T09:00:00+09:00', decision_at='2026-01-01T00:00:00Z'))

    def test_naive_time_rejected(self):
        with self.assertRaises(ValueError):
            m.evidence_available(first_available_at='2026-01-01', decision_at='2026-01-02T00:00:00Z')

    def test_cross_end_date_overlap(self):
        self.assertTrue(m.windows_overlap('2024-12-16', '2024-12-18', '2024-12-17', '2024-12-19'))

    def test_disjoint_windows(self):
        self.assertFalse(m.windows_overlap('2024-12-16', '2024-12-18', '2024-12-19', '2024-12-20'))

    def test_reversed_window(self):
        with self.assertRaises(ValueError):
            m.windows_overlap('2024-12-18', '2024-12-16', '2024-12-19', '2024-12-20')

    def test_package(self):
        self.assertEqual(checker.check(ROOT)['errors'], [])

    def test_missing_package(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(checker.check(Path(d))['status'], 'failed')

    def test_tamper(self):
        with tempfile.TemporaryDirectory() as d:
            target = Path(d) / 'skill'
            shutil.copytree(ROOT, target, ignore=shutil.ignore_patterns('__pycache__'))
            with (target / 'SKILL.md').open('a') as f:
                f.write('\nchanged\n')
            self.assertIn('hash mismatch: SKILL.md', checker.check(target)['errors'])


def bad_decimal(value):
    def test(self):
        with self.assertRaises(ValueError):
            m.decimal(value)
    return test


for label, value in [('bool', True), ('float', 0.1), ('nan', 'NaN'), ('infinity', 'Infinity'),
                     ('huge', '1e19'), ('boundary', '1000000000000000000.000000000001'), ('tiny', '1e-13'), ('none', None), ('text', 'abc')]:
    setattr(FinanceTests, 'test_reject_decimal_' + label, bad_decimal(value))


def bad_risk(key, value):
    def test(self):
        with self.assertRaises(ValueError):
            m.risk_ceiling(**{**BASE, key: value})
    return test


for label, key, value in [('existing', 'existing_shares', 100), ('negative_existing', 'existing_shares', -1),
                         ('lot_bool', 'lot', True), ('lot_zero', 'lot', 0),
                         ('zero_nav', 'nav', 0), ('stress_equal', 'stress_exit', 20),
                         ('stress_negative', 'stress_exit', -1), ('percent', 'position_cap_pct', 101),
                         ('negative_cash', 'cash', -1), ('cost', 'roundtrip_cost_bps', 10001),
                         ('currency', 'currency', '')]:
    setattr(FinanceTests, 'test_reject_risk_' + label, bad_risk(key, value))


def bad_pe(key, value):
    def test(self):
        with self.assertRaises(ValueError):
            m.pe_scenario(**{**dict(price=100, eps=5, pe=20, horizon_years=1), key: value})
    return test


for label, key, value in [('negative_eps', 'eps', -1), ('zero_pe', 'pe', 0),
                         ('zero_price', 'price', 0), ('horizon', 'horizon_years', 0),
                         ('dividends', 'dividends', -1)]:
    setattr(FinanceTests, 'test_reject_pe_' + label, bad_pe(key, value))


if __name__ == '__main__':
    unittest.main()
