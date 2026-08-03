"""Django admin registration -- a working UI for free.

This is why Django was chosen: a usable back office exists before any
frontend work, so demo data can be entered and inspected by hand.
"""

from django.contrib import admin

from infrastructure.models import (
    AllocationModel,
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


class AllocationInline(admin.TabularInline):
    """See and edit someone's bookings on their own page."""

    model = AllocationModel
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
    list_display = ["full_name", "cost_rate", "available_from", "peak_load"]
    list_filter = ["available_from"]
    search_fields = ["full_name"]
    inlines = [SpecialistSkillInline, AllocationInline]

    @admin.display(description="peak load")
    def peak_load(self, obj):
        """Show the sweep-line result right in the list -- over-allocation is visible at a glance."""
        from domain.allocation import Calendar
        from infrastructure.repositories import specialist_to_domain

        peak = Calendar(specialist_to_domain(obj).allocations).peak_load()
        return f"{peak:.0%}" + (" OVER" if peak > 1 else "")


@admin.register(RequestModel)
class RequestAdmin(admin.ModelAdmin):
    list_display = ["client_name", "headcount", "starts_on", "ends_on", "fraction", "max_bill_rate"]
    list_filter = ["starts_on"]
    search_fields = ["client_name"]
    inlines = [RequestRequirementInline]
