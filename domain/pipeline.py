"""The request pipeline: a guarded state machine with an audit trail.

A request moves from Draft to Ended through a fixed set of states. Only the
moves listed in ALLOWED are possible; anything else raises. Every accepted
move is recorded, so "who moved this to Placed, and when" always has an
answer -- which matters when the clients are regulated banks.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class RequestState(Enum):
    DRAFT = "draft"
    OPEN = "open"
    SOURCING = "sourcing"
    PROPOSED = "proposed"
    INTERVIEW = "interview"
    OFFERED = "offered"
    PLACED = "placed"
    ACTIVE = "active"
    ENDED = "ended"
    CANCELLED = "cancelled"


# Which moves are legal, from each state. Anything absent is forbidden.
ALLOWED: dict[RequestState, set[RequestState]] = {
    RequestState.DRAFT: {RequestState.OPEN, RequestState.CANCELLED},
    RequestState.OPEN: {RequestState.SOURCING, RequestState.CANCELLED},
    RequestState.SOURCING: {RequestState.PROPOSED, RequestState.CANCELLED},
    # Rejected at any client-facing stage -> back to sourcing for more candidates.
    RequestState.PROPOSED: {RequestState.INTERVIEW, RequestState.SOURCING, RequestState.CANCELLED},
    RequestState.INTERVIEW: {RequestState.OFFERED, RequestState.SOURCING, RequestState.CANCELLED},
    RequestState.OFFERED: {RequestState.PLACED, RequestState.SOURCING, RequestState.CANCELLED},
    RequestState.PLACED: {RequestState.ACTIVE, RequestState.CANCELLED},
    RequestState.ACTIVE: {RequestState.ENDED},
    # Terminal states. Nothing leaves them.
    RequestState.ENDED: set(),
    RequestState.CANCELLED: set(),
}

# The SLA clock starts here -- the 3-day placement promise is measured from
# the moment we begin looking, not from when the client first made contact.
SLA_STARTS_AT = RequestState.SOURCING


class IllegalTransition(Exception):
    """Raised when a move is not permitted from the current state."""


@dataclass(frozen=True)
class Transition:
    """One recorded move. Frozen: history must never be rewritten."""

    from_state: RequestState
    to_state: RequestState
    at: datetime
    by: str


@dataclass
class Pipeline:
    """Where a request is, and everywhere it has been."""

    state: RequestState = RequestState.DRAFT
    history: list[Transition] = field(default_factory=list)

    def can_move_to(self, target: RequestState) -> bool:
        """Is this move permitted from where we are now?"""
        return target in ALLOWED[self.state]
    
    def move_to(self, target: RequestState, by: str = "system", at: datetime | None = None):
        """Move, or refuse loudly. Never silently ignore an illegal move."""
        if not self.can_move_to(target):
            raise IllegalTransition(
                f"cannot move from {self.state.value} to {target.value}; "
                f"allowed: {sorted(s.value for s in ALLOWED[self.state]) or 'none (terminal)'}"
            )
        self.history.append(
            Transition(self.state, target, at or datetime.now(), by)
        )
        self.state = target

    @property
    def is_terminal(self) -> bool:
        return not ALLOWED[self.state]

    @property
    def sourcing_started_at(self) -> datetime | None:
        """When the SLA clock started, or None if sourcing never began."""
        for transition in self.history:
            if transition.to_state is SLA_STARTS_AT:
                return transition.at
        return None

    def time_to_fill(self) -> "timedelta | None":
        """How long from starting to source until the specialist was placed.

        None if either end has not happened yet. This is the number Expert
        Choice advertises as three days.
        """
        started = self.sourcing_started_at
        if started is None:
            return None
        for transition in self.history:
            if transition.to_state is RequestState.PLACED:
                return transition.at - started
        return None
