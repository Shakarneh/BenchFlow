from datetime import date
from decimal import Decimal

from domain.allocation import Allocation, Calendar


def booking(start_day, end_day, fraction, month=8):
    """Aug 2026 by default -- tests only vary the days."""
    return Allocation(
        starts_on=date(2026, month, start_day),
        ends_on=date(2026, month, end_day),
        fraction=Decimal(fraction),
    )


def test_an_empty_calendar_has_no_load():
    assert Calendar().peak_load() == Decimal("0.00")


def test_a_single_booking_peaks_at_its_own_fraction():
    assert Calendar([booking(1, 10, "0.50")]).peak_load() == Decimal("0.50")


def test_two_overlapping_bookings_add_up():
    calendar = Calendar([booking(1, 10, "0.50"), booking(5, 15, "0.50")])
    assert calendar.peak_load() == Decimal("1.00")
    assert not calendar.is_over_allocated()


def test_three_overlapping_bookings_tip_over_capacity():
    calendar = Calendar([booking(1, 10, "0.50"), booking(5, 15, "0.50"), booking(8, 9, "0.25")])
    assert calendar.peak_load() == Decimal("1.25")
    assert calendar.is_over_allocated()


def test_sequential_bookings_never_overlap():
    """Two full-time bookings back to back are fine, not 200%."""
    calendar = Calendar([booking(1, 10, "1.00"), booking(11, 20, "1.00")])
    assert calendar.peak_load() == Decimal("1.00")
    assert not calendar.is_over_allocated()


def test_a_booking_ending_the_day_another_starts_does_not_overlap():
    """THE off-by-one test. Ends Aug 10 inclusive -> free on Aug 11."""
    calendar = Calendar([booking(1, 10, "1.00"), booking(11, 11, "1.00")])
    assert calendar.peak_load() == Decimal("1.00")


def test_a_booking_ending_the_same_day_another_starts_does_overlap():
    """Both occupy Aug 10 -- that IS a clash."""
    calendar = Calendar([booking(1, 10, "1.00"), booking(10, 20, "1.00")])
    assert calendar.peak_load() == Decimal("2.00")
    assert calendar.is_over_allocated()


def test_a_one_day_booking_is_a_full_day():
    assert Calendar([booking(5, 5, "1.00")]).peak_load() == Decimal("1.00")


def test_load_on_a_specific_day():
    calendar = Calendar([booking(1, 10, "0.50"), booking(5, 15, "0.25")])
    assert calendar.load_on(date(2026, 8, 3)) == Decimal("0.50")
    assert calendar.load_on(date(2026, 8, 7)) == Decimal("0.75")
    assert calendar.load_on(date(2026, 8, 12)) == Decimal("0.25")
    assert calendar.load_on(date(2026, 8, 20)) == Decimal("0.00")


def test_can_take_a_booking_that_fits():
    calendar = Calendar([booking(1, 30, "0.50")])
    assert calendar.can_take(booking(1, 30, "0.50"))


def test_cannot_take_a_booking_that_would_overcommit():
    calendar = Calendar([booking(1, 30, "0.50")])
    assert not calendar.can_take(booking(1, 30, "0.75"))


def test_can_take_a_booking_that_only_overlaps_a_quiet_period():
    """Busy in August, free in September -- a September booking is fine."""
    calendar = Calendar([booking(1, 31, "1.00")])
    assert calendar.can_take(booking(1, 30, "1.00", month=9))


def test_a_specialist_with_no_bookings_is_free(make_specialist):
    ivan = make_specialist()
    assert ivan.is_free_for(date(2026, 8, 1), date(2026, 8, 31))


def test_a_half_booked_specialist_can_take_half_more(make_specialist):
    ivan = make_specialist(allocations=[booking(1, 31, "0.50")])
    assert ivan.is_free_for(date(2026, 8, 1), date(2026, 8, 31), Decimal("0.50"))


def test_a_half_booked_specialist_cannot_take_full_time_work(make_specialist):
    ivan = make_specialist(allocations=[booking(1, 31, "0.50")])
    assert not ivan.is_free_for(date(2026, 8, 1), date(2026, 8, 31), Decimal("1.00"))


def test_a_fully_booked_specialist_is_free_after_the_booking_ends(make_specialist):
    ivan = make_specialist(allocations=[booking(1, 31, "1.00")])
    assert not ivan.is_free_for(date(2026, 8, 15), date(2026, 8, 20))
    assert ivan.is_free_for(date(2026, 9, 1), date(2026, 9, 30))


def test_overlaps_is_symmetric():
    a, b = booking(1, 10, "0.50"), booking(5, 15, "0.50")
    assert a.overlaps(b) and b.overlaps(a)


def test_touching_intervals_do_not_overlap():
    assert not booking(1, 10, "0.50").overlaps(booking(11, 20, "0.50"))
