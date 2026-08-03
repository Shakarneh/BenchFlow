"""Measure the three matchers against each other: python manage.py benchmark_matchers

Phase 7 of CLAUDE.md asks for the trade-off to be MEASURED, not asserted.
Two things get compared: how good the answer is (slots filled, total cost)
and how long it takes to produce.
"""

import random
import time
from datetime import date
from decimal import Decimal

from django.core.management.base import BaseCommand

from domain.matcher import GreedyMatcher, HungarianMatcher, OptimalMatcher
from domain.request import Request
from domain.skill import Skill
from domain.skill_level import Level, SkillLevel
from domain.specialist import Specialist

SKILLS = [Skill(name) for name in ("Django", "Go", "React", "Docker", "PostgreSQL")]


def build_world(rng, n_requests, n_specialists):
    requests = [
        Request(
            client_name=f"Client{i}",
            required_skills=[SkillLevel(rng.choice(SKILLS), rng.choice(list(Level)))],
            headcount=rng.randint(1, 2),
            starts_on=date(2026, 9, 1),
            ends_on=date(2026, 12, 31),
            max_bill_rate=Decimal("90.00"),
        )
        for i in range(n_requests)
    ]
    specialists = [
        Specialist(
            full_name=f"Dev{j}",
            cost_rate=Decimal(f"{rng.randint(40, 85)}.00"),
            available_from=date(2026, 1, 1),
            skills=[
                SkillLevel(skill, rng.choice(list(Level)))
                for skill in rng.sample(SKILLS, rng.randint(1, 3))
            ],
        )
        for j in range(n_specialists)
    ]
    return requests, specialists


def measure(matcher, requests, specialists, repeats):
    start = time.perf_counter()
    for _ in range(repeats):
        results = matcher.assign(requests, specialists)
    elapsed_ms = (time.perf_counter() - start) * 1000 / repeats
    return results, elapsed_ms


class Command(BaseCommand):
    help = "Benchmark greedy vs exhaustive vs Hungarian matching"

    # Exhaustive search is skipped above this size -- it would take minutes.
    BRUTE_FORCE_LIMIT = 6

    SIZES = [(2, 4), (3, 6), (4, 8), (5, 12), (8, 25), (15, 60), (30, 150)]

    def handle(self, *args, **options):
        rng = random.Random(42)

        self.stdout.write("")
        self.stdout.write(f"{'requests x people':>18} | {'matcher':<10} | "
                          f"{'unfilled':>8} | {'cost':>9} | {'ms':>10}")
        self.stdout.write("-" * 70)

        for n_requests, n_specialists in self.SIZES:
            requests, specialists = build_world(rng, n_requests, n_specialists)
            repeats = 20 if n_specialists <= 25 else 3

            candidates = [("greedy", GreedyMatcher()), ("hungarian", HungarianMatcher())]
            if n_requests <= self.BRUTE_FORCE_LIMIT:
                candidates.insert(1, ("exhaustive", OptimalMatcher()))

            for label, matcher in candidates:
                results, ms = measure(matcher, requests, specialists, repeats)
                self.stdout.write(
                    f"{f'{n_requests} x {n_specialists}':>18} | {label:<10} | "
                    f"{matcher.unfilled(results):>8} | "
                    f"{matcher.total_cost(results):>9} | {ms:>9.2f}"
                )
            self.stdout.write("-" * 70)

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(
            "greedy    O(n log n)  fast, can strand requests, order-dependent\n"
            "exhaustive O(k^n)     provably optimal, unusable past ~6 requests\n"
            "hungarian O(n^3)      same answer as exhaustive, scales"
        ))
