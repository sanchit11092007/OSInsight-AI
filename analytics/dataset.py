from __future__ import annotations

import pandas as pd


def clean_history(frame: pd.DataFrame) -> pd.DataFrame:
    """Normalize a CSV monitoring history for models and charting."""
    result = frame.copy()
    for column in ("cpu_percent", "memory_percent", "disk_percent"):
        result[column] = pd.to_numeric(result[column], errors="coerce").clip(0, 100)
    return result.dropna(subset=["cpu_percent", "memory_percent", "disk_percent"])
