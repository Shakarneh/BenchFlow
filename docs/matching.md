# The Matching Engine

How benchFlow decides which specialists to propose for which client requests.

---

## The problem

An IT outstaffing company has a pool of specialists and a set of open client requests.
Each request names required skills at minimum levels, a date range, a headcount and a
budget. Each specialist has skills at levels, a cost rate, and a calendar that may
already be partly booked.

Assigning people to requests is the **assignment problem**: pair two sets so that the
total cost is minimised, with nobody assigned twice.

## The four rules a candidate must satisfy

Implemented in `Request.is_satisfied_by()`:

1. **Skills** — covers every required skill, at or above the level asked for
2. **Employment** — available by the start date
3. **Capacity** — their calendar has room for this fraction over the whole period
4. **Budget** — cost rate within the client's maximum

Rules 1 and 3 are not simple lookups:

- **Skills are resolved through a DAG first.** "Django implies Python" — a Django
  developer matches a Python request without anyone typing Python on their profile.
  Transitive closure by BFS, O(V+E). See `domain/skill_graph.py`.
- **Capacity is fractional and overlapping.** Someone 50% booked can take a 50%
  engagement. Peak simultaneous load is found with a sweep-line in O(n log n).
  See `domain/allocation.py`.

## The objective function

When filling requests and saving money conflict, **filling wins**:

```python
if filled != best_filled:
    return filled > best_filled   # more slots filled always wins
return cost < best_cost           # cost only breaks ties
```

This is a business decision, not a mathematical one. An unfilled request is a lost
client; an expensive placement is thinner margin. A company with different economics
would order these differently, and the algorithm would follow.

---

## Three strategies

All three implement the same `Matcher` interface, so they are interchangeable.

| Strategy | Complexity | Optimal? | Notes |
|---|---|---|---|
| `GreedyMatcher` | O(n log n) | ❌ | Cheapest qualified person, per request, in arrival order |
| `OptimalMatcher` | O(k^n) | ✅ | Exhaustive search over every arrangement |
| `HungarianMatcher` | O(n³) | ✅ | Kuhn–Munkres with potentials |

### Why greedy is wrong

Greedy makes a locally optimal choice per request. Locally optimal is not globally
optimal:

|  | Request A (needs Junior) | Request B (needs Middle) |
|---|---|---|
| **Alice** — Middle, 50 | qualifies | qualifies |
| **Dmitry** — Junior, 60 | qualifies | **not qualified** |

Greedy processes A first, takes the cheaper Alice, and then B has nobody — because
only Alice could fill B. The correct arrangement is Dmitry→A, Alice→B: both filled.

Worse, **reversing the request order makes greedy succeed.** An algorithm whose
correctness depends on input order is not an algorithm.

### How Hungarian encodes the problem

The business problem becomes a square cost matrix:

|  | real specialist | dummy specialist |
|---|---|---|
| **real slot** | cost in cents, or `PENALTY` if unqualified | `PENALTY` — slot goes unfilled |
| **dummy slot** | `0` — specialist simply unused | `0` |

`PENALTY = 10⁹`, far larger than any achievable total cost. So *minimising total cost*
automatically prefers filling slots — the objective function above, expressed as
arithmetic rather than a branch. Costs are integer cents, keeping the maths exact.

A request needing 2 people becomes 2 slots. The matrix is padded to square with
dummies. `PENALTY` cells in the result mean "unfilled", and are dropped.

---

## Correctness

The Hungarian implementation is the textbook algorithm and was not derived here.
Confidence in it comes from testing against an oracle rather than from re-reading it:

- `OptimalMatcher` is exhaustive, therefore cannot be wrong — only slow
- **200 randomly generated worlds** are solved by both; the tests assert identical
  slots-filled and identical total cost
- A further **300 random worlds** assert Hungarian is never worse than greedy, that
  nobody is assigned twice, and that nobody unqualified is ever assigned

Seeded with `random.Random(seed)`, so any failure is reproducible rather than a ghost.
See `tests/test_hungarian_matches_brute_force.py`.

---

## Benchmark

`python manage.py benchmark_matchers` — measured on Python 3.13, seeded worlds.

| requests × people | matcher | unfilled | total cost | ms |
|---|---|---|---|---|
| 4 × 8 | greedy | 3 | 196.00 | 0.12 |
| | exhaustive | 3 | 196.00 | 0.15 |
| | hungarian | 3 | 196.00 | 0.14 |
| 5 × 12 | greedy | 3 | 345.00 | 0.20 |
| | exhaustive | 3 | 345.00 | **7.17** |
| | hungarian | 3 | 345.00 | 0.42 |
| **8 × 25** | greedy | **1** | 605.00 | 0.76 |
| | hungarian | **0** | 652.00 | 1.34 |
| 15 × 60 | greedy | 0 | 917.00 | 3.80 |
| | hungarian | 0 | **904.00** | 11.57 |
| 30 × 150 | greedy | 0 | 2097.00 | 19.43 |
| | hungarian | 0 | **2071.00** | 160.14 |

### Reading it

**Exhaustive search dies fast.** 0.15ms at 4×8, 7.17ms at 5×12 — roughly 48× for one
extra request. It is a correctness oracle, not a production strategy.

**Greedy strands clients when supply is tight.** At 8×25 it left a request unfilled to
save 47. For a company advertising a three-day placement promise, that is the product
failing, not a saving.

**Greedy is also quietly more expensive when supply is loose.** At 15×60 and 30×150
both fill everything, and Hungarian is cheaper by 13 and 26 respectively.

**Hungarian costs about 8× the runtime.** 160ms at 30×150 — irrelevant for work that
runs as a background job, which is what Phase 13 makes it.

## Decision

**`HungarianMatcher` is the default.** `GreedyMatcher` is kept as a fast baseline and
as the thing the tests measure against. `OptimalMatcher` is kept as the test oracle and
is never used in production paths.

## Not implemented

**Min-cost max-flow** generalises the assignment problem and would be the route to
richer constraints — partial allocations across several requests at once, or preferences
weighted rather than binary. The Hungarian algorithm is sufficient for the constraints
benchFlow currently models, so MCMF was deliberately left out rather than half-built.
