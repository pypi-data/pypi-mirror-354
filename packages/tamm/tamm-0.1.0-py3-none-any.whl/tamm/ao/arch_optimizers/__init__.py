"""
Architecture optimizers
=======================

Architecture optimizers are high-level objects that attach layers from
:mod:`tamm.ao.layers` to |tamm| models.  They are also configurable and
JSON-serializable.


.. autoclass:: tamm.ao.arch_optimizers.ArchOptimizer
    :members:

.. autoclass:: tamm.ao.arch_optimizers.KVQuantArchOptimizer
    :members:
"""

from tamm.ao.arch_optimizers.common import ArchOptimizer
from tamm.ao.arch_optimizers.kv_quant import KVQuantArchOptimizer

__all__ = ["ArchOptimizer", "KVQuantArchOptimizer"]
