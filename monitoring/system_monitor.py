from __future__ import annotations

import time
from typing import Iterable

import psutil

from .models import SystemSnapshot


class SystemMonitor:
    """Collects an inexpensive point-in-time view of local resource usage."""

    def __init__(self, disk_path: str = "/") -> None:
        self.disk_path = disk_path
        psutil.cpu_percent(interval=None)  # prime psutil's non-blocking counter

    @staticmethod
    def _safe_processes(limit: int) -> Iterable[dict]:
        records: list[dict] = []
        for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent", "status"]):
            try:
                info = proc.info
                records.append({
                    "pid": info["pid"], "name": info["name"] or "Unknown",
                    "cpu_percent": round(float(info["cpu_percent"] or 0), 2),
                    "memory_percent": round(float(info["memory_percent"] or 0), 2),
                    "status": info["status"] or "unknown",
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return sorted(records, key=lambda p: (p["cpu_percent"], p["memory_percent"]), reverse=True)[:limit]

    def sample(self, top_n: int = 8) -> SystemSnapshot:
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage(self.disk_path)
        return SystemSnapshot.now(
            cpu_percent=round(psutil.cpu_percent(interval=None), 2),
            memory_percent=round(memory.percent, 2),
            memory_used_mb=round(memory.used / 1024**2, 2),
            disk_percent=round(disk.percent, 2),
            disk_used_gb=round(disk.used / 1024**3, 2),
            process_count=len(psutil.pids()),
            top_processes=tuple(self._safe_processes(top_n)),
        )
