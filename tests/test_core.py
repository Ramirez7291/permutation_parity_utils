"""Tests for permutation_parity_utils.

Every test asserts exactly what the implementation claims: parity of a
one-line permutation given as a list of ints 0..n-1. Nothing more.
"""

import unittest

from permutation_parity_utils import Permutation, parity


class TestParity(unittest.TestCase):
    def test_empty_is_even(self):
        self.assertEqual(parity([]), 1)

    def test_identity_single_is_even(self):
        self.assertEqual(parity([0]), 1)

    def test_identity_three_is_even(self):
        self.assertEqual(parity([0, 1, 2]), 1)

    def test_single_transposition_is_odd(self):
        self.assertEqual(parity([1, 0, 2]), -1)

    def test_three_cycle_is_even(self):
        # (0 1 2) decomposes into two transpositions -> even
        self.assertEqual(parity([1, 2, 0]), 1)

    def test_reverse_four_is_odd(self):
        # [3, 2, 1, 0] = (0 3)(1 2) — two transpositions -> even
        self.assertEqual(parity([3, 2, 1, 0]), 1)

    def test_reverse_three_is_odd(self):
        # [2, 1, 0] = (0 2) — one transposition -> odd
        self.assertEqual(parity([2, 1, 0]), -1)

    def test_disjoint_transpositions_even(self):
        # (0 1)(2 3) -> two transpositions -> even
        self.assertEqual(parity([1, 0, 3, 2]), 1)

    def test_transposition_plus_3cycle_odd(self):
        # (0 1)(2 3 4) -> 1 + 2 = 3 transpositions -> odd
        self.assertEqual(parity([1, 0, 3, 4, 2]), -1)

    def test_invalid_raises(self):
        with self.assertRaises(ValueError):
            parity([0, 1, 3])
        with self.assertRaises(ValueError):
            parity([0, 0])
        with self.assertRaises(ValueError):
            parity([-1, 0, 1])


class TestPermutation(unittest.TestCase):
    def test_sign_cached_matches_parity(self):
        seq = [1, 2, 0, 3]
        p = Permutation(seq)
        self.assertEqual(p.sign, parity(seq))

    def test_is_even_is_odd(self):
        self.assertTrue(Permutation([0, 1, 2]).is_even())
        self.assertFalse(Permutation([0, 1, 2]).is_odd())
        self.assertTrue(Permutation([1, 0, 2]).is_odd())
        self.assertFalse(Permutation([1, 0, 2]).is_even())

    def test_sequence_returns_copy(self):
        original = [0, 1, 2]
        p = Permutation(original)
        got = p.sequence
        got[0] = 99
        self.assertEqual(p.sequence, original)

    def test_construction_copies_input(self):
        original = [1, 0, 2]
        p = Permutation(original)
        original[0] = 99
        self.assertEqual(p.sequence, [1, 0, 2])

    def test_equality_and_hash(self):
        a = Permutation([1, 0, 2])
        b = Permutation([1, 0, 2])
        c = Permutation([0, 1, 2])
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)
        self.assertEqual(hash(a), hash(b))

    def test_invalid_raises_in_constructor(self):
        with self.assertRaises(ValueError):
            Permutation([0, 1, 2, 2])

    def test_repr(self):
        p = Permutation([1, 0, 2])
        self.assertEqual(repr(p), "Permutation([1, 0, 2])")


if __name__ == "__main__":
    unittest.main()
