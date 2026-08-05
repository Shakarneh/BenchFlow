"""Caching, and the harder half: knowing when to forget."""

from datetime import date
from decimal import Decimal

import pytest
from django.contrib.auth.models import User
from django.core.cache import cache
from rest_framework.test import APIClient

from domain.skill_level import Level
from infrastructure.cache import data_version, invalidate
from infrastructure.models import (
    RequestModel,
    RequestRequirementModel,
    SkillModel,
    SpecialistModel,
    SpecialistSkillModel,
)


@pytest.fixture(autouse=True)
def clean_cache():
    """Every test starts from an empty cache, or they poison each other."""
    cache.clear()
    yield
    cache.clear()


@pytest.fixture
def admin_client():
    user = User.objects.create_superuser("boss", password="irrelevant")
    api = APIClient()
    api.force_authenticate(user)
    return api


def make_world():
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
    return request, alice


def test_invalidate_bumps_the_version():
    before = data_version()
    invalidate()
    assert data_version() == before + 1


@pytest.mark.django_db
def test_the_first_call_is_computed_and_the_second_is_cached(admin_client):
    request, _ = make_world()
    url = f"/api/requests/{request.pk}/propose/"

    assert admin_client.post(url).json()["cached"] is False
    assert admin_client.post(url).json()["cached"] is True


@pytest.mark.django_db
def test_the_cached_answer_is_the_same_answer(admin_client):
    request, _ = make_world()
    url = f"/api/requests/{request.pk}/propose/"

    fresh = admin_client.post(url).json()
    cached = admin_client.post(url).json()
    assert fresh["proposed"] == cached["proposed"]


@pytest.mark.django_db
def test_changing_a_specialist_invalidates_the_cache(admin_client):
    """The signal fires on save -- no cache-clearing code at the call site."""
    request, alice = make_world()
    url = f"/api/requests/{request.pk}/propose/"

    admin_client.post(url)  # warm the cache
    assert admin_client.post(url).json()["cached"] is True  # confirmed warm

    alice.cost_rate = Decimal("70.00")
    alice.save()

    assert admin_client.post(url).json()["cached"] is False  # forgotten


@pytest.mark.django_db
def test_a_stale_answer_is_never_served_after_data_changes(admin_client):
    """Alice becomes too expensive -- the cache must not keep proposing her."""
    request, alice = make_world()
    url = f"/api/requests/{request.pk}/propose/"

    assert admin_client.post(url).json()["proposed"][0]["full_name"] == "Alice Johnson"

    alice.cost_rate = Decimal("500.00")  # way over the 90.00 budget
    alice.save()

    assert admin_client.post(url).json()["proposed"] == []
