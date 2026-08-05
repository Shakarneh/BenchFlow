"""Booking a specialist onto a request -- safely, under concurrency.

The dangerous pattern this exists to prevent:

    manager A: is Alice free?  -> yes
    manager B: is Alice free?  -> yes     (A has not written yet)
    manager A: book Alice 100%
    manager B: book Alice 100%            -> Alice is now at 200%

Nothing in that sequence is a coding mistake. The bug lives in the GAP
between checking and writing. Closing that gap is what row locking does.

This lives in infrastructure/ because locking is a database capability --
application/ is not allowed to know the database exists.
"""

from decimal import Decimal

from django.db import transaction

from domain.allocation import Allocation, Calendar
from infrastructure.models import (
    AllocationModel,
    PlacementModel,
    RequestModel,
    SpecialistModel,
)


class OverAllocated(Exception):
    """Refused: this booking would push the specialist past 100%."""


def _lock_specialist(specialist_id: int) -> SpecialistModel:
    """Fetch the specialist AND hold their row until this transaction ends.

    Any other transaction trying to lock the same row WAITS here instead of
    reading stale data. That wait is the whole safety mechanism.
    """
    return SpecialistModel.objects.select_for_update().get(pk=specialist_id)


@transaction.atomic
def place(specialist_id: int, request_id: int, bill_rate: Decimal) -> PlacementModel:
    """Book a specialist onto a request. All of it, or none of it."""
    specialist = _lock_specialist(specialist_id)
    request = RequestModel.objects.get(pk=request_id)

    # Now that the row is locked, this reading of the calendar is trustworthy:
    # nobody else can write bookings for this person until we commit.
    calendar = Calendar([
        Allocation(booking.starts_on, booking.ends_on, booking.fraction)
        for booking in specialist.allocations.all()
    ])
    wanted = Allocation(request.starts_on, request.ends_on, request.fraction)

    if not calendar.can_take(wanted):
        raise OverAllocated(
            f"{specialist.full_name} cannot take {request.fraction:.0%} "
            f"from {request.starts_on} to {request.ends_on} "
            f"(already peaks at {calendar.peak_load():.0%})"
        )

    allocation = AllocationModel.objects.create(
        specialist=specialist,
        request=request,
        starts_on=request.starts_on,
        ends_on=request.ends_on,
        fraction=request.fraction,
    )
    return PlacementModel.objects.create(
        specialist=specialist,
        request=request,
        allocation=allocation,
        cost_rate=specialist.cost_rate,
        bill_rate=bill_rate,
    )
