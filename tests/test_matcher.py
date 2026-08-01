from datetime import date
from decimal import Decimal

import pytest

from domain.matcher import GreedyMatcher, Matcher
from domain.request import Request
from domain.skill import Skill
from domain.skill_level import Level, SkillLevel
from domain.specialist import Specialist

DJANGO_MIDDLE = SkillLevel(Skill("Django"), Level.MIDDLE)
DJANGO_SENIOR = SkillLevel(Skill("Django"), Level.SENIOR)


def make_request(headcount=1):
    return Request(
        client_name="BCS",
        required_skills=[DJANGO_MIDDLE],
        headcount=headcount,
        starts_on=date(2026, 9, 1),
        max_bill_rate=Decimal("120.00"),
    )


def make_specialist(name, cost_rate, skills=None):
    return Specialist(
        full_name=name,
        cost_rate=Decimal(cost_rate),
        available_from=date(2026, 8, 1),
        skills=[DJANGO_SENIOR] if skills is None else skills,
    )


def test_the_abstract_matcher_cannot_be_instantiated():
    with pytest.raises(TypeError):
        Matcher()


def test_returns_only_specialists_who_satisfy_the_request():
    ivan = make_specialist("Ivan", "50.00")
    anna = make_specialist("Anna", "40.00", skills=[])  # no skills at all
    proposed = GreedyMatcher().match(make_request(headcount=5), [ivan, anna])
    assert proposed == [ivan]


def test_cheapest_specialist_comes_first():
    expensive = make_specialist("Expensive", "90.00")
    cheap = make_specialist("Cheap", "40.00")
    middle = make_specialist("Middle", "60.00")
    proposed = GreedyMatcher().match(make_request(headcount=3), [expensive, cheap, middle])
    assert proposed == [cheap, middle, expensive]


def test_returns_no_more_than_the_requested_headcount():
    people = [make_specialist(f"Dev{i}", f"{40 + i}.00") for i in range(5)]
    proposed = GreedyMatcher().match(make_request(headcount=2), people)
    assert len(proposed) == 2


def test_returns_empty_when_nobody_qualifies():
    nobody = make_specialist("Nobody", "40.00", skills=[])
    assert GreedyMatcher().match(make_request(), [nobody]) == []
