from abc import ABC, abstractmethod
from dataclasses import replace
from decimal import Decimal

from domain.skill_graph import SkillGraph
from domain.specialist import Specialist

PENALTY = 10**9


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
        return sum((s.cost_rate for _, chosen in results for s in chosen), Decimal("0.00"))


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
        slots = [
            (index, request)
            for index, request in enumerate(requests)
            for _ in range(request.headcount)
        ]
        resolved = [self.resolved(s) for s in specialists]

        # Precompute eligibility once -- otherwise we re-check it thousands
        # of times inside the recursion.
        fits = [
            [request.is_satisfied_by(resolved[j]) for j in range(len(specialists))]
            for _, request in slots
        ]

        # Separate typed variables rather than one dict: a dict of mixed value
        # types is opaque to a type checker, and `nonlocal` says plainly that
        # the inner function reassigns them.
        best_filled: int = -1
        best_cost: Decimal = Decimal("0.00")
        best_picks: list[int | None] = []

        def search(
            slot_index: int,
            used: set[int],
            picks: list[int | None],
            filled: int,
            cost: Decimal,
        ) -> None:
            nonlocal best_filled, best_cost, best_picks
            if slot_index == len(slots):
                if self.is_better(filled, cost, best_filled, best_cost):
                    best_filled, best_cost, best_picks = filled, cost, list(picks)
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
        chosen_per_request: list[list[Specialist]] = [[] for _ in requests]
        # strict=False on purpose: if the search found nothing, picks is
        # shorter than slots and the remaining slots stay unfilled.
        for (request_index, _), pick in zip(slots, best_picks, strict=False):
            if pick is not None:
                chosen_per_request[request_index].append(specialists[pick])
        # strict=True: these two must be the same length. If they ever are
        # not, that is a bug and should crash rather than silently truncate.
        return list(zip(requests, chosen_per_request, strict=True))


class HungarianMatcher(Matcher):
    """The assignment problem solved properly, in O(n^3).

    Same answers as OptimalMatcher, without the exponential blow-up. The
    heavy lifting is in _solve() below, which is the textbook Kuhn-Munkres
    algorithm with potentials; the interesting part of THIS class is how the
    business problem gets encoded into a cost matrix.
    """

    def match(self, request, specialists):
        return sorted(self.eligible(request, specialists), key=lambda s: s.cost_rate)[
            : request.headcount
        ]

    def cell_cost(self, slot_index, spec_index, slots, specialists, fits):
        """What does putting this specialist in this slot cost?

        THE ENCODING -- where the business problem becomes arithmetic.
        Costs are integer cents so the maths stays exact.
        """
        if slot_index >= len(slots):
            return 0  # dummy slot: specialist unused, free
        if spec_index >= len(specialists):
            return PENALTY  # dummy specialist: slot unfilled
        if not fits[slot_index][spec_index]:
            return PENALTY  # not qualified
        return int(specialists[spec_index].cost_rate * 100)

    def assign(self, requests, specialists):
        slots = [
            (index, request)
            for index, request in enumerate(requests)
            for _ in range(request.headcount)
        ]
        if not slots or not specialists:
            return [(request, []) for request in requests]

        resolved = [self.resolved(s) for s in specialists]
        fits = [
            [request.is_satisfied_by(resolved[j]) for j in range(len(specialists))]
            for _, request in slots
        ]

        # The matrix must be square, so pad to whichever side is larger.
        size = max(len(slots), len(specialists))
        cost = [
            [self.cell_cost(i, j, slots, specialists, fits) for j in range(size)]
            for i in range(size)
        ]

        assignment = _solve(cost)

        chosen_per_request: list[list[Specialist]] = [[] for _ in requests]
        for slot_index, (request_index, _) in enumerate(slots):
            spec_index = assignment[slot_index]
            # A real specialist, actually qualified -- not a dummy or a penalty.
            if spec_index < len(specialists) and fits[slot_index][spec_index]:
                chosen_per_request[request_index].append(specialists[spec_index])

        # Cheapest first, so the output reads like the other matchers'.
        for chosen in chosen_per_request:
            chosen.sort(key=lambda s: s.cost_rate)
        # strict=True: these two must be the same length. If they ever are
        # not, that is a bug and should crash rather than silently truncate.
        return list(zip(requests, chosen_per_request, strict=True))


def _solve(cost: list[list[int]]) -> list[int]:
    """Kuhn-Munkres (Hungarian) assignment, O(n^3).

    Takes a square matrix of integer costs, returns a list where
    result[row] = the column that row is assigned to, minimising the total.

    This is the standard textbook implementation. `u` and `v` are the row and
    column "potentials" -- the generalised form of the row/column reduction
    from the concept card: subtracting a constant from a whole row cannot
    change which assignment is best, because every complete assignment uses
    exactly one cell from that row.
    """
    n = len(cost)
    INF = float("inf")
    # float, not int: the potentials absorb `delta`, which can be INF.
    u: list[float] = [0.0] * (n + 1)  # row potentials
    v: list[float] = [0.0] * (n + 1)  # column potentials
    p = [0] * (n + 1)  # p[col] = row currently matched to that column
    way = [0] * (n + 1)  # backtracking pointers for the augmenting path

    for i in range(1, n + 1):
        p[0] = i
        j0 = 0
        minv = [INF] * (n + 1)
        used = [False] * (n + 1)

        # Grow an augmenting path until it reaches a free column.
        while True:
            used[j0] = True
            i0, delta, j1 = p[j0], INF, 0
            for j in range(1, n + 1):
                if used[j]:
                    continue
                reduced = cost[i0 - 1][j - 1] - u[i0] - v[j]
                if reduced < minv[j]:
                    minv[j], way[j] = reduced, j0
                if minv[j] < delta:
                    delta, j1 = minv[j], j
            # Shift the potentials so a new zero appears -- without changing
            # which assignment is optimal.
            for j in range(n + 1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta
            j0 = j1
            if p[j0] == 0:
                break

        # Walk the path backwards, flipping the matching along it.
        while j0:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1

    assignment = [-1] * n
    for j in range(1, n + 1):
        if p[j] > 0:
            assignment[p[j] - 1] = j - 1
    return assignment


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
