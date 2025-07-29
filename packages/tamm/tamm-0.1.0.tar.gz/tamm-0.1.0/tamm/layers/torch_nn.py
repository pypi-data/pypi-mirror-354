"""
This submodule contains |tamm| versions of layers from :mod:`torch.nn`.  These layers
have the same behavior as their :mod:`torch` counterparts.  The difference is that the
|tamm| versions also have a :class:`LayerBuilder` attached as the ``Builder`` class
attribute.
"""

import torch.nn as _nn

from tamm.layers.common import LayerMixin as _LayerMixin


class MaxPool2d(_nn.MaxPool2d, _LayerMixin):
    """A |tamm| version of :class:`torch.nn.MaxPool2d`."""


class AdaptiveAvgPool2d(_nn.AdaptiveAvgPool2d, _LayerMixin):
    """A |tamm| version of :class:`torch.nn.AdaptiveAvgPool2d`."""


class AvgPool2d(_nn.AvgPool2d, _LayerMixin):
    """A |tamm| version of :class:`torch.nn.AvgPool2d`."""


class BatchNorm2d(_nn.BatchNorm2d, _LayerMixin):
    """A |tamm| version of :class:`torch.nn.BatchNorm2d`."""


class GroupNorm(_nn.GroupNorm, _LayerMixin):
    """A |tamm| version of :class:`torch.nn.GroupNorm`."""


class Softmax(_nn.Softmax, _LayerMixin):
    """A |tamm| version of :class:`torch.nn.Softmax`."""
