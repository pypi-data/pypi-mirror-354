from typing import Dict as _Dict
from typing import List as _List
from typing import Optional as _Optional
from typing import Tuple as _Tuple
from typing import Union as _Union

import torch as _torch
from torch.nn import functional as _F

from tamm import _helpers
from tamm.utils import _torch_compatibility


def rms_norm(
    tensor: _torch.Tensor,
    normalized_shape: _Tuple[int],
    *,
    weight: _torch.Tensor = None,
    bias: _torch.Tensor = None,
    eps: float = 1e-05,
    cast_dtype: _Optional[_torch.dtype] = _torch.float32,
) -> _torch.Tensor:
    """Applies RMS normalization."""
    input_dtype = tensor.dtype
    with _helpers.autocast_disabled(tensor.device):
        if cast_dtype is not None:
            tensor = tensor.type(cast_dtype)
        tensor = _torch_compatibility.rms_norm(
            tensor, normalized_shape=normalized_shape, weight=weight, eps=eps
        )
        if bias is not None:
            tensor = tensor + bias
        return tensor.type(input_dtype)


def batched_rms_norms(
    tensor: _torch.Tensor,
    normalized_shape: _Tuple[int],
    *,
    weight: _torch.Tensor = None,
    bias: _torch.Tensor = None,
    eps: float = 1e-05,
    cast_dtype: _Optional[_torch.dtype] = _torch.float32,
) -> _torch.Tensor:
    """
    Applies RMS normalization.  This the same a :func:`rms_norm`, but the weight
    and bias tensors can have more dimensions than ``len(normalized_shape)``.
    """
    input_dtype = tensor.dtype
    with _helpers.autocast_disabled(tensor.device):
        if cast_dtype is not None:
            tensor = tensor.type(cast_dtype)
        tensor = _torch_compatibility.rms_norm(
            tensor, normalized_shape=normalized_shape, eps=eps
        )
        if weight is not None and bias is not None:
            tensor = _torch.addcmul(bias, tensor, weight)
        elif weight is not None:
            tensor = tensor * weight
        elif bias is not None:
            tensor = tensor + bias
        return tensor.type(input_dtype)


def layer_norm(
    tensor: _torch.Tensor,
    normalized_shape: _List[int],
    *,
    weight: _Union[_torch.Tensor, None] = None,
    bias: _Union[_torch.Tensor, None] = None,
    eps: float = 1e-05,
    cast_dtype: _Optional[_torch.dtype] = _torch.float32,
) -> _torch.Tensor:
    with _helpers.autocast_disabled(tensor.device):
        input_dtype = tensor.dtype
        if cast_dtype is not None:
            tensor = tensor.type(cast_dtype)
        if weight is not None:
            weight = weight.type_as(tensor)
        if bias is not None:
            bias = bias.type_as(tensor)
        result = _torch.nn.functional.layer_norm(
            tensor, normalized_shape=normalized_shape, weight=weight, bias=bias, eps=eps
        )
        return result.type(input_dtype)


def batch_norm(
    tensor: _torch.Tensor,
    *,
    running_mean: _Union[_torch.Tensor, None],
    running_var: _Union[_torch.Tensor, None],
    weight: _Union[_torch.Tensor, None] = None,
    bias: _Union[_torch.Tensor, None] = None,
    training: bool = False,
    momentum: float = 0.1,
    eps: float = 1e-05,
    cast_dtype: _Optional[_torch.dtype] = _torch.float32,
) -> _torch.Tensor:
    with _helpers.autocast_disabled(tensor.device):
        input_dtype = tensor.dtype
        if cast_dtype is not None:
            tensor = tensor.type(cast_dtype)
        result = _torch.nn.functional.batch_norm(
            tensor,
            running_mean=running_mean,
            running_var=running_var,
            weight=weight,
            bias=bias,
            training=training,
            momentum=momentum,
            eps=eps,
        )
        return result.type(input_dtype)


# pylint: disable-next=redefined-builtin
def swi_glu(gate_input, input):
    """
    GLU variant that uses Swish nonlinear function in place of sigmoid.

    Args:
        gate_input (:obj:`torch.Tensor`): The input to the silu function.
        input (:obj:`torch.Tensor`): The input to scale by the silu output.

    Returns:
        The activation tensor.
    """
    return input * _F.silu(gate_input)


def l2_norm(
    tensor: _torch.Tensor,
    eps: float = 1e-05,
    cast_dtype: _Optional[_torch.dtype] = _torch.float32,
) -> _torch.Tensor:
    if cast_dtype is not None:
        cast_tensor = tensor.type(cast_dtype)
    else:
        cast_tensor = tensor

    return _F.normalize(cast_tensor, dim=-1, eps=eps)


def rearrange_embeddings_to_channels_first(embeddings, *, unflattened_shape):
    embeddings = embeddings.movedim(1, -1)
    return embeddings.reshape(*embeddings.shape[:-1], *unflattened_shape)


def rearrange_embeddings_from_channels_first(tensor):
    return tensor.flatten(start_dim=2).movedim(1, -1)


def geglu(gate_input, input):  # pylint: disable=redefined-builtin
    """
    GLU variant that uses GELU function in place of sigmoid.

    Args:
        gate_input (:obj:`torch.Tensor`): The input to the GELU function.
        input (:obj:`torch.Tensor`): The input to scale by the GELU output.

    Returns:
        The activation tensor.
    """
    # pylint: disable=not-callable
    return input * _F.gelu(gate_input, approximate="tanh")


def add_batch_dim(tensor: _torch.Tensor, batch_size: int = 1) -> _torch.Tensor:
    """
    Adds a new first dimension to ``tensor`` and then repeats it ``batch_size`` times
    along that dimension.
    """
    tile_shape = (batch_size,) + (1,) * tensor.ndim
    return tensor.tile(tile_shape)


def maybe_flatten_sequence(
    sequence: _Union[_torch.Tensor, _Dict[str, _torch.Tensor]], end_dim: int = -1
) -> _torch.Tensor:
    """
    If ``sequence`` is a tensor, this function flattens the dimensions between ``1``
    and ``end_dim``.  If ``sequence`` is a :obj:`dict`, this function flattens each
    of its values and then concatenates the flat tensors along dimension 1 in the order
    that they appear in the :obj:`dict`.  If ``sequence`` is neither a tensor nor a
    :obj:`dict`, this function simply returns the ``sequence`` unchanged.
    """
    if _torch.is_tensor(sequence):
        end_dim = end_dim % sequence.ndim
        if end_dim > 1:
            return sequence.flatten(start_dim=1, end_dim=end_dim)
        return sequence

    if not isinstance(sequence, dict):
        return sequence

    sequence = [
        maybe_flatten_sequence(tensor, end_dim=end_dim) for tensor in sequence.values()
    ]
    return _torch.cat(sequence, dim=1)


def maybe_unflatten_sequence(sequence, *, original, end_dim: int = -1):
    """
    This function performs the inverse of :func:`maybe_flatten_sequence`.  It unflattens
    ``sequence`` to match the structure of ``original``.  Here ``original`` may be
    a :obj:`dict` or tensor.
    """
    if _torch.is_tensor(original):
        spatial_shape = original.shape[1 : (end_dim % original.ndim) + 1]
        if len(spatial_shape) == 1:
            return sequence
        return sequence.reshape(sequence.shape[0], *spatial_shape, *sequence.shape[2:])

    if not isinstance(original, dict):
        return sequence

    original_tensors = list(original.values())
    flat_original_tensors = [
        maybe_flatten_sequence(tensor, end_dim=end_dim) for tensor in original.values()
    ]
    seq_lens = [o_i.size(1) for o_i in flat_original_tensors]
    sequence = _torch.split(sequence, seq_lens, dim=1)
    sequence = [
        maybe_unflatten_sequence(e_i, original=o_i, end_dim=end_dim)
        for e_i, o_i in zip(sequence, original_tensors)
    ]
    return dict(zip(original, sequence))


def maybe_flatten_embeddings(
    embeddings: _Union[_torch.Tensor, _Dict[str, _torch.Tensor]]
) -> _torch.Tensor:
    """
    A convenience function for calling :func:`maybe_flatten_sequence` with
    ``end_dim=-2``.  This is helpful for flattening spatial embeddings with shape
    ``(batch_size, height, width, dim)`` into shape ``(batch_size, sequence_len, dim)``.
    """
    return maybe_flatten_sequence(embeddings, end_dim=-2)


def maybe_unflatten_embeddings(
    embeddings: _torch.Tensor,
    *,
    original: _Union[_torch.Tensor, _Dict[str, _torch.Tensor]],
) -> _Union[_torch.Tensor, _Dict[str, _torch.Tensor]]:
    """
    A convenience function for calling :func:`maybe_unflatten_sequence` with
    ``end_dim=-2``.
    """
    return maybe_unflatten_sequence(embeddings, original=original, end_dim=-2)


def inverse_permute(tensor: _torch.Tensor, perm: _List[int]):
    """
    A function that performs the inverse of :func:`torch.permute`.

    Args:
        tensor (:obj:`torch.Tensor`): Tensor to unpermute.
        perm (:obj:`List[int]`): Int list specifying the original axis permutation.

    Returns:
        The inverse permutation of tensor.
    """
    inv_perm = [perm.index(idx) for idx in range(len(perm))]
    assert len(inv_perm) == len(perm)
    return _torch.permute(tensor, inv_perm)


def stack(*tensors, dim=0):
    """
    This function operates similarly to torch.stack, but accepts multiple tensors as
    input arguments instead of a list of tensors. It can be frequently used to fuse
    parameters because the 'to_tamm' and 'from_tamm' functions in ParamMapper
    do not accept lists as input.
    """
    return _torch.stack(tensors, dim=dim)


def relaxed_one_hot(
    tensor: _torch.Tensor, *, num_classes: int, dtype: _torch.dtype = _torch.bool
):
    """
    This function is similar to :func:`torch.nn.functional` except for the following
    differences:

    1. The function ignores indices outside the range ``[0, num_classes)`` rather
       than raising an error.
    2. The dtype of the result defaults to ``bool``, and it is also configurable.
    3. The ``num_classes`` argument is required.

    Args:
        tensor (:obj:`torch.Tensor`): An integer tensor of indices.
        num_classes (:obj:`int`): The embedding size of the resulting one-hot encodings.
        dtype (:obj:`torch.dtype`): The result dtype.

    Returns:
        A binary-valued tensor with shape ``(*tensor.shape, num_classes)``.  Each
        entry takes value ``1`` if its index corresponds to an index in ``tensor``
        (and ``0`` otherwise).
    """
    input_shape = tensor.shape
    if tensor.device.type == "mps":
        tensor = tensor.flatten()  # due to an mps bug as of torch 2.5

    arange = _torch.arange(num_classes, device=tensor.device, dtype=tensor.dtype)
    result = tensor[..., None] == arange

    if tensor.device.type == "mps":
        result = result.reshape(*input_shape, -1)

    return result.type(dtype)


def cumsum(tensor: _torch.Tensor, dim: int) -> _torch.Tensor:
    """
    This is the same as :func:`torch.cumsum` but it is much faster on CUDA
    for important use cases.
    """
    should_move_dim = dim not in (-1, tensor.ndim - 1)
    if should_move_dim:
        tensor = tensor.movedim(dim, -1)
    result = tensor.cumsum(dim=-1)
    if should_move_dim:
        result = result.movedim(-1, dim)
    return result


def segment_matmul(segmented_input, group_sizes, weight):
    """
    Segment matrix multiplication:
    Perform a segmented or jagged/nested matrix multiplication against input,
    with different lengths of batched inputs against correspondingly indexed weights.
    Written for the purpose of dropless MoE mode.
    Example: (t=tracks/vectorized dim, b=batch, d_in=hidden in dim, d_out=hidden out dim)
    - `segmented_input` with shape (t, b, d_in)
    - `group_sizes` with shape (t, e)
    - `weight` with shape (t, e, d_in, d_out)
    - Returns:
          tensor of shape (t, b, d_out), where
          cum_group_sizes = cumsum(group_sizes, dim=1)
          result = stack([cat([segmented_input[i][0:cum_group_sizes[i][0]] @ weight[i,0]
                               segmented_input[i][cum_group_sizes[i][0]:cum_group_sizes[i][1]] @ weight[i,1]
                               ...
                              ]
                              for i in tracks
                          ])
    Args:
        segmented_input: The input tensor
        group_sizes: sizes of each group of `segmented_input` to matmul against `weight`
        weight: Weight tensor
    Returns:
        Output of segmented matrix multiplication
    """

    # Ensure that we're executing "vectorized segment matmul" (i.e: a PTT MoE activation layer)
    # A normal non-vectorized segment matmul can be performed with an explicit tracks=1.
    # input expected to be of shape (tracks, batch*seq*top_k, hidden_dim) in MoE case
    if len(segmented_input.shape) != 3:
        raise ValueError(
            "segment_matmul currently only accepts 3-dimensional inputs (parallel-track op)"
        )

    # For each track, perform segment matmul
    tracks = segmented_input.shape[0]
    group_sizes_list = group_sizes.tolist()
    track_results = []
    for track in range(tracks):
        # Following contains a list of tensors to pass to each expert, of length experts
        track_experts_tensors = _torch.split(
            segmented_input[track], group_sizes_list[track]
        )

        # Perform feedforward per expert
        for idx, expert_tensor in enumerate(track_experts_tensors):
            track_results.append(_torch.matmul(expert_tensor, weight[track, idx]))

    return _torch.cat(track_results).reshape((tracks, -1, weight.shape[-1]))


def crop(tensor: _torch.Tensor, *, shape: _Tuple[int, ...]) -> _torch.Tensor:
    """
    Truncates tensors with shape ``(batch_size, num_channels, *spatial_shape)``
    at top left corner to tensors with shape ``(batch_size, num_channels, *shape)``.
    """
    tensor_spatial_shape = tensor.shape[2:]
    if tensor_spatial_shape == shape:
        return tensor
    if any(i_dim > j_dim for i_dim, j_dim in zip(shape, tensor_spatial_shape)):
        raise ValueError(
            "Each dimension of truncation_shape must not be larger than the "
            "corresponding dimension in the tensor to be truncated."
        )
    slices = (slice(None), slice(None)) + tuple(slice(dim) for dim in shape)
    tensor = tensor[slices]
    return tensor


def soft_cap(tensor: _torch.Tensor, *, cap: float) -> _torch.Tensor:
    """
    Computes ``cap * tanh(tensor / cap)``, which is a smooth and differentiable way
    to cap the values of a tensor.

    Raises: ValueError: If ``cap`` is non-positive.
    """

    if cap <= 0:
        raise ValueError(f"soft_cap requires cap > 0, but cap is {cap}")
    return cap * _torch.tanh(tensor / cap)
