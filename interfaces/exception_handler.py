"""One place that turns domain errors into HTTP answers.

Without this, a refused booking would surface as a 500 Server Error -- which
tells the client "we broke", when the truth is "you asked for something the
rules forbid". Those are different, and the status code must say which.

    DomainRuleViolated -> 409 Conflict   (legitimate ask, rules said no)
    NotFound           -> 404
    anything else      -> DRF's default, and a 500 if it is a real bug
"""

import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_default

from domain.errors import DomainRuleViolated, NotFound

logger = logging.getLogger(__name__)


def benchflow_exception_handler(exc, context):
    if isinstance(exc, DomainRuleViolated):
        logger.warning("rule violated: %s: %s", type(exc).__name__, exc)
        return Response(
            {"detail": str(exc), "error": type(exc).__name__},
            status=status.HTTP_409_CONFLICT,
        )

    if isinstance(exc, NotFound):
        return Response({"detail": str(exc)}, status=status.HTTP_404_NOT_FOUND)

    response = drf_default(exc, context)
    if response is None:
        # DRF did not recognise it -> a real bug. Log the full traceback so
        # it is debuggable, and let it become a 500.
        logger.exception("unhandled error in %s", context.get("view"))
    return response
