from domain.skill import Skill


def test_skills_with_the_same_name_are_equal():
    assert Skill("Django") == Skill("Django")


def test_skills_with_different_names_are_not_equal():
    assert Skill("Django") != Skill("Python")


def test_comparing_to_a_non_skill_does_not_crash():
    assert Skill("Django") != "Django"


def test_duplicate_skills_collapse_in_a_set():
    assert len({Skill("Django"), Skill("Django")}) == 1