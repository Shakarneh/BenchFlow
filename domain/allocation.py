"""Time booked on a specialist's calendar.

A specialist is not simply "free" or "busy" -- they can be 50% on one project
and 50% on another. This module answers: how loaded is someone at their
busiest moment, and can they take on more?

Pure Python. No database, no Django.
"""

from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal

FULL_CAPACITY = Decimal("1.00")


@dataclass(frozen=True)
class Allocation:
    """A booking: a fraction of one person's time, over a date range.

    Both dates are INCLUSIVE -- a booking of Aug 1 to Aug 1 means one full
    day of work, and the person is free again on Aug 2.
    """

    starts_on: date
    ends_on: date
    fraction: Decimal

    def overlaps(self, other: "Allocation") -> bool:
        """Do these two bookings share at least one day?"""
        return self.starts_on <= other.ends_on and other.starts_on <= self.ends_on


class Calendar:
    """Everything booked for one specialist."""

    def __init__(self, allocations: list[Allocation] | None = None):
        self._allocations = list(allocations or [])

    def peak_load(self) -> Decimal:
        """The highest simultaneous commitment across the whole calendar.

        Sweep-line: turn every booking into two events -- capacity taken at
        the start, capacity released the day AFTER the end -- then sort them
        by date and walk through once, tracking a running total.

        Returns 0 for an empty calendar.
        """
        events: list[tuple[date, Decimal]] = []

        for allocation in self._allocations:
            events.append((allocation.starts_on, allocation.fraction))
            events.append((allocation.ends_on + timedelta(days=1), -allocation.fraction))

        events.sort()

        running = Decimal("0.00")
        peak = Decimal("0.00")

        for _, delta in events:
            running += delta
            peak = max(peak, running)

        return peak

    def is_over_allocated(self) -> bool:
        """Is this person committed beyond 100% at any moment?"""
        return self.peak_load() > FULL_CAPACITY

    def load_on(self, day: date) -> Decimal:
        """How committed is this person on one specific day?"""
        return sum(
            (a.fraction for a in self._allocations if a.starts_on <= day <= a.ends_on),
            Decimal("0.00"),
        )

    def can_take(self, allocation: Allocation) -> bool:
        """Would adding this booking push the person past 100% at any point?"""
        trial = Calendar(self._allocations + [allocation])
        return not trial.is_over_allocated()
