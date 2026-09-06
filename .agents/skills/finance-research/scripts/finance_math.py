"""Offline research arithmetic. No brokerage, networking or data persistence.

All values are explicit assumptions, not fetched facts. Currency and market rules
must be verified by the caller. This module is NOT an execution or alpha model.
"""
from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal, InvalidOperation, ROUND_FLOOR, localcontext
import re


def decimal(value: str | int | Decimal) -> Decimal:
    if isinstance(value, bool) or not isinstance(value, (str, int, Decimal)):
        raise ValueError('Use a decimal string, integer or Decimal; no bool/float.')
    if isinstance(value, str) and len(value) > 128:
        raise ValueError('Numeric string is too long.')
    try:
        n = Decimal(value)
    except (InvalidOperation, ValueError):
        raise ValueError('Invalid decimal.') from None
    if not n.is_finite():
        raise ValueError('Finite numbers required.')
    if n.copy_abs() > Decimal('1e18') or (n and n.adjusted() < -12):
        raise ValueError('Magnitude outside supported range.')
    if len(n.as_tuple().digits) > 40:
        raise ValueError('At most 40 significant digits.')
    return n


def pe_scenario(*, price, eps, pe, horizon_years, dividends=0) -> dict:
    """Positive-earnings terminal PE scenario; cumulative, not annualized return.

    Dividends are held as terminal cash, with no reinvestment assumed. The result
    is not discounted fair value and does not incorporate tax or trading costs.
    """
    p, e, m, h, d = map(decimal, (price, eps, pe, horizon_years, dividends))
    if min(p, e, m, h) <= 0 or d < 0:
        raise ValueError('Positive price/EPS/PE/horizon and nonnegative dividends required.')
    with localcontext() as ctx:
        ctx.prec = 60
        terminal = e * m
        return {'terminal_price': str(terminal),
                'implied_eps_at_assumed_pe': str(p / m),
                'cumulative_return_pct': str(((terminal + d) / p - 1) * 100),
                'horizon_years': str(h),
                'scope': 'assumption_scenario_not_forecast_or_discounted_value'}


def risk_ceiling(*, nav, entry, stress_exit, risk_budget_pct,
                 position_cap_pct, theme_remaining_pct, cash,
                 liquidity_cap, roundtrip_cost_bps, lot: int,
                 existing_shares, currency: str) -> dict:
    """Planning ceiling for a NEW cash long only; explicitly rejects additions.

    Full linear round-trip cost is reserved in cash. Stress loss is a scenario,
    NOT a guaranteed maximum. Existing portfolio risk must be checked upstream.
    """
    n, p, s, r, pc, tc, c, l, b, old = map(decimal, (
        nav, entry, stress_exit, risk_budget_pct, position_cap_pct,
        theme_remaining_pct, cash, liquidity_cap, roundtrip_cost_bps, existing_shares))
    if old != 0:
        raise ValueError('Existing position: calculate portfolio-aware remaining risk separately.')
    if type(lot) is not int or not 1 <= lot <= 10**12:
        raise ValueError('lot must be a positive bounded integer.')
    if not isinstance(currency, str) or re.fullmatch(r'[A-Z]{3}', currency) is None:
        raise ValueError('Explicit three-letter currency required; no FX conversion.')
    if n <= 0 or p <= 0 or not 0 <= s < p:
        raise ValueError('Expected nav>0, entry>0 and 0<=stress_exit<entry.')
    if any(not 0 <= x <= 100 for x in (r, pc, tc)):
        raise ValueError('Percentage outside [0,100].')
    if min(c, l) < 0 or not 0 <= b <= 10000:
        raise ValueError('Invalid cash, liquidity or cost.')
    with localcontext() as ctx:
        ctx.prec = 60
        fee = p * b / 10000
        per_share_loss = p - s + fee
        budget = n * r / 100
        caps = {'stress_budget': budget / per_share_loss,
                'position_cap': n * pc / 100 / p,
                'theme_remaining': n * tc / 100 / p,
                'cash_with_cost_reserved': c / (p + fee),
                'liquidity_cap': l / p}
        q = int((min(caps.values()) / lot).to_integral_value(rounding=ROUND_FLOOR)) * lot
        return {'share_ceiling': q, 'currency': currency,
                'cash_required': str(q * (p + fee)),
                'stress_loss': str(q * per_share_loss), 'risk_budget': str(budget),
                'raw_caps': {k: str(v) for k, v in caps.items()},
                'binding_constraints': [k for k, v in caps.items() if v == min(caps.values())],
                'warning': 'Planning ceiling only. Loss can exceed stress scenario. Not an order.'}


def evidence_available(*, first_available_at: str, decision_at: str) -> bool:
    """Check chronology only, not whether a claimed publication time is genuine."""
    times = []
    for value in (first_available_at, decision_at):
        if not isinstance(value, str):
            raise ValueError('Timezone-aware ISO timestamp required.')
        try:
            t = datetime.fromisoformat(value.replace('Z', '+00:00'))
        except ValueError:
            raise ValueError('Invalid ISO timestamp.') from None
        if t.utcoffset() is None:
            raise ValueError('Timestamp needs a timezone.')
        times.append(t)
    return times[0] <= times[1]


def windows_overlap(start_a: str, end_a: str, start_b: str, end_b: str) -> bool:
    """Inclusive date-interval overlap; does not infer missing trading calendars."""
    dates = []
    for value in (start_a, end_a, start_b, end_b):
        if not isinstance(value, str) or re.fullmatch(r'\d{4}-\d{2}-\d{2}', value) is None:
            raise ValueError('Expected YYYY-MM-DD.')
        dates.append(date.fromisoformat(value))
    a, b, c, d = dates
    if a > b or c > d:
        raise ValueError('Reversed interval.')
    return max(a, c) <= min(b, d)
