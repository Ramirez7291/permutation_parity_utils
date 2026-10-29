"""permutation_parity_utils public surface.

Re-exports ``parity`` and ``Permutation`` from the internal ``core``
module. Keeping ``__init__`` as a thin re-export layer means the only
thing the package commits to is its import surface — callers never
touch ``core`` directly, so internal restructuring stays free.
"""

from .core import Permutation, parity

__all__ = ["Permutation", "parity"]
