import logging as _logging

from tamm import _helpers
from tamm.utils import partial as _partial
from tamm.utils.json import JSONSerializableMixin as _JSONSerializableMixin

_logger = _logging.getLogger(__name__)


class _BaseConfig(
    _partial.DataclassedPartial,
    _JSONSerializableMixin,
):
    """
    The base class for :class:`.ModelConfig` and :class:`.LayerConfig`.
    Not to be instantiated directly.
    """

    @property
    def has_adapters(self):
        sub_modules = ["decoder", "image_tokenizer"]
        for sub_module in sub_modules:
            if hasattr(self, sub_module) and getattr(self, sub_module).has_adapters:
                return True
        if not hasattr(self, "adapters"):
            return False
        # pylint: disable=no-member
        return isinstance(self.adapters, dict) and len(self.adapters) > 0

    def _create(self, *override_args, **override_kwargs):
        """
        Creates and returns a configured instance of the module.

        Args:
            override_args: Optional positional arguments to override args specified in
                the config.  These args replace the first ``len(override_args)``
                positional args (and *all* varargs if ``override_args`` contains
                varargs) in the layer's :meth:`~.ModelMixin.create_builder` method.
            override_kwargs: Optional keyword override arguments.  These arguments
                replace any additional named arguments not overridden by
                ``override_args``.

        Returns:
            The newly created layer.
        """
        builder = self.create_builder(*override_args, **override_kwargs)
        return builder.build()

    def create_builder(self, *override_args, **override_kwargs):
        """
        Creates and returns a configured module builder. This method accepts the same
        arguments as ``create_layer()`` or ``create_model()``.
        """
        return self(*override_args, **override_kwargs)

    @classmethod
    def _create_subclass_from_module_cls(cls, layer_cls):
        """
        Creates a :class:`.LayerConfig` for a layer class which implements
        create_builder(*args, **kwargs)
        """
        layer_name = layer_cls.__name__
        config_name = f"{layer_name}Config"
        config_cls = cls.create_subclass(
            target_callable=layer_cls.create_builder,
            name=config_name,
            module_path=layer_cls.__module__,
        )
        config_cls.__doc__ = (
            f"A :class:`.LayerConfig` subclass for configuring :class:`.{layer_name}` "
            f"layers.  Use the alias :attr:`.{layer_name}.Config` to access this "
            f"class.  Please check :meth:`.{layer_name}.create_builder` for more "
            f"details about the  signature."
        )
        return config_cls

    def _to_json_dict_impl(self):
        result = _helpers.dataclass_to_dict(
            self.configured_args,
            omit_defaults=True,
            # only save non-default values for forward compatibility (if we include
            # default values, older tamm versions cannot load configs from newer
            # tamm versions that introduce new options)
        )
        result.pop("pretrained", None)  # specify pretrained=True in code, not config
        return result

    @classmethod
    def _from_json_dict_impl(cls, **obj):
        obj.pop("__versioning_info__", None)
        is_pretrained = obj.pop("pretrained", False)
        if is_pretrained:
            _logger.warning(
                "Dropping pretrained=True option when loading LayerConfig from JSON. "
                "Please specify this argument explicitly after loading the config."
            )
        return super()._from_json_dict_impl(**obj)


class LayerConfig(
    _BaseConfig,
    json_namespace="layers",
):
    """
    The base class for layer configs.  A :class:`.LayerConfig` is a
    :class:`.DataclassedPartial` with the layer class as the target callable.

    For usage examples, please see the layer
    configuration :ref:`user guide <configure_models>`.  Layer developers should use the
    ``.LayerMixin`` to create :class:`.LayerConfig` subclasses for new layers.
    """

    def create_layer(self, *override_args, **override_kwargs):
        """
        Creates and returns a configured instance of the layer.

        Args:
            override_args: Optional positional arguments to override args specified in
                the config.  These args replace the first ``len(override_args)``
                positional args (and *all* varargs if ``override_args`` contains
                varargs) in the layer's :meth:`~.ModelMixin.create_builder` method.
            override_kwargs: Optional keyword override arguments.  These arguments
                replace any additional named arguments not overridden by
                ``override_args``.

        Returns:
            The newly created layer.
        """
        return self._create(*override_args, **override_kwargs)
