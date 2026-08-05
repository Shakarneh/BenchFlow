"""The exception hierarchy, and that logs actually say something."""

import logging
from datetime import date
from decimal import Decimal

import pytest

from domain.errors import (
    BenchFlowError,
    DomainRuleViolated,
    IllegalTransition,
    NotFound,
    OverAllocated,
)
from domain.pipeline import Pipeline, RequestState
from infrastructure.models import RequestModel, SpecialistModel
from infrastructure.placements import place

# ── The family tree ───────────────────────────────────────────────────────


def test_catching_the_general_case_catches_the_specific_one():
    """This is why the hierarchy exists."""
    with pytest.raises(DomainRuleViolated):
        raise OverAllocated("too busy")

    with pytest.raises(BenchFlowError):
        raise IllegalTransition("no")

    with pytest.raises(BenchFlowError):
        raise NotFound("gone")


def test_a_rule_violation_is_not_a_not_found():
    """Different failures must stay distinguishable."""
    assert not issubclass(OverAllocated, NotFound)
    assert issubclass(OverAllocated, DomainRuleViolated)


def test_the_pipeline_raises_the_shared_error_type():
    pipeline = Pipeline()
    with pytest.raises(DomainRuleViolated):
        pipeline.move_to(RequestState.PLACED)


# ── Logging ───────────────────────────────────────────────────────────────


def make_specialist():
    return SpecialistModel.objects.create(
        full_name="Alice Johnson",
        cost_rate=Decimal("50.00"),
        available_from=date(2026, 1, 1),
    )


def make_request(client="BCS"):
    return RequestModel.objects.create(
        client_name=client,
        headcount=1,
        starts_on=date(2026, 9, 1),
        ends_on=date(2026, 12, 31),
        max_bill_rate=Decimal("90.00"),
        fraction=Decimal("1.00"),
    )


@pytest.mark.django_db(transaction=True)
def test_a_successful_placement_is_logged_at_info(caplog):
    alice, request = make_specialist(), make_request()
    with caplog.at_level(logging.INFO):
        place(alice.pk, request.pk, Decimal("70.00"))

    assert any("placement created" in r.message for r in caplog.records)


@pytest.mark.django_db(transaction=True)
def test_a_refused_placement_is_logged_as_a_warning_not_an_error(caplog):
    """A refusal is the system WORKING. It must not look like a crash."""
    alice = make_specialist()
    place(alice.pk, make_request("BCS").pk, Decimal("70.00"))

    with caplog.at_level(logging.INFO):
        with pytest.raises(OverAllocated):
            place(alice.pk, make_request("Alfa").pk, Decimal("70.00"))

    refusals = [r for r in caplog.records if "placement refused" in r.message]
    assert refusals
    assert refusals[0].levelname == "WARNING"
