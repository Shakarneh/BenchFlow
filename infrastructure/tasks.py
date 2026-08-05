"""Background jobs. Celery workers run these, not the web server.

A user should never wait for whole-bench matching. They ask, we hand the job
to a worker and answer immediately; the worker publishes the result later.
"""

from celery import shared_task

from infrastructure.cache import invalidate
from infrastructure.container import fill_all_requests


@shared_task
def fill_all_requests_task() -> dict:
    """Match the entire bench against every open request.

    Idempotent: it only READS and reports. Running it twice by accident
    changes nothing -- which is what makes it safe to retry.
    """
    proposals = fill_all_requests()()
    return {
        "requests": len(proposals),
        "fully_staffed": sum(1 for p in proposals if p.is_fully_staffed),
        "total_shortfall": sum(p.shortfall for p in proposals),
        "assignments": {
            p.request.client_name: [s.full_name for s in p.proposed]
            for p in proposals
        },
    }


@shared_task
def invalidate_match_cache_task() -> str:
    """Force every cached proposal to be recomputed on next request."""
    invalidate()
    return "match cache invalidated"
