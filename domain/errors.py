"""Every error benchFlow raises on purpose, in one family tree.

Why a hierarchy instead of loose classes: callers can catch at the level of
detail they care about.

    except OverAllocated        -> this exact problem
    except DomainRuleViolated   -> any business rule said no
    except BenchFlowError       -> anything we raised deliberately

Anything NOT descending from BenchFlowError is a bug, not a business
outcome -- and should crash loudly rather than be swallowed.
"""


class BenchFlowError(Exception):
    """Base for every error this system raises deliberately."""


class DomainRuleViolated(BenchFlowError):
    """A business rule refused the operation. The caller asked for something
    legitimate; the answer is no. Maps to HTTP 409 Conflict."""


class OverAllocated(DomainRuleViolated):
    """Booking would push a specialist beyond 100% capacity."""


class IllegalTransition(DomainRuleViolated):
    """This pipeline move is not permitted from the current state."""


class InvalidEngagement(DomainRuleViolated):
    """Rates that make no commercial sense."""


class NotFound(BenchFlowError):
    """The thing asked for does not exist. Maps to HTTP 404."""
