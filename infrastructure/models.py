"""Django ORM models -- the DATABASE shape of benchFlow.

These are NOT the domain entities. They know about tables, columns, indexes
and foreign keys, and nothing about matching rules. repositories.py converts
between these rows and the pure objects in domain/.

Note the import direction: infrastructure imports domain (for Level), never
the other way round. That is the dependency rule holding.
"""

from decimal import Decimal

from django.db import models

from domain.skill_level import Level

LEVEL_CHOICES = [(level.value, level.name.title()) for level in Level]


class SkillModel(models.Model):
    """A capability, e.g. "Django". Unique by name.

    `implies` is a self-referencing many-to-many: a skill points at other
    skills it necessarily includes. Django -> Python. symmetrical=False is
    essential -- the relation only runs one way.
    """

    name = models.CharField(max_length=100, unique=True)
    implies = models.ManyToManyField(
        "self",
        symmetrical=False,
        blank=True,
        related_name="implied_by",
        help_text="Skills this one necessarily includes. Django implies Python.",
    )

    class Meta:
        db_table = "skill"
        ordering = ["name"]
        # Without this the admin calls the class by its Python name and shows
        # "Skill models". These names are what a manager reads, not a coder.
        verbose_name = "skill"
        verbose_name_plural = "skills"

    def __str__(self):
        return self.name


class SpecialistModel(models.Model):
    """An engineer we can place."""

    full_name = models.CharField(max_length=200)
    cost_rate = models.DecimalField(max_digits=10, decimal_places=2)
    available_from = models.DateField(db_index=True)

    class Meta:
        db_table = "specialist"
        ordering = ["full_name"]
        verbose_name = "specialist"
        verbose_name_plural = "specialists"

    def __str__(self):
        return self.full_name


class SpecialistSkillModel(models.Model):
    """One skill held by one specialist, at one level.

    This is a JOIN TABLE. A specialist has many skills and a skill belongs to
    many specialists -- but the pairing carries extra data (the level), so it
    needs its own table rather than a plain ManyToManyField.
    """

    specialist = models.ForeignKey(SpecialistModel, on_delete=models.CASCADE, related_name="skills")
    skill = models.ForeignKey(SkillModel, on_delete=models.PROTECT)
    level = models.PositiveSmallIntegerField(choices=LEVEL_CHOICES)

    class Meta:
        db_table = "specialist_skill"
        verbose_name = "skill"
        verbose_name_plural = "skills"
        constraints = [
            models.UniqueConstraint(
                fields=["specialist", "skill"], name="one_level_per_skill_per_specialist"
            )
        ]

    def __str__(self):
        return f"{self.specialist} - {self.skill} ({self.get_level_display()})"


class RequestModel(models.Model):
    """An open demand from a client."""

    client_name = models.CharField(max_length=200)
    headcount = models.PositiveIntegerField()
    starts_on = models.DateField(db_index=True)
    ends_on = models.DateField(db_index=True)
    max_bill_rate = models.DecimalField(max_digits=10, decimal_places=2)
    fraction = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=Decimal("1.00"),
        help_text="Share of a specialist's time this engagement needs. 0.50 = half time.",
    )

    class Meta:
        db_table = "request"
        ordering = ["starts_on"]
        verbose_name = "request"
        verbose_name_plural = "requests"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(ends_on__gte=models.F("starts_on")),
                name="request_ends_on_or_after_it_starts",
            ),
            models.CheckConstraint(
                condition=models.Q(fraction__gt=0) & models.Q(fraction__lte=1),
                name="request_fraction_between_zero_and_one",
            ),
        ]

    def __str__(self):
        return f"{self.client_name} x{self.headcount} from {self.starts_on}"


class AllocationModel(models.Model):
    """Time booked on a specialist's calendar.

    Both dates are INCLUSIVE. `fraction` is the share of their working time:
    0.50 means half time. The database itself enforces both invariants below,
    so no application bug can write a nonsense row.
    """

    specialist = models.ForeignKey(
        SpecialistModel, on_delete=models.CASCADE, related_name="allocations"
    )
    request = models.ForeignKey(
        RequestModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="allocations",
    )
    starts_on = models.DateField(db_index=True)
    ends_on = models.DateField(db_index=True)
    fraction = models.DecimalField(max_digits=3, decimal_places=2)

    class Meta:
        db_table = "allocation"
        ordering = ["starts_on"]
        verbose_name = "booking"
        verbose_name_plural = "bookings"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(ends_on__gte=models.F("starts_on")),
                name="allocation_ends_on_or_after_it_starts",
            ),
            models.CheckConstraint(
                condition=models.Q(fraction__gt=0) & models.Q(fraction__lte=1),
                name="allocation_fraction_between_zero_and_one",
            ),
        ]

    def __str__(self):
        return f"{self.specialist} {self.fraction:.0%} {self.starts_on}..{self.ends_on}"


class PlacementModel(models.Model):
    """A confirmed placement, with its commercial terms.

    cost_rate and bill_rate are COPIED here, not looked up live: if the
    specialist's rate changes next year, this placement's margin must not
    silently change with it. A signed deal is a snapshot.
    """

    specialist = models.ForeignKey(
        SpecialistModel, on_delete=models.PROTECT, related_name="placements"
    )
    request = models.ForeignKey(RequestModel, on_delete=models.PROTECT, related_name="placements")
    allocation = models.OneToOneField(
        "AllocationModel", on_delete=models.CASCADE, related_name="placement"
    )
    cost_rate = models.DecimalField(max_digits=10, decimal_places=2)
    bill_rate = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "placement"
        ordering = ["-created_at"]
        verbose_name = "placement"
        verbose_name_plural = "placements"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(cost_rate__gt=0) & models.Q(bill_rate__gt=0),
                name="placement_rates_are_positive",
            ),
        ]

    def __str__(self):
        return f"{self.specialist} -> {self.request.client_name}"


class RequestRequirementModel(models.Model):
    """One skill required by one request, at a minimum level."""

    request = models.ForeignKey(RequestModel, on_delete=models.CASCADE, related_name="requirements")
    skill = models.ForeignKey(SkillModel, on_delete=models.PROTECT)
    level = models.PositiveSmallIntegerField(choices=LEVEL_CHOICES)

    class Meta:
        db_table = "request_requirement"
        verbose_name = "required skill"
        verbose_name_plural = "required skills"
        constraints = [
            models.UniqueConstraint(
                fields=["request", "skill"], name="one_level_per_skill_per_request"
            )
        ]

    def __str__(self):
        return f"{self.skill} ({self.get_level_display()})"
