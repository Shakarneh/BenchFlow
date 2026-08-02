from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from domain.allocation import FULL_CAPACITY
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
    ends_on: date
    max_bill_rate: Decimal
    fraction: Decimal = FULL_CAPACITY

    def is_satisfied_by(self, specialist: Specialist) -> bool:
        """Can this specialist take this engagement?

        Four rules, all of which must hold:
          1. they cover EVERY required skill, at or above the level asked for
          2. they are employed and available by the start date
          3. their calendar has room for this fraction over the whole period
          4. they cost no more than the client will pay
        """
        return (
            all(specialist.covers(required) for required in self.required_skills)
            and specialist.available_from <= self.starts_on
            and specialist.is_free_for(self.starts_on, self.ends_on, self.fraction)
            and specialist.cost_rate <= self.max_bill_rate
        )
