# WORKFLOW SCHEMA — **benchFlow**
### How we work, drawn out

> Companion to `CLAUDE.md`. Every diagram below is Mermaid — it renders automatically on
> GitHub, so this file is readable straight from the repository page.

---

## 1. THE SESSION LOOP
### The single most important diagram in this project

This is the cycle we repeat for every feature. **Nothing skips a step.**

```mermaid
flowchart TD
    A["🎯 Claude proposes the next step<br/>WHAT · WHY · WHAT IT CHANGES"] --> B{"Mohammed<br/>approves?"}
    B -- "No / change it" --> A
    B -- "Yes" --> C{"Does this involve<br/>a NEW concept?"}

    C -- "Yes" --> D["🎓 CONCEPT CARD<br/>what it is · how to recognise it<br/>why here · simplest example"]
    D --> E{"Mohammed<br/>understands?"}
    E -- "No — explain differently" --> D
    E -- "Yes" --> F

    C -- "No" --> F["📐 Claude explains the design<br/>in plain language"]
    F --> G{"Mohammed<br/>approves design?"}
    G -- "No" --> F
    G -- "Yes" --> H["⌨️ Claude scaffolds<br/>Mohammed types the core logic"]

    H --> I["🔍 Line-by-line walkthrough<br/>of what we just wrote"]
    I --> J{"Mohammed can<br/>explain it back?"}
    J -- "No" --> I
    J -- "Yes" --> K["✅ Tests written and passing"]
    K --> L["📋 Claude PROVIDES git commands<br/>❗ Mohammed RUNS them"]
    L --> M["📝 CLAUDE.md updated"]
    M --> A

    style D fill:#2d5016,stroke:#7cb342,color:#fff
    style L fill:#5d1049,stroke:#e91e63,color:#fff
    style J fill:#4a148c,stroke:#ba68c8,color:#fff
```

**The two red-flag gates:** the 🎓 Concept Card (never skipped) and the ❗ Git handover
(Claude *never* executes).

---

## 2. THE THREE HARD RULES

```mermaid
flowchart LR
    subgraph FORBIDDEN["❌ CLAUDE MUST NEVER"]
        F1["Act without<br/>permission"]
        F2["Run any<br/>git command"]
        F3["Write code before<br/>explaining it"]
    end

    subgraph REQUIRED["✅ CLAUDE MUST ALWAYS"]
        R1["Explain WHAT & WHY<br/>before every step"]
        R2["Provide git commands<br/>for Mohammed to run"]
        R3["Teach the concept,<br/>then build"]
    end

    F1 -.->|"instead"| R1
    F2 -.->|"instead"| R2
    F3 -.->|"instead"| R3

    style FORBIDDEN fill:#4a0e0e,stroke:#d32f2f,color:#fff
    style REQUIRED fill:#0d3d16,stroke:#43a047,color:#fff
```

---

## 3. THE PHASE ROADMAP

```mermaid
flowchart TD
    P0["✅ PHASE 0<br/>Foundations & setup"] --> P1

    subgraph CORE["🧠 THE THINKING LAYER — pure Python, no framework"]
        P1["✅ PHASE 1 ⭐⭐<br/>Object-Oriented Programming"] --> P2["✅ PHASE 2<br/>Clean code & SOLID"]
        P2 --> P3["✅ PHASE 3<br/>Testing & TDD"]
    end

    P3 --> P4["✅ PHASE 4<br/>Databases & persistence"]

    subgraph ALGO["⚙️ THE HARD PART — real computer science"]
        P5["✅ PHASE 5<br/>Data structures: skill graph"] --> P6["✅ PHASE 6<br/>Algorithms I: intervals"]
        P6 --> P7["✅ PHASE 7 ⭐⭐<br/>Algorithms II: MATCHING ENGINE"]
    end

    P4 --> P5
    P7 --> P8["✅ PHASE 8<br/>Design patterns"]
    P8 --> P9["✅ PHASE 9<br/>Software architecture"]

    subgraph WEB["🌐 THE OUTSIDE WORLD"]
        P10["✅ PHASE 10<br/>Web & REST APIs"] --> P11["✅ PHASE 11<br/>Auth & RBAC"]
        P11 --> P12["✅ PHASE 12<br/>Money & correctness"]
        P12 --> P13["✅ PHASE 13<br/>Caching & async"]
    end

    P9 --> P10
    P13 --> P14["✅ PHASE 14<br/>Errors & logging"]
    P14 --> P15["✅ PHASE 15<br/>Security"]
    P15 --> P16["✅ PHASE 16<br/>Tooling & typing"]

    subgraph OPS["🚢 SHIPPING IT"]
        P17["✅ PHASE 17<br/>Docker"] --> P18["✅ PHASE 18<br/>CI/CD"]
        P18 --> P19["✅ PHASE 19<br/>Deployment"]
    end

    P16 --> P17
    P19 --> P20["✅ PHASE 20<br/>Frontend — only now"]
    P20 --> P21["🔄 PHASE 21<br/>Docs & showcase<br/><i>in progress</i>"]
    P21 --> DONE(["🎯 Apply to<br/>Expert Choice CIS"])

    style CORE fill:#1a237e,stroke:#5c6bc0,color:#fff
    style ALGO fill:#4a148c,stroke:#ab47bc,color:#fff
    style WEB fill:#004d40,stroke:#26a69a,color:#fff
    style OPS fill:#3e2723,stroke:#8d6e63,color:#fff
    style DONE fill:#1b5e20,stroke:#66bb6a,color:#fff
```

---

## 4. THE ARCHITECTURE & THE DEPENDENCY RULE

```mermaid
flowchart TD
    subgraph OUT["🌍 Outside world"]
        BROWSER["Browser / API client"]
    end

    BROWSER --> INT

    subgraph INT["interfaces/ — speaks HTTP"]
        V["DRF views · serializers · URLs"]
    end

    INT --> APP

    subgraph APP["application/ — use cases"]
        UC["'Propose candidates for request X'<br/>Orchestrates. No HTTP. No SQL."]
    end

    APP --> DOM

    subgraph DOM["domain/ — PURE PYTHON, zero Django"]
        E["Entities: Specialist · Skill · Request"]
        R["Rules & algorithms: matcher · calendar"]
    end

    INF -.->|"handed to application/<br/>at startup"| APP

    subgraph INF["infrastructure/ — the machinery"]
        ORM["Django ORM"]
        RD["Redis"]
        CEL["Celery"]
    end

    INF --> DB[("PostgreSQL")]
    INF --> RCACHE[("Redis")]
    INF -.->|"implements interfaces<br/>defined in domain/"| DOM

    style DOM fill:#1b5e20,stroke:#66bb6a,color:#fff
    style APP fill:#0d47a1,stroke:#5c6bc0,color:#fff
    style INT fill:#4a148c,stroke:#ab47bc,color:#fff
    style INF fill:#3e2723,stroke:#8d6e63,color:#fff
```

> **The dependency rule:** every solid arrow points *inward*. `domain/` imports nothing from the
> layers outside it — no Django, no database, no HTTP. That is precisely why it can be tested in
> milliseconds, and it is the single biggest architectural idea in this project.
>
> **Read the two dotted arrows carefully — they are the whole trick.** `application/` never imports
> `infrastructure/`. Instead `domain/` declares an *interface* ("something that can list all
> specialists"), `infrastructure/` writes the real Django-ORM version of it, and at startup that
> real object is **handed in** to `application/`. In tests we hand in a fake list instead and the
> exact same code runs with no database.

---

## 5. THE DOMAIN MODEL

```mermaid
erDiagram
    CLIENT ||--o{ REQUEST : "raises"
    REQUEST ||--o{ CANDIDATE : "generates"
    SPECIALIST ||--o{ CANDIDATE : "proposed as"
    CANDIDATE ||--o| PLACEMENT : "becomes"
    PLACEMENT ||--|| ENGAGEMENT : "priced by"
    PLACEMENT ||--o{ ALLOCATION : "books"
    SPECIALIST ||--o{ ALLOCATION : "committed via"
    SPECIALIST ||--o{ SKILL_LEVEL : "possesses"
    SKILL ||--o{ SKILL_LEVEL : "measured in"
    SKILL ||--o{ SKILL : "implies"
    REQUEST ||--o{ REQUIREMENT : "specifies"
    SKILL ||--o{ REQUIREMENT : "referenced by"

    SPECIALIST {
        string full_name
        decimal cost_rate
        date available_from
    }
    SKILL {
        string name
        string category
    }
    REQUEST {
        int headcount
        date starts_on
        decimal max_bill_rate
        string state
    }
    ALLOCATION {
        date starts_on
        date ends_on
        decimal fraction
    }
    ENGAGEMENT {
        decimal cost_rate
        decimal bill_rate
        decimal margin
    }
```

---

## 6. THE REQUEST PIPELINE — a state machine

```mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> Open : client confirms
    Open --> Sourcing : matcher runs
    Sourcing --> Proposed : candidates sent
    Proposed --> CheckUp : technical check-up
    CheckUp --> Interview : client interviews
    CheckUp --> Sourcing : rejected — find more
    Interview --> Offered : client accepts
    Interview --> Sourcing : rejected — find more
    Offered --> Placed : start date agreed
    Placed --> Active : specialist starts
    Active --> Ended : engagement finishes
    Ended --> [*]

    Open --> Cancelled : client withdraws
    Sourcing --> Cancelled
    Proposed --> Cancelled
    Cancelled --> [*]

    note right of Sourcing
        ⏱ The 3-day SLA clock
        runs from here
    end note
```

---

## 7. HOW A MATCH ACTUALLY HAPPENS

```mermaid
sequenceDiagram
    actor M as Account manager
    participant API as interfaces/ (DRF)
    participant UC as application/
    participant SG as domain/ skill graph
    participant CAL as domain/ calendar
    participant MATCH as domain/ matcher
    participant CACHE as Redis
    participant DB as PostgreSQL

    M->>API: POST /requests/42/match
    API->>UC: propose_candidates(42)
    UC->>CACHE: cached result?
    alt cache hit
        CACHE-->>UC: candidates
    else cache miss
        UC->>DB: load specialists + request
        UC->>SG: expand required skills<br/>(Django ⇒ Python)
        SG-->>UC: full skill set
        UC->>CAL: who is free in the window?
        CAL-->>UC: available specialists
        UC->>MATCH: solve assignment problem
        MATCH-->>UC: ranked candidates + scores
        UC->>CACHE: store result
    end
    UC-->>API: candidates
    API-->>M: 200 OK · ranked list with reasons
```

---

## 8. THE GIT WORKFLOW

```mermaid
gitGraph
    commit id: "init"
    branch develop
    checkout develop
    commit id: "phase 0 setup"
    branch feat/oop-specialist
    checkout feat/oop-specialist
    commit id: "add Specialist class"
    commit id: "add SkillLevel"
    commit id: "tests for Specialist"
    checkout develop
    merge feat/oop-specialist tag: "PR #1 ✅ CI"
    branch feat/skill-graph
    checkout feat/skill-graph
    commit id: "skill DAG"
    commit id: "traversal + tests"
    checkout develop
    merge feat/skill-graph tag: "PR #2 ✅ CI"
    checkout main
    merge develop tag: "v0.1.0"
```

**Who does what:**

```mermaid
flowchart LR
    C["🤖 Claude"] -->|"writes"| CODE["Code + explanations"]
    C -->|"provides as text"| CMD["git commands"]
    CMD -->|"❗ never executed by Claude"| M["👤 Mohammed"]
    M -->|"runs every one"| GIT[("Git / GitHub")]

    style CMD fill:#5d1049,stroke:#e91e63,color:#fff
    style M fill:#1b5e20,stroke:#66bb6a,color:#fff
```

---

## 9. THE CI/CD PIPELINE *(Phase 18)*

```mermaid
flowchart LR
    PUSH["git push"] --> PR["Pull Request"]
    PR --> GA["GitHub Actions"]

    GA --> L["ruff<br/>lint"]
    GA --> F["black --check<br/>format"]
    GA --> T["mypy<br/>types"]
    GA --> U["pytest<br/>tests"]

    L --> GATE{"all green?"}
    F --> GATE
    T --> GATE
    U --> GATE

    GATE -- "❌ no" --> FIX["Fix and push again"]
    FIX --> GA
    GATE -- "✅ yes" --> MERGE["Merge to develop"]
    MERGE --> DEPLOY["Deploy demo"]

    style GATE fill:#4a148c,stroke:#ab47bc,color:#fff
    style DEPLOY fill:#1b5e20,stroke:#66bb6a,color:#fff
```

---

## 10. WHAT RUNS WHERE *(Phase 17)*

```mermaid
flowchart TB
    subgraph COMPOSE["docker compose up"]
        WEB["web<br/>Django + DRF"]
        WORKER["worker<br/>Celery"]
        BEAT["beat<br/>Celery scheduler"]
        PG[("db<br/>PostgreSQL")]
        RD[("cache<br/>Redis")]
    end

    WEB --> PG
    WEB --> RD
    WORKER --> PG
    WORKER --> RD
    BEAT --> RD
    RD -.->|"queues tasks"| WORKER

    style COMPOSE fill:#0d47a1,stroke:#5c6bc0,color:#fff
```

One command brings the entire system up. That is the point of Phase 17 — anyone, including an
interviewer, can run this project in under a minute.

---

## 11. CONCEPT COVERAGE MAP

Where each thing from the learning plan is actually taught:

```mermaid
mindmap
  root((benchFlow))
    OOP
      Phase 1 entities
      encapsulation
      ABCs
      composition
    Clean code
      Phase 2 SOLID
      code smells
    Data structures
      Phase 5 skill DAG
      Phase 6 heaps
      hash maps
    Algorithms
      Phase 6 sweep line
      Phase 7 assignment problem
      Big-O throughout
    Patterns
      Phase 8 Strategy
      Specification
      State
      Repository
    Architecture
      Phase 9 hexagonal
      dependency rule
      ADRs
    Databases
      Phase 4 modelling
      Phase 12 transactions
    Web & APIs
      Phase 10 REST
      OpenAPI
    Security
      Phase 11 authN authZ
      Phase 15 OWASP
    Async
      Phase 13 Celery
      Redis
    Testing
      Phase 3 TDD
      throughout
    DevOps
      Phase 17 Docker
      Phase 18 CI CD
      Phase 19 deploy
```

---

## 12. THE END GOAL

```mermaid
flowchart LR
    B["benchFlow<br/>this project"] --> PORT["Portfolio<br/>mohammedshakarneh.com"]
    L["lolo-cosmetics"] --> PORT
    A["attendance-tracking-system"] --> PORT
    N["My Notes"] --> PORT
    PORT --> GH["GitHub profile"]
    PORT --> LI["LinkedIn"]
    GH --> MSG["Message to the<br/>practice supervisor"]
    LI --> MSG
    MSG --> JOB(["💼 Expert Choice CIS"])

    style B fill:#4a148c,stroke:#ab47bc,color:#fff
    style JOB fill:#1b5e20,stroke:#66bb6a,color:#fff
```
