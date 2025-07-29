"""
transformer.layer_sequence
^^^^^^^^^^^^^^^^^^^^^^^^^^

This submodule implements the sequence of transformer layers within a
:mod:`transformer stack <tamm.layers.transformer.stack>`.

.. autoclass:: tamm.layers.transformer.BaseTransformerLayerSequence
    :members:

.. autoclass:: tamm.layers.KVReuseTransformerLayerSequence
    :show-inheritance:

.. autoclass:: tamm.layers.TransformerLayerSequence
    :show-inheritance:

.. autoclass:: tamm.layers.UniformTransformerLayerSequence
    :show-inheritance:
"""

from tamm.layers.transformer.layer_sequence.common import BaseTransformerLayerSequence
from tamm.layers.transformer.layer_sequence.kv_reuse import (
    KVReuseTransformerLayerSequence,
)
from tamm.layers.transformer.layer_sequence.uniform import (
    UniformTransformerLayerSequence,
)
from tamm.layers.transformer.layer_sequence.vanilla import TransformerLayerSequence
