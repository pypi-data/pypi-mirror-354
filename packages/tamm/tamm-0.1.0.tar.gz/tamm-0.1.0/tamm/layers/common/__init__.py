"""
Layer Utilities
---------------

.. autoclass:: tamm.layers.common.LayerBuilder
    :members:
    :show-inheritance:

.. autoclass:: tamm.layers.common.LayerConfig
    :members: create_builder, create_layer

.. autoclass:: tamm.layers.common.LayerMixin
    :members:
    :show-inheritance:

.. autoclass:: tamm.layers.common.BuildableMixin
    :members:
    :show-inheritance:

.. autoclass:: tamm.layers.common.ConfigurableLayerMixin
    :members:

.. autoclass:: tamm.layers.common.PretrainedLoader


Module Markers
^^^^^^^^^^^^^^

.. autofunction:: tamm.layers.common.init_marker
.. autofunction:: tamm.layers.common.update_marker
.. autofunction:: tamm.layers.common.get_marker

.. autoclass:: tamm.layers.common.ModuleMarker
    :members:

.. automodule:: tamm.layers.common.context_hooks
.. automodule:: tamm.layers.common.post_hooks
"""
from tamm.layers.common._marker import (
    ModuleMarker,
    get_marker,
    init_marker,
    update_marker,
)
from tamm.layers.common.builder import BuildableMixin, LayerBuilder
from tamm.layers.common.config import LayerConfig, _BaseConfig
from tamm.layers.common.context_hooks import (
    DefaultDeviceContextHook,
    DtypeContextHook,
    PretrainedContextHook,
    UseMetaInitTrickContextHook,
)
from tamm.layers.common.mixins import (
    ConfigurableLayerMixin,
    LayerMixin,
    _BaseConfigurableMixin,
)
from tamm.layers.common.post_hooks import (
    ArchOptimizersPostHook,
    AttachConfigPostHook,
    AttachMetadataPostHook,
    FreezeParamsPostHook,
    ModelInitializerPostHook,
    get_model_adapters_post_hook,
)
from tamm.layers.common.pretrained_loader import PretrainedLoader

__all__ = [
    "LayerBuilder",
    "LayerConfig",
    "LayerBuilder",
    "LayerMixin",
    "BuildableMixin",
    "ConfigurableLayerMixin",
    "ArchOptimizersPostHook",
    "AttachConfigPostHook",
    "AttachMetadataPostHook",
    "FreezeParamsPostHook",
    "ModelInitializerPostHook",
    "get_model_adapters_post_hook",
    "DefaultDeviceContextHook",
    "PretrainedContextHook",
    "UseMetaInitTrickContextHook",
    "PretrainedLoader",
    "DtypeContextHook",
    "ModuleMarker",
    "init_marker",
    "update_marker",
    "get_marker",
    "_BaseConfig",
    "_BaseConfigurableMixin",
]
