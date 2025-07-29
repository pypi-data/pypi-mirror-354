"""
layers.sequential
^^^^^^^^^^^^^^^^^

This module implements a generalization of ``torch.nn.Sequential``.  The |tamm| version
supports more complex sequential scenarios and includes features to help with training
optimizations such as FSDP.

.. autoclass:: tamm.layers.Sequential
    :show-inheritance:
    :members:
"""

import collections as _collections
import dataclasses as _dataclasses
import logging as _logging
from typing import Any as _Any
from typing import Dict as _Dict
from typing import List as _List
from typing import Optional as _Optional
from typing import Tuple as _Tuple
from typing import Union as _Union

import torch.nn as _nn
from torch.utils import checkpoint as _torch_utils_checkpoint

from tamm import _helpers, _warnings
from tamm.layers import side_outputs as _side_outputs
from tamm.layers.common import LayerMixin as _LayerMixin
from tamm.typing import OptionalModuleOrBuilder as _OptionalModuleOrBuilder

_logger = _logging.getLogger(__name__)


@_dataclasses.dataclass
class _ActivationCheckpointingOptions:
    is_enabled: bool = False
    use_reentrant: bool = False
    preserve_rng_state: bool = True


class Sequential(_nn.Module, _LayerMixin):
    """
    This layer generalizes ``torch.nn.Sequential``.  Like the native PyTorch version,
    its output is the chained output of child layers.  Additional features include:

    * Side inputs: Rather than receiving as input only the prior layer's output, each
        layer has the option of receiving additional arguments "from the side."  Users
        pass side inputs to :meth:`Sequential.forward`, which forwards the args to the
        appropriate layers in the sequence.
    * Side outputs: Rather than returning only the output of the final layer, the
        forward pass can return additional outputs from intermediate layers.
    * Groupable layers: The :meth:`group_subsequences_by_lengths` method reorganizes the
        ``nn.Module`` graph by replacing contiguous subsequences of layers with one
        :class:`Sequential` module per subsequence.  This provides flexibility to apply
        training optimizations to arbitrary subsequences of layers.  This reorganization
        does not affect the output of the forward pass.

    This layer implements the full interface of ``torch.nn.Sequential``, which means
    that code that supports ``torch.nn.Sequential`` should also support this layer.

    Args:
        named_layers (:obj:`dict` that maps :obj:`str` to :obj:`nn.Module`): A mapping
            of layer names to layer objects.  This defines the layer sequence, including
            its ordering (the sequence follows the same ordering as the :obj:`dict`).
        residual_connection (:obj:`_ModuleOrBuilder`): A Residual Connection layer,
            which when provided, applies that residual connection to the output of the
            :class: `Sequential` instance.
        side_input_keys (:obj:`dict` that maps :obj:`str` to a list of either \
            :obj:`str` or pairs of :obj:`str`, optional): A mapping of layer names to
            side argument names.  A value of ``["a", "c"]`` for ``layer_1`` means that
            the :class:`Sequential` instance forwards keyword arguments ``a`` and ``c``
            to ``layer_1`` during forward computation.  A value of
            ``["a", ("c", "new_c")]`` for ``layer_1`` means that the layer forwards
            ``a`` and ``c`` but uses the keyword ``new_c`` when passing the ``c``
            argument to ``layer_1``.  A value of ``["a", ("c", "**c")]`` means that
            the layer forwards ``a`` and ``c`` but passes ``c`` as ``**c``
            (``c`` is a dictionary of keyword arguments, which the layer unpacks when
            calling ``layer_1``).
        side_output_keys (:obj:`dict` that maps :obj:`str` to :obj:`str`, optional): A
            mapping of layer names to output names.  For example, a value of
            ``"hidden_state"`` for ``hidden_layer`` configures the forward pass to also
            return the output of ``hidden_layer`` as a side output with key
            ``"hidden_state"``.
        unpack_tuple_inputs (:obj:`bool`, optional): A flag that when ``True``,
            configures the forward pass to unpack inputs when calling each layer if the
            input is a :obj:`tuple`.  This enables a layer to receive multiple
            positional inputs if the output of the preceding layer is a :obj:`tuple`.

    """

    def __init__(
        self,
        named_layers: _Dict[str, _nn.Module],
        *,
        residual_connection: _OptionalModuleOrBuilder = None,
        side_input_keys: _Optional[
            _Dict[str, _List[_Union[str, _Tuple[str, str]]]]
        ] = None,
        side_output_keys: _Optional[_Dict[str, str]] = None,
        unpack_tuple_inputs: bool = False,
    ):
        _nn.Module.__init__(self)
        self._init_side_input_keys(side_input_keys)
        self._side_output_keys = (
            side_output_keys if side_output_keys is not None else {}
        )

        for layer_name in list(named_layers):
            if named_layers[layer_name] is not None:
                continue
            setattr(self, layer_name, None)
            named_layers.pop(layer_name)

        if residual_connection is not None:
            self._side_input_keys["residual_connection"].append(
                ("residual_input", "residual_input")
            )
            named_layers["residual_connection"] = residual_connection

        self._unpack_tuple_inputs = unpack_tuple_inputs
        for name, layer in named_layers.items():
            layer = _helpers.maybe_build_module(layer)
            self.add_module(name, layer)

        if "residual_connection" not in self.layer_names:
            self.residual_connection = None

        self._activation_checkpointing_options = _ActivationCheckpointingOptions()

    def _init_side_input_keys(self, side_input_keys):
        self._side_input_keys = _collections.defaultdict(list)
        if side_input_keys is None:
            side_input_keys = {}
        for layer_name, input_names in side_input_keys.items():
            for input_name in input_names:
                _logger.debug("init side input key %s", input_name)
                if isinstance(input_name, str):
                    input_name = (input_name, input_name)
                else:
                    input_name = tuple(input_name)
                    if len(input_name) != 2:
                        raise ValueError(
                            f"side input key does not have length 2: {input_name}"
                        )
                self._side_input_keys[layer_name].append(input_name)

    def __repr__(self):
        # Fall back if there is no more than 1 layers
        if len(self.named_layers) <= 1:
            return super().__repr__()

        class _REPRItem:
            def __init__(self, layer, name, index):
                self.layer = layer
                self.layer_repr = repr(layer)
                self.name = name
                self.index = index
                self.num_duplicated_layers = 1

            def __str__(self):
                lines = self.layer_repr.split("\n")
                if self.num_duplicated_layers > 1:
                    lines[0] = (
                        f"({self.index} - {self.index + self.num_duplicated_layers - 1}):"
                        f" {self.num_duplicated_layers} x " + lines[0]
                    )
                else:
                    lines[0] = f"({self.name}): " + lines[0]
                lines = [f"  {line}" for line in lines]
                return "\n".join(lines)

        all_repr_items = [
            _REPRItem(layer, name, index)
            for index, (name, layer) in enumerate(self.named_layers)
        ]

        idx = 0
        while idx < len(all_repr_items) - 1:
            if all_repr_items[idx].layer_repr == all_repr_items[idx + 1].layer_repr:
                all_repr_items.pop(idx + 1)
                all_repr_items[idx].num_duplicated_layers += 1
            else:
                idx += 1

        extra_repr = self.extra_repr()
        if extra_repr:
            extra_repr = f"\n  {extra_repr}"

        return (
            f"{self.__class__.__name__}(\n"
            + "\n".join(str(_) for _ in all_repr_items)
            + extra_repr
            + "\n)"
        )

    @property
    def side_input_keys(self) -> _Dict[str, _List[str]]:
        """The side inputs configuration."""
        return self._side_input_keys

    @property
    def has_residual_connection(self) -> bool:
        """Whether the layer has a residual connection."""
        return self.residual_connection is not None

    @property
    def side_output_keys(self) -> _Dict[str, str]:
        """The side outputs configuration."""
        return self._side_output_keys

    @property
    def unpack_tuple_inputs(self) -> bool:
        """The unpack_tuple_inputs setting."""
        return self._unpack_tuple_inputs

    @property
    def layer_names(self) -> _collections.abc.KeysView:
        """The names of layers in the sequence as a :obj:`KeysView`."""
        return self._modules.keys()

    @property
    def layers(self) -> _collections.abc.ValuesView:
        """The layers in the sequence as a :obj:`ValuesView`."""
        return self._modules.values()

    @property
    def named_layers(self) -> _collections.abc.ItemsView:
        """The names and layers in the sequence as an :obj:`ItemsView`."""
        return self._modules.items()

    @classmethod
    def from_nn_sequential(cls, module: _nn.Sequential) -> "Sequential":
        """
        Creates a new :obj:`Sequential` instance using the layer sequence from a
        :obj:`torch.nn.Sequential` module.
        """
        named_layers = {f"layer_{idx}": layer for idx, layer in enumerate(module)}
        return cls(named_layers)

    def register_side_input(
        self,
        layer_name: str,
        parent_input_name: str,
        child_input_name: _Optional[str] = None,
    ):
        """
        Register a side input argument for :meth:`forward`.

        Args:
            layer_name (:obj:`str`): The name of the layer that receives the side input
                during :meth:`forward`.
            parent_input_name (:obj:`str`): The name of the side input when passed to
                :meth:`Sequential.forward`.
            child_input_name (:obj:`str`, optional): The name for
                :meth:`Sequential.forward` to use when passing the side input to the
                child layer as a keyword argument.  This defaults to the
                ``parent_input_name`` value.
        """
        if child_input_name is None:
            child_input_name = parent_input_name
        input_pair = (parent_input_name, child_input_name)

        input_keys_for_layer = self._side_input_keys[layer_name]
        if input_pair not in input_keys_for_layer:
            input_keys_for_layer.append(input_pair)

    def unregister_side_input(
        self,
        layer_name: str,
        parent_input_name: str,
        child_input_name: str,
    ):
        """
        Un-register a side input argument.  This raises a :obj:`ValueError` if there is
        no side input registered with ``layer_name`` and ``parent_input_name``.

        Args:
            layer_name (:obj:`str`): The name of the layer that receives the side input
                during :meth:`forward`.
            parent_input_name (:obj:`str`): The name of the side input when passed to
                :meth:`Sequential.forward`.
            child_input_name (:obj:`str`, optional): The name for
                :meth:`Sequential.forward` to use when passing the side input to the
                child layer as a keyword argument.
        """
        input_pair = (parent_input_name, child_input_name)

        input_keys_for_layer = self._side_input_keys[layer_name]
        if input_pair not in input_keys_for_layer:
            raise ValueError(
                f"Could not unregister side input {input_pair} for layer "
                f"{layer_name}.  This input does not exist."
            )
        input_keys_for_layer.remove(input_pair)

    def checkpoint_activations(
        self, preserve_rng_state: bool = True, use_reentrant: bool = False
    ) -> None:
        """
        Enables activation checkpointing for the forward pass.  After this method is
        called, the full forward sequence executes using
        ``torch.utils.checkpoint.checkpoint()``.  Use :meth:`.store_activations` to
        undo this change.

        Args:
            preserve_rng_state (:obj:`bool`): The ``preserve_rng_state`` argument for
                ``torch.utils.checkpoint.checkpoint()``.
            use_reentrant (:obj:`bool`): The ``use_reentrant`` argument for
                ``torch.utils.checkpoint.checkpoint()``.
        """
        self._activation_checkpointing_options.is_enabled = True
        self._activation_checkpointing_options.preserve_rng_state = preserve_rng_state
        self._activation_checkpointing_options.use_reentrant = use_reentrant
        _logger.debug(
            "Enabled activation checkpointing for Sequential layer "
            "(preserve_rng_state=%s, use_reentrant=%s)",
            preserve_rng_state,
            use_reentrant,
        )

    def store_activations(self) -> None:
        """
        Reverses the effect of :meth:`checkpoint_activations`.
        """
        self._activation_checkpointing_options.is_enabled = False

    # pylint: disable-next=all
    def forward(self, input, **side_inputs):
        """
        Performs a forward pass.

        Each layer receives as input (1) the output from the previous layer, which is
        unpacked if the output is a :obj:`tuple` and ``unpack_tuple_inputs`` is
        ``True``, and (2) a mapped subset of keyword arguments from ``side_inputs``,
        where the subset for each layer is controlled by the layer's
        ``side_input_keys``.  Specifically, the layer receives a side input if the
        keyword passed to :meth:`Sequential.forward` is in the layer's list of
        ``side_input_keys``.

        If the layer has no side outputs, then the method returns the output of the
        final layer.  Otherwise, the method returns a :class:`OutputWithSideOutputs`.
        The ``output`` attribute contains the output of the final layer, and the
        ``side_outputs`` entry contains a :obj:`dict` of side outputs.  The keys of this
        :obj:`dict` correspond to output names (specified by ``side_output_keys``), and
        the values correspond to outputs of the specified layers.
        """

        if self.has_residual_connection:
            side_inputs["residual_input"] = input
        if not self._activation_checkpointing_options.is_enabled:
            return self._compute_forward_sequence(input, **side_inputs)

        options = self._activation_checkpointing_options

        return _torch_utils_checkpoint.checkpoint(
            self._compute_forward_sequence,
            input,
            preserve_rng_state=options.preserve_rng_state,
            use_reentrant=options.use_reentrant,
            **side_inputs,
        )

    # pylint: disable-next=all
    def _compute_forward_sequence(self, input, **side_inputs):
        side_outputs = {}
        output = input

        for layer_name, layer in self.named_layers:
            layer_kwargs = self._map_side_inputs_for_layer(side_inputs, layer_name)
            should_unpack_input = isinstance(output, tuple) and self.unpack_tuple_inputs

            if should_unpack_input:
                output = layer(*output, **layer_kwargs)
            else:
                output = layer(output, **layer_kwargs)

            if isinstance(output, _side_outputs.OutputWithSideOutputs):
                side_outputs = _side_outputs.merge_side_outputs(
                    side_outputs, output.side_outputs
                )
                output = output.output
            if layer_name in self.side_output_keys:
                key = self.side_output_keys[layer_name]
                side_outputs = _side_outputs.merge_side_outputs(
                    side_outputs, {key: output}
                )

        if len(side_outputs) > 0:
            return _side_outputs.OutputWithSideOutputs(output, side_outputs)
        return output

    def _map_side_inputs_for_layer(
        self, side_inputs: _Dict[str, _Any], layer_name: str
    ) -> _Dict[str, _Any]:
        mapped_side_inputs = {}
        keys_for_layer = self.side_input_keys.get(layer_name, [])
        for parent_input_name, child_input_name in keys_for_layer:
            if parent_input_name not in side_inputs:
                continue
            if child_input_name.startswith("**"):
                mapped_side_inputs.update(side_inputs[parent_input_name])
            else:
                mapped_side_inputs[child_input_name] = side_inputs[parent_input_name]
        return mapped_side_inputs

    def group_subsequences_by_lengths(self, lengths: _List[int]) -> None:
        """
        Reorganizes the ``nn.Module`` graph without affecting the output of the forward
        pass.  In particular, this method replaces contiguous subsequences of child
        layers with one :class:`Sequential` child per subsequence.  This provides
        flexibility to wrap arbitrary subsequences of layers with training optimizations
        such as FSDP.

        Args:
            lengths (:obj:`list` of :obj:`int`): A list that specifies the length of
                each contiguous subsequence to group.  This arg must contain strictly
                positive values, and it must sum to the total number of layers.
        """

        if any(length <= 0 for length in lengths):
            raise ValueError(
                "Input to group_subsequences_by_lengths contains a non-positive value"
            )
        boundaries = [0] + _helpers.cumsum(lengths)
        lengths_sum = boundaries[-1]
        if lengths_sum != len(self):
            raise ValueError(
                f"Input to group_subsequences_by_lengths sums to {lengths_sum}, which "
                f"is not the length of the Sequential instance ({len(self)})"
            )
        original_copy = self[:]
        del self[:]
        self._unpack_tuple_inputs = False
        for start_idx, end_idx in zip(boundaries[:-1], boundaries[1:]):
            layer = original_copy[start_idx:end_idx]
            group_idx = len(self)
            name = f"group_{group_idx}"
            side_input_keys = set()
            for input_keys_for_sublayer in layer.side_input_keys.values():
                new_keys = [key for key, _ in input_keys_for_sublayer]
                side_input_keys.update(new_keys)
            side_input_keys = [(key, key) for key in side_input_keys]
            self.append(layer, name=name, side_input_keys=side_input_keys)

    @_warnings.deprecate(alternative="group_subsequences_by_lengths")
    def group_children_by_sizes(self, sizes: _List[int]) -> None:
        """Deprecated.  Please use group_subsequences_by_lengths instead."""
        return self.group_subsequences_by_lengths(sizes)

    def rename_layers(self, new_names: _List[str]) -> None:
        """
        Renames all of the layers in the sequence.

        Args:
            new_names (:obj:`list` of :obj:`str`): The new names for each layer.  The
                names must be unique, and if the sequence has a residual connection, its
                name must remain ``'residual_connection'``.
        """
        if len(new_names) != len(self):
            raise ValueError(
                "The length of new_names differs from the number of layers"
            )
        if len(set(new_names)) != len(new_names):
            raise ValueError("new_names is not unique")

        old2new = dict(zip(self.layer_names, new_names))

        if self.has_residual_connection:
            if old2new["residual_connection"] != "residual_connection":
                raise ValueError(
                    "The name of 'residual_connection' must remain "
                    "'residual_connection'"
                )
        elif "residual_connection" in new_names:
            raise ValueError(
                "new_names cannot contain 'residual_connection' when there is no "
                "residual connection layer"
            )

        self_copy = self[:]
        input_keys_copy = self.side_input_keys.copy()
        output_keys_copy = self.side_output_keys.copy()

        del self[:]
        for idx, name in enumerate(new_names):
            self.add_module(name, self_copy[idx])

        self._side_input_keys = {  # pylint: disable=attribute-defined-outside-init
            old2new[key]: value for key, value in input_keys_copy.items()
        }

        self._side_output_keys = {
            old2new[key]: value for key, value in output_keys_copy.items()
        }

    def append(
        self,
        module: _nn.Module,
        *,
        name: _Optional[str] = None,
        side_input_keys: _Optional[_Union[_List[str], _List[_Tuple[str, str]]]] = None,
        side_output_key: _Optional[str] = None,
    ) -> "Sequential":
        """
        Appends ``module`` to the end of the sequence.

        Args:
            module (:obj:`nn.Module`): The module to append.
            name (:obj:`str`): The module's name.
            side_input_keys (:obj:`list` of :obj:`str`, optional): A list of side input
                names that ``module`` accepts.
            side_output_key (:obj:`str`, optional): A name for the output if the
                ``module`` produces a side output.
        """

        if name is None:
            name = f"layer_{len(self)}"
        name = _helpers.make_key_unique(name, self.layer_names)
        self.add_module(name, module)
        if side_input_keys is not None:
            side_input_keys = [
                (key, key) if isinstance(key, str) else key for key in side_input_keys
            ]
            self.side_input_keys[name] = side_input_keys
        if side_output_key is not None:
            self.side_output_keys[name] = side_output_key
        return self

    def insert(
        self,
        index: int,
        module: _nn.Module,
        *,
        name: _Optional[str] = None,
        side_input_keys: _Optional[_List[str]] = None,
        side_output_key: _Optional[str] = None,
    ):
        """
        Inserts ``module`` into the sequence before position ``index``.

        Args:
            index (:obj:`int`): The insert position.
            module (:obj:`nn.Module`): The module to append.
            name (:obj:`str`): The module's name.
            side_input_keys (:obj:`list` of :obj:`str`, optional): A list of side input
                names that ``module`` accepts.
            side_output_key (:obj:`str`, optional): A name for the output if the
                ``module`` produces a side output.
        """

        right_side = self[index:]
        del self[index:]
        self.append(
            module,
            name=name,
            side_input_keys=side_input_keys,
            side_output_key=side_output_key,
        )
        self += right_side
        return self

    def extend(self, sequential) -> "Sequential":
        """
        Extends the sequence by appending layers from another sequential layer.

        Args:
            sequential (:obj:`Sequential` or :obj:`torch.nn.Sequential`): The other
                sequential module that contains layers to append.
        """

        self += sequential
        return self

    def __getitem__(self, idx):
        if isinstance(idx, slice):
            selected_modules = dict(list(self.named_layers)[idx])
            side_input_keys = {
                key: self.side_input_keys[key].copy()
                for key in selected_modules
                if key in self.side_input_keys
            }
            side_output_keys = {
                key: self.side_output_keys[key]
                for key in selected_modules
                if key in self.side_output_keys
            }
            return Sequential(
                selected_modules,
                side_input_keys=side_input_keys,
                side_output_keys=side_output_keys,
                unpack_tuple_inputs=self.unpack_tuple_inputs,
            )
        if isinstance(idx, str):
            return self._modules[idx]
        return _helpers.get_item_by_index(self.layers, idx)

    def __setitem__(self, idx, value):
        if isinstance(idx, slice):
            selected_keys = list(self.layer_names)[idx]
            if len(selected_keys) != len(value):
                raise ValueError(
                    f"slice specifies {len(selected_keys)} layers but value has length "
                    f"{len(value)}"
                )
            for key, module in zip(selected_keys, value):
                self.add_module(key, module)
        elif isinstance(idx, str):
            self.add_module(idx, value)
        else:
            key = _helpers.get_item_by_index(self.layer_names, idx)
            self.add_module(key, value)

    def __delitem__(self, idx):
        if isinstance(idx, slice):
            selected_keys = list(self.layer_names)[idx]
            for key in selected_keys:
                delattr(self, key)
                self.side_input_keys.pop(key, None)
                self.side_output_keys.pop(key, None)
        elif isinstance(idx, str):
            delattr(self, idx)
            self.side_input_keys.pop(idx, None)
            self.side_output_keys.pop(idx, None)
        else:
            key = _helpers.get_item_by_index(self.layer_names, idx)
            delattr(self, key)
            self.side_input_keys.pop(key, None)
            self.side_output_keys.pop(key, None)

    def __len__(self) -> int:
        return len(self._modules)

    def _add(self, other, in_place=False) -> "Sequential":
        result = self if in_place else self[:]
        if isinstance(other, Sequential):
            if self.unpack_tuple_inputs != other.unpack_tuple_inputs:
                raise ValueError(
                    "Add operator requires objects with the same value for "
                    "unpack_tuple_inputs but this is not the case "
                    f"({self.unpack_tuple_inputs} vs. {other.unpack_tuple_inputs})"
                )
            for name, layer in other.named_layers:
                side_input_keys = other.side_input_keys.get(name)
                side_input_keys = _helpers.copy_if_not_none(side_input_keys)
                side_output_key = other.side_output_keys.get(name)
                result.append(
                    layer,
                    name=name,
                    side_input_keys=side_input_keys,
                    side_output_key=side_output_key,
                )
        elif isinstance(other, _collections.abc.Mapping):
            for name, layer in other.items():
                result.append(layer, name=name)
        else:
            for layer in other:
                result.append(layer)
        return result

    def __add__(self, other) -> "Sequential":
        return self._add(other, in_place=False)

    def __radd__(self, other) -> "Sequential":
        result = self[:0]
        result += other
        result += self
        return result

    def __iadd__(self, other) -> "Sequential":
        return self._add(other, in_place=True)

    def _mul(self, other: int, in_place: bool = False) -> "Sequential":
        if not isinstance(other, int):
            raise TypeError(
                f"Unsupported operand types for *: {type(self)} and {type(other)}"
            )
        if other < 0:
            raise ValueError(
                f"Non-positive multiplication factor {other} for {type(self)}"
            )
        original_copy = self[:]
        result = self if in_place else self[:]
        del result[:]
        for _ in range(other):
            result += original_copy
        return result

    def __mul__(self, other: int) -> "Sequential":
        return self._mul(other, in_place=False)

    def __rmul__(self, other: int) -> "Sequential":
        return self * other

    def __imul__(self, other: int) -> "Sequential":
        return self._mul(other, in_place=True)

    def __iter__(self):
        return iter(self.layers)
