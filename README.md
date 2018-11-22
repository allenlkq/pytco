# pytco
Python tail call optimization by means of trampoline.
The function `tail_rec` converts a recursive function to an iterative equivalent at runtime.
```python
from tail_rec import tail_rec

def factorial(n, acc=1):
    if n == 1:
        return acc
    return factorial(n-1, n*acc)

global_context = globals()
local_context = locals()
factorial2 = tail_rec(factorial, global_context, local_context)
print(factorial2(10000))
```