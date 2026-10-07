from __future__ import annotations

from pathlib import Path
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from analytics.engine import AnalyticsResult


def export_csv(history: pd.DataFrame, destination: str | Path) -> Path:
    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=True)
    history.to_csv(path, index=False)
    return path


def export_pdf(result: AnalyticsResult, destination: str | Path) -> Path:
    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(path), pagesize=A4)
    _, height = A4
    y = height - 60
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(50, y, "OSInsight-AI System Health Report")
    y -= 38
    pdf.setFont("Helvetica", 11)
    for line in [f"Health score: {result.health_score}/100 ({result.status})", f"Forecast CPU: {result.cpu_forecast:.1f}%", f"Forecast memory: {result.memory_forecast:.1f}%", "Recommendations:", *[f"- {x}" for x in result.recommendations]]:
        pdf.drawString(50, y, line[:110])
        y -= 20
    pdf.save()
    return path
