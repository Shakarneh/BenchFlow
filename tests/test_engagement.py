"""Money maths that must be exact -- every assertion is to the cent."""

from decimal import Decimal

import pytest

from domain.engagement import Engagement


def test_margin_is_bill_minus_cost():
    engagement = Engagement(cost_rate=Decimal("45.00"), bill_rate=Decimal("65.00"))
    assert engagement.margin() == Decimal("20.00")


def test_margin_ratio_is_margin_over_bill():
    engagement = Engagement(cost_rate=Decimal("45.00"), bill_rate=Decimal("65.00"))
    assert engagement.margin_ratio() == Decimal("0.3077")  # 20/65, half-up at 4 places


def test_a_loss_making_engagement_is_legal_but_visible():
    engagement = Engagement(cost_rate=Decimal("80.00"), bill_rate=Decimal("70.00"))
    assert engagement.margin() == Decimal("-10.00")
    assert not engagement.is_profitable


def test_rounding_is_half_up_not_bankers():
    """0.01/0.32 = 0.03125 exactly. Python's default rounds it DOWN to 0.0312
    (ties go to the even digit). Finance rounds half-up: 0.0313."""
    engagement = Engagement(cost_rate=Decimal("0.31"), bill_rate=Decimal("0.32"))
    assert engagement.margin_ratio() == Decimal("0.0313")


def test_zero_or_negative_rates_are_refused_at_creation():
    with pytest.raises(ValueError):
        Engagement(cost_rate=Decimal("0.00"), bill_rate=Decimal("65.00"))
    with pytest.raises(ValueError):
        Engagement(cost_rate=Decimal("45.00"), bill_rate=Decimal("-1.00"))


def test_margin_arithmetic_never_drifts():
    """The float horror show, done right: 0.1 + 0.2 style sums stay exact."""
    engagement = Engagement(cost_rate=Decimal("0.10"), bill_rate=Decimal("0.30"))
    assert engagement.margin() == Decimal("0.20")  # float would give 0.19999...
