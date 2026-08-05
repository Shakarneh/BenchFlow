from dataclasses import dataclass
from enum import IntEnum

from domain.skill import Skill


class Level(IntEnum):
    """Proficiency in one skill. The numbers define the ordering."""

    JUNIOR = 1
    MIDDLE = 2
    SENIOR = 3


@dataclass(frozen=True)
class SkillLevel:
    """One skill held at one level, e.g. Django at Senior.

    Composition: it HAS a Skill and HAS a Level rather than being either.
    """

    skill: Skill
    level: Level

    def covers(self, required: "SkillLevel") -> bool:
        """Does what I have satisfy what is required?

        Same skill, and at least as senior. The skill must match first --
        a very high level in Django says nothing about Python.
        """
        return self.skill == required.skill and self.level >= required.level
