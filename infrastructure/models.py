"""Django ORM models -- the DATABASE shape of benchFlow.

These are NOT the domain entities. They know about tables, columns, indexes
and foreign keys, and nothing about matching rules. repositories.py converts
between these rows and the pure objects in domain/.

Note the import direction: infrastructure imports domain (for Level), never
the other way round. That is the dependency rule holding.
"""

from django.db import models

from domain.skill_level import Level

LEVEL_CHOICES = [(level.value, level.name.title()) for level in Level]


class SkillModel(models.Model):
    """A capability, e.g. "Django". Unique by name."""

    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "skill"
        ordering = ["name"]

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

    def __str__(self):
        return self.full_name


class SpecialistSkillModel(models.Model):
    """One skill held by one specialist, at one level.

    This is a JOIN TABLE. A specialist has many skills and a skill belongs to
    many specialists -- but the pairing carries extra data (the level), so it
    needs its own table rather than a plain ManyToManyField.
    """

    specialist = models.ForeignKey(
        SpecialistModel, on_delete=models.CASCADE, related_name="skills"
    )
    skill = models.ForeignKey(SkillModel, on_delete=models.PROTECT)
    level = models.PositiveSmallIntegerField(choices=LEVEL_CHOICES)

    class Meta:
        db_table = "specialist_skill"
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
    max_bill_rate = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "request"
        ordering = ["starts_on"]

    def __str__(self):
        return f"{self.client_name} x{self.headcount} from {self.starts_on}"


class RequestRequirementModel(models.Model):
    """One skill required by one request, at a minimum level."""

    request = models.ForeignKey(
        RequestModel, on_delete=models.CASCADE, related_name="requirements"
    )
    skill = models.ForeignKey(SkillModel, on_delete=models.PROTECT)
    level = models.PositiveSmallIntegerField(choices=LEVEL_CHOICES)

    class Meta:
        db_table = "request_requirement"
        constraints = [
            models.UniqueConstraint(
                fields=["request", "skill"], name="one_level_per_skill_per_request"
            )
        ]

    def __str__(self):
        return f"{self.skill} ({self.get_level_display()})"
