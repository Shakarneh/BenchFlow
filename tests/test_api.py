"""API tests: fake browser in, JSON out.

pytest-django builds a TEMPORARY empty database for each test run (named
test_benchflow), so these tests never touch your real data.
"""

from datetime import date
from decimal import Decimal

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from domain.skill_level import Level
from infrastructure.models import (
    RequestModel,
    RequestRequirementModel,
    SkillModel,
    SpecialistModel,
    SpecialistSkillModel,
)


@pytest.fixture
def client():
    """Logged in, but in NO group -- can browse, cannot act."""
    user = User.objects.create_user("test_recruiter", password="irrelevant")
    api = APIClient()
    api.force_authenticate(user)
    return api


@pytest.fixture
def manager_client():
    """Logged in AND an account manager -- allowed to run the matcher."""
    from django.contrib.auth.models import Group

    user = User.objects.create_user("test_manager", password="irrelevant")
    group, _ = Group.objects.get_or_create(name="Account Managers")
    user.groups.add(group)
    api = APIClient()
    api.force_authenticate(user)
    return api


def make_world():
    """One skill, one qualified specialist, one request that wants them."""
    django = SkillModel.objects.create(name="Django")
    alice = SpecialistModel.objects.create(
        full_name="Alice Johnson",
        cost_rate=Decimal("65.00"),
        available_from=date(2026, 8, 1),
    )
    SpecialistSkillModel.objects.create(specialist=alice, skill=django, level=Level.SENIOR.value)
    request = RequestModel.objects.create(
        client_name="BCS",
        headcount=1,
        starts_on=date(2026, 9, 1),
        ends_on=date(2026, 12, 31),
        max_bill_rate=Decimal("90.00"),
    )
    RequestRequirementModel.objects.create(request=request, skill=django, level=Level.MIDDLE.value)
    return request


@pytest.mark.django_db
def test_anonymous_visitors_are_locked_out():
    """No login -> 403. This is the whole point of Phase 11."""
    make_world()
    response = APIClient().get("/api/specialists/")
    assert response.status_code == 403


@pytest.mark.django_db
def test_specialist_list_returns_200_with_the_data(client):
    make_world()
    response = client.get("/api/specialists/")
    assert response.status_code == 200
    assert response.json()[0]["full_name"] == "Alice Johnson"


@pytest.mark.django_db
def test_a_plain_user_cannot_run_the_matcher(client):
    """Browsing is fine; proposing is a business action reserved for managers."""
    request = make_world()
    response = client.post(f"/api/requests/{request.pk}/propose/")
    assert response.status_code == 403


@pytest.mark.django_db
def test_propose_returns_the_matchers_answer(manager_client):
    request = make_world()
    response = manager_client.post(f"/api/requests/{request.pk}/propose/")
    assert response.status_code == 200
    body = response.json()
    assert body["is_fully_staffed"] is True
    assert body["proposed"][0]["full_name"] == "Alice Johnson"


@pytest.mark.django_db
def test_proposing_for_a_missing_request_is_404(manager_client):
    response = manager_client.post("/api/requests/99999/propose/")
    assert response.status_code == 404


@pytest.mark.django_db
def test_reading_the_propose_url_is_405(manager_client):
    """GET on a do-something endpoint is refused, not silently accepted."""
    request = make_world()
    response = manager_client.get(f"/api/requests/{request.pk}/propose/")
    assert response.status_code == 405
