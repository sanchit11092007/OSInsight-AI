# Test Cases

| ID | Area | Input | Expected result |
|---|---|---|---|
| TC01 | Data cleaning | Non-numeric CPU row | Row is removed |
| TC02 | Analytics | Empty history | Healthy score of 100 |
| TC03 | Bottleneck detection | Rising CPU values above 80% | CPU bottleneck and recommendation |
| TC04 | Monitor | Running host | Snapshot has CPU, memory, disk, and processes |
| TC05 | Export | Analytics result | PDF and CSV files are written |

Run the automated subset with `python -m pytest -q`.
