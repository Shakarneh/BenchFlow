from datetime import date

from tests.conftest import DJANGO_MIDDLE, DJANGO_SENIOR, PYTHON_MIDDLE


def test_satisfied_when_every_required_skill_is_covered(make_request, make_specialist):
    request = make_request(required_skills=[DJANGO_MIDDLE, PYTHON_MIDDLE])
    ivan = make_specialist(skills=[DJANGO_SENIOR, PYTHON_MIDDLE])
    assert request.is_satisfied_by(ivan)


def test_not_satisfied_when_one_required_skill_is_missing(make_request, make_specialist):
    request = make_request(required_skills=[DJANGO_MIDDLE, PYTHON_MIDDLE])
    ivan = make_specialist(skills=[DJANGO_SENIOR])
    assert not request.is_satisfied_by(ivan)


def test_not_satisfied_when_a_skill_is_held_at_too_low_a_level(make_request, make_specialist):
    request = make_request(required_skills=[DJANGO_SENIOR])
    ivan = make_specialist(skills=[DJANGO_MIDDLE])
    assert not request.is_satisfied_by(ivan)


def test_not_satisfied_when_the_specialist_is_not_free_in_time(make_request, make_specialist):
    request = make_request(required_skills=[DJANGO_MIDDLE], starts_on=date(2026, 9, 1))
    ivan = make_specialist(skills=[DJANGO_SENIOR], available_from=date(2026, 10, 1))
    assert not request.is_satisfied_by(ivan)


def test_satisfied_when_the_specialist_frees_up_exactly_on_the_start_date(make_request, make_specialist):
    request = make_request(required_skills=[DJANGO_MIDDLE], starts_on=date(2026, 9, 1))
    ivan = make_specialist(skills=[DJANGO_SENIOR], available_from=date(2026, 9, 1))
    assert request.is_satisfied_by(ivan)


def test_a_request_with_no_required_skills_is_satisfied_by_anyone(make_request, make_specialist):
    assert make_request().is_satisfied_by(make_specialist())
