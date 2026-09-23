# Project 1 — SLA & Incident Root-Cause Analysis

**Problem.** Support SLA breach rate climbed for 3 months, but leadership only saw the total — no breakdown by channel, priority, or assignee, so nobody knew where to intervene.

**Approach.**
1. Pulled 90 days of ticket history with SQL (`sql/sla_breach_analysis.sql`): breach flag, first-response and resolution times, channel, priority, agent.
2. Analyzed breach concentration with pandas (`src/analyze_tickets.py`): Pareto of breach share by channel, breach rate by priority, MTTR trend by week.
3. Output: a breach-rate table and an MTTR trend chart (`mttr_trend.png`).

**Result (on sample data).** Two channels account for ~60% of all breaches; `P3` tickets breached most in absolute terms because volume is highest there — the fix was prioritization rules, not more headcount.

## Run it
```bash
pip install -r requirements.txt
python src/analyze_tickets.py   # writes breach_summary.csv + mttr_trend.png
```
`sql/sla_breach_analysis.sql` is the equivalent query for the production warehouse (BigQuery-flavored).
