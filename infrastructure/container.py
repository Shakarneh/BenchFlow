"""The composition root: where interfaces meet implementations.

This is the ONLY module in benchFlow that knows both the abstract ports and
the concrete Django adapters. Everything else receives what it needs as a
constructor argument and stays ignorant of where data comes from.

It lives in infrastructure/ on purpose. It has to import Django, so putting
it in application/ would break the dependency rule -- and import-linter
would fail the build.
"""

from application.propose_candidates import FillAllRequests, ProposeCandidates
from domain.matcher import HungarianMatcher
from infrastructure.repositories import (
    DjangoRequestRepository,
    DjangoSkillGraphRepository,
    DjangoSpecialistRepository,
)


def propose_candidates(matcher_class=HungarianMatcher) -> ProposeCandidates:
    """A ready-to-use ProposeCandidates, wired to the real database."""
    return ProposeCandidates(
        specialists=DjangoSpecialistRepository(),
        skill_graphs=DjangoSkillGraphRepository(),
        matcher_class=matcher_class,
    )


def fill_all_requests(matcher_class=HungarianMatcher) -> FillAllRequests:
    """A ready-to-use FillAllRequests, wired to the real database."""
    return FillAllRequests(
        specialists=DjangoSpecialistRepository(),
        requests=DjangoRequestRepository(),
        skill_graphs=DjangoSkillGraphRepository(),
        matcher_class=matcher_class,
    )
