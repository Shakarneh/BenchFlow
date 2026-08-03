"""The Observer pattern: the pipeline announces, listeners react."""

from datetime import datetime, timedelta

from domain.events import EventBus, RequestPlaced, RequestStateChanged, SourcingStarted
from domain.pipeline import Pipeline, RequestState


def collector():
    """A handler that just records what it was given."""
    received = []
    return received, received.append


def test_nothing_breaks_when_nobody_is_listening():
    """A pipeline with no bus must work exactly as before."""
    pipeline = Pipeline()
    pipeline.move_to(RequestState.OPEN)
    assert pipeline.state is RequestState.OPEN


def test_a_state_change_is_announced():
    received, handler = collector()
    bus = EventBus()
    bus.subscribe(RequestStateChanged, handler)

    pipeline = Pipeline(client_name="BCS", events=bus)
    pipeline.move_to(RequestState.OPEN, by="mohammed")

    assert len(received) == 1
    assert received[0].client_name == "BCS"
    assert received[0].from_state is RequestState.DRAFT
    assert received[0].to_state is RequestState.OPEN
    assert received[0].by == "mohammed"


def test_a_refused_move_announces_nothing():
    received, handler = collector()
    bus = EventBus()
    bus.subscribe(RequestStateChanged, handler)

    pipeline = Pipeline(client_name="BCS", events=bus)
    try:
        pipeline.move_to(RequestState.PLACED)
    except Exception:
        pass
    assert received == []


def test_entering_sourcing_starts_the_sla_clock():
    received, handler = collector()
    bus = EventBus()
    bus.subscribe(SourcingStarted, handler)

    pipeline = Pipeline(client_name="Alfa", events=bus)
    pipeline.move_to(RequestState.OPEN)
    assert received == []           # not yet
    pipeline.move_to(RequestState.SOURCING)
    assert len(received) == 1       # now
    assert received[0].client_name == "Alfa"


def test_placement_reports_the_time_to_fill():
    received, handler = collector()
    bus = EventBus()
    bus.subscribe(RequestPlaced, handler)

    start = datetime(2026, 8, 1, 9, 0)
    pipeline = Pipeline(client_name="MKB", events=bus)
    pipeline.move_to(RequestState.OPEN, at=start)
    pipeline.move_to(RequestState.SOURCING, at=start + timedelta(hours=1))
    pipeline.move_to(RequestState.PROPOSED, at=start + timedelta(days=1))
    pipeline.move_to(RequestState.INTERVIEW, at=start + timedelta(days=2))
    pipeline.move_to(RequestState.OFFERED, at=start + timedelta(days=2, hours=6))
    pipeline.move_to(RequestState.PLACED, at=start + timedelta(days=3, hours=1))

    assert received[0].time_to_fill_hours == 72.0


def test_several_listeners_all_receive_the_same_event():
    """The whole point: adding a reaction touches no existing code."""
    sla_log, sla_handler = collector()
    audit_log, audit_handler = collector()
    email_log, email_handler = collector()

    bus = EventBus()
    for handler in (sla_handler, audit_handler, email_handler):
        bus.subscribe(RequestStateChanged, handler)

    Pipeline(client_name="BCS", events=bus).move_to(RequestState.OPEN)

    assert len(sla_log) == len(audit_log) == len(email_log) == 1


def test_listeners_only_get_the_event_types_they_asked_for():
    state_changes, state_handler = collector()
    sourcing, sourcing_handler = collector()

    bus = EventBus()
    bus.subscribe(RequestStateChanged, state_handler)
    bus.subscribe(SourcingStarted, sourcing_handler)

    pipeline = Pipeline(client_name="BCS", events=bus)
    pipeline.move_to(RequestState.OPEN)
    pipeline.move_to(RequestState.SOURCING)

    assert len(state_changes) == 2   # both moves
    assert len(sourcing) == 1        # only the one that matters


def test_events_are_immutable_facts():
    """An event describes something that already happened. It cannot be edited."""
    event = SourcingStarted(datetime(2026, 8, 1), "BCS")
    try:
        event.client_name = "someone else"
        assert False, "should have raised"
    except Exception:
        pass
