from abc import ABC, abstractmethod


class Matcher(ABC):
    """A strategy for proposing specialists for a request.

    This is a contract, not an implementation. Every matching strategy in
    benchFlow inherits from this and provides its own match().
    """

    @abstractmethod
    def match(self, request, specialists):
        """Return the specialists proposed for this request, best first."""


class GreedyMatcher(Matcher):
    """The simplest strategy: take everyone who qualifies, cheapest first.

    Not optimal across several requests at once -- Phase 7 replaces it with
    the Hungarian algorithm and measures the difference.
    """

    def match(self, request, specialists):
        eligible = [s for s in specialists if request.is_satisfied_by(s)]
        return sorted(eligible, key=lambda s: s.cost_rate)[: request.headcount]