from datetime import date
from decimal import Decimal

from domain.request import Request
from domain.skill import Skill
from domain.skill_level import Level, SkillLevel
from domain.specialist import Specialist

DJANGO_MIDDLE = SkillLevel(Skill("Django"), Level.MIDDLE)
DJANGO_SENIOR = SkillLevel(Skill("Django"), Level.SENIOR)
PYTHON_MIDDLE = SkillLevel(Skill("Python"), Level.MIDDLE)


def make_request(required_skills, starts_on=date(2026, 9, 1)):
    return Request(
        client_name="BCS",
        required_skills=required_skills,
        headcount=2,
        starts_on=starts_on,
        max_bill_rate=Decimal("120.00"),
    )


def make_specialist(skills, available_from=date(2026, 8, 1)):
    return Specialist(
        full_name="Ivan Petrov",
        cost_rate=Decimal("45.50"),
        available_from=available_from,
        skills=skills,
    )


def test_satisfied_when_every_required_skill_is_covered():
    request = make_request([DJANGO_MIDDLE, PYTHON_MIDDLE])
    ivan = make_specialist([DJANGO_SENIOR, PYTHON_MIDDLE])
    assert request.is_satisfied_by(ivan)


def test_not_satisfied_when_one_required_skill_is_missing():
    request = make_request([DJANGO_MIDDLE, PYTHON_MIDDLE])
    ivan = make_specialist([DJANGO_SENIOR])
    assert not request.is_satisfied_by(ivan)


def test_not_satisfied_when_a_skill_is_held_at_too_low_a_level():
    request = make_request([DJANGO_SENIOR])
    ivan = make_specialist([DJANGO_MIDDLE])
    assert not request.is_satisfied_by(ivan)


def test_not_satisfied_when_the_specialist_is_not_free_in_time():
    request = make_request([DJANGO_MIDDLE], starts_on=date(2026, 9, 1))
    ivan = make_specialist([DJANGO_SENIOR], available_from=date(2026, 10, 1))
    assert not request.is_satisfied_by(ivan)


def test_satisfied_when_the_specialist_frees_up_exactly_on_the_start_date():
    request = make_request([DJANGO_MIDDLE], starts_on=date(2026, 9, 1))
    ivan = make_specialist([DJANGO_SENIOR], available_from=date(2026, 9, 1))
    assert request.is_satisfied_by(ivan)


def test_a_request_with_no_required_skills_is_satisfied_by_anyone():
    request = make_request([])
    assert make_request([]).is_satisfied_by(make_specialist([]))
