"""Composable business rules.

`Request.is_satisfied_by()` used to be four rules welded into one boolean
expression. It could answer "no" but never "why not".

Here each rule is its own object with one method. They combine with & | ~,
and each one can name itself when it fails -- so a recruiter can be told
"Alice was rejected: cost rate 80.00 exceeds the budget of 70.00" instead
of just False.
"""

from abc import ABC, abstractmethod


class Specification(ABC):
    """One business rule that a Specialist either satisfies or does not."""

    @abstractmethod
    def is_satisfied_by(self, specialist) -> bool:
        """Does this specialist pass this rule?"""

    @abstractmethod
    def describe_failure(self, specialist) -> str:
        """Plain English: why did they fail? Only called when they did."""

    def reasons_against(self, specialist) -> list[str]:
        """Every reason this specialist fails. Empty list means they pass."""
        return [] if self.is_satisfied_by(specialist) else [self.describe_failure(specialist)]

    # ── Composition. These let us write  rule_a & rule_b  instead of nesting. ──

    def __and__(self, other):
        return AndSpecification(self, other)

    def __or__(self, other):
        return OrSpecification(self, other)

    def __invert__(self):
        return NotSpecification(self)


class AndSpecification(Specification):
    """Both rules must hold."""

    def __init__(self, *specs):
        # Flatten nested Ands so (a & b) & c reports three reasons, not two.
        self.specs = [s for spec in specs
                      for s in (spec.specs if isinstance(spec, AndSpecification) else [spec])]

    def is_satisfied_by(self, specialist) -> bool:
        return all(spec.is_satisfied_by(specialist) for spec in self.specs)

    def describe_failure(self, specialist) -> str:
        return "; ".join(self.reasons_against(specialist))

    def reasons_against(self, specialist) -> list[str]:
        """ALL failing rules, not just the first -- that is the whole point."""
        return [reason for spec in self.specs for reason in spec.reasons_against(specialist)]


class OrSpecification(Specification):
    """At least one rule must hold."""

    def __init__(self, *specs):
        self.specs = list(specs)

    def is_satisfied_by(self, specialist) -> bool:
        return any(spec.is_satisfied_by(specialist) for spec in self.specs)

    def describe_failure(self, specialist) -> str:
        inner = " and ".join(spec.describe_failure(specialist) for spec in self.specs)
        return f"none of the alternatives held ({inner})"


class NotSpecification(Specification):
    """The rule must NOT hold."""

    def __init__(self, spec):
        self.spec = spec

    def is_satisfied_by(self, specialist) -> bool:
        return not self.spec.is_satisfied_by(specialist)

    def describe_failure(self, specialist) -> str:
        return f"should not have matched: {self.spec.__class__.__name__}"


# ── The four rules that used to live inside Request.is_satisfied_by ───────


class CoversAllSkills(Specification):
    def __init__(self, required_skills):
        self.required_skills = required_skills

    def is_satisfied_by(self, specialist) -> bool:
        return all(specialist.covers(required) for required in self.required_skills)

    def describe_failure(self, specialist) -> str:
        missing = [
            f"{r.skill.name} at {r.level.name.title()}"
            for r in self.required_skills
            if not specialist.covers(r)
        ]
        return f"missing {', '.join(missing)}"


class IsEmployedBy(Specification):
    def __init__(self, starts_on):
        self.starts_on = starts_on

    def is_satisfied_by(self, specialist) -> bool:
        return specialist.available_from <= self.starts_on

    def describe_failure(self, specialist) -> str:
        return f"not available until {specialist.available_from}, needed by {self.starts_on}"


class HasCapacityFor(Specification):
    def __init__(self, starts_on, ends_on, fraction):
        self.starts_on = starts_on
        self.ends_on = ends_on
        self.fraction = fraction

    def is_satisfied_by(self, specialist) -> bool:
        return specialist.is_free_for(self.starts_on, self.ends_on, self.fraction)

    def describe_failure(self, specialist) -> str:
        peak = specialist.calendar.peak_load()
        return (
            f"no room for {self.fraction:.0%} between {self.starts_on} and "
            f"{self.ends_on} (already peaks at {peak:.0%})"
        )


class IsWithinBudget(Specification):
    def __init__(self, max_bill_rate):
        self.max_bill_rate = max_bill_rate

    def is_satisfied_by(self, specialist) -> bool:
        return specialist.cost_rate <= self.max_bill_rate

    def describe_failure(self, specialist) -> str:
        return f"cost rate {specialist.cost_rate} exceeds budget {self.max_bill_rate}"
