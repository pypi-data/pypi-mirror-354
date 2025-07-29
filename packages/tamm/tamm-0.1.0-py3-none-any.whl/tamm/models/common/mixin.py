import inspect as _inspect
import logging as _logging
from typing import TYPE_CHECKING
from typing import Dict as _Dict
from typing import Optional as _Optional
from typing import Union as _Union

from tamm.layers.common import _BaseConfigurableMixin
from tamm.layers.common import post_hooks as _post_hooks
from tamm.models.common.config import ModelConfig as _ModelConfig
from tamm.models.common.metadata import ModelMetadata as _ModelMetadata
from tamm.utils import OptionalBool as _OptionalBool

if TYPE_CHECKING:
    from tamm._adapters_v1 import ModelAdapter
    from tamm.ao import ArchOptimizer
    from tamm.typing import (
        LenientOptionalBool,
        OptionalDeviceOrString,
        OptionalDtypeOrString,
    )

_logger = _logging.getLogger(__name__)


class ModelMixin(_BaseConfigurableMixin):
    """
    A mixin for common functionality of |tamm| models.  Model subclasses must implement
    the ``.create_basic_builder()`` method.

    Here is what this mixin brings to the model:

    1. Creates :class:`.ModelConfig` and :class:`.LayerBuilder` subclasses for the model
       type and attaches them to the model class as ``.Config`` and ``.Builder``
       attributes.
    2. Implements the :meth:`.create_builder` method, which wraps
       ``.create_basic_builder()`` to implement common functionality across models.
    3. Implements the ``<model_cls>.create()`` method, which is an
       alias of ``<model_cls>.Builder.build()``
    4. Decorates the model's initializer to collect usage telemetry.

    """

    def __init_subclass__(cls, /, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls._should_update_signature():
            cls._update_create_builder_signature()
            cls._update_create_signature()
        cls.Config = _ModelConfig._create_subclass_from_model(cls)

    @classmethod
    def _should_update_signature(cls):
        """
        This predicate determine whether the signature for create_builder() should
        be updated
        """

        if "create_builder" in cls.__dict__:
            # model_yz = config_yz.create_model()
            _logger.debug(
                f"Skipping update to the signature of {cls.__name__}.create_builder() "
                "because this class overrides create_builder().  This may impact the "
                f"ModelConfig type for {cls}."
            )
            return False
        return True

    @staticmethod
    def _get_base_create_builder_signature():
        return _inspect.signature(ModelMixin.create_builder.__func__)

    @classmethod
    def create_builder(
        cls,
        *basic_builder_args,
        device: "OptionalDeviceOrString" = None,
        adapters: _Optional[_Dict[str, "ModelAdapter"]] = None,
        active_adapter: _Union[int, str] = 0,
        arch_optimizers: _Optional[_Dict[str, "ArchOptimizer"]] = None,
        pretrained: "LenientOptionalBool" = _OptionalBool.NOTSET,
        pretrained_path: _Optional[str] = None,
        freeze_params: "LenientOptionalBool" = _OptionalBool.NOTSET,
        dtype: "OptionalDtypeOrString" = None,
        metadata: _Optional["_ModelMetadata"] = None,
        **basic_builder_kwargs,
    ):
        """
        Creates and returns a configured instance of the model's
        :class:`~.layers.LayerBuilder` subclass.  This method adds hooks to the result
        of :meth:`cls.create_basic_builder` to add common functionality related to model
        instantiation.

        Args:
            device (:obj:`torch.device` or :obj:`str`, optional): The target device for
                model parameters and other state.  This is also the default device for
                adapter layers, which can be overridden in :obj:`.ModelAdapter`.
            adapters (:obj:`dict`, optional): A dictionary that maps :obj:`str` adapter
                IDs to instances of :obj:`.ModelAdapter`.  The returned builder will
                call these adapters to attach adapter layers (such as LoRA) to newly
                created models.
            active_adapter (:obj:`int` or `str`, optional): A variable indicates which
                adapter should be activated when the model is being instantiated.
                If the value is an integer, that stands for the index of the adapter.
                If the value is a string, it should be a valid adapter id.
            arch_optimizers (:obj:`dict`, optional): A dictionary that maps :obj:`str`
                architecture optimizer IDs to instances of
                :obj:`.ArchOptimizer`. The returned builder will apply these
                architecture optimizers (such as KVQuant) to newly created models.
            pretrained (:obj:`bool`): A flag for loading pre-trained weights.  The model
                only loads from pretrained paths when ``pretrained`` is ``True``.  This
                same flag also applies to the model adapters when initializing adapters.
            pretrained_path (:obj:`str`, optional): A pretrained checkpoint path for the
                backbone model's state dict.  This state should not include adapter
                state.
            freeze_params (:obj:`bool`): A flag for freezing parameters of the model
                (i.e., setting their ``requires_grad`` attributes to ``False``).  Note:
                this flag only applies to the backbone model, not adapter parameters,
                since adapters have their own ``freeze_params`` option.
            metadata (:obj:`ModelMetadata`): Additional information about the model,
                such as details regarding the model's origination.
            dtype (:obj:`torch.dtype`, optional): The parameter dtype.

        Returns:
            The configured :obj:`.LayerBuilder`.
        """
        builder = super().create_builder(
            *basic_builder_args,
            device=device,
            adapters=adapters,
            active_adapter=active_adapter,
            arch_optimizers=arch_optimizers,
            pretrained=pretrained,
            pretrained_path=pretrained_path,
            freeze_params=freeze_params,
            dtype=dtype,
            **basic_builder_kwargs,
        )

        config = cls.Config(
            *basic_builder_args,
            device=device,
            adapters=adapters,
            active_adapter=active_adapter,
            arch_optimizers=arch_optimizers,
            pretrained=pretrained,
            pretrained_path=pretrained_path,
            freeze_params=freeze_params,
            dtype=dtype,
            metadata=metadata,
            **basic_builder_kwargs,
        )
        builder.post_hooks.register(_post_hooks.AttachConfigPostHook(config))

        if metadata is None:
            metadata = _ModelMetadata()
        builder.post_hooks.register(_post_hooks.AttachMetadataPostHook(metadata))

        return builder

    @property
    def config(self) -> _Union["_ModelConfig", None]:
        """The :obj:`ModelConfig` used to create the model."""
        return getattr(self, "_tamm_model_config", None)

    @config.setter
    def config(self, value: "_ModelConfig") -> None:
        self._tamm_model_config = value

    @property
    def metadata(self) -> _Union["_ModelMetadata", None]:
        """
        A :obj:`ModelMetadata` for the model (or ``None`` if this has not been set).
        """
        return getattr(self, "_tamm_model_metadata", None)

    @metadata.setter
    def metadata(self, value: "_ModelMetadata") -> None:
        self._tamm_model_metadata = value
