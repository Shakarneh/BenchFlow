from dataclasses import dataclass


@dataclass(frozen=True)
class Skill:
    """A capability, e.g. "Django".

    A value object: two skills with the same name ARE the same skill, and a
    skill has no life cycle of its own. Hence frozen.
    """

    name: str
