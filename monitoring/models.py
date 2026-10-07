from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class SystemSnapshot:
    timestamp: str
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    disk_percent: float
    disk_used_gb: float
    process_count: int
    top_processes: tuple[dict, ...]

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def now(cls, **values: object) -> "SystemSnapshot":
        return cls(timestamp=datetime.now(timezone.utc).isoformat(), **values)
