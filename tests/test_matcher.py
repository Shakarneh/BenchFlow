import pytest

from domain.matcher import GreedyMatcher, Matcher
from tests.conftest import DJANGO_MIDDLE, DJANGO_SENIOR


def test_the_abstract_matcher_cannot_be_instantiated():
    with pytest.raises(TypeError):
        Matcher()


def test_returns_only_specialists_who_satisfy_the_request(make_request, make_specialist):
    request = make_request(required_skills=[DJANGO_MIDDLE], headcount=5)
    ivan = make_specialist(full_name="Ivan", skills=[DJANGO_SENIOR])
    anna = make_specialist(full_name="Anna", skills=[])
    assert GreedyMatcher().match(request, [ivan, anna]) == [ivan]


def test_cheapest_specialist_comes_first(make_request, make_specialist):
    request = make_request(required_skills=[DJANGO_MIDDLE], headcount=3)
    expensive = make_specialist(full_name="Expensive", cost_rate="90.00", skills=[DJANGO_SENIOR])
    cheap = make_specialist(full_name="Cheap", cost_rate="40.00", skills=[DJANGO_SENIOR])
    middle = make_specialist(full_name="Middle", cost_rate="60.00", skills=[DJANGO_SENIOR])
    assert GreedyMatcher().match(request, [expensive, cheap, middle]) == [cheap, middle, expensive]


def test_returns_no_more_than_the_requested_headcount(make_request, make_specialist):
    request = make_request(required_skills=[DJANGO_MIDDLE], headcount=2)
    people = [
        make_specialist(full_name=f"Dev{i}", cost_rate=f"{40 + i}.00", skills=[DJANGO_SENIOR])
        for i in range(5)
    ]
    assert len(GreedyMatcher().match(request, people)) == 2


def test_returns_empty_when_nobody_qualifies(make_request, make_specialist):
    request = make_request(required_skills=[DJANGO_MIDDLE])
    nobody = make_specialist(skills=[])
    assert GreedyMatcher().match(request, [nobody]) == []
