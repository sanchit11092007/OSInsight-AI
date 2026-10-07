from pathlib import Path

import pandas as pd

from analytics.engine import AnalyticsResult
from utils.reporting import export_csv, export_pdf


def test_report_exports(tmp_path: Path) -> None:
    csv_path = export_csv(pd.DataFrame({"cpu_percent": [10]}), tmp_path / "history.csv")
    pdf_path = export_pdf(AnalyticsResult(90, "Healthy", 10.0, 20.0, (), ("Keep monitoring.",)), tmp_path / "health.pdf")
    assert csv_path.exists() and pdf_path.exists()
