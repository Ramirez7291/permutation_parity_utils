"""Core permutation-parity logic.

The library reduces permutation parity to the same problem stated in two
shapes (one-shot and reusable). Two shapes, one decision: the one-shot
function is the simpler surface; the class saves re-derivation cost when
the same permutation is queried more than once. Both end up calling
``_cycle_lengths``, the single shared engine, so their results agree
by construction.
"""

from __future__ import annotations

from typing import List


def _validate(seq: List[int]) -> None:
    """Check that *seq* is a permutation of 0..n-1.

    Permutations here are always in one-line notation where element *i*
    is the image of *i*. Accepting duplicate, negative, or non-contiguous
    values would silently return a meaningless sign, so we reject them
    early — loud and now beats wrong and later.
    """
    n = len(seq)
    # ``range(n)`` is already sorted; comparing as sorted lists is the
    # cleanest way to confirm "the multiset is exactly {0,1,...,n-1}".
    if sorted(seq) != list(range(n)):
        raise ValueError(
            "sequence must be a permutation of range(len(seq)); "
            "got %r" % (seq,)
        )


def _cycle_lengths(seq: List[int]) -> List[int]:
    """Return the length of every cycle in *seq*.

    Cycles are discovered by a single linear sweep: visit each position,
    follow images until we return to the starting index, and mark every
    node we touch as visited so it is never walked again. Each position
    ends up in exactly one cycle, so a plain ``visited`` list of length
    *n* is enough — no hash set needed for indices in ``[0, n)``.
    """
    n = len(seq)
    visited = [False] * n
    lengths: List[int] = []
    for start in range(n):
        if visited[start]:
            continue
        length = 0
        cur = start
        while not visited[cur]:
            visited[cur] = True
            cur = seq[cur]
            length += 1
        lengths.append(length)
    return lengths


def parity(seq: List[int]) -> int:
    """Return +1 if *seq* is an even permutation, -1 if odd.

    A cycle of length *k* is a product of *k-1* transpositions, so the
    total transposition count is ``sum(k-1) = sum(k) - n``. Its sign is
    ``(-1)**count``. Counting by cycle lengths (rather than counting
    inversions) keeps the work O(n) — inversions would be O(n²) in the
    naive form and need a Fenwick tree to beat, all for no gain here.
    """
    _validate(seq)
    lengths = _cycle_lengths(seq)
    # transposition count = (sum of cycle lengths) - (number of cycles)
    # = n - (number of cycles). Written the first way because it mirrors
    # the mathematical identity directly and stays correct even if the
    # caller passes an empty list (0 - 0 = 0, even).
    transpositions = sum(lengths) - len(lengths)
    return 1 if transpositions % 2 == 0 else -1


class Permutation:
    """Thin object wrapper around :func:`parity`.

    Construction is the expensive part; ``sign`` caches the result so
    repeated queries on the same permutation are free. A ``KeyError``-
    free equality test (two plain ``==`` comparisons on tuples) makes the
    object hashable and usable as a dict key.
    """

    __slots__ = ("_seq", "_sign")

    def __init__(self, seq: List[int]) -> None:
        """Create a permutation from one-line notation *seq*.

        ``seq[i]`` is the image of ``i``. Validation runs here so any
        later call to :meth:`sign` is guaranteed safe.
        """
        _validate(seq)
        # Store a defensive copy: callers may mutate the list they
        # passed us, and a silent change of identity after construction
        # is exactly the kind of bug that is impossible to trace later.
        self._seq = list(seq)
        self._sign = parity(self._seq)

    @property
    def sequence(self) -> List[int]:
        """One-line notation of this permutation (a fresh list)."""
        return list(self._seq)

    @property
    def sign(self) -> int:
        """+1 for even, -1 for odd. Cached at construction."""
        return self._sign

    def is_even(self) -> bool:
        """True if this is an even permutation."""
        return self._sign == 1

    def is_odd(self) -> bool:
        """True if this is an odd permutation."""
        return self._sign == -1

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Permutation):
            return NotImplemented
        return self._seq == other._seq

    def __hash__(self) -> int:
        # ``sign`` is derived from ``_seq``, so hashing on ``_seq``
        # alone respects the ``a == b  =>  hash(a) == hash(b)`` rule.
        return hash(tuple(self._seq))

    def __repr__(self) -> str:
        return "Permutation(%r)" % (self._seq,)
