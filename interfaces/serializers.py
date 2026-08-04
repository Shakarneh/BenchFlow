"""Translators: domain objects in, JSON out.

A serializer describes which fields appear in the JSON and how. These read
the pure domain objects -- the API never touches ORM rows directly.
"""

from rest_framework import serializers


class SkillLevelSerializer(serializers.Serializer):
    skill = serializers.CharField(source="skill.name")
    level = serializers.CharField(source="level.name")


class SpecialistSerializer(serializers.Serializer):
    full_name = serializers.CharField()
    cost_rate = serializers.DecimalField(max_digits=10, decimal_places=2)
    available_from = serializers.DateField()
    skills = SkillLevelSerializer(many=True)


class RequestSerializer(serializers.Serializer):
    client_name = serializers.CharField()
    headcount = serializers.IntegerField()
    starts_on = serializers.DateField()
    ends_on = serializers.DateField()
    fraction = serializers.DecimalField(max_digits=3, decimal_places=2)
    max_bill_rate = serializers.DecimalField(max_digits=10, decimal_places=2)
    required_skills = SkillLevelSerializer(many=True)
