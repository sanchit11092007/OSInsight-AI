# Architecture Decisions

## ADR 001 Local CSV history

CSV keeps the first version transparent, portable, and easy to inspect. A database can replace it when history becomes large.

## ADR 002 Explainable forecast

Linear regression provides an understandable baseline for short monitoring windows.
