from __future__ import annotations

import csv
from pathlib import Path

from .models import SystemSnapshot


class DataLogger:
    fields = ("timestamp", "cpu_percent", "memory_percent", "memory_used_mb", "disk_percent", "disk_used_gb", "process_count")

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, snapshot: SystemSnapshot) -> None:
        new_file = not self.path.exists()
        with self.path.open("a", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=self.fields)
            if new_file:
                writer.writeheader()
            writer.writerow({field: snapshot.to_dict()[field] for field in self.fields})
