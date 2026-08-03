"""The Hungarian algorithm checked against an oracle.

OptimalMatcher is exhaustive, so it cannot be wrong -- only slow. If the
fast algorithm disagrees with it on ANY scenario, the fast one is broken.

This is how you gain justified confidence in an algorithm you did not
derive yourself: not by re-reading it, but by testing it against something
you cannot doubt, on inputs you did not hand-pick.
"""

import random
from datetime import date
from decimal import Decimal

import pytest

from domain.matcher import GreedyMatcher, HungarianMatcher, OptimalMatcher
from domain.request import Request
from domain.skill import Skill
from domain.skill_level import Level, SkillLevel
from domain.specialist import Specialist

SKILLS = [Skill("Django"), Skill("Go"), Skill("React")]


def random_scenario(rng):
    """A small random world: 1-3 requests, 1-5 specialists, random skills and rates."""
    requests = [
        Request(
            client_name=f"Client{i}",
            required_skills=[SkillLevel(rng.choice(SKILLS), rng.choice(list(Level)))],
            headcount=rng.randint(1, 2),
            starts_on=date(2026, 9, 1),
            ends_on=date(2026, 12, 31),
            max_bill_rate=Decimal(rng.choice(["60.00", "80.00", "120.00"])),
        )
        for i in range(rng.randint(1, 3))
    ]
    specialists = [
        Specialist(
            full_name=f"Dev{j}",
            cost_rate=Decimal(f"{rng.randint(40, 90)}.00"),
            available_from=date(2026, 1, 1),
            skills=[
                SkillLevel(skill, rng.choice(list(Level)))
                for skill in rng.sample(SKILLS, rng.randint(1, len(SKILLS)))
            ],
        )
        for j in range(rng.randint(1, 5))
    ]
    return requests, specialists


@pytest.mark.parametrize("seed", range(200))
def test_hungarian_agrees_with_brute_force(seed):
    """Same number of slots filled, and the same total cost, on 200 random worlds."""
    rng = random.Random(seed)
    requests, specialists = random_scenario(rng)

    brute = OptimalMatcher().assign(requests, specialists)
    fast = HungarianMatcher().assign(requests, specialists)

    assert OptimalMatcher.unfilled(fast) == OptimalMatcher.unfilled(brute)
    assert OptimalMatcher.total_cost(fast) == OptimalMatcher.total_cost(brute)


@pytest.mark.parametrize("seed", range(100))
def test_hungarian_is_never_worse_than_greedy(seed):
    rng = random.Random(seed)
    requests, specialists = random_scenario(rng)

    greedy = GreedyMatcher().assign(requests, specialists)
    fast = HungarianMatcher().assign(requests, specialists)

    assert OptimalMatcher.unfilled(fast) <= GreedyMatcher.unfilled(greedy)


@pytest.mark.parametrize("seed", range(100))
def test_nobody_is_ever_assigned_twice(seed):
    rng = random.Random(seed)
    requests, specialists = random_scenario(rng)
    results = HungarianMatcher().assign(requests, specialists)
    assigned = [s.full_name for _, chosen in results for s in chosen]
    assert len(assigned) == len(set(assigned))


@pytest.mark.parametrize("seed", range(100))
def test_nobody_unqualified_is_ever_assigned(seed):
    rng = random.Random(seed)
    requests, specialists = random_scenario(rng)
    for request, chosen in HungarianMatcher().assign(requests, specialists):
        for specialist in chosen:
            assert request.is_satisfied_by(specialist)


def test_hungarian_solves_the_alice_dmitry_case(make_request, make_specialist):
    """The scenario greedy fails, now with the fast algorithm."""
    django = Skill("Django")
    request_a = make_request(required_skills=[SkillLevel(django, Level.JUNIOR)], client_name="A")
    request_b = make_request(required_skills=[SkillLevel(django, Level.MIDDLE)], client_name="B")
    alice = make_specialist(
        full_name="Alice", cost_rate="50.00", skills=[SkillLevel(django, Level.MIDDLE)]
    )
    dmitry = make_specialist(
        full_name="Dmitry", cost_rate="60.00", skills=[SkillLevel(django, Level.JUNIOR)]
    )

    results = HungarianMatcher().assign([request_a, request_b], [alice, dmitry])
    assert HungarianMatcher.unfilled(results) == 0
    assert {r.client_name: [s.full_name for s in c] for r, c in results} == {
        "A": ["Dmitry"],
        "B": ["Alice"],
    }
