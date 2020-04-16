# Lazer-project-2020

## How To Run

```python
from reader import Reader
from printer import output_img
from solver import solve

# read data
start, checkpoints = Reader(f'maps/{map}.bff')

# print initial map
output_img(start, checkpoints)

# solve
solution = solve(start, checkpoints)

# print solution
output_img(solution, checkpoints)
```
