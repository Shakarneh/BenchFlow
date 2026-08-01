"""Django admin registration -- a working UI for free.

This is why Django was chosen: a usable back office exists before any
frontend work, so demo data can be entered and inspected by hand.
"""

from django.contrib import admin

from infrastructure.models import (
    RequestModel,
    RequestRequirementModel,
    SkillModel,
    SpecialistModel,
    SpecialistSkillModel,
)


class SpecialistSkillInline(admin.TabularInline):
    """Edit a specialist's skills on the specialist's own page."""

    model = SpecialistSkillModel
    extra = 1


class RequestRequirementInline(admin.TabularInline):
    model = RequestRequirementModel
    extra = 1


@admin.register(SkillModel)
class SkillAdmin(admin.ModelAdmin):
    list_display = ["name", "implied_skills"]
    search_fields = ["name"]
    filter_horizontal = ["implies"]

    @admin.display(description="implies")
    def implied_skills(self, obj):
        return ", ".join(s.name for s in obj.implies.all()) or "-"


@admin.register(SpecialistModel)
class SpecialistAdmin(admin.ModelAdmin):
    list_display = ["full_name", "cost_rate", "available_from"]
    list_filter = ["available_from"]
    search_fields = ["full_name"]
    inlines = [SpecialistSkillInline]


@admin.register(RequestModel)
class RequestAdmin(admin.ModelAdmin):
    list_display = ["client_name", "headcount", "starts_on", "max_bill_rate"]
    list_filter = ["starts_on"]
    search_fields = ["client_name"]
    inlines = [RequestRequirementInline]
