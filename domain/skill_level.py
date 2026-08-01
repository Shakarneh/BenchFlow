from enum import IntEnum


class Level(IntEnum):
    JUNIOR = 1
    MIDDLE = 2 
    SENIOR = 3
    
class SkillLevel:
    def __init__(self, skill, level ):
        self.skill = skill 
        self.level = level
        
    def covers(self, required):
        return self.skill == required.skill and self.level >= required.level

    def __repr__(self):
        return f"SkillLevel({self.skill!r}, {self.level!r})"

    def __eq__(self, other):
        if not isinstance(other, SkillLevel):
            return NotImplemented
        return self.skill == other.skill and self.level == other.level

    def __hash__(self):
        return hash((self.skill, self.level))
