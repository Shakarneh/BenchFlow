from abc import ABC, abstractmethod
from dataclasses import replace
from decimal import Decimal

from domain.skill_graph import SkillGraph


class Matcher(ABC):
    """A strategy for proposing specialists for a request.

    This is a contract, not an implementation. Every matching strategy in
    benchFlow inherits from this and provides its own match().
    """

    def __init__(self, skill_graph: SkillGraph | None = None):
        # No graph supplied means no implications -- everyone is judged on
        # exactly the skills written on their profile.
        self.skill_graph = skill_graph or SkillGraph()

    def resolved(self, specialist):
        """A COPY of this specialist with implied skills filled in.

        Django on the profile becomes Django + Python + Programming. We work
        on a copy so the original -- the thing we return to the caller and
        eventually save -- is never quietly rewritten.
        """
        return replace(specialist, skills=self.skill_graph.expand(specialist.skills))

    def eligible(self, request, specialists):
        """Everyone who satisfies the request once implied skills are resolved."""
        return [s for s in specialists if request.is_satisfied_by(self.resolved(s))]

    @abstractmethod
    def match(self, request, specialists):
        """Return the specialists proposed for this request, best first."""

    def assign(self, requests, specialists):
        """Fill SEVERAL competing requests from one shared pool of people.

        Returns [(request, [specialists]), ...]. Nobody is proposed twice --
        once someone is assigned they leave the pool.
        """
        remaining = list(specialists)
        results = []
        for request in requests:
            chosen = self.match(request, remaining)
            results.append((request, chosen))
            for specialist in chosen:
                remaining.remove(specialist)
        return results

    @staticmethod
    def unfilled(results):
        """How many head are still missing across all requests."""
        return sum(request.headcount - len(chosen) for request, chosen in results)

    @staticmethod
    def total_cost(results):
        """Total cost rate of everyone assigned."""
        return sum(
            (s.cost_rate for _, chosen in results for s in chosen), Decimal("0.00")
        )


class GreedyMatcher(Matcher):
    """The simplest strategy: take everyone who qualifies, cheapest first.

    Correct for ONE request in isolation. Across several competing requests
    it can strand a request that only one specialist could have filled --
    OptimalMatcher exists to fix exactly that.
    """

    def match(self, request, specialists):
        return sorted(self.eligible(request, specialists), key=lambda s: s.cost_rate)[
            : request.headcount
        ]
