# Security Review — benchFlow

A review of this codebase against the **OWASP Top 10**, written by the author.
Each item states what benchFlow does, and — where something is not done — says so
plainly rather than leaving a gap unmentioned.

Verified with `python manage.py check --deploy`, Django's own auditor.

---

## A01 — Broken Access Control

**What it is.** Users reaching data or actions that should not be theirs.

**Here.** Deny by default: `IsAuthenticated` is the DRF *default* permission, so a new
endpoint is locked unless it explicitly opens itself. Running the matcher additionally
requires membership of the **Account Managers** group (`interfaces/permissions.py`);
superusers bypass role checks so an admin cannot be locked out.

Proven by tests: an anonymous request gets 403, and a logged-in non-manager also gets 403
— the same status, two different failures (authentication vs authorization).

**Not done.** Object-level permissions. Any authenticated user can read *all* specialists,
not just those in their own department. benchFlow is a small internal tool, so this is
acceptable today; a multi-tenant version would need per-object rules.

## A02 — Cryptographic Failures

**Here.** No secret is stored in code. `SECRET_KEY` and all five `POSTGRES_*` values are
read from environment variables, kept in `.env`, which `.gitignore` blocks. `settings.py`
contains only variable *names*. The auto-generated `django-insecure-` key was replaced with
a properly random one.

Passwords are never handled by our code — Django hashes them with PBKDF2 and salts them.

In production (`DEBUG=False`) the session and CSRF cookies are marked `Secure`, so they are
never transmitted over plain HTTP, and HSTS instructs browsers to refuse HTTP entirely.

## A03 — Injection

**SQL injection.** Every database access goes through the Django ORM, which parameterises
queries — user input is never concatenated into SQL. There is not one raw query in the
codebase. Verified: `grep -r "raw(\|cursor.execute" .` returns nothing.

**XSS.** The API returns JSON via DRF serializers, which escape output. No user-supplied
HTML is rendered anywhere.

## A04 — Insecure Design

**Here.** Two design decisions with security consequences:

- **Invariants are enforced at the lowest possible level.** `CheckConstraint`s in PostgreSQL
  reject an allocation with `fraction > 1` or `ends_on < starts_on`. An application bug —
  or a direct database write — cannot create nonsense data.
- **Race conditions are designed out, not patched.** `place()` wraps check-and-book in a
  single transaction with `select_for_update()` row locking, so two managers cannot
  double-book the same person.

## A05 — Security Misconfiguration

**Here.** Production hardening is switched on automatically by `DEBUG=False` rather than
relying on someone remembering: SSL redirect, secure cookies, HSTS, `nosniff`,
`X_FRAME_OPTIONS = DENY`. `ALLOWED_HOSTS` comes from the environment; an empty list in
production is refused by Django, which blocks Host-header attacks.

`check --deploy` goes from **10 warnings to 3** with production settings applied, and the
remaining 3 are drf-spectacular documentation hints, not security findings.

## A06 — Vulnerable and Outdated Components

**Here.** Every dependency is pinned to an exact version in `requirements.txt`, so builds
are reproducible and an upgrade is a deliberate, reviewable change. Django 5.2 is an **LTS**
release, chosen specifically because it receives security patches for years.

**Not done.** Automated vulnerability scanning (`pip-audit`, Dependabot). This belongs in
Phase 18's CI pipeline.

## A07 — Identification and Authentication Failures

**Here.** Django's own auth system: PBKDF2 password hashing, signed session cookies, and
the four default password validators (similarity, minimum length, common-password list,
numeric-only rejection).

**Deliberately not done.** JWT. Session authentication is sufficient for a single Django
application; JWT earns its complexity when a separate frontend or mobile client exists.
It would slot into DRF's authentication classes without touching a single view.

## A08 — Software and Data Integrity Failures

**Here.** `@transaction.atomic` means partial writes cannot survive a failure — a refused
placement leaves no orphan allocation, pinned by a test. Placement rates are stored as a
**snapshot**: changing a specialist's cost rate next year cannot silently rewrite the margin
on a deal already signed.

## A09 — Security Logging and Monitoring Failures

**Here.** Structured logging with meaningful levels: a refused placement logs `WARNING`
(the system working correctly), an unexpected failure logs a full traceback (the system
broken). Every log line carries the module that produced it, so logs are searchable.

The pipeline keeps an **append-only audit trail** — every state transition records who moved
it and when, in frozen records that cannot be edited after the fact.

**Not done.** Log aggregation and alerting. Logs go to the console; production would ship
them somewhere queryable.

## A10 — Server-Side Request Forgery

**Not applicable.** benchFlow makes no outbound HTTP requests from user-supplied input.

---

## Personal data — ФЗ-152 considerations

Expert Choice operates under Russian personal-data law (ФЗ-152) and ГОСТ 57580.1 for banking
clients, so this deserves explicit thought rather than silence.

**What benchFlow stores about a person:** full name, hourly cost rate, availability dates,
skills and levels. This is employment data, not sensitive personal data — no passport
numbers, no addresses, no health information, no biometrics.

**What would be required for a real deployment:**

| Requirement | Status |
|---|---|
| Data stored on servers located in Russia | deployment decision, not a code decision |
| Access limited by role | ✅ done — Django Groups |
| Audit trail of who accessed and changed what | ⚠️ partial — pipeline transitions are audited; reads are not |
| Right to erasure | ❌ not implemented — `on_delete=PROTECT` currently *prevents* deleting a specialist who has placements |
| Encryption at rest | deployment decision (PostgreSQL/disk level) |

The erasure gap is the honest one: history is deliberately preserved, and a real
implementation would need anonymisation (replacing the name, keeping the placement record)
rather than deletion.

---

## Summary

| | |
|---|---|
| Handled in code | access control · secrets in env · ORM-only queries · DB-level invariants · row locking · atomic transactions · audit trail · production hardening |
| Deferred deliberately | object-level permissions · JWT · dependency scanning (Phase 18) · log aggregation |
| Known gap | right to erasure vs. preserved history |

The point of this document is not to claim benchFlow is secure. It is to show that the
threats were enumerated, most were addressed, and the remainder are known rather than
overlooked.
