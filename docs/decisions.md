# Architecture Decision Records

Short notes on decisions that shaped the system — what we chose, and why.

---

## ADR-1: The default matcher is Hungarian, not greedy

**Decision.** `HungarianMatcher` is the production default. Greedy stays as a baseline,
exhaustive stays as a test oracle.

**Why.** Measured, not guessed: at 8 requests × 25 people, greedy left one client
unstaffed to save 47. Hungarian filled everyone, and at larger sizes it was cheaper
too. The runtime price (~160ms at 30×150) doesn't matter for a background job.
Details: [matching.md](matching.md).

---

## ADR-2: The dependency rule is enforced by a machine, not a promise

**Decision.** `import-linter` runs with three contracts: business code (`domain/`)
may import only the standard library; use cases (`application/`) may not touch
Django; arrows always point inward. From Phase 18 this runs on every push.

**Why.** The rule existed since day 0, but only as text in CLAUDE.md. We broke it on
purpose (`from django.db import models` inside `domain/skill.py`) and watched the
build fail with the exact file and line. A rule a computer checks cannot quietly rot.

---

## ADR-3: Requests and specialists meet only through interfaces

**Decision.** `application/` receives its data sources as constructor arguments
(`SpecialistRepository`, `RequestRepository`). The only place that connects the
real Django versions is `infrastructure/container.py`.

**Why.** The same use case runs against PostgreSQL in production and against a
4-line fake list in tests. 10 application tests run with no database at all.
