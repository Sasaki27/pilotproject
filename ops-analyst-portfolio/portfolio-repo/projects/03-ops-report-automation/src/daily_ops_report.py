"""Daily ops report generator: yesterday's numbers as an HTML email body.

Run manually for a demo, or schedule with cron:  0 7 * * 1-5 /usr/bin/python3 daily_ops_report.py
"""
from datetime import timedelta
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import pandas as pd

HERE = Path(__file__).resolve().parent
DATA = HERE.parent.parent / "01-sla-incident-analysis" / "data" / "sample_tickets.csv"


def load_tickets() -> pd.DataFrame:
    return pd.read_csv(DATA, parse_dates=["created_at", "resolved_at"])


def compute(tickets: pd.DataFrame, as_of: pd.Timestamp) -> dict:
    day = tickets[
        (tickets["created_at"] >= as_of.normalize())
        & (tickets["created_at"] < as_of.normalize() + timedelta(days=1))
    ]
    open_items = tickets[tickets["resolved_at"].isna() & (tickets["created_at"] < as_of)]
    overdue = open_items[open_items["created_at"] < as_of - timedelta(days=3)]
    return {
        "new_tickets": len(day),
        "resolved_yesterday": len(tickets[tickets["resolved_at"].dt.normalize() == as_of.normalize()]),
        "open_backlog": len(open_items),
        "overdue_gt3d": len(overdue),
        "top_requester": day["agent_id"].value_counts().idxmax() if len(day) else "—",
    }


def render_html(m: dict, as_of: pd.Timestamp) -> str:
    rows = "".join(f"<tr><td><b>{k}</b></td><td>{v}</td></tr>" for k, v in m.items())
    return (
        f"<h2>Ops daily report — {as_of:%Y-%m-%d}</h2>"
        f"<table border='1' cellpadding='6' style='border-collapse:collapse'>{rows}</table>"
    )


def send_email(html: str) -> None:
    """Production stub: fill in SMTP settings and send."""
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Ops daily report"
    msg["From"], msg["To"] = "ops-bot@example.com", "ops-team@example.com"
    msg.attach(MIMEText(html, "html"))
    # smtp.send_message(msg)  # uncomment with real SMTP config
    return msg


def main() -> None:
    # Use the latest date in the data as "yesterday" so the demo works on
    # any sample export; in production this would be pd.Timestamp.today().
    as_of = load_tickets()["created_at"].max().normalize()
    metrics = compute(load_tickets(), as_of)
    html = render_html(metrics, as_of)
    out = HERE.parent / "daily_report.html"
    out.write_text(html)
    for k, v in metrics.items():
        print(f"{k:20s} {v}")
    print(f"Wrote {out.name} (email body ready)")


if __name__ == "__main__":
    main()
