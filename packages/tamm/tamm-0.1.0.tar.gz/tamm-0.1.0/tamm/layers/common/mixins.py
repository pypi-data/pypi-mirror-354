import abc as _abc
import contextlib as _contextlib
import inspect as _inspect
import logging as _logging
from typing import TYPE_CHECKING
from typing import Dict as _Dict
from typing import Optional as _Optional
from typing import Union as _Union

from tamm import _helpers
from tamm.layers.common.builder import BuildableMixin as _BuildableMixin
from tamm.layers.common.config import LayerConfig
from tamm.layers.common.context_hooks import (
    DefaultDeviceContextHook,
    DtypeContextHook,
    FreezeParamsContextHook,
    PretrainedContextHook,
    UseMetaInitTrickContextHook,
)
from tamm.layers.common.post_hooks import (
    ArchOptimizersPostHook,
    FreezeParamsPostHook,
    IdentityPostHook,
    get_model_adapters_post_hook,
)
from tamm.layers.common.post_hooks.model_initializer import ModelInitializerPostHook
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


class LayerMixin(_BuildableMixin):
    """
    Common layer mixin for all |tamm| layers.
    All layers are expected to inherit from this class

    This mixin makes layer

    1. Buildable: layer inherits this class has attribute ``.Builder``.
    """


class _BaseConfigurableMixin(LayerMixin, _abc.ABC):
    def __init_subclass__(cls, /, **kwargs):
        super().__init_subclass__(**kwargs)
        if not _inspect.ismethod(cls.create_basic_builder):
            raise TypeError(
                f"Expected {cls.__name__}.create_basic_builder() to be a classmethod"
            )

    @classmethod
    @_abc.abstractmethod
    def _should_update_signature(cls):
        """
        This predicate determines whether the signature for create_builder() should
        be updated
        """

    @classmethod
    def _update_create_signature(cls):
        new_func = _helpers.passthrough_decorator(cls.create.__func__)
        new_func.__signature__ = _inspect.signature(cls.create_builder.__func__)
        cls.create = classmethod(new_func)

    @classmethod
    def _update_create_builder_signature(cls):
        """
        This classmethod applies a wrapper to the create_builder() classmethod to
        update its signature.  This is important because we derive the fields for
        each module's Config from the signature of create_builder().

        create_builder() takes its own keyword arguments but it also accepts *args and
        **kwargs for create_basic_builder().  To create the signature for
        create_builder(), we take the signature of create_basic_builder() and append
        the keyword arguments from create_builder().
        """

        basic_sig = _inspect.signature(cls.create_basic_builder.__func__)
        sig = cls._get_base_create_builder_signature()
        common_params = [p for p in sig.parameters.values() if p.kind is p.KEYWORD_ONLY]

        for param in common_params:
            if param.name in basic_sig.parameters:
                raise RuntimeError(
                    f"{cls.__name__}.create_basic_builder() contains a parameter named "
                    f"'{param.name}', but this is reserved for create_builder(), which "
                    "wraps create_basic_builder()."
                )

        new_sig = _helpers.add_kw_only_params_to_signature(basic_sig, common_params)
        new_func = _helpers.passthrough_decorator(cls.create_builder.__func__)
        new_func.__signature__ = new_sig
        cls.create_builder = classmethod(new_func)

    @staticmethod
    def _get_base_create_builder_signature():
        return _inspect.signature(_BaseConfigurableMixin.create_builder.__func__)

    @classmethod
    @_abc.abstractmethod
    def create_basic_builder(cls):
        """
        Creates and returns a configured instance of the module's
        :class:`~.layers.LayerBuilder` subclass. subclasses should
        implement this method and add keyword arguments for configuring module options
        (such as the number of layers, dtype of parameters, etc.).  These keyword
        arguments cannot include keyword arguments from ``.create_builder``
        (``device``, ``pretrained_path``, etc.), since ``.create_builder``
        wraps ``.create_basic_builder()`` and adds additional functionality.
        """

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
        dtype: "OptionalDtypeOrString" = None,
        freeze_params: "LenientOptionalBool" = _OptionalBool.NOTSET,
        **basic_builder_kwargs,
    ):
        # pylint: disable=too-many-locals
        """
        Creates and returns a configured instance of the module's
        :class:`~.layers.LayerBuilder` subclass.  This method adds hooks to the result
        of ``.create_basic_builder()`` to add common functionality related to module
        instantiation.

        Args:
            device (:obj:`torch.device` or :obj:`str`, optional): The target device for
                module parameters and other state.  This is also the default device for
                adapter layers, which can be overridden in :obj:`.ModelAdapter`.
            adapters (:obj:`dict`, optional): A dictionary that maps :obj:`str` adapter
                IDs to instances of :obj:`.ModelAdapter`.  The returned builder will
                call these adapters to attach adapter layers (such as LoRA) to newly
                created modules.
            active_adapter (:obj:`int` or `str`, optional): A variable indicates which
                adapter should be activated when the model is being instantiated.
                If the value is an integer, that stands for the index of the adapter.
                If the value is a string, it should be a valid adapter id.
            arch_optimizers (:obj:`dict`, optional): A dictionary that maps :obj:`str`
                architecture optimizer IDs to instances of
                :obj:`.ArchOptimizer`. The returned builder will apply these
                architecture optimizers (such as KVQuant) to newly created modules.
            pretrained (:obj:`OptionalBool`, `bool`): A flag for loading pre-trained
                weights.  The module only loads from pretrained paths when
                ``pretrained`` is ``True``. This same flag also applies to the module
                adapters when initializing adapters.
            pretrained_path (:obj:`str`, optional): A pretrained checkpoint path for the
                backbone module's state dict.  This state should not include adapter
                state.
            freeze_params (:obj:`OptionalBool`, `bool`): A flag for freezing parameters
                of the module (i.e., setting their ``requires_grad`` attributes to
                ``False``).  Note: this flag only applies to the backbone module,
                not adapter parameters, since adapters have their own
                ``freeze_params`` option.
            dtype (:obj:`torch.dtype`, optional): The parameter dtype.

        Returns:
            The configured :obj:`.LayerBuilder`.
        """
        # Type casting first since ``pretrained`` can be either `bool` or `OptionalBool`
        disable_meta_device_init_trick = (
            _OptionalBool(pretrained) is _OptionalBool.FALSE
        )
        extended_context_hooks = [
            DefaultDeviceContextHook(
                device=device,
                disable_meta_device_init_trick=disable_meta_device_init_trick,
            ),
            PretrainedContextHook(pretrained),
            DtypeContextHook(dtype),
            FreezeParamsContextHook(freeze_params),
        ]
        with _contextlib.ExitStack() as stack:
            for extended_context_hook in extended_context_hooks:
                # Apply the same set of extended contexts to the calling context of
                # `create_basic_builder`, in case module developers instantiate concrete
                # ``nn.Modules`` within the builder.
                # fixme: Debate whether to un-support this use case and enforce builder
                # to only compose other 'pure' builders
                # (i.e., no nn.Module gets created 'within' a builder)
                stack.enter_context(extended_context_hook())

            builder = cls.create_basic_builder(
                *basic_builder_args, **basic_builder_kwargs
            )

        # UseMetaInitTrickContextHook is the only 'narrow scoped' context hook
        # (covering builder() only)
        builder.context_hooks.register(
            UseMetaInitTrickContextHook(
                pretrained=pretrained, pretrained_path=pretrained_path
            )
        )

        for extended_context_hook in extended_context_hooks:
            # Register 'extended' context-hooks (covering both builder() and post_hooks)
            builder.extended_context_hooks.register(extended_context_hook)

        post_hooks = [
            ModelInitializerPostHook(pretrained_path),
            FreezeParamsPostHook(),
            get_model_adapters_post_hook(
                adapters=adapters,
                active_adapter=active_adapter,
            ),
            ArchOptimizersPostHook(
                arch_optimizers=arch_optimizers,
            ),
        ]
        for post_hook in post_hooks:
            # fixme: refactor dataclass partial's hook registration API to filter out
            #  IdentityPostHook
            if not isinstance(post_hook, IdentityPostHook):
                builder.post_hooks.register(post_hook)

        return builder

    @classmethod
    def create(cls, *args, **kwargs):
        """
        Creates and returns a configured instance of the module. This method accepts the
        same arguments as :meth:`.create_builder`.
        """
        builder = cls.create_builder(*args, **kwargs)
        return builder.build()


class ConfigurableLayerMixin(_BaseConfigurableMixin):
    """
    Common layer mixin for all configurable |tamm| layers.

    This mixin makes layer

    1. Buildable: layer inherits this class has attribute ``.Builder``.
    2. Configurable: <layer_cls>.Config() instantiates a Config object representing the
       layer itself. ``<layer_cls>.Config().create_layer(*args, **kwargs)`` creates an
       instance of the layer with optional argument overrides ``*args`` and ``**kwargs``

    """

    def __init_subclass__(cls, /, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls._should_update_signature():
            cls._update_create_builder_signature()
            cls._update_create_signature()
        cls.Config = LayerConfig._create_subclass_from_module_cls(cls)

    @classmethod
    def _should_update_signature(cls):
        if "create_builder" in cls.__dict__:
            _logger.debug(
                f"Skipping update to the signature of {cls.__name__}.create_builder() "
                "because this class overrides create_builder().  This may impact the "
                f"LayerConfig type for {cls}."
            )
            return False
        return True

    @classmethod
    @_abc.abstractmethod
    def create_basic_builder(cls):
        """
        Creates and returns a configured instance of the layer's
        :class:`~.layers.LayerBuilder` subclass. :class:`.ConfigurableLayerMixin`
        subclasses should implement this method and add keyword arguments for
        configuring layer options (such as the number of layers, dtype of parameters,
        etc.).  These keyword arguments cannot include keyword arguments from
        :meth:`_BaseConfigurableMixin.create_builder` (``device``, ``pretrained_path``,
        etc.), since :meth:`_BaseConfigurableMixin.create_builder` wraps
        ``.create_basic_builder()`` and adds additional functionality.
        """
