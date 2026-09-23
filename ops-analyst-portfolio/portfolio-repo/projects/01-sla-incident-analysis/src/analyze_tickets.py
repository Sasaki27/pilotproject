"""SLA breach root-cause analysis on ticket export.

Reads data/sample_tickets.csv, computes breach rates and MTTR, writes
breach_summary.csv and mttr_trend.png.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data" / "sample_tickets.csv"

FR_TARGET_MIN = {"P1": 15, "P2": 60, "P3": 240, "P4": 480}   # first response
RES_TARGET_H = {"P1": 4, "P2": 8, "P3": 24, "P4": 72}        # resolution


def load() -> pd.DataFrame:
    df = pd.read_csv(DATA, parse_dates=["created_at", "first_responded_at", "resolved_at"])
    df["first_response_min"] = (
        df["first_responded_at"] - df["created_at"]
    ).dt.total_seconds() / 60
    df["resolution_hours"] = (
        df["resolved_at"] - df["created_at"]
    ).dt.total_seconds() / 3600
    df["fr_breached"] = df["first_response_min"] > df["priority"].map(FR_TARGET_MIN)
    df["res_breached"] = df["resolution_hours"] > df["priority"].map(RES_TARGET_H)
    return df


def summarize(df: pd.DataFrame) -> pd.DataFrame:
    g = df.groupby(["priority", "channel"])
    summary = g.agg(
        tickets=("ticket_id", "count"),
        fr_breach_rate=("fr_breached", "mean"),
        res_breach_rate=("res_breached", "mean"),
        mttr_hours=("resolution_hours", "mean"),
    ).round(3)
    return summary.sort_values("res_breach_rate", ascending=False)


def mttr_trend(df: pd.DataFrame, out: Path) -> None:
    df["week"] = df["created_at"].dt.to_period("W").dt.start_time
    weekly = df.groupby("week")["resolution_hours"].mean()
    ax = weekly.plot(marker="o", figsize=(8, 4), title="MTTR by week (hours)")
    ax.set_ylabel("MTTR (h)")
    ax.figure.tight_layout()
    ax.figure.savefig(out, dpi=150)


def main() -> None:
    df = load()
    summary = summarize(df)
    out_csv = HERE.parent / "breach_summary.csv"
    summary.to_csv(out_csv)
    mttr_trend(df, HERE.parent / "mttr_trend.png")

    total_breach = df["res_breached"].mean()
    top2_share = summary["res_breach_rate"].head(2).index.tolist()
    print(f"Tickets analyzed: {len(df)}")
    print(f"Overall resolution breach rate: {total_breach:.1%}")
    print(f"Worst priority/channel combos: {top2_share}")
    print(f"Wrote {out_csv.name} and mttr_trend.png")


if __name__ == "__main__":
    main()
