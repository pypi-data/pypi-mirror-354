"""
layers.norm
-----------

This module provides norm layers and a factory function for creating norm layers.

.. autoclass:: tamm.layers.BatchNorm
    :show-inheritance:

.. autoclass:: tamm.layers.LayerNorm
    :show-inheritance:

.. autoclass:: tamm.layers.RMSNorm
    :show-inheritance:

.. autofunction:: tamm.layers.norm.create_norm_builder
"""

import abc as _abc
from typing import Iterable as _Iterable
from typing import List as _List
from typing import Optional as _Optional
from typing import Tuple as _Tuple
from typing import Union as _Union

import torch as _torch
from torch import nn as _nn
from torch.nn.modules.batchnorm import _BatchNorm as _PyTorchBatchNorm

from tamm.layers import functional as _tamm_F
from tamm.layers.common import LayerMixin as _LayerMixin
from tamm.typing import OptionalModuleOrBuilder as _OptionalModuleOrBuilder


class _BaseNorm(_nn.Module, _abc.ABC):
    """
    A Base class for norm layers.

    Args:
        features_shape (:obj:`tuple` of :obj:`int`): The shape of the feature (channel)
            dimension(s).
        bias (:obj:`bool`): A flag for including a bias parameter.  Defaults to
            ``False``.
        dim (:obj:`int` or :obj:`tuple` of :obj:`int`): The feature dimension index
            (or indices) to scale using the ``weight`` parameter.  Defaults to ``-1``,
            corresponding to channels-last inputs.  Use ``1`` for channels-first inputs.
        device: The device of the parameters.
        dtype: The dtype of the parameters.
    """

    _IMPL_CHANNELS_DIM = -1
    """The index of the features dimension for :meth:`_forward_impl`."""

    def __init__(
        self,
        features_shape: _Optional[_Iterable[int]] = None,
        *,
        dim: _Union[int, _Iterable[int]] = -1,
        eps: float = 1e-5,
        bias: bool = False,
        device=None,
        dtype=None,
    ):
        _nn.Module.__init__(self)

        if features_shape is not None:
            features_shape = tuple(features_shape)
        self._features_shape = features_shape

        if not isinstance(dim, int):
            dim = tuple(dim)
        self.dim = dim

        self.eps = eps

        if self._features_shape is not None:
            self.weight = _nn.Parameter(
                _torch.empty(self._features_shape, device=device, dtype=dtype)
            )
        else:
            self.weight = None

        if bias:
            self.bias = _nn.Parameter(
                _torch.empty(self._features_shape, device=device, dtype=dtype)
            )
        else:
            self.bias = None

        self.reset_parameters()

    def reset_parameters(self) -> None:
        if self.weight is not None:
            _nn.init.ones_(self.weight)
        if self.bias is not None:
            _nn.init.zeros_(self.bias)

    def _permute(
        self, x: _torch.Tensor
    ) -> _Tuple[_torch.Tensor, _Optional[_List[int]]]:
        """
        Permutes the dimensions which will be normalized
        on to dimensions start from self._IMPL_CHANNELS_DIM.
        Returns a tuple with the permuted tensors and a list of indices
        which indicate how the permutation was performed. If the `_IMPL_CHANNELS_DIM`
        is a single dimension, returns None for the second return value.
        """
        if self.dim == self._IMPL_CHANNELS_DIM:
            return x, None
        if isinstance(self.dim, int):
            return x.transpose(self.dim, self._IMPL_CHANNELS_DIM), None

        # Permute multiple dimensions to the last dimensions
        norm_dim_list = sorted([d if d >= 0 else d + len(x.shape) for d in self.dim])
        remained_dim_list = [
            idx for idx in range(len(x.shape)) if idx not in norm_dim_list
        ]
        perm = remained_dim_list + norm_dim_list
        return _torch.permute(x, perm), perm

    def _unpermute(
        self, x: _torch.Tensor, perm: _Optional[_Iterable[int]] = None
    ) -> _torch.Tensor:
        if self.dim == self._IMPL_CHANNELS_DIM:
            return x
        if isinstance(self.dim, int):
            return x.transpose(self.dim, self._IMPL_CHANNELS_DIM)
        return _tamm_F.inverse_permute(x, perm)

    @_abc.abstractmethod
    def _forward_impl(self, x: _torch.Tensor) -> _torch.Tensor:
        """Normalize x assuming the features dimension of x is _IMPL_CHANNELS_DIM"""

    # pylint: disable=redefined-builtin
    def forward(self, input: _torch.Tensor) -> _torch.Tensor:
        x, perm = self._permute(input)
        x = self._forward_impl(x)
        return self._unpermute(x, perm)


class LayerNorm(_BaseNorm, _LayerMixin):
    """LayerNorm with optional bias param."""

    def __init__(
        self,
        normalized_shape: _Iterable[int],
        *,
        dim: _Union[int, _Iterable[int]] = -1,
        eps: float = 1e-5,
        bias: bool = False,
        cast_dtype: _Optional[_torch.dtype] = _torch.float32,
        device=None,
        dtype=None,
    ):
        super().__init__(
            features_shape=normalized_shape,
            dim=dim,
            eps=eps,
            bias=bias,
            device=device,
            dtype=dtype,
        )
        self.cast_dtype = cast_dtype

    def _forward_impl(self, x: _torch.Tensor) -> _torch.Tensor:
        return _tamm_F.layer_norm(
            x,
            normalized_shape=self._features_shape,
            weight=self.weight,
            bias=self.bias,
            eps=self.eps,
            cast_dtype=self.cast_dtype,
        )

    def extra_repr(self) -> str:
        shape = tuple(self._features_shape)
        return (
            f"normalized_shape={shape}, dim={self.dim}, eps={self.eps}, "
            f"bias={self.bias is not None}, cast_dtype={self.cast_dtype}"
        )


class RMSNorm(_BaseNorm, _LayerMixin):
    """RMSNorm with no bias param."""

    def __init__(
        self,
        normalized_shape: _Iterable[int],
        *,
        dim: _Union[int, _Iterable[int]] = -1,
        eps: float = 1e-5,
        bias: bool = False,
        cast_dtype: _Optional[_torch.dtype] = _torch.float32,
        device=None,
        dtype=None,
    ):
        super().__init__(
            features_shape=normalized_shape,
            dim=dim,
            eps=eps,
            bias=bias,
            device=device,
            dtype=dtype,
        )
        self.cast_dtype = cast_dtype

    def _forward_impl(self, x: _torch.Tensor) -> _torch.Tensor:
        x = _tamm_F.rms_norm(
            x,
            self._features_shape,
            weight=self.weight,
            bias=self.bias,
            eps=self.eps,
            cast_dtype=self.cast_dtype,
        )
        return x

    def extra_repr(self) -> str:
        shape = tuple(self._features_shape)
        return (
            f"normalized_shape={shape}, dim={self.dim}, eps={self.eps}, "
            f"bias={self.bias is not None}, cast_dtype={self.cast_dtype}"
        )


class VectorizedRMSNorm(RMSNorm):
    def __init__(
        self,
        normalized_shape: _Iterable[int],
        vec_dim: int,
        vec_indx: int,
        *,
        dim: _Union[int, _Iterable[int]] = -1,
        eps: float = 1e-5,
        bias: bool = False,
        cast_dtype: _Optional[_torch.dtype] = _torch.float32,
        device=None,
        dtype=None,
    ):
        # TODO: actually vectorize this function
        new_shape = (vec_dim,) + tuple(normalized_shape)
        super(RMSNorm, self).__init__(
            features_shape=new_shape,
            dim=dim,
            eps=eps,
            bias=bias,
            device=device,
            dtype=dtype,
        )

        self.vec_dim = vec_dim
        self.vec_indx = vec_indx
        self.cast_dtype = cast_dtype

    # pylint: disable=redefined-builtin
    def forward(self, input: _torch.Tensor) -> _torch.Tensor:
        to_shape = list(
            ((1,) * (len(input.shape) - len(self._features_shape) + 1))
            + self._features_shape[1:]
        )
        to_shape[self.vec_indx] = self.vec_dim
        return _tamm_F.batched_rms_norms(
            input,
            self._features_shape[1:],
            weight=self.weight.reshape(to_shape),
            bias=None if self.bias is None else self.bias.reshape(to_shape),
            cast_dtype=self.cast_dtype,
        )


class BatchNorm(_BaseNorm, _LayerMixin, _PyTorchBatchNorm):
    """BatchNorm."""

    # Inherit from _PyTorchBatchNorm to extend functionality.
    #
    # Specifically, torch uses isinstance(module, _PyTorchBatchNorm),
    # in FSDP MixedPrecision to exclude some layers from low-precision
    # computation.
    #
    # We want this to return True for our BatchNorm layer too,
    # to exclude it from low precision computation.

    def __init__(
        self,
        features_shape: _Iterable[int],
        *,
        dim: _Optional[int] = -1,
        momentum: float = 0.1,
        eps: float = 1e-5,
        bias: bool = False,
        cast_dtype: _Optional[_torch.dtype] = _torch.float32,
        device=None,
        dtype=None,
    ):
        super().__init__(
            features_shape=features_shape,
            dim=dim,
            eps=eps,
            bias=bias,
            device=device,
            dtype=dtype,
        )
        self.momentum = momentum
        self.cast_dtype = cast_dtype
        self.register_buffer("running_mean", _torch.zeros_like(self.weight))
        self.register_buffer("running_var", _torch.ones_like(self.weight))
        self.register_buffer("num_batches_tracked", _torch.tensor(0, device=device))

    def _forward_impl(self, x: _torch.Tensor) -> _torch.Tensor:
        dim = (self.dim,) if not isinstance(self.dim, tuple) else self.dim

        # Flatten features then move features to dimension 1
        x, shape = x.flatten(start_dim=-len(dim)), x.shape[-len(dim) :]
        running_mean = self.running_mean.flatten()
        running_var = self.running_var.flatten()
        weight = self.weight.flatten()
        bias = self.bias.flatten() if self.bias is not None else None
        x = x.transpose(-1, 1)

        # Batch norm
        if self.training:
            self.num_batches_tracked.add_(1)
        normed_x = _tamm_F.batch_norm(
            x,
            running_mean=running_mean,
            running_var=running_var,
            weight=weight,
            bias=bias,
            training=self.training,
            momentum=self.momentum,
            eps=self.eps,
            cast_dtype=self.cast_dtype,
        )

        # Move features back to last dimension and unflatten features
        normed_x = normed_x.transpose(-1, 1)
        return normed_x.unflatten(self._IMPL_CHANNELS_DIM, shape)

    def extra_repr(self) -> str:
        shape = tuple(self._features_shape)
        return (
            f"features_shape={shape}, momentum={self.momentum}, dim={self.dim}, "
            f"eps={self.eps}, bias={self.bias is not None}, "
            f"cast_dtype={self.cast_dtype}"
        )

    @property
    def track_running_stats(self):
        return True

    @property
    def affine(self):
        return True


class L2Norm(_BaseNorm, _LayerMixin):
    def __init__(
        self,
        *,
        dim: _Optional[int] = -1,
        eps: float = 1e-5,
        cast_dtype: _Optional[_torch.dtype] = _torch.float32,
    ):
        super().__init__(dim=dim, eps=eps)
        self.cast_dtype = cast_dtype

    def _forward_impl(self, x: _torch.Tensor):
        return _tamm_F.l2_norm(x, eps=self.eps, cast_dtype=self.cast_dtype)

    def extra_repr(self) -> str:
        return f"eps={self.eps}, cast_dtype={self.cast_dtype}, dim={self.dim}"


def create_norm_builder(
    features_shape: _Tuple[int],
    spec: _Union[str, _OptionalModuleOrBuilder] = "layer_norm",
    *,
    bias: bool = False,
    dim: int = -1,
    eps: float = 1e-5,
    device=None,
    dtype=None,
):
    """
    Creates and returns a builder for a norm layer.

    Args:
        features_shape (:obj:`tuple` of :obj:`int`): The shape of the feature (channel)
            dimension(s).
        spec:
            Typically a :obj:`str` from the choices ``"layer_norm"``, ``"rms_norm"``,
            or ``"batch_norm"``.  This can also be ``None`` or a module builder,
            in which case the function returns spec directly.
        dim (:obj:`int` or :obj:`tuple` of :obj:`int`): The feature dimension index
            (or indices) to scale using the ``weight`` parameter.  Defaults to ``-1``,
            corresponding to channels-last inputs.  Use ``1`` for channels-first inputs.
        eps (:obj:`float`): The norm's epsilon parameter.  Defaults to ``1e-5``.
        bias (:obj:`bool`): A flag for including a bias parameter.  Defaults to
            ``False``.
        device: The device for parameters.
        dtype: The dtype for parameters.
    """
    if not isinstance(spec, str):
        return spec

    kwargs = {"dim": dim, "bias": bias, "eps": eps, "device": device, "dtype": dtype}
    if spec == "batch_norm":
        return BatchNorm.Builder(features_shape, **kwargs)
    if spec == "layer_norm":
        return LayerNorm.Builder(features_shape, **kwargs)
    if spec == "rms_norm":
        return RMSNorm.Builder(features_shape, **kwargs)
    raise ValueError(f"spec {spec} not recognized")
