from monitoring.data_logger import DataLogger
from monitoring.models import SystemSnapshot


def test_logger_writes_header_and_snapshot(tmp_path) -> None:
    target = tmp_path / "history.csv"
    DataLogger(target).append(SystemSnapshot.now(cpu_percent=1, memory_percent=2, memory_used_mb=3, disk_percent=4, disk_used_gb=5, process_count=6, top_processes=()))
    assert "cpu_percent" in target.read_text(encoding="utf-8")
