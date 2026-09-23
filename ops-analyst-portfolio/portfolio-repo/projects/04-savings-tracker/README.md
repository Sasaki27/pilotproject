# Project 4 — Savings Tracker (Money-Saving App)

**Problem.** People set savings goals but have no feedback loop: spending happens across categories, and by month-end it's unclear *where* the money went and whether the goal is on track.

**Approach.** A command-line app (`src/savings_app.py`) that:
1. records expenses with categories (`add 12.50 lunch --cat food`),
2. tracks a monthly savings goal and shows days-left pace ("need £X/day to hit goal"),
3. produces a category breakdown and cumulative spend-vs-budget chart,
4. persists everything to `data/expenses.csv` — no database needed.

**Commands.**
```bash
python src/savings_app.py add 12.50 lunch --cat food        # record an expense
python src/savings_app.py summary                           # month summary + pace
python src/savings_app.py set-goal 500                      # set monthly savings goal
python src/savings_app.py chart                             # spend-vs-budget chart PNG
```

**Why this design.** Zero-setup (CSV file, stdlib + pandas only) — the point is a working tool a recruiter can run in one command, not a framework showcase.

## Run it
```bash
pip install -r requirements.txt
python src/savings_app.py demo          # loads bundled sample month, writes summary + chart
```
