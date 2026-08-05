from dataclasses import FrozenInstanceError
from datetime import datetime, timedelta

import pytest

from domain.pipeline import (
    ALLOWED,
    IllegalTransition,
    Pipeline,
    RequestState,
)


def test_a_new_request_starts_as_a_draft():
    assert Pipeline().state is RequestState.DRAFT


def test_a_legal_move_is_accepted():
    pipeline = Pipeline()
    pipeline.move_to(RequestState.OPEN)
    assert pipeline.state is RequestState.OPEN


def test_an_illegal_move_is_refused():
    """Draft straight to Placed would skip every check in the process."""
    pipeline = Pipeline()
    with pytest.raises(IllegalTransition):
        pipeline.move_to(RequestState.PLACED)


def test_a_refused_move_leaves_the_state_untouched():
    pipeline = Pipeline()
    with pytest.raises(IllegalTransition):
        pipeline.move_to(RequestState.ACTIVE)
    assert pipeline.state is RequestState.DRAFT
    assert pipeline.history == []


def test_the_error_says_what_would_have_been_allowed():
    pipeline = Pipeline()
    with pytest.raises(IllegalTransition, match="allowed: "):
        pipeline.move_to(RequestState.PLACED)


def test_the_happy_path_runs_end_to_end():
    pipeline = Pipeline()
    for state in [
        RequestState.OPEN,
        RequestState.SOURCING,
        RequestState.PROPOSED,
        RequestState.INTERVIEW,
        RequestState.OFFERED,
        RequestState.PLACED,
        RequestState.ACTIVE,
        RequestState.ENDED,
    ]:
        pipeline.move_to(state)
    assert pipeline.state is RequestState.ENDED
    assert len(pipeline.history) == 8


def test_a_rejected_candidate_sends_the_request_back_to_sourcing():
    pipeline = Pipeline()
    pipeline.move_to(RequestState.OPEN)
    pipeline.move_to(RequestState.SOURCING)
    pipeline.move_to(RequestState.PROPOSED)
    pipeline.move_to(RequestState.INTERVIEW)
    pipeline.move_to(RequestState.SOURCING)  # client said no
    assert pipeline.state is RequestState.SOURCING


def test_terminal_states_allow_nothing():
    for terminal in (RequestState.ENDED, RequestState.CANCELLED):
        assert ALLOWED[terminal] == set()
        pipeline = Pipeline(state=terminal)
        assert pipeline.is_terminal
        with pytest.raises(IllegalTransition):
            pipeline.move_to(RequestState.OPEN)


def test_an_active_engagement_cannot_be_cancelled():
    """Once someone has started work, the engagement ends -- it is not undone."""
    pipeline = Pipeline(state=RequestState.ACTIVE)
    with pytest.raises(IllegalTransition):
        pipeline.move_to(RequestState.CANCELLED)


# ── The audit trail ───────────────────────────────────────────────────────


def test_every_move_is_recorded_with_who_and_when():
    at = datetime(2026, 8, 3, 14, 30)
    pipeline = Pipeline()
    pipeline.move_to(RequestState.OPEN, by="mohammed", at=at)

    entry = pipeline.history[0]
    assert entry.from_state is RequestState.DRAFT
    assert entry.to_state is RequestState.OPEN
    assert entry.by == "mohammed"
    assert entry.at == at


def test_history_entries_cannot_be_rewritten():
    pipeline = Pipeline()
    pipeline.move_to(RequestState.OPEN)
    with pytest.raises(FrozenInstanceError):
        pipeline.history[0].by = "someone else"


# ── Time to fill: the three-day promise ───────────────────────────────────


def test_time_to_fill_measures_from_sourcing_to_placed():
    start = datetime(2026, 8, 1, 9, 0)
    pipeline = Pipeline()
    pipeline.move_to(RequestState.OPEN, at=start)
    pipeline.move_to(RequestState.SOURCING, at=start + timedelta(hours=1))
    pipeline.move_to(RequestState.PROPOSED, at=start + timedelta(days=1))
    pipeline.move_to(RequestState.INTERVIEW, at=start + timedelta(days=2))
    pipeline.move_to(RequestState.OFFERED, at=start + timedelta(days=2, hours=12))
    pipeline.move_to(RequestState.PLACED, at=start + timedelta(days=3, hours=1))

    assert pipeline.time_to_fill() == timedelta(days=3)


def test_time_to_fill_is_none_before_placement():
    pipeline = Pipeline()
    pipeline.move_to(RequestState.OPEN)
    pipeline.move_to(RequestState.SOURCING)
    assert pipeline.time_to_fill() is None


def test_time_to_fill_is_none_if_sourcing_never_started():
    assert Pipeline().time_to_fill() is None
