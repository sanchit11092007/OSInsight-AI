# User Guide

1. Install dependencies from `requirements.txt` in a Python virtual environment.
2. Run `python main.py`.
3. Keep the dashboard open long enough to collect a trend. The status line shows the next-step CPU and memory estimate.
4. Review the ranked process list before closing applications. Process CPU percentages reflect the last psutil interval and may initially appear low.
5. Use the export buttons to create files under `reports/`.

The tool is an advisory monitor. It does not terminate processes, change operating-system settings, or send telemetry over a network.
