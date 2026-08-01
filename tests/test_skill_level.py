from domain.skill import Skill
from domain.skill_level import Level, SkillLevel


def test_skill_levels_with_the_same_skill_and_level_are_equal():
    assert SkillLevel(Skill("Django"), Level.SENIOR) == SkillLevel(Skill("Django"), Level.SENIOR)


def test_skill_levels_with_different_levels_are_not_equal():
    assert SkillLevel(Skill("Django"), Level.SENIOR) != SkillLevel(Skill("Django"), Level.JUNIOR)


def test_comparing_to_a_non_skill_level_does_not_crash():
    assert SkillLevel(Skill("Django"), Level.SENIOR) != "Django Senior"


def test_duplicate_skill_levels_collapse_in_a_set():
    assert len({
        SkillLevel(Skill("Django"), Level.SENIOR),
        SkillLevel(Skill("Django"), Level.SENIOR),
    }) == 1



# 1. test_higher_level_in_the_same_skill_covers_a_lower_requirement
#       senior Django  covers  middle Django   → assert ...covers(...) is True

def test_senior_covers_a_middle_requirement():
    senior = SkillLevel(Skill("Django"), Level.SENIOR)
    required = SkillLevel(Skill("Django"), Level.MIDDLE)
    assert senior.covers(required)
    
    
# 2. test_lower_level_in_the_same_skill_does_not_cover_a_higher_requirement
#       junior Django  does NOT cover  middle Django   → assert not ...

def test_junior_does_not_cover_a_middle_requirement():
    junior = SkillLevel(Skill("Django"), Level.JUNIOR)
    required = SkillLevel(Skill("Django"), Level.MIDDLE)
    assert not junior.covers(required)

# 3. test_a_different_skill_is_never_covered_whatever_the_level
#       senior Django  does NOT cover  junior Python   → assert not ...

def test_a_different_skill_is_never_covered():
    django = SkillLevel(Skill("Django"), Level.SENIOR)
    required = SkillLevel(Skill("Python"), Level.JUNIOR)
    assert not django.covers(required) 