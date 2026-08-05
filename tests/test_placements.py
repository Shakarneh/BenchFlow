"""Placement: the check-and-book must be one indivisible step."""

from datetime import date
from decimal import Decimal

import pytest

from domain.engagement import Engagement
from infrastructure.models import (
    AllocationModel,
    PlacementModel,
    RequestModel,
    SpecialistModel,
)
from infrastructure.placements import OverAllocated, place


def make_specialist(cost_rate="50.00"):
    return SpecialistModel.objects.create(
        full_name="Alice Johnson",
        cost_rate=Decimal(cost_rate),
        available_from=date(2026, 1, 1),
    )


def make_request(fraction="1.00", client="BCS"):
    return RequestModel.objects.create(
        client_name=client,
        headcount=1,
        starts_on=date(2026, 9, 1),
        ends_on=date(2026, 12, 31),
        max_bill_rate=Decimal("90.00"),
        fraction=Decimal(fraction),
    )


@pytest.mark.django_db(transaction=True)
def test_a_placement_books_the_calendar_and_records_the_terms():
    alice, request = make_specialist(), make_request()
    placement = place(alice.pk, request.pk, Decimal("70.00"))

    assert placement.cost_rate == Decimal("50.00")
    assert placement.bill_rate == Decimal("70.00")
    assert AllocationModel.objects.count() == 1


@pytest.mark.django_db(transaction=True)
def test_booking_the_same_person_full_time_twice_is_refused():
    """The exact race the lock exists to prevent, run sequentially."""
    alice = make_specialist()
    place(alice.pk, make_request(client="BCS").pk, Decimal("70.00"))

    with pytest.raises(OverAllocated):
        place(alice.pk, make_request(client="Alfa").pk, Decimal("70.00"))


@pytest.mark.django_db(transaction=True)
def test_a_refused_placement_leaves_nothing_behind():
    """Atomic: the allocation must not survive a failed placement."""
    alice = make_specialist()
    place(alice.pk, make_request(client="BCS").pk, Decimal("70.00"))

    with pytest.raises(OverAllocated):
        place(alice.pk, make_request(client="Alfa").pk, Decimal("70.00"))

    assert AllocationModel.objects.count() == 1
    assert PlacementModel.objects.count() == 1


@pytest.mark.django_db(transaction=True)
def test_two_half_time_placements_both_fit():
    alice = make_specialist()
    place(alice.pk, make_request(fraction="0.50", client="BCS").pk, Decimal("70.00"))
    place(alice.pk, make_request(fraction="0.50", client="Alfa").pk, Decimal("75.00"))

    assert PlacementModel.objects.count() == 2


@pytest.mark.django_db(transaction=True)
def test_the_placement_margin_uses_the_stored_snapshot_rates():
    """Raise Alice's rate afterwards -- the signed deal's margin must not move."""
    alice, request = make_specialist("50.00"), make_request()
    placement = place(alice.pk, request.pk, Decimal("70.00"))

    alice.cost_rate = Decimal("65.00")
    alice.save()

    placement.refresh_from_db()
    engagement = Engagement(placement.cost_rate, placement.bill_rate)
    assert engagement.margin() == Decimal("20.00")
