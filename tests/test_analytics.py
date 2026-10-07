import pandas as pd
from analytics.engine import AnalyticsEngine


def test_empty_history_is_healthy() -> None:
    result = AnalyticsEngine().analyze(pd.DataFrame(columns=["cpu_percent", "memory_percent", "disk_percent"]))
    assert result.health_score == 100


def test_high_cpu_creates_bottleneck() -> None:
    frame = pd.DataFrame({"cpu_percent": [80, 88, 95], "memory_percent": [40, 42, 43], "disk_percent": [20, 20, 20]})
    result = AnalyticsEngine().analyze(frame)
    assert result.status in {"Warning", "Critical"}
    assert any("CPU" in item for item in result.bottlenecks)
