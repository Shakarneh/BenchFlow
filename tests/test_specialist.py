from datetime import date
from decimal import Decimal

from domain.skill import Skill
from domain.skill_level import Level, SkillLevel
from domain.specialist import Specialist


def make_specialist(skills):
    """A specialist with sensible defaults, so each test only states what it cares about."""
    return Specialist(
        full_name="Ivan Petrov",
        cost_rate=Decimal("45.50"),
        available_from=date(2026, 8, 1),
        skills=skills,
    )


def test_covers_a_requirement_held_at_a_higher_level():
    ivan = make_specialist([SkillLevel(Skill("Django"), Level.SENIOR)])
    assert ivan.covers(SkillLevel(Skill("Django"), Level.MIDDLE))


def test_does_not_cover_a_skill_they_do_not_have():
    ivan = make_specialist([SkillLevel(Skill("Django"), Level.SENIOR)])
    assert not ivan.covers(SkillLevel(Skill("Go"), Level.JUNIOR))


def test_does_not_cover_a_requirement_above_their_level():
    ivan = make_specialist([SkillLevel(Skill("Django"), Level.JUNIOR)])
    assert not ivan.covers(SkillLevel(Skill("Django"), Level.SENIOR))


def test_a_specialist_with_no_skills_covers_nothing():
    ivan = make_specialist([])
    assert not ivan.covers(SkillLevel(Skill("Django"), Level.JUNIOR))


def test_finds_the_matching_skill_among_several():
    ivan = make_specialist([
        SkillLevel(Skill("Python"), Level.JUNIOR),
        SkillLevel(Skill("Django"), Level.SENIOR),
        SkillLevel(Skill("Docker"), Level.MIDDLE),
    ])
    assert ivan.covers(SkillLevel(Skill("Django"), Level.MIDDLE))


def test_cost_rate_arithmetic_is_exact():
    ivan = make_specialist([])
    assert ivan.cost_rate * 2 == Decimal("91.00")
