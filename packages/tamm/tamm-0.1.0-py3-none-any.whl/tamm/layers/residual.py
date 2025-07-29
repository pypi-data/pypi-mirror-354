"""
Implements a residual connection layers for :class:`tamm.layers.Sequential`.
"""

from typing import Optional as _Optional

import torch as _torch
import torch.nn as _nn

from tamm import _helpers
from tamm.layers import activation as _activation
from tamm.layers.common import LayerMixin as _LayerMixin
from tamm.typing import OptionalModuleOrBuilder as _OptionalModuleOrBuilder


class ResidualAdd(_nn.Module, _LayerMixin):
    """
    A simple module for implementing residual connections.  The forward function takes
    ``input`` and ``residual_input`` arguments and returns their sum.
    """

    def __init__(self):
        super().__init__()  # Needed because builder doesn't support *args

    def forward(
        self,
        input: _torch.Tensor,  # pylint: disable=redefined-builtin
        residual_input: _torch.Tensor,
    ) -> _torch.Tensor:
        return input + residual_input


class ShortcutAddActResidualConnection(_nn.Module, _LayerMixin):
    """
    A residual connection that applies a shortcut transformation to the residual
    inputs, then adds the shortcut result to outputs, and finally applies an activation
    transform to the sum.
    """

    def __init__(
        self,
        shortcut: _OptionalModuleOrBuilder = None,
        activation: _Optional[_activation.ActivationSpecType] = None,
    ):
        super().__init__()
        self.shortcut = _helpers.maybe_build_module(shortcut)
        self.activation = _activation.create_activation_layer(activation)

    # pylint: disable=redefined-builtin
    def forward(
        self,
        input: _torch.Tensor,
        residual_input: _torch.Tensor,
    ) -> _torch.Tensor:
        if self.shortcut is not None:
            residual_input = self.shortcut(residual_input)
        x = input + residual_input
        if self.activation is None:
            return x
        return self.activation(x)


class GatedActivationResidualConnection(_nn.Module, _LayerMixin):
    """
    A residual connection that applies gated activation to the residual inputs (using
    the non-residual inputs for gating).
    """

    def __init__(self, activation: _activation.ActivationSpecType):
        super().__init__()
        self.activation = _activation.create_activation_layer(activation)

    # pylint: disable=redefined-builtin
    def forward(
        self,
        input: _torch.Tensor,
        residual_input: _torch.Tensor,
    ) -> _torch.Tensor:
        return self.activation(gate_input=input, input=residual_input)
