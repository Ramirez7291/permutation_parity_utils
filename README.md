# permutation_parity_utils

Determines the sign (+1 for even, -1 for odd) of a permutation given in one-line notation, using its cycle decomposition.

```python
from permutation_parity_utils import parity, Permutation

print(parity([1, 0, 2]))            # -1  (one transposition: odd)
print(parity([1, 2, 0]))            # +1  (3-cycle = two transpositions: even)

p = Permutation([2, 0, 1])
print(p.sign)                       # +1
print(p.is_odd())                   # False
```

The library exists because determinant and orientation code often needs a parity check that is correct, dependency-free, and fast enough that it never shows up in a profile. Cycle decomposition runs in O(n); counting inversions would be O(n²) for no real-world benefit at the sizes these problems actually hit.

The edge to be aware of: input must be a permutation of `range(len(seq))` — duplicates, gaps, or negative values raise `ValueError`. The empty list is treated as the identity (even). Construction of a `Permutation` validates and caches the sign, so repeated `sign` queries are free; the class also makes a defensive copy of the input list, so mutating the original after construction has no effect.

Exported names: `parity(seq: list[int]) -> int` and `Permutation(seq)` with `.sign`, `.is_even()`, `.is_odd()`, `.sequence`.
