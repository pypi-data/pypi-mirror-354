"""
tamm.ao
-------

This module implements building blocks for architecture optimizations, similar to
:mod:`torch.ao`.  Activation quantization is one type of supported optimization.

.. automodule:: tamm.ao.arch_optimizers

.. automodule:: tamm.ao.layers

.. automodule:: tamm.ao.utils
"""

from tamm.ao import arch_optimizers, layers, utils
from tamm.ao.arch_optimizers import ArchOptimizer, KVQuantArchOptimizer

__all__ = [
    "ArchOptimizer",
    "KVQuantArchOptimizer",
    "arch_optimizers",
    "layers",
    "utils",
]
