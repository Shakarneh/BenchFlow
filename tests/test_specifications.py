"""The Specification pattern: rules as objects, and rejections that explain themselves."""

from datetime import date
from decimal import Decimal

from domain.allocation import Allocation
from domain.skill_level import Level, SkillLevel
from domain.specifications import (
    CoversAllSkills,
    HasCapacityFor,
    IsEmployedBy,
    IsWithinBudget,
)
from tests.conftest import DJANGO, GO

DJANGO_MIDDLE = SkillLevel(DJANGO, Level.MIDDLE)
DJANGO_SENIOR = SkillLevel(DJANGO, Level.SENIOR)
GO_SENIOR = SkillLevel(GO, Level.SENIOR)


# ── Each rule works, and can be tested completely on its own ──────────────


def test_covers_all_skills_passes(make_specialist):
    spec = CoversAllSkills([DJANGO_MIDDLE])
    assert spec.is_satisfied_by(make_specialist(skills=[DJANGO_SENIOR]))


def test_covers_all_skills_names_what_is_missing(make_specialist):
    spec = CoversAllSkills([DJANGO_MIDDLE, GO_SENIOR])
    alice = make_specialist(skills=[DJANGO_SENIOR])
    assert not spec.is_satisfied_by(alice)
    assert spec.describe_failure(alice) == "missing Go at Senior"


def test_is_within_budget_names_the_numbers(make_specialist):
    spec = IsWithinBudget(Decimal("70.00"))
    pricey = make_specialist(cost_rate="80.00")
    assert not spec.is_satisfied_by(pricey)
    assert "80.00" in spec.describe_failure(pricey)
    assert "70.00" in spec.describe_failure(pricey)


def test_is_employed_by_the_start_date(make_specialist):
    spec = IsEmployedBy(date(2026, 9, 1))
    assert spec.is_satisfied_by(make_specialist(available_from=date(2026, 8, 1)))
    assert not spec.is_satisfied_by(make_specialist(available_from=date(2026, 10, 1)))


def test_has_capacity_reports_the_current_peak(make_specialist):
    spec = HasCapacityFor(date(2026, 9, 1), date(2026, 9, 30), Decimal("1.00"))
    booked = make_specialist(
        allocations=[Allocation(date(2026, 8, 1), date(2026, 12, 31), Decimal("0.75"))]
    )
    assert not spec.is_satisfied_by(booked)
    assert "75%" in spec.describe_failure(booked)


# ── Composition with & | ~ ────────────────────────────────────────────────


def test_and_requires_both_rules(make_specialist):
    spec = CoversAllSkills([DJANGO_MIDDLE]) & IsWithinBudget(Decimal("70.00"))
    assert spec.is_satisfied_by(make_specialist(skills=[DJANGO_SENIOR], cost_rate="50.00"))
    assert not spec.is_satisfied_by(make_specialist(skills=[DJANGO_SENIOR], cost_rate="90.00"))


def test_or_requires_either_rule(make_specialist):
    spec = CoversAllSkills([GO_SENIOR]) | IsWithinBudget(Decimal("70.00"))
    assert spec.is_satisfied_by(make_specialist(skills=[DJANGO_SENIOR], cost_rate="50.00"))
    assert not spec.is_satisfied_by(make_specialist(skills=[DJANGO_SENIOR], cost_rate="90.00"))


def test_not_inverts_a_rule(make_specialist):
    spec = ~IsWithinBudget(Decimal("70.00"))
    assert spec.is_satisfied_by(make_specialist(cost_rate="90.00"))
    assert not spec.is_satisfied_by(make_specialist(cost_rate="50.00"))


# ── The payoff: every reason, not just the first ──────────────────────────


def test_a_qualifying_specialist_has_no_reasons_against(make_request, make_specialist):
    request = make_request(required_skills=[DJANGO_MIDDLE], max_bill_rate="70.00")
    alice = make_specialist(skills=[DJANGO_SENIOR], cost_rate="50.00")
    assert request.reasons_against(alice) == []


def test_a_rejection_reports_ALL_failing_rules(make_request, make_specialist):
    """Three things wrong -> three reasons. A boolean would have said 'False'."""
    request = make_request(
        required_skills=[DJANGO_MIDDLE, GO_SENIOR],
        starts_on=date(2026, 9, 1),
        ends_on=date(2026, 9, 30),
        max_bill_rate="70.00",
    )
    hopeless = make_specialist(
        skills=[DJANGO_SENIOR],
        cost_rate="95.00",
        available_from=date(2026, 11, 1),
        allocations=[Allocation(date(2026, 8, 1), date(2026, 12, 31), Decimal("1.00"))],
    )
    reasons = request.reasons_against(hopeless)
    assert len(reasons) == 4
    assert any("missing Go at Senior" in r for r in reasons)
    assert any("not available until" in r for r in reasons)
    assert any("no room for" in r for r in reasons)
    assert any("exceeds budget" in r for r in reasons)


def test_the_refactor_did_not_change_matching_behaviour(make_request, make_specialist):
    """is_satisfied_by must behave exactly as it did before the pattern landed."""
    request = make_request(required_skills=[DJANGO_MIDDLE], max_bill_rate="70.00")
    assert request.is_satisfied_by(make_specialist(skills=[DJANGO_SENIOR], cost_rate="50.00"))
    assert not request.is_satisfied_by(make_specialist(skills=[DJANGO_SENIOR], cost_rate="90.00"))
