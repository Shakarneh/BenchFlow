"""The application layer, tested with FAKE repositories.

Not a single Django import, no database, no migrations -- and the exact same
use-case code runs in production against PostgreSQL. That is what the ports
in domain/repositories.py are for, and this file is the proof.
"""

from datetime import date
from decimal import Decimal

from application.propose_candidates import FillAllRequests, ProposeCandidates
from domain.allocation import Allocation
from domain.matcher import GreedyMatcher
from domain.repositories import (
    RequestRepository,
    SkillGraphRepository,
    SpecialistRepository,
)
from domain.skill_graph import SkillGraph
from domain.skill_level import Level, SkillLevel
from tests.conftest import DJANGO, GO, PYTHON

DJANGO_JUNIOR = SkillLevel(DJANGO, Level.JUNIOR)
DJANGO_MIDDLE = SkillLevel(DJANGO, Level.MIDDLE)
DJANGO_SENIOR = SkillLevel(DJANGO, Level.SENIOR)
PYTHON_MIDDLE = SkillLevel(PYTHON, Level.MIDDLE)
GO_SENIOR = SkillLevel(GO, Level.SENIOR)


# ── The fakes. Each is ~4 lines and satisfies the same port as Django. ────


class FakeSpecialists(SpecialistRepository):
    def __init__(self, specialists):
        self._specialists = list(specialists)

    def all(self):
        return list(self._specialists)


class FakeRequests(RequestRepository):
    def __init__(self, requests):
        self._requests = list(requests)

    def all(self):
        return list(self._requests)


class FakeSkillGraph(SkillGraphRepository):
    def __init__(self, implications=None):
        self._graph = SkillGraph(implications or {})

    def load(self):
        return self._graph


# ── ProposeCandidates ─────────────────────────────────────────────────────


def test_proposes_the_qualifying_specialist(make_request, make_specialist):
    alice = make_specialist(full_name="Alice", skills=[DJANGO_SENIOR], cost_rate="50.00")
    bob = make_specialist(full_name="Bob", skills=[GO_SENIOR], cost_rate="40.00")

    use_case = ProposeCandidates(FakeSpecialists([alice, bob]), FakeSkillGraph())
    proposal = use_case(make_request(required_skills=[DJANGO_MIDDLE]))

    assert [s.full_name for s in proposal.proposed] == ["Alice"]


def test_explains_why_each_other_specialist_was_not_proposed(make_request, make_specialist):
    alice = make_specialist(full_name="Alice", skills=[DJANGO_SENIOR], cost_rate="50.00")
    pricey = make_specialist(full_name="Pricey", skills=[DJANGO_SENIOR], cost_rate="99.00")

    use_case = ProposeCandidates(FakeSpecialists([alice, pricey]), FakeSkillGraph())
    proposal = use_case(make_request(required_skills=[DJANGO_MIDDLE], max_bill_rate="70.00"))

    rejected = dict((s.full_name, reasons) for s, reasons in proposal.rejected)
    assert "Pricey" in rejected
    assert any("exceeds budget" in reason for reason in rejected["Pricey"])


def test_the_skill_graph_is_applied_through_the_use_case(make_request, make_specialist):
    """Alice knows only Django. The graph says Django implies Python."""
    alice = make_specialist(full_name="Alice", skills=[DJANGO_SENIOR])

    without = ProposeCandidates(FakeSpecialists([alice]), FakeSkillGraph())
    with_graph = ProposeCandidates(FakeSpecialists([alice]), FakeSkillGraph({DJANGO: {PYTHON}}))
    request = make_request(required_skills=[PYTHON_MIDDLE])

    assert without(request).proposed == []
    assert [s.full_name for s in with_graph(request).proposed] == ["Alice"]


def test_rejection_reasons_account_for_implied_skills(make_request, make_specialist):
    """Must not say 'missing Python' for someone whose Django implies it."""
    alice = make_specialist(full_name="Alice", skills=[DJANGO_SENIOR], cost_rate="99.00")
    use_case = ProposeCandidates(FakeSpecialists([alice]), FakeSkillGraph({DJANGO: {PYTHON}}))
    proposal = use_case(make_request(required_skills=[PYTHON_MIDDLE], max_bill_rate="70.00"))

    reasons = proposal.rejected[0][1]
    assert any("exceeds budget" in r for r in reasons)
    assert not any("missing" in r for r in reasons)


def test_reports_a_shortfall_when_nobody_qualifies(make_request, make_specialist):
    nobody = make_specialist(full_name="Nobody", skills=[GO_SENIOR])
    use_case = ProposeCandidates(FakeSpecialists([nobody]), FakeSkillGraph())
    proposal = use_case(make_request(required_skills=[DJANGO_MIDDLE], headcount=2))

    assert not proposal.is_fully_staffed
    assert proposal.shortfall == 2


def test_reports_full_staffing_when_headcount_is_met(make_request, make_specialist):
    people = [
        make_specialist(full_name=f"Dev{i}", skills=[DJANGO_SENIOR], cost_rate=f"{40 + i}.00")
        for i in range(3)
    ]
    use_case = ProposeCandidates(FakeSpecialists(people), FakeSkillGraph())
    proposal = use_case(make_request(required_skills=[DJANGO_MIDDLE], headcount=2))

    assert proposal.is_fully_staffed
    assert proposal.shortfall == 0


def test_a_booked_specialist_is_rejected_with_a_calendar_reason(make_request, make_specialist):
    busy = make_specialist(
        full_name="Busy",
        skills=[DJANGO_SENIOR],
        allocations=[Allocation(date(2026, 1, 1), date(2027, 12, 31), Decimal("1.00"))],
    )
    use_case = ProposeCandidates(FakeSpecialists([busy]), FakeSkillGraph())
    proposal = use_case(make_request(required_skills=[DJANGO_MIDDLE]))

    assert proposal.proposed == []
    assert any("no room for" in r for r in proposal.rejected[0][1])


# ── FillAllRequests: requests compete for one pool ────────────────────────


def test_filling_all_requests_beats_running_them_one_at_a_time(make_request, make_specialist):
    """The Alice/Dmitry case, now through the application layer."""
    request_a = make_request(required_skills=[DJANGO_JUNIOR], client_name="A")
    request_b = make_request(required_skills=[DJANGO_MIDDLE], client_name="B")
    alice = make_specialist(full_name="Alice", cost_rate="50.00", skills=[DJANGO_MIDDLE])
    dmitry = make_specialist(full_name="Dmitry", cost_rate="60.00", skills=[DJANGO_JUNIOR])

    use_case = FillAllRequests(
        FakeSpecialists([alice, dmitry]),
        FakeRequests([request_a, request_b]),
        FakeSkillGraph(),
    )
    proposals = use_case()

    assert all(p.is_fully_staffed for p in proposals)
    assert {p.request.client_name: [s.full_name for s in p.proposed] for p in proposals} == {
        "A": ["Dmitry"],
        "B": ["Alice"],
    }


def test_the_matcher_strategy_is_swappable_from_outside(make_request, make_specialist):
    """Same use case, different algorithm, injected -- Strategy through DI."""
    request_a = make_request(required_skills=[DJANGO_JUNIOR], client_name="A")
    request_b = make_request(required_skills=[DJANGO_MIDDLE], client_name="B")
    alice = make_specialist(full_name="Alice", cost_rate="50.00", skills=[DJANGO_MIDDLE])
    dmitry = make_specialist(full_name="Dmitry", cost_rate="60.00", skills=[DJANGO_JUNIOR])

    specialists = FakeSpecialists([alice, dmitry])
    requests = FakeRequests([request_a, request_b])

    greedy = FillAllRequests(specialists, requests, FakeSkillGraph(), matcher_class=GreedyMatcher)()
    hungarian = FillAllRequests(specialists, requests, FakeSkillGraph())()

    assert sum(p.shortfall for p in greedy) == 1  # greedy strands one
    assert sum(p.shortfall for p in hungarian) == 0  # hungarian does not
