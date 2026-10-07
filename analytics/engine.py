from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


@dataclass(frozen=True)
class AnalyticsResult:
    health_score: int
    status: str
    cpu_forecast: float
    memory_forecast: float
    bottlenecks: tuple[str, ...]
    recommendations: tuple[str, ...]


class AnalyticsEngine:
    """Small, explainable forecasting model for recent monitoring history."""

    required_columns = ("cpu_percent", "memory_percent", "disk_percent")

    @staticmethod
    def _forecast(values: Sequence[float]) -> float:
        if not values:
            return 0.0
        if len(values) == 1:
            return round(float(values[0]), 2)
        x = np.arange(len(values)).reshape(-1, 1)
        model = LinearRegression().fit(x, np.asarray(values, dtype=float))
        return round(float(np.clip(model.predict([[len(values)]])[0], 0, 100)), 2)

    def analyze(self, history: pd.DataFrame) -> AnalyticsResult:
        if history.empty:
            return AnalyticsResult(100, "Healthy", 0.0, 0.0, (), ("Collect samples to enable analysis.",))
        latest = history.iloc[-1]
        cpu_next = self._forecast(history["cpu_percent"].tail(30).tolist())
        memory_next = self._forecast(history["memory_percent"].tail(30).tolist())
        disk = float(latest["disk_percent"])
        severity = max(cpu_next, memory_next, disk)
        score = int(round(max(0, 100 - (0.42 * cpu_next + 0.36 * memory_next + 0.22 * disk))))
        bottlenecks: list[str] = []
        advice: list[str] = []
        for label, value, message in (
            ("CPU", cpu_next, "Review the CPU-heavy processes and defer nonessential workloads."),
            ("Memory", memory_next, "Close unused applications or investigate memory growth."),
            ("Disk", disk, "Archive temporary files and verify available disk capacity."),
        ):
            if value >= 80:
                bottlenecks.append(f"{label} pressure predicted at {value:.1f}%")
                advice.append(message)
        if not advice:
            advice.append("Resource levels are within the configured healthy range.")
        status = "Critical" if severity >= 90 else "Warning" if severity >= 75 else "Healthy"
        return AnalyticsResult(score, status, cpu_next, memory_next, tuple(bottlenecks), tuple(advice))
