"""The commercial wrapper: what we pay vs what we charge.

Pure money arithmetic, all Decimal, all rounding explicit. This is the
company's income statement in miniature, so exactness is the whole point.
"""

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

CENTS = Decimal("0.01")  # money is quantized to cents
RATIO = Decimal("0.0001")  # ratios to 4 places, e.g. 0.3077 = 30.77%


@dataclass(frozen=True)
class Engagement:
    """One priced placement: hourly cost to us, hourly bill to the client.

    Frozen: an engagement is a priced snapshot. Renegotiating rates creates
    a new engagement; it does not quietly edit history.
    """

    cost_rate: Decimal
    bill_rate: Decimal

    def __post_init__(self):
        # Invariants: fail at creation, not at report time three weeks later.
        if self.cost_rate <= 0:
            raise ValueError(f"cost_rate must be positive, got {self.cost_rate}")
        if self.bill_rate <= 0:
            raise ValueError(f"bill_rate must be positive, got {self.bill_rate}")

    def margin(self) -> Decimal:
        """Profit per hour, in money, rounded half-up to cents.

        May be negative -- a loss-making placement is legal, but visible.
        """
        return (self.bill_rate - self.cost_rate).quantize(CENTS, ROUND_HALF_UP)

    def margin_ratio(self) -> Decimal:
        """The share of every billed unit that we keep. 0.3077 = 30.77%."""
        return ((self.bill_rate - self.cost_rate) / self.bill_rate).quantize(RATIO, ROUND_HALF_UP)

    @property
    def is_profitable(self) -> bool:
        return self.margin() > 0
