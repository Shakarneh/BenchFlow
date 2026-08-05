from domain.skill import Skill
from domain.skill_graph import SkillGraph
from domain.skill_level import Level, SkillLevel

DJANGO = Skill("Django")
PYTHON = Skill("Python")
PROGRAMMING = Skill("Programming")
REACT = Skill("React")
JAVASCRIPT = Skill("JavaScript")

# Django -> Python -> Programming,  React -> JavaScript -> Programming
CHAIN = {
    DJANGO: {PYTHON},
    PYTHON: {PROGRAMMING},
    REACT: {JAVASCRIPT},
    JAVASCRIPT: {PROGRAMMING},
}


def test_a_skill_with_no_implications_implies_nothing():
    assert SkillGraph().implied_by(DJANGO) == set()


def test_one_hop():
    graph = SkillGraph({DJANGO: {PYTHON}})
    assert graph.implied_by(DJANGO) == {PYTHON}


def test_transitive_closure_follows_the_whole_chain():
    assert SkillGraph(CHAIN).implied_by(DJANGO) == {PYTHON, PROGRAMMING}


def test_implications_are_one_directional():
    """Django implies Python. Python does NOT imply Django."""
    assert SkillGraph(CHAIN).implied_by(PYTHON) == {PROGRAMMING}


def test_two_paths_reaching_the_same_skill_do_not_duplicate():
    assert SkillGraph(CHAIN).implied_by(REACT) == {JAVASCRIPT, PROGRAMMING}


def test_a_cycle_does_not_hang_the_traversal():
    """A -> B -> A. Should terminate, not loop forever."""
    a, b = Skill("A"), Skill("B")
    graph = SkillGraph({a: {b}, b: {a}})
    assert graph.implied_by(a) == {a, b}


def test_expand_adds_implied_skills_at_the_same_level():
    graph = SkillGraph({DJANGO: {PYTHON}})
    expanded = graph.expand([SkillLevel(DJANGO, Level.SENIOR)])
    assert set(expanded) == {
        SkillLevel(DJANGO, Level.SENIOR),
        SkillLevel(PYTHON, Level.SENIOR),
    }


def test_expand_keeps_the_highest_level_when_a_skill_appears_twice():
    """Django-Senior implies Python-Senior; a declared Python-Junior must not win."""
    graph = SkillGraph({DJANGO: {PYTHON}})
    expanded = graph.expand([SkillLevel(DJANGO, Level.SENIOR), SkillLevel(PYTHON, Level.JUNIOR)])
    assert SkillLevel(PYTHON, Level.SENIOR) in expanded
    assert SkillLevel(PYTHON, Level.JUNIOR) not in expanded


def test_a_specialist_covers_an_implied_requirement_after_expansion(make_specialist):
    """The whole point: Alice knows only Django, but Django implies Python."""
    graph = SkillGraph({DJANGO: {PYTHON}})
    alice = make_specialist(skills=[SkillLevel(DJANGO, Level.SENIOR)])
    assert not alice.covers(SkillLevel(PYTHON, Level.MIDDLE))

    alice.skills = graph.expand(alice.skills)
    assert alice.covers(SkillLevel(PYTHON, Level.MIDDLE))
