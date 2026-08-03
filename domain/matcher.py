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


class OptimalMatcher(Matcher):
    """Exhaustive search over every complete arrangement.

    Slow -- the number of arrangements grows exponentially -- but provably
    optimal, because it examines all of them. Its real job is to be the
    oracle the faster algorithm is checked against.
    """

    def match(self, request, specialists):
        """One request in isolation: cheapest-first IS optimal.

        With nothing competing for the same people, there is no arrangement
        to get wrong. Greedy only fails when requests compete.
        """
        return sorted(self.eligible(request, specialists), key=lambda s: s.cost_rate)[
            : request.headcount
        ]

    def is_better(self, filled, cost, best_filled, best_cost):
        """Is this arrangement better than the best one found so far?

        THE OBJECTIVE FUNCTION -- the business rule the whole search obeys.
        """
        if filled != best_filled:
            return filled > best_filled
        return cost < best_cost

    def assign(self, requests, specialists):
        # One slot per head required: headcount=2 means two slots to fill.
        slots = [(index, request) for index, request in enumerate(requests)
                 for _ in range(request.headcount)]
        resolved = [self.resolved(s) for s in specialists]

        # Precompute eligibility once -- otherwise we re-check it thousands
        # of times inside the recursion.
        fits = [
            [request.is_satisfied_by(resolved[j]) for j in range(len(specialists))]
            for _, request in slots
        ]

        best = {"filled": -1, "cost": Decimal("0.00"), "picks": []}

        def search(slot_index, used, picks, filled, cost):
            if slot_index == len(slots):
                if self.is_better(filled, cost, best["filled"], best["cost"]):
                    best.update(filled=filled, cost=cost, picks=list(picks))
                return

            # Option 1: assign someone eligible and not yet used.
            for j, specialist in enumerate(specialists):
                if j in used or not fits[slot_index][j]:
                    continue
                used.add(j)
                picks.append(j)
                search(slot_index + 1, used, picks, filled + 1, cost + specialist.cost_rate)
                picks.pop()
                used.remove(j)

            # Option 2: leave this slot empty. Sometimes correct -- holding a
            # specialist back for a slot only they can fill.
            picks.append(None)
            search(slot_index + 1, used, picks, filled, cost)
            picks.pop()

        search(0, set(), [], 0, Decimal("0.00"))

        # Regroup the flat slot picks back into one list per request.
        chosen_per_request = [[] for _ in requests]
        for (request_index, _), pick in zip(slots, best["picks"]):
            if pick is not None:
                chosen_per_request[request_index].append(specialists[pick])
        return list(zip(requests, chosen_per_request))


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
