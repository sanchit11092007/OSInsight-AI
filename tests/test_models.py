from monitoring.models import SystemSnapshot


def test_snapshot_serializes_to_dictionary() -> None:
    snapshot = SystemSnapshot.now(cpu_percent=1.0, memory_percent=2.0, memory_used_mb=3.0, disk_percent=4.0, disk_used_gb=5.0, process_count=6, top_processes=())
    assert snapshot.to_dict()["process_count"] == 6
