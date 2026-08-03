# Design Patterns in benchFlow

Which patterns are used, where, why — and which were considered and rejected.

A pattern is only worth its complexity if it solves a problem the code actually
has. Each entry below states the problem first.

---

## Strategy — `domain/matcher.py`

**Problem.** Three matching algorithms with different trade-offs. Calling code should
not care which one is running.

**Solution.** `Matcher` is an abstract base class with one method. `GreedyMatcher`,
`OptimalMatcher` and `HungarianMatcher` implement it.

**What it bought.** Switching the default from greedy to Hungarian changed **zero**
calling code. The benchmark command runs all three through the same interface.
Shared behaviour — skill-graph resolution, eligibility filtering, multi-request
assignment — lives on the base class, so a new strategy inherits it for free.

---

## Repository — `domain/repositories.py` + `infrastructure/repositories.py`

**Problem.** The domain needs specialists and requests, but must not import Django,
or the business rules become untestable without a database.

**Solution.** `domain/` declares abstract *ports* (`SpecialistRepository`,
`RequestRepository`, `SkillGraphRepository`). `infrastructure/` provides Django
*adapters*. `specialist_to_domain()` is the border where everything Django-shaped stops.

**What it bought.** `GreedyMatcher`, written in Phase 1 with no database in existence,
ran against real PostgreSQL rows in Phase 4 without a single change. The full test
suite runs in under a second because it never touches a database.

---

## Specification — `domain/specifications.py`

**Problem.** `Request.is_satisfied_by()` was four rules welded into one boolean
expression. It could answer "no" but never "why not" — so a recruiter asking why a
candidate was rejected could not be told.

**Solution.** Each rule is an object with `is_satisfied_by()` and `describe_failure()`.
They compose with `&`, `|`, `~`.

**What it bought.** Rules became independently testable and reusable. And rejections
became explainable:

```
Elena Petrova   no room for 100% between 2026-09-01 and 2026-12-31 (already peaks at 75%)
```

One reason, not four — so an account manager immediately knows Elena is the right
person blocked only by 25% of her calendar, and can ask the client about a later start.
That information existed for a microsecond inside an `and` chain and was thrown away.

---

## State — `domain/pipeline.py`

**Problem.** A request moves Draft → Open → Sourcing → … → Ended. Some moves are legal
(Interview → Sourcing when a client rejects a candidate); others are nonsense
(Draft → Placed, skipping every check). Without a guard, one bad call places a
specialist on a request the client never confirmed, with no record of how.

**Solution.** An explicit `ALLOWED` table of permitted transitions, a single guard
(`target in ALLOWED[self.state]`), and an append-only history of frozen `Transition`
records.

**What it bought.** Illegal transitions raise instead of corrupting state. Business
rules live in data, not in branching code — *"an active engagement cannot be cancelled"*
is expressed purely as an absence from the table. And `time_to_fill()` measures
Sourcing → Placed, which is Expert Choice's advertised three-day promise.

---

## Observer — `domain/events.py`

**Problem.** Entering `SOURCING` should start the SLA clock, notify a recruiter, and
write an audit line. Those are three unrelated concerns, and the pipeline should not
know about any of them.

**Solution.** The pipeline publishes events; handlers subscribe to the event types they
care about. Events are frozen dataclasses named in the past tense — they are facts.

**What it bought.** Adding a fourth reaction touches no existing code — the Open/Closed
principle at system level. And it draws the seam that Phase 13 needs: `EventBus` is
the interface a real message broker (Celery + Redis) slots behind, without the domain
learning that queues exist.

---

## Factory — **considered and rejected**

**The case for it.** Constructing a `Specialist` involves a name, a `Decimal` rate, a
date, a skill list and an allocation list. That is the kind of assembly a Factory
usually exists to hide.

**Why it was rejected.** The problem it solves is already solved twice over:

- `@dataclass` generates a keyword-argument constructor that is clear at the call site
  and validated by type hints.
- `specialist_to_domain()` and `request_to_domain()` in the repository adapters
  already do the real "build a domain object from raw external data" job — that is
  the only place in the system where construction is non-trivial.
- Test setup is handled by **factory fixtures** in `tests/conftest.py`, which serve
  the same purpose with less ceremony and no production code.

Adding a `SpecialistFactory` class would mean a third construction path that wraps a
constructor which needs no wrapping. More indirection, no problem solved.

**The general rule.** A pattern earns its place by removing a pain that exists. Applying
one because it appears on a list is how codebases acquire layers nobody can justify.
`CLAUDE.md` §6 lists *"and when patterns are overkill"* as a Phase 8 concept — this is
that entry, and it is written down rather than demonstrated by making the mistake.

If a future requirement makes construction genuinely complex — say, building a
`Specialist` differently per client contract type — Factory becomes the right answer
and this decision should be revisited.

---

## Summary

| Pattern | Status | Where |
|---|---|---|
| Strategy | ✅ used | `domain/matcher.py` |
| Repository | ✅ used | `domain/repositories.py`, `infrastructure/repositories.py` |
| Specification | ✅ used | `domain/specifications.py` |
| State | ✅ used | `domain/pipeline.py` |
| Observer | ✅ used | `domain/events.py` |
| Factory | ❌ rejected | not needed — see above |
