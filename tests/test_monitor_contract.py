from monitoring.system_monitor import SystemMonitor


def test_monitor_returns_snapshot_contract() -> None:
    snapshot = SystemMonitor().sample(top_n=1)
    assert 0 <= snapshot.cpu_percent <= 100
    assert snapshot.process_count >= 1
