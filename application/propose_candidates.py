"""Use case: who should we propose for this request, and why not the others?

This is the application layer. It ORCHESTRATES -- loads data through ports,
runs domain logic, publishes events. It contains no business rules of its
own, no SQL, and no HTTP.

Everything it needs arrives through the constructor. It never imports
infrastructure, so a test can hand it fakes and run with no database.
"""

from dataclasses import dataclass

from domain.matcher import HungarianMatcher
from domain.repositories import SkillGraphRepository, SpecialistRepository
from domain.request import Request
from domain.specialist import Specialist


@dataclass(frozen=True)
class Proposal:
    """The answer to one request: who, and why not everyone else."""

    request: Request
    proposed: list[Specialist]
    rejected: list[tuple[Specialist, list[str]]]

    @property
    def is_fully_staffed(self) -> bool:
        return len(self.proposed) >= self.request.headcount

    @property
    def shortfall(self) -> int:
        return max(0, self.request.headcount - len(self.proposed))


class ProposeCandidates:
    """Propose specialists for a single request."""

    def __init__(
        self,
        specialists: SpecialistRepository,
        skill_graphs: SkillGraphRepository,
        matcher_class=HungarianMatcher,
    ):
        # Ports, not concrete classes. This object cannot tell whether the
        # data is coming from PostgreSQL or a list literal in a test.
        self._specialists = specialists
        self._skill_graphs = skill_graphs
        self._matcher_class = matcher_class

    def __call__(self, request: Request) -> Proposal:
        everyone = self._specialists.all()
        matcher = self._matcher_class(self._skill_graphs.load())

        proposed = matcher.match(request, everyone)

        # Explain every rejection -- against the RESOLVED specialist, so we
        # never report "missing Python" for someone whose Django implies it.
        rejected = [
            (person, request.reasons_against(matcher.resolved(person)))
            for person in everyone
            if person not in proposed
        ]
        return Proposal(request=request, proposed=proposed, rejected=rejected)


class FillAllRequests:
    """Assign the whole bench across every open request at once.

    Different from calling ProposeCandidates in a loop: here the requests
    COMPETE for one shared pool, which is the case greedy gets wrong and
    Hungarian gets right.
    """

    def __init__(
        self,
        specialists: SpecialistRepository,
        requests,
        skill_graphs: SkillGraphRepository,
        matcher_class=HungarianMatcher,
    ):
        self._specialists = specialists
        self._requests = requests
        self._skill_graphs = skill_graphs
        self._matcher_class = matcher_class

    def __call__(self) -> list[Proposal]:
        everyone = self._specialists.all()
        requests = self._requests.all()
        matcher = self._matcher_class(self._skill_graphs.load())

        results = matcher.assign(requests, everyone)
        return [
            Proposal(
                request=request,
                proposed=chosen,
                rejected=[
                    (person, request.reasons_against(matcher.resolved(person)))
                    for person in everyone
                    if person not in chosen
                ],
            )
            for request, chosen in results
        ]
