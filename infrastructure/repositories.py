"""Adapters: the Django implementation of the ports declared in domain/.

This is the ONLY place that knows both worlds -- ORM rows on one side,
pure domain objects on the other. Its whole job is translation.
"""

from domain.allocation import Allocation
from domain.repositories import (
    RequestRepository,
    SkillGraphRepository,
    SpecialistRepository,
)
from domain.request import Request
from domain.skill import Skill
from domain.skill_graph import SkillGraph
from domain.skill_level import Level, SkillLevel
from domain.specialist import Specialist
from infrastructure.models import RequestModel, SkillModel, SpecialistModel


def specialist_to_domain(row: SpecialistModel) -> Specialist:
    """Convert one database row into a pure domain Specialist.

    Everything Django-shaped stops here. What comes out the other side is
    plain Python that the matcher can use without a database.
    """
    return Specialist(
        full_name=row.full_name,
        cost_rate=row.cost_rate,
        available_from=row.available_from,
        skills=[
            SkillLevel(Skill(link.skill.name), Level(link.level))
            for link in row.skills.all()
        ],
        allocations=[
            Allocation(booking.starts_on, booking.ends_on, booking.fraction)
            for booking in row.allocations.all()
        ],
    )


class DjangoSpecialistRepository(SpecialistRepository):
    """Loads specialists out of PostgreSQL via the Django ORM."""

    def all(self) -> list[Specialist]:
        rows = SpecialistModel.objects.prefetch_related("skills__skill", "allocations")
        return [specialist_to_domain(row) for row in rows]


def request_to_domain(row: RequestModel) -> Request:
    """Convert one database row into a pure domain Request."""
    return Request(
        client_name=row.client_name,
        required_skills=[
            SkillLevel(Skill(req.skill.name), Level(req.level))
            for req in row.requirements.all()
        ],
        headcount=row.headcount,
        starts_on=row.starts_on,
        ends_on=row.ends_on,
        max_bill_rate=row.max_bill_rate,
        fraction=row.fraction,
        id=row.pk,
    )


class DjangoRequestRepository(RequestRepository):
    """Loads client requests out of PostgreSQL."""

    def all(self) -> list[Request]:
        rows = RequestModel.objects.prefetch_related("requirements__skill")
        return [request_to_domain(row) for row in rows]


class DjangoSkillGraphRepository(SkillGraphRepository):
    """Builds the whole implication graph in ONE query.

    The graph is small (dozens of skills) and needed on every match, so we
    load it entirely rather than walking the database hop by hop. The BFS
    then runs in memory, which is why it is measured in microseconds.
    """

    def load(self) -> SkillGraph:
        implications = {
            Skill(row.name): {Skill(implied.name) for implied in row.implies.all()}
            for row in SkillModel.objects.prefetch_related("implies")
        }
        return SkillGraph(implications)
