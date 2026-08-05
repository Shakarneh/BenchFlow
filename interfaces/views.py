"""The web layer. Each view answers one URL.

Views stay thin on purpose: load through the repositories, hand to a
serializer, return. No business rules live here -- those are in domain/.
"""

import logging

from django.core.cache import cache
from django.db import connection
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from infrastructure.cache import TTL_SECONDS, proposal_key
from infrastructure.container import propose_candidates
from infrastructure.models import RequestModel
from infrastructure.repositories import (
    DjangoRequestRepository,
    DjangoSpecialistRepository,
    request_to_domain,
)
from interfaces.permissions import IsAccountManager
from interfaces.serializers import RequestSerializer, SpecialistSerializer

logger = logging.getLogger(__name__)


class HealthCheck(APIView):
    """GET /api/health/ -- is this instance actually working?

    Deliberately open (no login): the hosting platform pings this to decide
    whether to keep the instance in service, and it has no credentials.

    It checks the DATABASE too, not just "did Python start". An app that
    answers 200 while its database is unreachable is worse than one that
    admits it is down.
    """

    permission_classes = [AllowAny]

    def get(self, request):
        try:
            connection.ensure_connection()
        except Exception:
            logger.exception("health check failed: database unreachable")
            return Response({"status": "unhealthy", "database": "unreachable"}, status=503)
        return Response({"status": "ok", "database": "ok"})


class SpecialistList(APIView):
    """GET /api/specialists/ -- everyone in the pool, with their skills."""

    def get(self, request):
        people = DjangoSpecialistRepository().all()
        return Response(SpecialistSerializer(people, many=True).data)


class RequestList(APIView):
    """GET /api/requests/ -- every open client request."""

    def get(self, request):
        requests = DjangoRequestRepository().all()
        return Response(RequestSerializer(requests, many=True).data)


class ProposeCandidates(APIView):
    """POST /api/requests/<id>/propose/ -- run the matcher for one request.

    POST, not GET: reading data is GET; asking the system to DO something
    is POST. The heavy lifting happens in application/ -- this view only
    translates the answer to JSON.
    """

    permission_classes = [IsAuthenticated, IsAccountManager]

    def post(self, request, pk):
        row = get_object_or_404(RequestModel, pk=pk)

        # Cache hit? Hand back the stored answer without running the matcher.
        key = proposal_key(pk)
        cached = cache.get(key)
        if cached is not None:
            return Response({**cached, "cached": True})

        proposal = propose_candidates()(request_to_domain(row))
        payload = {
            "client_name": proposal.request.client_name,
            "is_fully_staffed": proposal.is_fully_staffed,
            "shortfall": proposal.shortfall,
            "proposed": SpecialistSerializer(proposal.proposed, many=True).data,
            "rejected": [
                {"full_name": person.full_name, "reasons": reasons}
                for person, reasons in proposal.rejected
            ],
        }
        cache.set(key, payload, TTL_SECONDS)
        return Response({**payload, "cached": False})
