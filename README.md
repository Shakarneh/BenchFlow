<div align="center">

# benchFlow

**A resourcing and allocation platform for IT service companies.**

*Who do we place on which client request — optimally, without over-committing anyone?*

[![CI](https://github.com/Shakarneh/BenchFlow/actions/workflows/ci.yml/badge.svg)](https://github.com/Shakarneh/BenchFlow/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.13-1a1815)
![Django](https://img.shields.io/badge/Django-5.2%20LTS-1a1815)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-1a1815)
![Tests](https://img.shields.io/badge/tests-649%20passing-4c6a4e)

**🌍 [benchflow-qfzq.onrender.com](https://benchflow-qfzq.onrender.com)** ·
[API docs](https://benchflow-qfzq.onrender.com/api/docs/) ·
[Admin](https://benchflow-qfzq.onrender.com/admin/)

<sub>Free hosting tier — the first request takes ~50s while the instance wakes up.</sub>

</div>

---

## The problem

An IT outstaffing company employs engineers. Clients send requests — *"two senior Python
developers for six months, starting in three weeks, at most €70/hour."* Someone must decide who
goes where, without over-committing anyone, fast. Engineers who aren't assigned sit on **the
bench**, costing money every day they're idle.

Doing this by hand is a spreadsheet and a good memory. Doing it correctly is an optimisation
problem: **N specialists × M requests**, each with skill, seniority, date and rate constraints,
where filling one request well may strand another.

benchFlow is the engine behind that decision. At its centre is the **assignment problem**, solved
with the Hungarian algorithm — not a set of CRUD forms.

---

## What makes it hard

| Problem | Why it isn't trivial |
|---|---|
| **Matching engine** | N × M under skill, level, date and rate constraints — the assignment problem |
| **Fractional allocation** | Someone can be 50% on project A and 50% on B. Overlapping intervals with capacity |
| **Skill graph** | "Django ⇒ Python" — implications resolved by graph traversal *before* matching |
| **Pipeline state machine** | Guarded transitions from request to placement, with an append-only audit trail |
| **Rate & margin engine** | `Decimal` money, cost vs bill, rounding that finance agrees with |
| **Concurrency** | Two managers must not book the same person into the same week |

---

## The matching engine

Three interchangeable strategies behind one `Matcher` interface:

| Strategy | Complexity | Optimal? | Role |
|---|---|---|---|
| `GreedyMatcher` | O(n log n) | ❌ order-dependent | Fast baseline, kept for comparison |
| `OptimalMatcher` | O(k<sup>n</sup>) | ✅ | Brute force — **test oracle only** |
| `HungarianMatcher` | O(n³) | ✅ | **The default** |

Measured with `python manage.py benchmark_matchers`:

| requests × people | matcher | unfilled | total cost | ms |
|---|---|---|---|---|
| **8 × 25** | greedy | **1** | 605.00 | 0.76 |
| | hungarian | **0** | 652.00 | 1.34 |
| 15 × 60 | greedy | 0 | 917.00 | 3.80 |
| | hungarian | 0 | **904.00** | 11.57 |
| 30 × 150 | greedy | 0 | 2097.00 | 19.43 |
| | hungarian | 0 | **2071.00** | 160.14 |

**Read the 8 × 25 row.** Greedy saved 47 in cost and left a client entirely unstaffed. That is a
locally optimal choice that is globally wrong, and it is exactly the trap the Hungarian algorithm
avoids. When supply is loose (15 × 60, 30 × 150) both fill everything and Hungarian is *also*
cheaper. It costs about 8× the runtime — 160 ms for 150 people, irrelevant for work a human does
over three days.

Trusting an algorithm nobody in this repo derived is its own problem, so it is verified by
**oracle testing**: 200 random worlds where the Hungarian result must equal the brute-force
optimum exactly, plus 300 more asserting invariants.

📄 Full write-up: [`docs/matching.md`](docs/matching.md)
