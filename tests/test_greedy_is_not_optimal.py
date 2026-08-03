"""The case that justifies the whole of Phase 7.

Greedy fills each request with the cheapest qualified person available at
that moment. Every individual decision is sensible. The overall result is
still worse than it needed to be -- a request goes unfilled that another
arrangement would have filled.

These tests assert the FAILURE deliberately. When OptimalMatcher lands,
its versions of the same scenario assert success, and the pair of files
documents the trade-off better than any comment could.
"""

from datetime import date

from domain.matcher import GreedyMatcher
from domain.skill_level import Level, SkillLevel
from tests.conftest import DJANGO

DJANGO_JUNIOR = SkillLevel(DJANGO, Level.JUNIOR)
DJANGO_MIDDLE = SkillLevel(DJANGO, Level.MIDDLE)


def build_scenario(make_request, make_specialist):
    """Two requests, two candidates, exactly one correct arrangement.

                    Request A (Junior)   Request B (Middle)
        Alice  50           ok                  ok
        Dmitry 60           ok               NOT qualified

    Only Alice can fill B. So Alice MUST go to B, and Dmitry to A.
    """
    request_a = make_request(required_skills=[DJANGO_JUNIOR], client_name="A")
    request_b = make_request(required_skills=[DJANGO_MIDDLE], client_name="B")
    alice = make_specialist(full_name="Alice", cost_rate="50.00", skills=[DJANGO_MIDDLE])
    dmitry = make_specialist(full_name="Dmitry", cost_rate="60.00", skills=[DJANGO_JUNIOR])
    return [request_a, request_b], [alice, dmitry]


def test_greedy_takes_the_cheapest_person_for_the_first_request(make_request, make_specialist):
    """Request A gets Alice -- cheapest of the two who qualify. Locally correct."""
    requests, people = build_scenario(make_request, make_specialist)
    results = GreedyMatcher().assign(requests, people)
    assert [s.full_name for s in results[0][1]] == ["Alice"]


def test_greedy_then_leaves_the_second_request_unfilled(make_request, make_specialist):
    """...and Request B is left with nobody, because only Alice could do it."""
    requests, people = build_scenario(make_request, make_specialist)
    results = GreedyMatcher().assign(requests, people)
    assert results[1][1] == []
    assert GreedyMatcher.unfilled(results) == 1


def test_a_better_arrangement_existed(make_request, make_specialist):
    """Proof the failure was avoidable: Dmitry->A and Alice->B fills both."""
    requests, people = build_scenario(make_request, make_specialist)
    request_a, request_b = requests
    alice, dmitry = people
    assert request_a.is_satisfied_by(dmitry)
    assert request_b.is_satisfied_by(alice)


def test_greedy_result_depends_on_the_order_requests_arrive(make_request, make_specialist):
    """Reverse the order and greedy suddenly gets it right -- by luck, not design."""
    requests, people = build_scenario(make_request, make_specialist)
    reversed_results = GreedyMatcher().assign(list(reversed(requests)), people)
    assert GreedyMatcher.unfilled(reversed_results) == 0


def test_nobody_is_ever_proposed_to_two_requests(make_request, make_specialist):
    requests, people = build_scenario(make_request, make_specialist)
    results = GreedyMatcher().assign(requests, people)
    proposed = [s.full_name for _, chosen in results for s in chosen]
    assert len(proposed) == len(set(proposed))
