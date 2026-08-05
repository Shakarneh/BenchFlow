"""Automatic cache invalidation.

Django fires a signal after any model is saved or deleted. We listen for the
models that affect matching, and bump the cache version when one changes.

Doing it here rather than at every call site means nobody can forget.
"""

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from infrastructure.cache import invalidate
from infrastructure.models import (
    AllocationModel,
    RequestModel,
    RequestRequirementModel,
    SkillModel,
    SpecialistModel,
    SpecialistSkillModel,
)

WATCHED = [
    SpecialistModel,
    SpecialistSkillModel,
    AllocationModel,
    RequestModel,
    RequestRequirementModel,
    SkillModel,
]


@receiver(post_save)
@receiver(post_delete)
def invalidate_match_cache(sender, **kwargs):
    if sender in WATCHED:
        invalidate()
