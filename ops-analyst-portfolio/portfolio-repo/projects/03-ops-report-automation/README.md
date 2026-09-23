# Project 3 — Daily Ops Report Automation

**Problem.** Every morning an analyst spent ~30 minutes copy-pasting ticket counts, open incidents, and overdue items from three systems into an email.

**Approach.** `src/daily_ops_report.py` — a single scheduled script that:
1. reads the same three exports (here: bundled CSVs; in production: API/warehouse queries),
2. computes yesterday's numbers: new tickets, resolved, open backlog, overdue items, top requester,
3. renders a compact HTML email body and writes the report file,
4. is scheduled with cron (`0 7 * * 1-5`) so the report lands at 07:00 with zero manual steps.

**Result.** ~30 min/day saved (~125 h/year), and the report stopped being skipped on busy mornings because nobody had to remember to build it.

## Run it
```bash
pip install -r requirements.txt
python src/daily_ops_report.py   # writes daily_report.html, prints the summary
```
## Production wiring
- Replace `load_*()` with your real sources (warehouse query / REST API / S3 drop).
- Send via SMTP or your chat webhook — the `send_email()` stub shows where.
- Schedule with cron or your scheduler; log to a file, alert on failure, never fail silently.
