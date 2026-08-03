"""Proof that the skill graph and the allocation calendar are actually USED.

Both were built and unit-tested in Phases 5 and 6, but nothing in the real
matching flow called them. These tests fail if that regresses.
"""

from datetime import date
from decimal import Decimal

from domain.allocation import Allocation
from domain.matcher import GreedyMatcher
from domain.skill import Skill
from domain.skill_graph import SkillGraph
from domain.skill_level import Level, SkillLevel
from tests.conftest import DJANGO, PYTHON

DJANGO_SENIOR = SkillLevel(DJANGO, Level.SENIOR)
PYTHON_MIDDLE = SkillLevel(PYTHON, Level.MIDDLE)
IMPLIES_PYTHON = SkillGraph({DJANGO: {PYTHON}})


# ── The skill graph is wired in ───────────────────────────────────────────


def test_without_a_graph_a_django_developer_does_not_match_python(make_request, make_specialist):
    request = make_request(required_skills=[PYTHON_MIDDLE])
    alice = make_specialist(skills=[DJANGO_SENIOR])
    assert GreedyMatcher().match(request, [alice]) == []


def test_with_a_graph_a_django_developer_matches_python(make_request, make_specialist):
    request = make_request(required_skills=[PYTHON_MIDDLE])
    alice = make_specialist(skills=[DJANGO_SENIOR])
    assert GreedyMatcher(IMPLIES_PYTHON).match(request, [alice]) == [alice]


def test_resolving_skills_does_not_mutate_the_original_specialist(make_request, make_specialist):
    """We match on a copy. Alice's stored profile must be untouched."""
    alice = make_specialist(skills=[DJANGO_SENIOR])
    GreedyMatcher(IMPLIES_PYTHON).match(make_request(required_skills=[PYTHON_MIDDLE]), [alice])
    assert alice.skills == [DJANGO_SENIOR]


# ── The allocation calendar is wired in ───────────────────────────────────


def test_a_fully_booked_specialist_is_not_proposed(make_request, make_specialist):
    request = make_request(
        required_skills=[DJANGO_SENIOR], starts_on=date(2026, 9, 1), ends_on=date(2026, 9, 30)
    )
    bob = make_specialist(
        skills=[DJANGO_SENIOR],
        allocations=[Allocation(date(2026, 8, 1), date(2026, 12, 31), Decimal("1.00"))],
    )
    assert GreedyMatcher().match(request, [bob]) == []


def test_a_half_booked_specialist_is_proposed_for_half_time_work(make_request, make_specialist):
    request = make_request(
        required_skills=[DJANGO_SENIOR],
        starts_on=date(2026, 9, 1),
        ends_on=date(2026, 9, 30),
        fraction="0.50",
    )
    bob = make_specialist(
        skills=[DJANGO_SENIOR],
        allocations=[Allocation(date(2026, 8, 1), date(2026, 12, 31), Decimal("0.50"))],
    )
    assert GreedyMatcher().match(request, [bob]) == [bob]


def test_a_booked_specialist_is_proposed_once_the_booking_ends(make_request, make_specialist):
    """Busy until Aug 31, so an engagement starting Sep 1 is fine."""
    request = make_request(
        required_skills=[DJANGO_SENIOR], starts_on=date(2026, 9, 1), ends_on=date(2026, 9, 30)
    )
    bob = make_specialist(
        skills=[DJANGO_SENIOR],
        allocations=[Allocation(date(2026, 8, 1), date(2026, 8, 31), Decimal("1.00"))],
    )
    assert GreedyMatcher().match(request, [bob]) == [bob]
