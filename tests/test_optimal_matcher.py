"""The optimal matcher against the exact scenarios greedy fails.

Same inputs as test_greedy_is_not_optimal.py -- opposite assertions.
Read the two files side by side and the trade-off documents itself.
"""

from decimal import Decimal

import pytest

from domain.matcher import GreedyMatcher, OptimalMatcher
from domain.skill_level import Level, SkillLevel
from tests.conftest import DJANGO, GO, PYTHON

DJANGO_JUNIOR = SkillLevel(DJANGO, Level.JUNIOR)
DJANGO_MIDDLE = SkillLevel(DJANGO, Level.MIDDLE)
DJANGO_SENIOR = SkillLevel(DJANGO, Level.SENIOR)
PYTHON_MIDDLE = SkillLevel(PYTHON, Level.MIDDLE)
GO_SENIOR = SkillLevel(GO, Level.SENIOR)


def build_scenario(make_request, make_specialist):
    """The Alice/Dmitry case. Only Alice can fill B, so Alice MUST go to B."""
    request_a = make_request(required_skills=[DJANGO_JUNIOR], client_name="A")
    request_b = make_request(required_skills=[DJANGO_MIDDLE], client_name="B")
    alice = make_specialist(full_name="Alice", cost_rate="50.00", skills=[DJANGO_MIDDLE])
    dmitry = make_specialist(full_name="Dmitry", cost_rate="60.00", skills=[DJANGO_JUNIOR])
    return [request_a, request_b], [alice, dmitry]


def names(results):
    return {request.client_name: sorted(s.full_name for s in chosen)
            for request, chosen in results}


# ── Optimal succeeds where greedy failed ──────────────────────────────────


def test_optimal_fills_both_requests(make_request, make_specialist):
    requests, people = build_scenario(make_request, make_specialist)
    results = OptimalMatcher().assign(requests, people)
    assert OptimalMatcher.unfilled(results) == 0
    assert names(results) == {"A": ["Dmitry"], "B": ["Alice"]}


def test_optimal_gives_the_same_answer_whatever_the_order(make_request, make_specialist):
    """Greedy's answer flipped when the order flipped. Optimal's must not."""
    requests, people = build_scenario(make_request, make_specialist)
    forward = OptimalMatcher().assign(requests, people)
    backward = OptimalMatcher().assign(list(reversed(requests)), people)
    assert names(forward) == names(backward)


def test_optimal_accepts_a_higher_total_cost_to_fill_more_slots(make_request, make_specialist):
    """Optimal pays 110 total. Greedy paid only 50 -- and left a client unstaffed."""
    requests, people = build_scenario(make_request, make_specialist)
    optimal = OptimalMatcher().assign(requests, people)
    greedy = GreedyMatcher().assign(requests, people)
    assert OptimalMatcher.total_cost(optimal) == Decimal("110.00")
    assert GreedyMatcher.total_cost(greedy) == Decimal("50.00")
    assert OptimalMatcher.unfilled(optimal) < GreedyMatcher.unfilled(greedy)


# ── It is still cost-minimising when nothing is at stake ──────────────────


def test_among_equally_valid_arrangements_the_cheapest_wins(make_request, make_specialist):
    """Two interchangeable candidates, one slot -> take the cheaper."""
    request = make_request(required_skills=[DJANGO_MIDDLE], client_name="A")
    cheap = make_specialist(full_name="Cheap", cost_rate="40.00", skills=[DJANGO_SENIOR])
    pricey = make_specialist(full_name="Pricey", cost_rate="90.00", skills=[DJANGO_SENIOR])
    results = OptimalMatcher().assign([request], [cheap, pricey])
    assert names(results) == {"A": ["Cheap"]}


def test_nobody_is_assigned_to_two_requests(make_request, make_specialist):
    request_a = make_request(required_skills=[DJANGO_MIDDLE], client_name="A")
    request_b = make_request(required_skills=[DJANGO_MIDDLE], client_name="B")
    only_one = make_specialist(full_name="Solo", cost_rate="50.00", skills=[DJANGO_SENIOR])
    results = OptimalMatcher().assign([request_a, request_b], [only_one])
    assigned = [s.full_name for _, chosen in results for s in chosen]
    assert assigned == ["Solo"]
    assert OptimalMatcher.unfilled(results) == 1


def test_an_unqualified_pool_fills_nothing(make_request, make_specialist):
    request = make_request(required_skills=[GO_SENIOR], client_name="A")
    django_dev = make_specialist(full_name="Alice", skills=[DJANGO_SENIOR])
    results = OptimalMatcher().assign([request], [django_dev])
    assert results[0][1] == []


def test_headcount_greater_than_one_is_filled_from_the_pool(make_request, make_specialist):
    request = make_request(required_skills=[DJANGO_MIDDLE], headcount=2, client_name="A")
    people = [
        make_specialist(full_name=f"Dev{i}", cost_rate=f"{40 + i * 10}.00", skills=[DJANGO_SENIOR])
        for i in range(3)
    ]
    results = OptimalMatcher().assign([request], people)
    assert names(results) == {"A": ["Dev0", "Dev1"]}  # the two cheapest


# ── Optimal is never worse than greedy ────────────────────────────────────


@pytest.mark.parametrize("order", [False, True])
def test_optimal_never_fills_fewer_slots_than_greedy(make_request, make_specialist, order):
    requests, people = build_scenario(make_request, make_specialist)
    if order:
        requests = list(reversed(requests))
    greedy = GreedyMatcher().assign(requests, people)
    optimal = OptimalMatcher().assign(requests, people)
    assert OptimalMatcher.unfilled(optimal) <= GreedyMatcher.unfilled(greedy)


def test_the_skill_graph_still_applies_in_optimal_matching(make_request, make_specialist):
    """Optimal inherits resolved() from the base class -- implications still work."""
    from domain.skill_graph import SkillGraph

    request = make_request(required_skills=[PYTHON_MIDDLE], client_name="A")
    alice = make_specialist(full_name="Alice", skills=[DJANGO_SENIOR])
    matcher = OptimalMatcher(SkillGraph({DJANGO: {PYTHON}}))
    assert names(matcher.assign([request], [alice])) == {"A": ["Alice"]}
