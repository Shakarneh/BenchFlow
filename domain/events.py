"""Domain events -- the Observer pattern.

When a request starts sourcing, several unrelated things should happen: the
SLA clock starts, a recruiter is notified, an audit line is written. The
pipeline should not know about any of them.

So instead of calling those things, it ANNOUNCES what happened. Whoever
cares subscribes. Adding a fifth reaction later touches no existing code --
that is the Open/Closed principle from Phase 2, at the system level.
"""

from dataclasses import dataclass, field
from datetime import datetime

from domain.pipeline import RequestState


@dataclass(frozen=True)
class DomainEvent:
    """Something that happened. Past tense, always -- events are facts."""

    at: datetime


@dataclass(frozen=True)
class RequestStateChanged(DomainEvent):
    client_name: str
    from_state: RequestState
    to_state: RequestState
    by: str


@dataclass(frozen=True)
class SourcingStarted(DomainEvent):
    """The SLA clock starts here. Expert Choice promises three days from now."""

    client_name: str


@dataclass(frozen=True)
class RequestPlaced(DomainEvent):
    client_name: str
    time_to_fill_hours: float | None


class EventBus:
    """Announces events to whoever subscribed to that kind of event.

    Deliberately tiny. A real system would put a message broker behind this
    interface -- Phase 13 does exactly that with Celery and Redis -- but the
    domain never needs to know.
    """

    def __init__(self):
        self._subscribers: dict[type, list] = {}

    def subscribe(self, event_type: type, handler):
        """Call `handler(event)` whenever an event of this type is published."""
        self._subscribers.setdefault(event_type, []).append(handler)

    def publish(self, event: DomainEvent):
        """Tell everyone who cares. One failing handler must not stop the rest."""
        for handler in self._subscribers.get(type(event), []):
            handler(event)

    def clear(self):
        self._subscribers.clear()
