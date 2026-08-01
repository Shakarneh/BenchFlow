# benchFlow

**A resourcing and allocation platform for IT service companies.**

An IT outstaffing company employs engineers. Clients send requests — *"two senior Python developers
for six months, starting in three weeks, at most X per hour."* Someone has to decide who goes where,
without over-committing anyone, fast. Engineers who aren't assigned sit on **the bench**, costing
money every day.

benchFlow is the engine behind that decision. At its centre is a real optimisation problem — the
**assignment problem** — not a set of CRUD forms.

> 🚧 **Status: in active development.** Phase 0 of 21 complete. See [`CLAUDE.md`](CLAUDE.md) for the
> full plan and progress log.

---

## What makes it interesting

| Problem | Why it's hard |
|---|---|
| **Matching engine** | N specialists × M requests under skill, level, date and rate constraints — the assignment problem |
| **Fractional allocation** | Someone can be 50% on project A and 50% on B. Overlapping intervals with capacity |
| **Skill graph** | "Django ⇒ Python" — implications resolved by graph traversal before matching |
| **Pipeline state machine** | Guarded transitions from request to placement, with an audit trail |
| **Rate & margin engine** | `Decimal` money, cost vs bill, margin by placement, client and period |

---

## Architecture

Four layers, and one rule: **dependencies point inward.**

```
interfaces/       DRF views, serializers, URLs.  Speaks HTTP. Knows no business rules.
    ↓
application/      Use cases: "propose candidates for request 42". No HTTP, no SQL.
    ↓
domain/           Pure Python. Entities, rules, algorithms. Zero Django imports.
    ↑
infrastructure/   Django ORM, Redis, Celery. Implements interfaces declared in domain/.
```

`domain/` depends on nothing — which is why the matching engine can be tested in milliseconds
without a database, and why the framework is a replaceable detail.

---

## Stack

Python 3.13 · Django 5.2 LTS · Django REST Framework · PostgreSQL · Redis · Celery ·
pytest · Docker · GitHub Actions

---

## Running it locally

```bash
git clone https://github.com/Shakarneh/benchFlow.git
cd benchFlow
```

```bash
py -3.13 -m venv .venv
source .venv/Scripts/activate      # Windows (Git Bash)
# source .venv/bin/activate        # macOS / Linux
```

```bash
pip install -r requirements.txt
```

```bash
python manage.py runserver
```

Run the tests:

```bash
pytest
```

---

## Why this project exists

Two reasons, both deliberate. To learn backend engineering properly — architecture, algorithms and
testing, not framework tutorials. And because it models the actual business of
**Expert Choice CIS**, whose homepage promises a three-day average time to place a specialist.
This is the system behind that promise.

**Author:** Mohammed M.Y. Shakarneh
