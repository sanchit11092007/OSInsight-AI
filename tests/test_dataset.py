import pandas as pd
from analytics.dataset import clean_history


def test_clean_history_removes_invalid_rows() -> None:
    frame = pd.DataFrame({"cpu_percent": [20, "bad"], "memory_percent": [30, 40], "disk_percent": [50, 60]})
    assert len(clean_history(frame)) == 1
