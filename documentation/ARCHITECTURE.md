# Architecture

OSInsight-AI separates hardware and operating-system access from analytics and presentation. `SystemMonitor` is the only component that queries `psutil`. It produces an immutable `SystemSnapshot`, which the logger serializes to a portable CSV schema. The dashboard retains a bounded in-memory frame for responsive rendering, while the analytics engine works from the same schema.

The forecast deliberately uses linear regression over a recent sliding window. This approach remains transparent for a university demonstration, needs no external training service, and makes the effect of the observed trend understandable. Threshold rules convert the forecast into operational recommendations.

All diagrams are stored in `diagrams/` as Mermaid source so they remain editable in GitHub.
