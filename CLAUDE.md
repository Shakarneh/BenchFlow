# PROJECT BIBLE — **benchFlow**
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

### 🔴 Rule 4 — Teach, don't just build *(mode v2 — 30 Jul 2026)*
I must understand everything we ship — but understanding is proven by **explaining, not typing**.
Claude writes most of the code and explains it in plain language. I type only the core: business
rules and algorithm hearts — the ~20% I must defend in an interview. Before every commit I explain
back, in 2–3 sentences, what the code does and why. If I can't, we stop and go again.

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
a company publishing exactly where its operational difficulty lives. **benchFlow is the engine behind
that promise.**

- They understand its value instantly — it is their P&L.
- I have first-hand insight: I lived their trainee programme (27 students sorted into 6 teams).
- It is the grown-up successor to my internship project. Attendance *detected conflicts in a fixed
  timetable*. benchFlow *generates the timetable* under competing constraints, with money attached.
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
    The specific problem in benchFlow that this solves.
    What would go wrong if we did NOT use it.

WHERE IT LIVES IN BENCHFLOW
    The exact file/class/function it will appear in.

THE SIMPLEST POSSIBLE EXAMPLE
    5–10 lines. Not the real code. Just the idea, naked.

WHAT I'LL BE ABLE TO SAY IN AN INTERVIEW
    One or two sentences I could genuinely say out loud.

⏸  Do you understand this? Say yes and we implement it.
    Say no, or ask anything, and I explain it differently.
════════════════════════════════════════════════
```

> **Mode v2 (30 Jul 2026):** the default is now the **short card** — WHAT IT IS · WHY HERE · THE
> IDEA · the interview line, a line or two each. The full template above is reserved for ⭐⭐
> topics: the matching engine (Phase 7) and architecture (Phase 9).

### 2.2 The loop for every single feature

```
1. You explain WHAT we're building next and WHY          →  I approve
2. If a new concept is involved → Concept Card            →  I confirm I understand
3. You explain the design in plain language               →  I approve
4. Claude writes most of it; I type only the core logic (business rules, algorithm hearts)
5. Claude explains what was written; I explain it BACK in 2–3 sentences before any commit
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

## 4. THE DOMAIN — what benchFlow actually models

> **"Domain" here has nothing to do with website domain names.** In software, *the domain* is
> **the real-world business area the program is about** — its subject, its vocabulary, its rules.
> Our domain is *resourcing an IT outstaffing company*: specialists, skills, requests, placements,
> margin. A word belongs to the domain if a manager at Expert Choice would use it in a meeting
> without knowing any programming. So `domain/` is the folder holding the code that models
> **the business**, not the code that talks to the database or the web.

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

**How `application/` uses the database without depending on it.** `domain/` declares an *interface*
— "something, I don't care what, that can give me all specialists". `infrastructure/` writes the
real Django-ORM version of that. At startup we hand the real one to `application/`. So the arrow
runs `infrastructure → domain`, never `application → infrastructure`. In tests we hand it a fake
list instead, and the same code runs with no database at all.

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
- Install **pytest** here as a *tool* (one command, one example test) so Phase 1 can be tested at all.
  Phase 3 then teaches testing as a *discipline* — that is a different thing.
- Create the four layer folders (`domain/ application/ infrastructure/ interfaces/`) empty, now
- Agree conventions (naming, commit messages, branch names)
- **Deliverable:** an empty Django project that runs, on GitHub, with a README

### PHASE 1 — Object-Oriented Programming ⭐⭐ (the big one)
**⭐ Concepts:** classes & objects · **encapsulation · inheritance · polymorphism · abstraction** ·
`@property` · `@classmethod` / `@staticmethod` · abstract base classes · **composition vs inheritance** ·
dunder methods (`__str__`, `__eq__`, `__lt__`) · when OOP is the *wrong* tool ·
**`Decimal` for money** (mini-card, see below) · **dates & inclusive-vs-exclusive ranges**
- Build `Specialist`, `Skill`, `SkillLevel`, `Request` as **pure Python classes, zero Django**
- ⚠️ The first money field (`cost_rate`) appears *here*, not in Phase 12. So `Decimal` gets a short
  card the moment we type it — never `float` for money, not even temporarily. Phase 12 keeps the
  *engine* (margin, rounding, DB constraints, race conditions), which genuinely needs a database.
- **Deliverable:** `domain/` package, unit-tested with the pytest installed in Phase 0, no framework

### PHASE 2 — Clean code & SOLID
**⭐ Concepts:** SOLID (all five, one at a time) · DRY · KISS · separation of concerns · naming ·
small functions · code smells
- Refactor Phase 1 with each principle, seeing what improves and why
- **Deliverable:** the same behaviour, visibly better code

### PHASE 3 — Testing *(the discipline, not the tool — the tool arrived in Phase 0)*
**⭐ Concepts:** unit vs integration vs e2e · fixtures · factories · **TDD** · what coverage
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
- The four folders already exist from Phase 0 — this phase does **not** restructure them. It
  *formalises* the rule: define the interfaces (ports) explicitly, wire them up at startup, and add
  `import-linter` to CI so a forbidden import turns the build red. We deliberately break one import
  and watch it fail.
- **Deliverable:** machine-enforced layering + first ADRs

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
- **The Grand Walkthrough (mode v2):** we read the ENTIRE codebase together, file by file, and I
  explain each one back — the final proof of understanding
- Real README, architecture docs, the ADR set, diagrams — including a section on the AI-assisted,
  spec-driven workflow this project was built with
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
- [ ] I can explain what every file does and why, out loud — and the core logic line by line
- [ ] Tests exist and pass
- [ ] Lint, format and type checks are clean
- [ ] The concepts used are named and carded in this file
- [ ] Committed on a feature branch, merged via PR with green CI
- [ ] §9 below is updated

---

## 9. PROGRESS LOG

> Updated at the end of every session. Newest entry at the top.

### ▶ CONTINUE FROM HERE — read this first in a new conversation

**Deadline:** the project must be finished and understood by **13 Aug 2026** (15 days from 29 Jul).

**Where we are:** Phases 0–8 **done.** **612 tests passing** (500 of them randomised oracle
checks), and `domain/` still has **zero Django imports**. Phase 8 work is on
`feat/phase-8-design-patterns`. Local folder is still `C:\Users\Mohammed_PC\my_projects\bench`.

**The five patterns in use — full write-up in [`docs/patterns.md`](docs/patterns.md):**
| Pattern | Where | What it bought |
|---|---|---|
| **Strategy** | `domain/matcher.py` | swapping greedy → Hungarian changed zero calling code |
| **Repository** | `domain/repositories.py` + infra adapters | matcher runs on PostgreSQL without importing it |
| **Specification** | `domain/specifications.py` | rejections explain themselves in plain English |
| **State** | `domain/pipeline.py` | illegal transitions raise; append-only audit trail |
| **Observer** | `domain/events.py` | pipeline announces; SLA/audit/email subscribe |
| ~~Factory~~ | — | **rejected** — `@dataclass` + repository mappers already cover it |

**The three matchers — all behind the same `Matcher` ABC, so they are interchangeable:**
| Strategy | Complexity | Optimal? | Role |
|---|---|---|---|
| `GreedyMatcher` | O(n log n) | ❌ order-dependent | fast baseline, kept for comparison |
| `OptimalMatcher` | O(k^n) | ✅ | **test oracle only** — never in production paths |
| `HungarianMatcher` | O(n³) | ✅ | **the default** |

Measured (`python manage.py benchmark_matchers`): at 8×25 greedy left **1 request unfilled**
to save 47; Hungarian filled everything. At 15×60 and 30×150 both filled everything and
Hungarian was *cheaper*. Full write-up in [`docs/matching.md`](docs/matching.md).

**Stack now live:** PostgreSQL **17.10** (service `postgresql-x64-17`, db `benchflow`, port 5432) ·
`psycopg[binary]` · `python-dotenv`. Secrets are in `.env` (gitignored): `DJANGO_SECRET_KEY` and
five `POSTGRES_*` vars. `settings.py` contains only variable *names*, never values.

```
bench/
├── .venv/ · .env       (ignored)   ├── config/          settings.py · urls.py · wsgi.py
├── .gitignore · README.md          ├── domain/          skill · skill_level · specialist ·
├── CLAUDE.md · WORKFLOW.md         │                    request · matcher · repositories
├── requirements.txt                ├── application/     empty — Phase 9 fills this
├── manage.py · tests/  (5 files)   ├── infrastructure/  models · admin · repositories ·
                                    │                    migrations/ · management/commands/
                                    └── interfaces/      empty — Phase 10
```

**The port/adapter pair — how `domain/` uses a database without importing one:**
`domain/repositories.py` declares the abstract `SpecialistRepository` (the **port**).
`infrastructure/repositories.py` has `DjangoSpecialistRepository` (the **adapter**) plus
`specialist_to_domain()`, which is the border where everything Django-shaped stops.
Proved live: `GreedyMatcher` — unchanged since Phase 1 — matched against real PostgreSQL rows.

**Value object vs entity — the rule that decided `frozen=`:**
`Skill` · `SkillLevel` are **value objects** (same contents = same thing, no life cycle) → frozen.
`Specialist` · `Request` are **entities** (identity + life cycle, fields change) → mutable.
This same distinction decides which tables get an ID in Phase 4.

**The three matching rules now in code — this is the spine of the whole project:**
| Method | Question it answers | Operator |
|---|---|---|
| `SkillLevel.covers(required)` | does this one skill cover it? | `==` skill **and** `>=` level |
| `Specialist.covers(required)` | do **any** of my skills cover it? | `any()` |
| `Request.is_satisfied_by(spec)` | all skills, free in time, **and** within budget? | `all()` + date + rate |
| `GreedyMatcher.match(req, people)` | who do we propose? | filter → sort by cost → take headcount |

**Known debt:** no tests yet for `infrastructure/` (the repository is only proven by hand in the
shell) — add one with a fake repository in Phase 9. PEP 8 nits in domain files — ruff/black clean
them in Phase 16. `db.sqlite3` is a leftover from Phase 0 and can be deleted.

**Mohammed's level — important.** True beginner. Cannot yet write code unaided and does not
memorise methods or syntax. Long-term goal: Big Tech. His English is a real constraint — define
terms, offer simpler wording when something doesn't land. **Explain the WHY of every command at
the moment it's given. Full reasoning is welcome; option-surveys and padding are not.**

**Mode v2 (Decision 11) governs everything:** Claude writes most code and explains it; Mohammed
types only business rules and algorithm cores; the gate before every commit is him explaining the
code back in 2–3 sentences. Short concept cards by default (§2.1 note). Phase 21 ends with the
Grand Walkthrough of the whole codebase.

**Shell:** Mohammed uses **Git Bash**, not PowerShell. Give every command in bash syntax
(e.g. venv activation is `source .venv/Scripts/activate`, not `Activate.ps1`).

**Stack decided:** Python **3.13** + Django **5.2 LTS**. All 22 phases are being attempted — nothing
was cut (Decision 10). Pace is high: keep Concept Cards short, no detours.

**The immediate next step:** **Phase 9 — architecture.** The four folders already exist; this phase
*formalises* them. Fill `application/` with use cases (`propose_candidates(request_id)`) that
orchestrate repository + matcher + events, wire the real adapters at startup, add `import-linter`
to enforce the dependency rule, write the first ADRs, and deliberately break one import to watch
CI go red. Also clears the standing debt: **no tests for `infrastructure/` yet** — add one using a
fake repository, which is exactly what the ports make possible.
**Useful commands:** `python manage.py seed_demo` · `python manage.py benchmark_matchers` · `/admin/`.

✅ **Both pieces of wiring debt are cleared.** `SkillGraph.expand()` runs inside `Matcher.resolved()`
on a *copy* of each specialist; `Specialist.is_free_for()` is rule 3 of four in
`Request.is_satisfied_by()`. Both are pinned by `tests/test_matcher_wiring.py`.
**Checkpoint:** Phase 7 matcher done by ~6 Aug, or the scope conversation returns (deadline 13 Aug).

| Date | Phase | What was done | Concepts learned | Commits/PRs |
|---|---|---|---|---|
| 3 Aug 2026 | 8 | **Phase 8 done.** Two patterns were already in the code (Strategy, Repository) — named them rather than rebuilt them. Then three real builds: **Specification** (`Request.is_satisfied_by` refactored from one boolean into composable rule objects with `&` `\|` `~`, and `reasons_against()` that names every failure), **State** (`Pipeline` with an `ALLOWED` transition table, Mohammed typed the guard; frozen append-only history; `time_to_fill()` = the «3 дня» promise), **Observer** (`EventBus`, frozen past-tense events, pipeline announces without knowing who listens). Factory considered and **rejected** in writing. `docs/patterns.md` | **Specification** & why composable rules beat a compound boolean (explainability as a feature) · dunder operator overloading (`__and__`/`__or__`/`__invert__`) · **State machines** — rules as a data table, not branching code; illegal states unrepresentable · audit trails & frozen history · **Observer / domain events** · past-tense event naming · Open/Closed at system level · **when a pattern is overkill** — and writing the rejection down | 4 commits |
| 2 Aug 2026 | 7 | **Phase 7 done — the centrepiece.** Cleared both pieces of wiring debt (skill graph + calendar now run inside real matching, pinned by tests). Added multi-request `assign()` so requests compete for one pool. Then three matchers: `GreedyMatcher`, exhaustive `OptimalMatcher` (Mohammed typed `is_better` — the objective function), and `HungarianMatcher` (Mohammed typed `cell_cost` — the penalty encoding). Verified by **oracle testing**: 200 random worlds where Hungarian must match the exhaustive answer exactly, plus 300 more asserting invariants. Benchmarked across 7 world sizes; wrote up `docs/matching.md`. **579 tests** | **the assignment problem** · bipartite graphs · **locally vs globally optimal** (greedy strands a client to save 47) · order-dependence as a correctness smell · **objective functions** as business decisions · **the Hungarian algorithm** & potentials as generalised row/column reduction · **penalty encoding** to turn "fill first, then save" into pure arithmetic · integer cents for exactness · padding to square · **oracle testing** — how to trust an algorithm you did not derive · seeded randomised testing · O(n log n) vs O(k^n) vs O(n³) measured, not claimed | 4 commits |
| 2 Aug 2026 | 6 | **Phase 6 done.** `domain/allocation.py` — `Allocation` (frozen, inclusive dates) + `Calendar`. `peak_load()` is a **sweep-line** Mohammed typed: each booking becomes `+fraction` at the start and `-fraction` the day *after* the end, sort, one pass tracking a running max. `Specialist` gained `allocations` + `is_free_for()`, so part-time people can take part-time work. DB: `AllocationModel` with two `CheckConstraint`s (`ends_on >= starts_on`, `0 < fraction <= 1`) enforced by PostgreSQL itself; admin shows a live **peak load** column — Carol was pushed to **125% OVER** by hand to watch it fire. 18 new tests | **intervals** · **inclusive vs exclusive ends** (the `+1 day` release, pinned by boundary tests one day apart) · **sweep-line** and why it beats pairwise O(n²) · **O(n log n)** — the sort dominates · **fractional capacity** · tuple sort order so a release precedes an acquire on the same day · DB `CheckConstraint` · `on_delete=SET_NULL` to preserve history | *(this batch)* |
| 1 Aug 2026 | 5 | **Phase 5 done.** `domain/skill_graph.py` — `SkillGraph.implied_by()` is a **BFS transitive closure** (Mohammed typed the loop), `expand()` adds implied skills at the same level and keeps the highest on conflict. 9 tests including a deliberate **cycle test** (wrong guard = infinite hang, not a failure). DB side: `implies` self-M2M on `SkillModel` with `symmetrical=False`, `DjangoSkillGraphRepository` loads the whole DAG in one query, `seed_demo` seeds 7 implications. Proved live: Alice knows only Django, and covers *Programming* two hops away | **graphs** · **DAGs** & why cycles are fatal · **BFS** and why `popleft()` makes it breadth-first · **transitive closure** · the visited-set as cycle guard · **Big-O: O(V+E)** · `deque` vs `list.pop(0)` (O(1) vs O(n)) · self-referencing many-to-many · loading a whole graph vs walking it hop-by-hop | 2 commits |
| 1 Aug 2026 | 4 | **Phase 4 done.** PostgreSQL 17 installed; secrets moved to `.env` via `python-dotenv` (`SECRET_KEY` debt from Phase 0 cleared). 5 ORM models in `infrastructure/` with FKs, unique constraints, indexes and two join tables; migrations applied; Django admin with inlines; `seed_demo` management command (6 specialists, 7 skills, 3 requests). Then the centrepiece: the **Repository** — port in `domain/`, Django adapter in `infrastructure/` — and `GreedyMatcher` matched real PostgreSQL data **without a single change** | **relational modelling** · PK/FK · `on_delete` CASCADE vs PROTECT · join tables (when M2M needs extra data) · unique constraints & indexes · **migrations** · **transactions & ACID** (`@transaction.atomic`) · **N+1 query problem** & `prefetch_related` · **Repository pattern** · **ports & adapters** · **Dependency Inversion** — the 5th SOLID principle, finally demonstrable · env vars for secrets | 2 commits |
| 1 Aug 2026 | 3 | **Phase 3 done.** Extracted `make_specialist`/`make_request` into `tests/conftest.py` as **factory fixtures** (frozen value objects stayed plain constants). Then a full **TDD cycle** on a real gap: `max_bill_rate` was being ignored — wrote the failing test first (incl. an exactly-on-budget boundary test), watched it go red for the right reason, then added the rule. Added `pytest-cov`: **100% of `domain/`** | **fixtures & `conftest.py`** (auto-discovery, injection by parameter name) · **factory fixture** pattern · why immutable test data needs no fixture · **TDD red→green→refactor** · **boundary testing** (`<=` vs `<`) · **what coverage really means** — seen live: `request.py` showed 100% coverage *while a test was failing*, because coverage can't measure code that was never written | 3 commits |
| 1 Aug 2026 | 1→2 | Phase 1 closed: `Matcher` ABC + `GreedyMatcher` (filter → sort → take), PR merged to `develop` then `main`. **Phase 2 done**: SOLID mapped onto the existing code (4 of 5 already satisfied — the ABC did it), then the one real violation, DRY, fixed by converting all four entities to `@dataclass` — ~40 lines of hand-written dunders deleted, 28 tests still green | **abstract base classes** · **inheritance & polymorphism** · list comprehensions · `lambda` · slicing · **SOLID** (all five, against his own code) · **DRY** · `@dataclass` & type hints · **value object vs entity** (what `frozen=True` really means) · refactoring = behaviour identical, code better | 2 commits · 2 PRs |
| 30 Jul 2026 | 1 | **Mode v2 adopted** after the AI-era strategy talk (three speeches analysed; verdict: plan content right, delivery too slow). Built `Level` · `SkillLevel.covers()` · `Specialist.covers()` · `Request.is_satisfied_by()` — Mohammed typed all three matching rules, Claude wrote the rest and the 23 tests. First real debugging session: three hand-typed bugs cornered by tests | enums & IntEnum · why enums start at 1 (falsy zero) · **composition vs inheritance** (has-a vs is-a) · **`Decimal` vs float for money** (and why to build it from a string) · `any()` vs `all()` · short-circuit evaluation · tests as the trust mechanism for code you didn't write | 3 commits |
| 29 Jul 2026 | 0→1 | Phase 0 closed: README · smoke test · `develop` branch · Git Flow kept. Phase 1 opened on `feat/phase-1-domain-entities`: `Skill` with `__repr__`/`__eq__`/`__hash__` + 4 tests, pushed. Smoke test later removed as superseded | classes & objects · `__init__`/`self` · dunder methods · value vs identity equality · the eq⇒hash invariant · `NotImplemented` vs `NotImplementedError` · REPL workflow · branching model · `git rm` | 6 commits |
| 29 Jul 2026 | 0 | Installed Python 3.13.14 alongside 3.14. Created `.venv` + `.gitignore`. Installed Django 5.2.16 + pytest, pinned in `requirements.txt`. `startproject config .` (dot layout, `config/` naming). Created the four layer folders as empty packages. `runserver` works | **virtual environments** (and that `.venv` never travels — `requirements.txt` does) · dependency pinning · semantic versioning · **Django** & batteries-included · `__init__.py` makes a folder a package · why `config/` beats a nested same-name folder | 4 commits |
| 29 Jul 2026 | 0 | Read both planning docs. Renamed project Bench → benchFlow. Fixed 7 contradictions between the two files (see Decisions 6–8). Defined "domain" in §4 and §10. Corrected the dependency-rule diagram in `WORKFLOW.md` §4 | what *domain* means in software · `.gitignore` is for secrets and regenerable junk — **not** documentation | 2 commits |

### Decisions made
| # | Decision | Reasoning | Date |
|---|---|---|---|
| 1 | Project is **benchFlow**, a resourcing platform | Mirrors Expert Choice's actual business model | Jul 2026 |
| 2 | **Django** (not FastAPI) | On their published stack; batteries-included teaches more architecture | Jul 2026 |
| 3 | **PostgreSQL** (not SQLite) | Real constraints/transactions; step up from the internship | Jul 2026 |
| 4 | Domain layer in **pure Python**, no Django | Teaches real OOP; keeps rules testable and portable | Jul 2026 |
| 5 | Backend fully before frontend | My explicit instruction | Jul 2026 |
| 6 | Repo is **`Shakarneh/benchFlow`**; the Bible is **`CLAUDE.md`** (was `PROJECT_BIBLE.md`) | Project named after planning docs were written | 29 Jul 2026 |
| 7 | The four layer folders exist from **Phase 0**; Phase 9 *enforces* rather than restructures | Phase 1 and Phase 9 contradicted each other. No time for a big refactor | 29 Jul 2026 |
| 8 | pytest installed in Phase 0; `Decimal` introduced in Phase 1 | Phase 1 demanded tests before Phase 3 gave us pytest; money fields appear in Phase 1, not Phase 12 | 29 Jul 2026 |
| 9 | **Python 3.13 + Django 5.2 LTS** | Whole stack (DRF, Celery, psycopg, mypy) is proven on it. Python 3.14 was already installed but the ecosystem lags new releases | 29 Jul 2026 |
| 10 | **No phases cut** — all 22 inside 15 days | Mohammed's explicit decision after Claude advised cutting. Pace increases instead: shorter cards, no detours | 29 Jul 2026 |
| 11 | **Mode v2** — Claude writes most code; Mohammed types core logic only; explain-back gate before every commit; short cards; Phase 21 = Grand Walkthrough | Typing every line couldn't reach 13 Aug — and reading/verifying is the durable AI-era skill. The explain-back gate is the anti-vibe-coding mechanism | 30 Jul 2026 |

> ⚠️ Decision 7 is Claude's call, made to resolve a contradiction. Reversible — say so and we flip it.

### Open questions
- Public or private repo during development

---

## 10. GLOSSARY

Every term gets defined the first time it appears. Add to this as we go.

| Term | Meaning |
|---|---|
| **Domain** *(software)* | The real-world business area a program is about — its subject and its rules. **Not** a website domain name. Ours is IT resourcing. `domain/` holds the code that models the business |
| **Entity** | One "thing" in the domain, modelled as a class — `Specialist`, `Request` |
| **Interface / port** | A promise about *what* something can do, with no *how*. `domain/` declares them; `infrastructure/` fulfils them |
| **The bench** | Employed engineers not currently assigned to a client — idle capacity that costs money. *(This is the industry term — it stays, even though the project is now benchFlow)* |
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
