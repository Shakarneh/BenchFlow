from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from domain.allocation import FULL_CAPACITY
from domain.skill_level import SkillLevel
from domain.specialist import Specialist
from domain.specifications import (
    CoversAllSkills,
    HasCapacityFor,
    IsEmployedBy,
    IsWithinBudget,
    Specification,
)


@dataclass
class Request:
    """An open demand from a client.

    An entity: it has a life cycle (draft, open, sourcing, placed...) that
    Phase 8 will model as a state machine. Hence NOT frozen.
    """

    client_name: str
    required_skills: list[SkillLevel]
    headcount: int
    starts_on: date
    ends_on: date
    max_bill_rate: Decimal
    fraction: Decimal = FULL_CAPACITY

    def specification(self) -> Specification:
        """The four rules a candidate must satisfy, as one composed object.

        Written with & rather than `and` so each rule stays a separate thing
        that can be tested, reused, and asked to explain its own failure.
        """
        return (
            CoversAllSkills(self.required_skills)
            & IsEmployedBy(self.starts_on)
            & HasCapacityFor(self.starts_on, self.ends_on, self.fraction)
            & IsWithinBudget(self.max_bill_rate)
        )

    def is_satisfied_by(self, specialist: Specialist) -> bool:
        """Can this specialist take this engagement?"""
        return self.specification().is_satisfied_by(specialist)

    def reasons_against(self, specialist: Specialist) -> list[str]:
        """Every reason this specialist was not proposed. Empty means they qualify.

        This is what the compound boolean could never do: name the failures.
        """
        return self.specification().reasons_against(specialist)
