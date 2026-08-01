"""Shared test setup.

pytest loads this file automatically -- no import needed for the fixtures.
Any test in any file can ask for a fixture simply by naming it as a parameter.
"""

from datetime import date
from decimal import Decimal

import pytest

from domain.request import Request
from domain.skill import Skill
from domain.skill_level import Level, SkillLevel
from domain.specialist import Specialist

# ── Skills and skill levels ───────────────────────────────────────────────
# Plain module constants, not fixtures: these are frozen value objects, so
# sharing one instance across every test is safe -- nothing can mutate them.

DJANGO = Skill("Django")
PYTHON = Skill("Python")
GO = Skill("Go")
DOCKER = Skill("Docker")

DJANGO_JUNIOR = SkillLevel(DJANGO, Level.JUNIOR)
DJANGO_MIDDLE = SkillLevel(DJANGO, Level.MIDDLE)
DJANGO_SENIOR = SkillLevel(DJANGO, Level.SENIOR)
PYTHON_JUNIOR = SkillLevel(PYTHON, Level.JUNIOR)
PYTHON_MIDDLE = SkillLevel(PYTHON, Level.MIDDLE)
GO_JUNIOR = SkillLevel(GO, Level.JUNIOR)
DOCKER_MIDDLE = SkillLevel(DOCKER, Level.MIDDLE)


# ── Factory fixtures ──────────────────────────────────────────────────────
# Each returns a FUNCTION rather than an object, so a test can override just
# the one field it cares about and ignore the rest.


@pytest.fixture
def make_specialist():
    def _make(
        skills=(),
        cost_rate="45.50",
        available_from=date(2026, 8, 1),
        full_name="Ivan Petrov",
    ):
        return Specialist(
            full_name=full_name,
            cost_rate=Decimal(cost_rate),
            available_from=available_from,
            skills=list(skills),
        )

    return _make


@pytest.fixture
def make_request():
    def _make(
        required_skills=(),
        headcount=1,
        starts_on=date(2026, 9, 1),
        max_bill_rate="120.00",
        client_name="BCS",
    ):
        return Request(
            client_name=client_name,
            required_skills=list(required_skills),
            headcount=headcount,
            starts_on=starts_on,
            max_bill_rate=Decimal(max_bill_rate),
        )

    return _make
