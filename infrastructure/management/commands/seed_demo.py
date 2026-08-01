"""Rebuild the demo dataset from scratch: python manage.py seed_demo

Seed data is not decoration -- every benchmark, screenshot and demo depends
on realistic rows existing. Keeping it as code means anyone (an interviewer,
CI, future you) reproduces the exact same database in one command.
"""

from datetime import date
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from domain.skill_level import Level
from infrastructure.models import (
    RequestModel,
    RequestRequirementModel,
    SkillModel,
    SpecialistModel,
    SpecialistSkillModel,
)

SKILLS = [
    "Programming", "Python", "Django", "FastAPI", "PostgreSQL",
    "Docker", "Linux", "Go", "React", "JavaScript",
]

# skill -> skills it necessarily includes. This is the DAG.
IMPLIES = {
    "Django": ["Python"],
    "FastAPI": ["Python"],
    "Python": ["Programming"],
    "Go": ["Programming"],
    "React": ["JavaScript"],
    "JavaScript": ["Programming"],
    "Docker": ["Linux"],
}

# (name, cost_rate, available_from, [(skill, level), ...])
SPECIALISTS = [
    ("Alice Johnson", "65.00", date(2026, 8, 10), [("Django", Level.MIDDLE), ("Python", Level.SENIOR)]),
    ("Bob Smith", "55.00", date(2026, 8, 15), [("FastAPI", Level.SENIOR), ("PostgreSQL", Level.MIDDLE)]),
    ("Carol Davis", "80.00", date(2026, 9, 1), [("Django", Level.SENIOR), ("Python", Level.SENIOR), ("Docker", Level.MIDDLE)]),
    ("Dmitry Volkov", "48.00", date(2026, 8, 1), [("Django", Level.JUNIOR), ("Python", Level.MIDDLE)]),
    ("Elena Petrova", "72.00", date(2026, 8, 20), [("Go", Level.SENIOR), ("Docker", Level.SENIOR)]),
    ("Farid Hassan", "60.00", date(2026, 10, 1), [("Django", Level.MIDDLE), ("React", Level.MIDDLE)]),
]

# (client, headcount, starts_on, max_bill_rate, [(skill, level), ...])
REQUESTS = [
    ("BCS Mir Investicij", 2, date(2026, 9, 15), "70.00", [("Django", Level.MIDDLE)]),
    ("Alfa Capital", 1, date(2026, 9, 1), "90.00", [("Go", Level.SENIOR), ("Docker", Level.MIDDLE)]),
    ("MKB", 3, date(2026, 10, 1), "65.00", [("Python", Level.MIDDLE)]),
]


class Command(BaseCommand):
    help = "Wipe and reseed the demo dataset"

    @transaction.atomic
    def handle(self, *args, **options):
        # Order matters: children before parents, or foreign keys complain.
        SpecialistSkillModel.objects.all().delete()
        RequestRequirementModel.objects.all().delete()
        SpecialistModel.objects.all().delete()
        RequestModel.objects.all().delete()
        SkillModel.objects.all().delete()

        skills = {name: SkillModel.objects.create(name=name) for name in SKILLS}

        for skill_name, implied_names in IMPLIES.items():
            skills[skill_name].implies.set([skills[n] for n in implied_names])

        for full_name, rate, available_from, skill_levels in SPECIALISTS:
            specialist = SpecialistModel.objects.create(
                full_name=full_name,
                cost_rate=Decimal(rate),
                available_from=available_from,
            )
            for skill_name, level in skill_levels:
                SpecialistSkillModel.objects.create(
                    specialist=specialist, skill=skills[skill_name], level=level.value
                )

        for client, headcount, starts_on, max_rate, requirements in REQUESTS:
            request = RequestModel.objects.create(
                client_name=client,
                headcount=headcount,
                starts_on=starts_on,
                max_bill_rate=Decimal(max_rate),
            )
            for skill_name, level in requirements:
                RequestRequirementModel.objects.create(
                    request=request, skill=skills[skill_name], level=level.value
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {len(SKILLS)} skills, {len(SPECIALISTS)} specialists, "
                f"{len(REQUESTS)} requests."
            )
        )
