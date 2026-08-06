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
