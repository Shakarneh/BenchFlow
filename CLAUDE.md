# PROJECT BIBLE — **Bench**
### A resourcing & allocation platform for IT service companies
> **Owner:** Mohammed M.Y. Shakarneh · **Started:** July 2026 · **Stack:** Python · Django
> **Purpose:** become a genuinely strong backend engineer, and earn a job at **Expert Choice CIS**.
>
> **This file is the source of truth.** Read it fully at the start of every session.
> It doubles as the repo's `CLAUDE.md` — keep it updated as the project grows.

---

## 0. THE RULES — read these first, they override everything

These are not suggestions. They are the terms of how we work together.

### 🔴 Rule 1 — Never do anything without my permission
Do not create files, write code, install packages, or change anything until I have said yes.
Propose → wait → I approve → then act. Every time. No exceptions.

### 🔴 Rule 2 — Explain before every step
Before *any* step, state plainly:
1. **What** you are about to do
2. **Why** you are doing it
3. **What it will change** in the project
Then stop and wait for my go-ahead.

### 🔴 Rule 3 — I run every Git command myself
Never execute `git add`, `git commit`, `git push`, `git checkout`, `git merge`, or any other Git
command. **Give me the commands and I will run them.** One command per code block.
Stage files **by name** — never `git add .`.

### 🔴 Rule 4 — Teach, don't just build
I want to understand every line. Assume I know nothing. When we hit a concept, stop and teach it
using the Concept Card in §2 before we write any code. I type the core logic myself.

### 🔴 Rule 5 — Simplest possible version first
Build every concept in its simplest, clearest form. No cleverness. No premature optimisation.
Clarity beats elegance. We can always make it sophisticated later — but only once I understand it.

### 🔴 Rule 6 — Keep this file current
At the end of every session, update §9 (Progress Log) and anything else that changed:
decisions made, conventions agreed, what's done, what's next.

---

## 1. WHY THIS PROJECT EXISTS

### 1.1 The target: Expert Choice CIS

I did my corporate-training practice there and built the back end of a student attendance system
(FastAPI + SQLAlchemy + SQLite). I want to be hired there. This project is built to make that case.

**What the company actually does** (researched from `expchoice.tech`, July 2026):

| Fact | Detail |
|---|---|
| Business model | **IT outstaffing + ВЦР** (dedicated development centres) — they supply engineers to clients |
| Age / size | 15+ years · 100+ experts · 63 staff (2024) · revenue 180.9M ₽ |
| Clients | БКС Мир Инвестиций, Альфа Капитал, РосЕвроБанк, МКБ — regulated finance. Also retail, АПК, medicine, manufacturing |
| Service lines | IT audit & consulting · AI implementation · 1C automation · infrastructure & DevOps |
| Compliance | Минцифры accreditation №7659 · ФЗ-152 (personal data) · ГОСТ 57580.1 (bank information security) |
| Partners | 1С Франчайзи · Сбер DTaaS · МТС ИИ · Astra · МойОфис · Kaiten (platinum) |
| Headline promise | **«3 дня — среднее время подключения специалиста»** |
| Their declared stack | Backend: `Java, Go, Kotlin, Python, C#, Node.js, 1C` — frameworks `Spring Boot, **Django**, FastAPI, ASP.NET Core` |
| 2024–2026 direction | Applied products for manufacturing · импортозамещение · AI in real business scenarios |

**Two facts that shaped this decision:**
1. **Django is explicitly on their stack.** No need to justify the framework choice.
2. **Their trainee programme is a recruitment funnel** — their own timeline lists *«корпоративный
   университет и базовые кафедры в вузах ЦФО»*. I'm already inside it.

### 1.2 Why *this* project and not something else

Their homepage advertises a five-step staffing pipeline and a three-day placement promise. That is
a company publishing exactly where its operational difficulty lives. **Bench is the engine behind
that promise.**

- They understand its value instantly — it is their P&L.
- I have first-hand insight: I lived their trainee programme (27 students sorted into 6 teams).
- It is the grown-up successor to my internship project. Attendance *detected conflicts in a fixed
  timetable*. Bench *generates the timetable* under competing constraints, with money attached.
- The core is real computer science, not CRUD — defensible in an interview and in an academic setting.

### 1.3 Known trade-off, accepted knowingly
This is an internal B2B tool. It will not attract public users the way a consumer app would.
I am trading reach for **depth and direct relevance to one employer**. That is deliberate.
The large global project lives in a separate conversation and a separate repository.

---

## 2. THE TEACHING CONTRACT

### 2.1 The Concept Card — used every single time we meet a new concept

Whenever we begin a new topic, you **stop** and post this card *before writing any code*:

```
════════════════════════════════════════════════
🎓  NEW CONCEPT: <name>
════════════════════════════════════════════════

WHAT IT IS
    Plain language. No jargon without defining it.

HOW I RECOGNISE IT
    "You know you are doing <concept> when you see …"
    The tell-tale signs, so I can spot it in any codebase.

WHY WE ARE USING IT HERE
    The specific problem in Bench that this solves.
    What would go wrong if we did NOT use it.

WHERE IT LIVES IN BENCH
    The exact file/class/function it will appear in.

THE SIMPLEST POSSIBLE EXAMPLE
    5–10 lines. Not the real code. Just the idea, naked.

WHAT I'LL BE ABLE TO SAY IN AN INTERVIEW
    One or two sentences I could genuinely say out loud.

⏸  Do you understand this? Say yes and we implement it.
    Say no, or ask anything, and I explain it differently.
════════════════════════════════════════════════
```

### 2.2 The loop for every single feature

```
1. You explain WHAT we're building next and WHY          →  I approve
2. If a new concept is involved → Concept Card            →  I confirm I understand
3. You explain the design in plain language               →  I approve
4. You scaffold; I type the core logic myself
5. You explain what we just wrote, line by line
6. You give me the git commands                           →  I run them
7. You update this file
```

**I never commit code I do not understand. If I say "I don't get it", we stop and go again.**

### 2.3 Concept announcements

When a phase introduces a big topic, announce it loudly:

> ### 🚩 WE ARE NOW STARTING: **Object-Oriented Programming**
> For the next N steps everything we write will be OOP. Here is how to recognise it…

Never slip a concept in silently. If we use a design pattern, name it and card it.

---

## 3. THE TECHNOLOGY STACK — what each thing is and why we use it

> **Rule: nothing enters this stack until you have explained it with a Concept Card and I've agreed.**

| Technology | What it is (plain language) | Why we use it here |
|---|---|---|
| **Python** | The programming language. | The language I'm building my career on; Expert Choice lists it under both Backend and Analytics. |
| **Django** | A "batteries-included" web framework — routing, ORM, admin, auth, migrations in one box. | Explicitly on their stack. Its structure teaches architecture by example, and the admin gives us a free UI while we build the backend. |
| **Django REST Framework (DRF)** | A Django add-on for building JSON APIs. | Turns our domain into an API other programs can call. Teaches serialization, versioning, pagination. |
| **PostgreSQL** | A serious relational database. | Real constraints, transactions and indexes — the internship used SQLite, this is the professional step up. On their stack too. |
| **Redis** | An in-memory key-value store; extremely fast, not durable. | Caching expensive match results, and acting as the message broker for Celery. |
| **Celery** | A background task queue — runs slow work outside the request. | Matching thousands of specialists takes seconds; users can't wait. Teaches async thinking. |
| **pytest** | A testing framework. | Because untested code is a guess. Our pure domain logic is a joy to unit-test. |
| **Docker** | Packages the app + its dependencies into a portable container. | "Works on my machine" ends here. Expert Choice lists Docker/Kubernetes. Makes the project runnable by anyone in one command. |
| **docker-compose** | Runs several containers together (app + Postgres + Redis). | One command brings the whole system up. |
| **GitHub Actions** | Runs our tests automatically on every push/PR. | This is CI. It proves engineering discipline at a glance. |
| **ruff / black** | Linter and auto-formatter. | Consistent style, caught mistakes, zero arguments about formatting. |
| **mypy** | Static type checker for Python. | Catches whole classes of bug before running. Teaches thinking in types. |
| **OpenAPI / Swagger** | Auto-generated interactive API documentation. | The single most impressive screenshot from my internship — we do it properly this time. |
| **Git / GitHub** | Version control and collaboration. | Feature branches → PR → review → merge. The workflow real teams use. |

---

## 4. THE DOMAIN — what Bench actually models

### 4.1 The story in one paragraph
An IT service company employs **specialists**. Clients send **requests** ("we need two senior Python
engineers for six months, starting in three weeks, at most X per hour"). The company must find the
best specialists for each request, without over-committing anyone, as fast as possible — their promise
is three days. Some specialists are on the **bench** (unassigned, costing money). The system finds
the best assignment, tracks the pipeline from request to placement, and reports on utilisation and margin.

### 4.2 The core entities

| Entity | What it represents | Interesting because |
|---|---|---|
| `Specialist` | An engineer we can place | Has skills at levels, a cost rate, availability |
| `Skill` | A capability, e.g. "Django" | Skills form a **graph** — Django implies Python |
| `SkillLevel` | A specialist's proficiency in one skill | Junior/Middle/Senior — ordered, comparable |
| `Client` | A company we supply to | Has contracts, rates, preferences |
| `Request` | An open demand from a client | Required skills, dates, budget, headcount |
| `Candidate` | A proposed specialist for a request | Moves through the pipeline |
| `Placement` | A confirmed assignment | Has a start, an end, a **fraction** of capacity |
| `Engagement` | The commercial wrapper | Cost rate, bill rate, margin |
| `Allocation` | Time booked on a specialist's calendar | Overlapping intervals — the hard part |

### 4.3 The seven hard problems (this is why it isn't CRUD)

1. **The matching engine** — N specialists × M requests, each with skill/level/date/rate constraints.
   Find the optimal assignment. This is the **assignment problem**.
2. **Fractional allocation** — someone can be 50% on project A and 50% on B. Overlapping intervals
   with capacity fractions; detect over-allocation.
3. **Skill graph** — "Django ⇒ Python" implications resolved before matching.
4. **Bench forecasting** — who frees up when; projected utilisation.
5. **Pipeline state machine** — guarded transitions with a full audit trail.
6. **SLA engine** — time-to-fill against the three-day promise; breach alerts.
7. **Rate & margin engine** — `Decimal` money, cost vs bill, margin by placement/client/period.

---

## 5. ARCHITECTURE

### 5.1 The shape we're building toward

```
interfaces/     ← Django views, DRF serializers, URLs.  Talks HTTP. Knows nothing about rules.
    ↓
application/    ← Use cases: "propose candidates for request X". Orchestrates. No HTTP, no SQL.
    ↓
domain/         ← Pure Python. The rules, the algorithms, the entities. NO Django imports at all.
    ↑
infrastructure/ ← Django ORM models, Redis, Celery, email. The outside world.
```

**The dependency rule:** arrows point *inward*. `domain/` depends on nothing. That's what makes it
testable in milliseconds without a database — and it's the single biggest idea in this project.

### 5.2 Why we build the domain in plain Python first
We will write `Specialist`, `Skill` and the matcher as **ordinary Python classes with no Django
anywhere**, and only later connect them to the database. Two reasons:
- You learn OOP properly, not "Django model syntax".
- The rules stay testable and portable. This is what "framework-independent" means.

---

## 6. THE STEP-BY-STEP PLAN

> Each phase names the concepts it teaches. **Every ⭐ gets a Concept Card before any code.**
> Phases are worked in order. Backend is finished before any frontend work begins.

### PHASE 0 — Foundations & setup
**⭐ Concepts:** virtual environments · dependency management · project structure · `.gitignore` · Git branching model · README
- Create the repo, virtualenv, install Django, first `runserver`
- Agree conventions (naming, commit messages, branch names)
- **Deliverable:** an empty Django project that runs, on GitHub, with a README

### PHASE 1 — Object-Oriented Programming ⭐⭐ (the big one)
**⭐ Concepts:** classes & objects · **encapsulation · inheritance · polymorphism · abstraction** ·
`@property` · `@classmethod` / `@staticmethod` · abstract base classes · **composition vs inheritance** ·
dunder methods (`__str__`, `__eq__`, `__lt__`) · when OOP is the *wrong* tool
- Build `Specialist`, `Skill`, `SkillLevel`, `Request` as **pure Python classes, zero Django**
- **Deliverable:** `domain/` package, fully unit-tested, no framework

### PHASE 2 — Clean code & SOLID
**⭐ Concepts:** SOLID (all five, one at a time) · DRY · KISS · separation of concerns · naming ·
small functions · code smells
- Refactor Phase 1 with each principle, seeing what improves and why
- **Deliverable:** the same behaviour, visibly better code

### PHASE 3 — Testing
**⭐ Concepts:** unit vs integration vs e2e · pytest · fixtures · factories · **TDD** · what coverage
really means · mocking (and why to avoid it)
- Write tests *first* for the next domain rule
- **Deliverable:** green suite, honest coverage report

### PHASE 4 — Databases & persistence
**⭐ Concepts:** relational modelling · normalisation · PK/FK · indexes · **transactions & ACID** ·
ORM trade-offs · migrations
- Django models mirroring the domain; migrations; Django admin as a free UI
- **Deliverable:** PostgreSQL schema with seeded demo data

### PHASE 5 — Data structures: the skill graph
**⭐ Concepts:** graphs · **DAGs** · BFS/DFS · transitive closure · adjacency list vs matrix ·
hash maps · **Big-O notation**
- Skill implication ("Django ⇒ Python") resolved via traversal
- **Deliverable:** skill-resolution service + complexity analysis in the docs

### PHASE 6 — Algorithms I: intervals & availability
**⭐ Concepts:** intervals · sorting · **sweep-line** · interval trees · priority queues (heaps) ·
fractional capacity
- The allocation calendar; over-allocation detection
- **Deliverable:** availability engine + tests covering the nasty overlap cases

### PHASE 7 — Algorithms II: the matching engine ⭐⭐ (the centrepiece)
**⭐ Concepts:** the **assignment problem** · bipartite graphs · greedy vs optimal · the
**Hungarian algorithm** · min-cost max-flow · scoring/objective functions · heuristics
- Naive greedy matcher first (simple, understandable), then the optimal one — and *measure the difference*
- **Deliverable:** matching service, benchmarked, with the trade-offs written up

### PHASE 8 — Design patterns
**⭐ Concepts:** **Strategy** (swappable matchers) · **Specification** (composable requirement rules) ·
**State** (the pipeline) · **Repository** (storage behind an interface) · **Observer / domain events** ·
**Factory** · and *when patterns are overkill*
- Each pattern gets its own card, its own commit, its own before/after
- **Deliverable:** pipeline state machine + pluggable strategies

### PHASE 9 — Software architecture
**⭐ Concepts:** layered architecture · **hexagonal / ports & adapters** · dependency inversion ·
the dependency rule · **ADRs** (architecture decision records)
- Restructure into `domain / application / infrastructure / interfaces`
- **Deliverable:** enforced layering + first ADRs

### PHASE 10 — Web & APIs
**⭐ Concepts:** HTTP verbs & status codes · **REST** · the request lifecycle · serialization ·
versioning · pagination · filtering · idempotency · OpenAPI
- DRF endpoints over the application layer
- **Deliverable:** documented API with interactive Swagger

### PHASE 11 — Authentication & authorization
**⭐ Concepts:** **authN vs authZ** · password hashing (bcrypt/argon2) · **sessions vs JWT** ·
token refresh · **RBAC** · object-level permissions
- Roles: admin · account manager · recruiter · specialist
- **Deliverable:** secured API where each role sees only what it should

### PHASE 12 — Money & correctness
**⭐ Concepts:** **`Decimal` vs float** · currency · rounding · invariants · database constraints ·
transaction isolation · race conditions · `select_for_update`
- The rate & margin engine
- **Deliverable:** financial calculations that are provably correct

### PHASE 13 — Caching & async
**⭐ Concepts:** why caching · cache **invalidation** · TTL · Redis data types · task queues ·
Celery workers & beat · idempotent tasks · sync vs async
- Cache match results; recompute forecasts in the background; SLA breach alerts
- **Deliverable:** Celery + Redis running under compose

### PHASE 14 — Errors, logging & debugging
**⭐ Concepts:** exception strategy · custom exception hierarchies · fail fast · **structured logging** ·
log levels · reading stack traces · using a real debugger
- **Deliverable:** consistent error handling and useful logs

### PHASE 15 — Security fundamentals
**⭐ Concepts:** **OWASP Top 10** · SQL injection · XSS/CSRF · secrets management · env vars ·
input validation · **personal-data handling** (their ФЗ-152 world)
- **Deliverable:** a written security review of our own code

### PHASE 16 — Tooling & typing
**⭐ Concepts:** linters · formatters · **static typing with mypy** · pre-commit hooks · dependency pinning
- **Deliverable:** clean `ruff`, `black`, `mypy` runs

### PHASE 17 — Docker
**⭐ Concepts:** containers vs VMs · images vs containers · Dockerfile · layers & caching ·
**docker-compose** · volumes · networks · multi-stage builds
- **Deliverable:** `docker compose up` brings up app + Postgres + Redis + worker

### PHASE 18 — CI/CD
**⭐ Concepts:** what CI actually is · pipelines · **GitHub Actions** · matrix builds · quality gates · CD
- **Deliverable:** every PR automatically runs tests, lint and type checks

### PHASE 19 — Deployment
**⭐ Concepts:** environments · **12-factor** config · migrations in production · zero-downtime ·
health checks · monitoring
- **Deliverable:** a live, public demo instance

### PHASE 20 — Frontend *(only now)*
**⭐ Concepts:** consuming a REST API · auth on the client · state · rendering the schedule
- **Deliverable:** a UI good enough to demo the matcher visually

### PHASE 21 — Documentation & showcase
- Real README, architecture docs, the ADR set, diagrams
- LinkedIn post · portfolio entry on `mohammedshakarneh.com` · interview talking points
- **Deliverable:** a project I can defend in a room

---

## 7. GIT WORKFLOW

**I run every command. You only ever provide them.**

```
main            ← always working, always deployable
 └── develop    ← integration branch
      └── feat/<phase>-<thing>   ← one branch per change
```

Cycle: branch → work → **I** commit → **I** push → PR → CI green → merge.

**Commit rules:**
- One commit per logical change, however small
- Stage **by name**: `git add domain/specialist.py` — never `git add .`
- Message: imperative mood, explains *why* when it isn't obvious
- Never bundle unrelated edits

**Conventions:** branches `feat/`, `fix/`, `docs/`, `refactor/`, `test/`, `chore/`

---

## 8. DEFINITION OF DONE

A phase is done when **all** of these are true:
- [ ] I can explain every line out loud, without notes
- [ ] Tests exist and pass
- [ ] Lint, format and type checks are clean
- [ ] The concepts used are named and carded in this file
- [ ] Committed on a feature branch, merged via PR with green CI
- [ ] §9 below is updated

---

## 9. PROGRESS LOG

> Updated at the end of every session. Newest entry at the top.

| Date | Phase | What was done | Concepts learned | Commits/PRs |
|---|---|---|---|---|
| — | 0 | *Not started* | — | — |

### Decisions made
| # | Decision | Reasoning | Date |
|---|---|---|---|
| 1 | Project is **Bench**, a resourcing platform | Mirrors Expert Choice's actual business model | Jul 2026 |
| 2 | **Django** (not FastAPI) | On their published stack; batteries-included teaches more architecture | Jul 2026 |
| 3 | **PostgreSQL** (not SQLite) | Real constraints/transactions; step up from the internship | Jul 2026 |
| 4 | Domain layer in **pure Python**, no Django | Teaches real OOP; keeps rules testable and portable | Jul 2026 |
| 5 | Backend fully before frontend | My explicit instruction | Jul 2026 |

### Open questions
- Final repository name (`bench` / `bench-platform` / other)
- Public or private repo during development

---

## 10. GLOSSARY

Every term gets defined the first time it appears. Add to this as we go.

| Term | Meaning |
|---|---|
| **The bench** | Employed engineers not currently assigned to a client — idle capacity that costs money |
| **Outstaffing** | Renting your engineers to work inside a client's team |
| **ВЦР** | Выделенный центр разработки — a dedicated development centre for one client |
| **Utilisation** | The share of a specialist's time that is billable |
| **Time-to-fill** | How long from a client's request to a specialist starting |
| **Margin** | Bill rate minus cost rate — the company's profit on a placement |
| **Assignment problem** | The classic optimisation problem of matching N workers to M jobs at minimum cost |
| **DAG** | Directed acyclic graph — a graph with direction and no cycles |
| **ORM** | Object-Relational Mapper — maps database rows to objects |
| **CI/CD** | Continuous Integration / Delivery — automated testing and shipping |
| **ADR** | Architecture Decision Record — a short note recording *why* a decision was made |

---

## 11. WHAT SUCCESS LOOKS LIKE

By the end I should be able to:
1. Explain **every** line of this codebase out loud
2. Whiteboard the architecture and defend each layer
3. Explain the assignment problem and why I chose my algorithm
4. Name each design pattern used, and where, and why
5. Demo the system live from a single `docker compose up`
6. Say honestly: *"I understand how professional backend software is built — here's proof"*

**And then send that message to Expert Choice CIS.**
