from decimal import Decimal

from tests.conftest import (
    DJANGO_JUNIOR,
    DJANGO_MIDDLE,
    DJANGO_SENIOR,
    DOCKER_MIDDLE,
    GO_JUNIOR,
    PYTHON_JUNIOR,
)


def test_covers_a_requirement_held_at_a_higher_level(make_specialist):
    ivan = make_specialist(skills=[DJANGO_SENIOR])
    assert ivan.covers(DJANGO_MIDDLE)


def test_does_not_cover_a_skill_they_do_not_have(make_specialist):
    ivan = make_specialist(skills=[DJANGO_SENIOR])
    assert not ivan.covers(GO_JUNIOR)


def test_does_not_cover_a_requirement_above_their_level(make_specialist):
    ivan = make_specialist(skills=[DJANGO_JUNIOR])
    assert not ivan.covers(DJANGO_SENIOR)


def test_a_specialist_with_no_skills_covers_nothing(make_specialist):
    assert not make_specialist().covers(DJANGO_JUNIOR)


def test_finds_the_matching_skill_among_several(make_specialist):
    ivan = make_specialist(skills=[PYTHON_JUNIOR, DJANGO_SENIOR, DOCKER_MIDDLE])
    assert ivan.covers(DJANGO_MIDDLE)


def test_cost_rate_arithmetic_is_exact(make_specialist):
    ivan = make_specialist(cost_rate="45.50")
    assert ivan.cost_rate * 2 == Decimal("91.00")
