"""Savings tracker CLI: record expenses, track a monthly savings goal, chart pace.

Data persists to data/expenses.csv. Run `demo` to try it on bundled sample data.
"""
import argparse
import csv
import sys
from datetime import date
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data" / "expenses.csv"
SAMPLE = HERE.parent / "data" / "sample_expenses.csv"
GOAL_FILE = HERE.parent / "data" / "goal.txt"
CATEGORIES = ["food", "transport", "housing", "fun", "bills", "other"]


def load() -> pd.DataFrame:
    if DATA.exists():
        return pd.read_csv(DATA, parse_dates=["date"])
    return pd.DataFrame(columns=["date", "amount", "category", "note"])


def save(df: pd.DataFrame) -> None:
    df.to_csv(DATA, index=False)


def month_df(df: pd.DataFrame) -> pd.DataFrame:
    m = date.today().strftime("%Y-%m")
    out = df[df["date"].dt.strftime("%Y-%m") == m]
    return out if len(out) else df.tail(30)  # demo fallback on sample data


def goal() -> float:
    return float(GOAL_FILE.read_text()) if GOAL_FILE.exists() else 500.0


def add(amount: float, note: str, cat: str) -> None:
    df = load()
    save(pd.concat([df, pd.DataFrame([{
        "date": date.today().isoformat(), "amount": amount,
        "category": cat if cat in CATEGORIES else "other", "note": note}])],
        ignore_index=True))
    print(f"Added £{amount:.2f} [{cat if cat in CATEGORIES else 'other'}] {note}")


def set_goal(amount: float) -> None:
    GOAL_FILE.write_text(str(amount))
    print(f"Monthly savings goal set to £{amount:.2f}")


def summary() -> None:
    m = month_df(load())
    if m.empty:
        print("No expenses recorded yet."); return
    g = goal()
    days_left = max(1, (date.today().replace(day=28) - date.today()).days + 2)
    spent = m["amount"].sum()
    by_cat = m.groupby("category")["amount"].sum().sort_values(ascending=False)
    print(f"\nMonth summary ({date.today().strftime('%Y-%m')})")
    print(f"  Goal (monthly savings): £{g:.2f}")
    print(f"  Spent this period:      £{spent:.2f}")
    print(f"  Days left in month:     {days_left}")
    print(f"  Largest category:       {by_cat.index[0]} (£{by_cat.iloc[0]:.2f})")
    print("\nCategory breakdown:")
    for c, v in by_cat.items():
        print(f"  {c:10s} £{v:7.2f}  {'#' * max(1, int(v / by_cat.max() * 20))}")
    over = spent > g
    print(f"\nPace: {'OVER' if over else 'WITHIN'} goal "
          f"(£{abs(spent - g):.2f} {'above' if over else 'under'})")


def chart() -> None:
    m = month_df(load())
    m = m.sort_values("date")
    m = m.assign(cumulative=m["amount"].cumsum())
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(m["date"], m["cumulative"], marker="o", label="cumulative spend")
    ax.axhline(goal(), color="red", linestyle="--", label=f"savings goal £{goal():.0f}")
    ax.set_title("Cumulative spend vs savings goal")
    ax.legend()
    fig.tight_layout()
    out = HERE.parent / "spend_trend.png"
    fig.savefig(out, dpi=150)
    print(f"Wrote {out.name}")


def demo() -> None:
    """Load the bundled sample month, then print summary + chart."""
    if SAMPLE.exists() and not DATA.exists():
        save(pd.read_csv(SAMPLE, parse_dates=["date"]))
    summary()
    chart()


def main() -> None:
    p = argparse.ArgumentParser(description="Savings tracker")
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("amount", type=float)
    a.add_argument("note")
    a.add_argument("--cat", default="other", choices=CATEGORIES)
    sub.add_parser("summary")
    g = sub.add_parser("set-goal")
    g.add_argument("amount", type=float)
    sub.add_parser("chart")
    sub.add_parser("demo")
    args = p.parse_args()
    if args.cmd == "add":
        add(args.amount, args.note, args.cat)
    elif args.cmd == "summary":
        summary()
    elif args.cmd == "set-goal":
        set_goal(args.amount)
    elif args.cmd == "chart":
        chart()
    elif args.cmd == "demo":
        demo()


if __name__ == "__main__":
    main()
