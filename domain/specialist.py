from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal

from domain.allocation import FULL_CAPACITY, Allocation, Calendar
from domain.skill_level import SkillLevel


@dataclass
class Specialist:
    """An engineer we can place with a client.

    An entity, not a value object: two specialists called "Ivan Petrov" are
    not the same person, and a specialist's rate and skills change over time.
    Hence NOT frozen.
    """

    full_name: str
    cost_rate: Decimal
    available_from: date
    skills: list[SkillLevel]
    allocations: list[Allocation] = field(default_factory=list)

    def covers(self, required: SkillLevel) -> bool:
        """Do ANY of my skills satisfy this one requirement?"""
        return any(skill_level.covers(required) for skill_level in self.skills)

    @property
    def calendar(self) -> Calendar:
        return Calendar(self.allocations)

    def is_free_for(self, starts_on: date, ends_on: date, fraction=FULL_CAPACITY) -> bool:
        """Can this person take on this much work over this period?

        Unlike `available_from`, this understands part-time work: someone who
        is 50% booked can still take a 50% engagement.
        """
        return self.calendar.can_take(Allocation(starts_on, ends_on, fraction))
