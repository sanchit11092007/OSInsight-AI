# Health Score Method

The health score starts from 100 and subtracts a weighted resource pressure value. CPU has a 0.42 weight, memory has 0.36, and disk has 0.22. The result is clipped to a usable 0 to 100 range.
