"""
Provides activation layers.
"""

import abc as _abc
from typing import Callable as _Callable
from typing import Union as _Union

import torch as _torch
import torch.nn as _nn
from torch.nn import functional as _F

from tamm.layers import functional as _tamm_F
from tamm.layers import lambda_layer as _lambda_layer
from tamm.layers.common import LayerMixin as _LayerMixin
from tamm.utils import registry as _registry_module

ActivationSpecType = _Union[str, list, tuple, _Callable, "Activation"]

ACTIVATION_REGISTRY = _registry_module.Registry("Activations")


def create_activation_layer(
    spec: _Union[ActivationSpecType, None]
) -> _Union["Activation", None]:
    """
    Factory function for creating activation layers from a variety of possible
    specification types.

    Args:
        spec: The specification for the activation.  If the arg is a valid key to the
            activation registry (such as ``"gelu"`` or ``"swi_glu"``), then the function
            creates the layer from the registry and returns it.  The ``spec`` arg can
            also be (1) an :obj:`Activation` instance, in which case it becomes the
            return object, (2) a callable that takes no arguments, in which case the
            returned layer is the result of the callable, or (3) the name of a function
            from ``torch.nn.functional``, in which case the function returns a
            :obj:`LambdaActivation` that wraps that function.

    Returns:
        An :obj:`Activation` instance corresponding to ``spec``.
    """
    if spec is None:
        return None
    if ACTIVATION_REGISTRY.is_valid_key(spec):
        return ACTIVATION_REGISTRY.create(spec)
    if isinstance(spec, Activation):
        return spec
    if callable(spec):
        return spec()
    is_torch_functional_name = isinstance(spec, str) and hasattr(_F, spec)
    if is_torch_functional_name:
        function = getattr(_F, spec)
        return LambdaActivation(function)
    return ACTIVATION_REGISTRY.create(spec)


class Activation(_nn.Module, _abc.ABC, _LayerMixin):
    """Abstract base class for activation layers."""

    def __init__(self):
        super().__init__()  # needed to remove nn.Module args from tamm Builder

    def __init_subclass__(cls, key=None, description=None, **kwargs):
        """Automatically register subclasses that provide a key."""
        super().__init_subclass__(**kwargs)
        if key is None:
            return
        ACTIVATION_REGISTRY.register(cls, key=key, description=description)

    @property
    def is_gated(self):
        """
        A flag with value ``True`` if the layer expects two tensors (with the same
        shape) as input and ``False`` otherwise.
        """
        return False

    @_abc.abstractmethod
    # pylint: disable-next=all
    def forward(self, input):
        """Subclasses implement forward"""


class LambdaActivation(_lambda_layer.Lambda, Activation):
    """
    Activation layer that wraps a callable function for :meth:`forward`.

    Args:
        function (:obj:`Callable`): A callable function that takes inputs to the forward
            function and returns the output of forward.
    """

    def __init__(self, function: _Callable):
        _lambda_layer.Lambda.__init__(self, function)
        Activation.__init__(self)


class GatedActivation(Activation):
    """
    Abstract base class for gated activation layers.  Gated activations receive a second
    input for gating.
    """

    @property
    def is_gated(self):
        return True

    @_abc.abstractmethod
    # pylint: disable-next=all
    def forward(self, gate_input, input):
        """Subclasses implement forward"""


class Tanh(_nn.Tanh, Activation, key="tanh"):
    """Tanh activation."""

    def __init__(self):
        _nn.Tanh.__init__(self)
        Activation.__init__(self)


class ReLU(_nn.ReLU, Activation, key="relu"):
    """ReLU activation."""

    def __init__(self):
        _nn.ReLU.__init__(self)
        Activation.__init__(self)


class GELU(_nn.GELU, Activation, key="gelu"):
    """GELU activation with tanh approximation by default."""

    def __init__(self, approximate="tanh"):
        _nn.GELU.__init__(self, approximate=approximate)
        Activation.__init__(self)


class SiLU(_nn.SiLU, Activation, key="silu"):
    """SiLU activation."""

    def __init__(self):
        _nn.SiLU.__init__(self)
        Activation.__init__(self)


class QuickGELU(Activation, key="quick_gelu"):
    """
    Quick GELU activation, which approximates GELU using ``x * sigmoid(1.702 * x)``.
    """

    def forward(self, input):  # pylint: disable=all
        return input * _torch.sigmoid(1.702 * input)


class GLU(GatedActivation, key="glu"):
    """Gated activation with sigmoid activation function (gated linear unit)."""

    # pylint: disable-next=all
    def forward(self, gate_input, input):
        return input * _torch.sigmoid(gate_input)


class SwiGLU(GatedActivation, key="swi_glu"):
    """GLU variant that uses Swish nonlinear function in place of sigmoid."""

    # pylint: disable-next=all
    def forward(self, gate_input, input):
        return _tamm_F.swi_glu(gate_input, input)


class GEGLU(GatedActivation, key="geglu"):
    """
    Implements `GeGLU < https://arxiv.org/abs/2002.05202 >`__,
    a variant of the gated linear unit activation function
    This implementation mirrors diffusers.models.activations.GEGLU.
    """

    # pylint: disable-next=all
    def forward(self, gate_input, input):
        return _tamm_F.geglu(gate_input, input)
