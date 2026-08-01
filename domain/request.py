from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from domain.skill_level import SkillLevel
from domain.specialist import Specialist


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
    max_bill_rate: Decimal

    def is_satisfied_by(self, specialist: Specialist) -> bool:
        """Does this specialist meet EVERY requirement, and start in time?"""
        return (
            all(specialist.covers(required) for required in self.required_skills)
            and specialist.available_from <= self.starts_on
        )
