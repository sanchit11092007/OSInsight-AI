# Monitoring Design

`SystemMonitor` gathers CPU, virtual memory, disk, and process data through psutil. It catches unavailable process entries so a single restricted process cannot stop a system sample.
