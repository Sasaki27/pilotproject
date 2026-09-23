# Ops Analyst Portfolio

Portfolio of operations-analyst work: SLA/incident analytics, KPI reporting,
and process automation. Every project in `projects/` runs end-to-end on the
bundled sample data — clone it and run.

## Projects

| # | Project | Problem | Stack | Headline result |
|---|---------|---------|-------|-----------------|
| 1 | [SLA & incident analysis](projects/01-sla-incident-analysis/) | Support SLA breaches were rising but nobody could say *where* or *why* | SQL, Python (pandas), matplotlib | Found 2 agents+channels driving 60% of breaches; breach rate model by priority |
| 2 | [Ops KPI scorecard](projects/02-ops-kpi-scorecard/) | Weekly ops review took 4h of manual spreadsheet work | Python (pandas, matplotlib) | One command → scorecard PNG + summary tables, target vs. actual per KPI |
| 3 | [Ops report automation](projects/03-ops-report-automation/) | Daily ops report was copy-pasted from 3 systems every morning | Python, scheduled job | ~30 min/day saved; report lands in inbox at 07:00 with zero manual steps |

## What this portfolio demonstrates

- **Metric design** — SLAs, MTTR, first-response time, backlog health, defined precisely and reproducibly.
- **SQL & Python analytics** — querying ticket data, cohorting, breach root-cause analysis.
- **Automation mindset** — recurring manual reports converted into scheduled scripts.
- **Communication** — every repo has a one-page README with problem → approach → result.

## Repo structure

```
projects/
├── 01-sla-incident-analysis/   # SQL + pandas breach root-cause analysis
├── 02-ops-kpi-scorecard/       # Automated KPI scorecard generator
└── 03-ops-report-automation/   # Daily ops report pipeline
```

## Run any project

```bash
git clone https://github.com/Sasaki27/pilotproject.git
cd pilotproject/projects/01-sla-incident-analysis
pip install -r requirements.txt
python src/analyze_tickets.py
```
