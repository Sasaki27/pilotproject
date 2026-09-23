"""Weekly ops KPI scorecard generator.

Reads an ops ticket export and produces a target-vs-actual scorecard
(PNG + markdown). Each KPI's definition lives next to its calculation.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

HERE = Path(__file__).resolve().parent
DATA = HERE.parent.parent / "01-sla-incident-analysis" / "data" / "sample_tickets.csv"
FR_TARGET_MIN = {"P1": 15, "P2": 60, "P3": 240, "P4": 480}
RES_TARGET_H = {"P1": 4, "P2": 8, "P3": 24, "P4": 72}
TARGETS = {  # weekly targets the ops team committed to
    "resolution SLA %": 90.0,
    "MTTR (h)": 18.0,
    "backlog >7d (count)": 8.0,
    "CSAT": 4.2,
}


def compute_kpis(df: pd.DataFrame) -> dict:
    resolved = df[df["resolved_at"].notna()].copy()
    resolved["res_hours"] = (resolved["resolved_at"] - resolved["created_at"]).dt.total_seconds() / 3600
    resolved["breached"] = resolved["res_hours"] > resolved["priority"].map(RES_TARGET_H)
    backlog = df[df["resolved_at"].isna() & (df["created_at"] < df["created_at"].max() - pd.Timedelta(days=7))]
    return {
        "tickets": len(df),
        "resolution SLA %": round((1 - resolved["breached"].mean()) * 100, 1),
        "MTTR (h)": round(resolved["res_hours"].mean(), 1),
        "backlog >7d (count)": len(backlog),
        "CSAT": round(df["csat"].mean(), 2),
    }


def status(kpi: str, actual: float, plain: bool = False) -> str:
    """plain=True avoids emoji glyphs matplotlib fonts may lack."""
    target = TARGETS.get(kpi)
    if target is None:
        return "n/a" if plain else "ℹ️"
    ok = actual >= target if "%" in kpi or kpi == "CSAT" else actual <= target
    if plain:
        return "OK" if ok else "MISS"
    return "✅" if ok else "❌"


def main() -> None:
    df = pd.read_csv(DATA, parse_dates=["created_at", "resolved_at"])
    df["csat"] = pd.Series(
        [round(min(5, max(1, 4.6 - 0.012 * h + (-0.4 if b else 0.1))), 1)
         for h, b in zip((df["resolved_at"] - df["created_at"]).dt.total_seconds().div(3600).fillna(24),
                         df["created_at"].notna() & df["resolved_at"].isna())],
        index=df.index)

    kpis = compute_kpis(df)

    lines = ["| KPI | Target | Actual | Status |", "|---|---|---|---|"]
    for kpi, actual in kpis.items():
        t = TARGETS.get(kpi, "—")
        lines.append(f"| {kpi} | {t} | {actual} | {status(kpi, actual)} |")
    md = HERE.parent / "scorecard_summary.md"
    md.write_text("\n".join(lines) + "\n")

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.axis("off")
    tbl = ax.table(
        cellText=[[k, str(TARGETS.get(k, "—")), str(v), status(k, v, plain=True)] for k, v in kpis.items()],
        colLabels=["KPI", "Target", "Actual", "Status"],
        loc="center", cellLoc="center",
    )
    tbl.scale(1, 1.6)
    fig.tight_layout()
    out_png = HERE.parent / "scorecard.png"
    fig.savefig(out_png, dpi=150)

    print(md.read_text())
    print(f"Wrote {out_png.name} and {md.name}")


if __name__ == "__main__":
    main()
