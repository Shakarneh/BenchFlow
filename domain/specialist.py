from dataclasses import dataclass
from datetime import date
from decimal import Decimal

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

    def covers(self, required):
        """Do ANY of my skills satisfy this one requirement?"""
        return any(skill_level.covers(required) for skill_level in self.skills)
