"""Composable business rules.

`Request.is_satisfied_by()` used to be four rules welded into one boolean
expression. It could answer "no" but never "why not".

Here each rule is its own object with one method. They combine with & | ~,
and each one can name itself when it fails -- so a recruiter can be told
"Alice was rejected: cost rate 80.00 exceeds the budget of 70.00" instead
of just False.
"""

from abc import ABC, abstractmethod
from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING

from domain.skill_level import SkillLevel

if TYPE_CHECKING:
    from domain.specialist import Specialist


class Specification(ABC):
    """One business rule that a Specialist either satisfies or does not."""

    @abstractmethod
    def is_satisfied_by(self, specialist: "Specialist") -> bool:
        """Does this specialist pass this rule?"""

    @abstractmethod
    def describe_failure(self, specialist: "Specialist") -> str:
        """Plain English: why did they fail? Only called when they did."""

    def reasons_against(self, specialist: "Specialist") -> list[str]:
        """Every reason this specialist fails. Empty list means they pass."""
        return [] if self.is_satisfied_by(specialist) else [self.describe_failure(specialist)]

    # ── Composition. These let us write  rule_a & rule_b  instead of nesting. ──

    def __and__(self, other: "Specification") -> "AndSpecification":
        return AndSpecification(self, other)

    def __or__(self, other: "Specification") -> "OrSpecification":
        return OrSpecification(self, other)

    def __invert__(self) -> "NotSpecification":
        return NotSpecification(self)


class AndSpecification(Specification):
    """Both rules must hold."""

    def __init__(self, *specs: Specification):
        # Flatten nested Ands so (a & b) & c reports three reasons, not two.
        self.specs: list[Specification] = [
            s
            for spec in specs
            for s in (spec.specs if isinstance(spec, AndSpecification) else [spec])
        ]

    def is_satisfied_by(self, specialist: "Specialist") -> bool:
        return all(spec.is_satisfied_by(specialist) for spec in self.specs)

    def describe_failure(self, specialist: "Specialist") -> str:
        return "; ".join(self.reasons_against(specialist))

    def reasons_against(self, specialist: "Specialist") -> list[str]:
        """ALL failing rules, not just the first -- that is the whole point."""
        return [reason for spec in self.specs for reason in spec.reasons_against(specialist)]


class OrSpecification(Specification):
    """At least one rule must hold."""

    def __init__(self, *specs: Specification):
        self.specs: list[Specification] = list(specs)

    def is_satisfied_by(self, specialist: "Specialist") -> bool:
        return any(spec.is_satisfied_by(specialist) for spec in self.specs)

    def describe_failure(self, specialist: "Specialist") -> str:
        inner = " and ".join(spec.describe_failure(specialist) for spec in self.specs)
        return f"none of the alternatives held ({inner})"


class NotSpecification(Specification):
    """The rule must NOT hold."""

    def __init__(self, spec: Specification):
        self.spec = spec

    def is_satisfied_by(self, specialist: "Specialist") -> bool:
        return not self.spec.is_satisfied_by(specialist)

    def describe_failure(self, specialist: "Specialist") -> str:
        return f"should not have matched: {self.spec.__class__.__name__}"


# ── The four rules that used to live inside Request.is_satisfied_by ───────


class CoversAllSkills(Specification):
    def __init__(self, required_skills: list[SkillLevel]):
        self.required_skills = required_skills

    def is_satisfied_by(self, specialist: "Specialist") -> bool:
        return all(specialist.covers(required) for required in self.required_skills)

    def describe_failure(self, specialist: "Specialist") -> str:
        missing = [
            f"{r.skill.name} at {r.level.name.title()}"
            for r in self.required_skills
            if not specialist.covers(r)
        ]
        return f"missing {', '.join(missing)}"


class IsEmployedBy(Specification):
    def __init__(self, starts_on: date):
        self.starts_on = starts_on

    def is_satisfied_by(self, specialist: "Specialist") -> bool:
        return specialist.available_from <= self.starts_on

    def describe_failure(self, specialist: "Specialist") -> str:
        return f"not available until {specialist.available_from}, needed by {self.starts_on}"


class HasCapacityFor(Specification):
    def __init__(self, starts_on: date, ends_on: date, fraction: Decimal):
        self.starts_on = starts_on
        self.ends_on = ends_on
        self.fraction = fraction

    def is_satisfied_by(self, specialist: "Specialist") -> bool:
        return specialist.is_free_for(self.starts_on, self.ends_on, self.fraction)

    def describe_failure(self, specialist: "Specialist") -> str:
        peak = specialist.calendar.peak_load()
        return (
            f"no room for {self.fraction:.0%} between {self.starts_on} and "
            f"{self.ends_on} (already peaks at {peak:.0%})"
        )


class IsWithinBudget(Specification):
    def __init__(self, max_bill_rate: Decimal):
        self.max_bill_rate = max_bill_rate

    def is_satisfied_by(self, specialist: "Specialist") -> bool:
        return specialist.cost_rate <= self.max_bill_rate

    def describe_failure(self, specialist: "Specialist") -> str:
        return f"cost rate {specialist.cost_rate} exceeds budget {self.max_bill_rate}"
