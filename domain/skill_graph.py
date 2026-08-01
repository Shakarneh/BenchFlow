"""The skill implication graph.

"Django implies Python" -- someone who knows Django necessarily knows Python,
even if nobody typed Python on their profile. Resolving those implications
BEFORE matching is what stops the matcher rejecting perfectly good people.

Pure Python. The graph is handed in as a plain dict; where it came from
(database, config file, test fixture) is not this file's problem.
"""

from collections import deque

from domain.skill import Skill
from domain.skill_level import SkillLevel


class SkillGraph:
    """A directed acyclic graph of skill implications."""

    def __init__(self, implications: dict[Skill, set[Skill]] | None = None):
        # skill -> the skills it DIRECTLY implies (one hop only)
        self._implications = implications or {}

    def implied_by(self, skill: Skill) -> set[Skill]:
        """Every skill reachable from this one, following arrows repeatedly.

        This is the transitive closure, computed with breadth-first search.
        The 'seen' set does double duty: it stops repeated work, and it makes
        an accidental cycle harmless instead of an infinite loop.

        Does NOT include the starting skill itself.
        """
        found: set[Skill] = set()
        queue = deque(self._implications.get(skill, set()))
        while queue:
            current = queue.popleft()
            if current in found:
                continue
            found.add(current)
            queue.extend(self._implications.get(current, set()))
        return found

    def expand(self, skill_levels: list[SkillLevel]) -> list[SkillLevel]:
        """Add every implied skill, held at the same level as the skill implying it.

        Simplification we are making on purpose: Django at Senior implies
        Python at Senior. Good enough, and easy to defend.
        """
        expanded = list(skill_levels)
        for held in skill_levels:
            for implied in self.implied_by(held.skill):
                expanded.append(SkillLevel(implied, held.level))
        # Deduplicate, keeping the highest level for any repeated skill.
        best: dict[Skill, SkillLevel] = {}
        for skill_level in expanded:
            current = best.get(skill_level.skill)
            if current is None or skill_level.level > current.level:
                best[skill_level.skill] = skill_level
        return list(best.values())
