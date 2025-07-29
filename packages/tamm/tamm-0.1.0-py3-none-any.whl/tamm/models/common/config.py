import logging as _logging

from tamm.layers.common import _BaseConfig
from tamm.models.common.metadata import ModelMetadata as _ModelMetadata

_logger = _logging.getLogger(__name__)


class ModelConfig(
    _BaseConfig,
    json_namespace="models",
):
    """
    The base class for model configs.  A :class:`.ModelConfig` is a
    :class:`.DataclassedPartial` with the model class as the target callable.

    For usage examples, please see the model
    configuration :ref:`user guide <configure_models>`.  Model developers should use the
    :class:`.ModelMixin` to create :class:`.ModelConfig` subclasses for new models.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # pylint: disable=access-member-before-definition
        if hasattr(self, "metadata") and self.metadata is None:
            self.metadata = _ModelMetadata()

    def create_model(self, *override_args, **override_kwargs):
        """
        Creates and returns a configured instance of the model.

        Args:
            override_args: Optional positional arguments to override args specified in
                the config.  These args replace the first ``len(override_args)``
                positional args (and *all* varargs if ``override_args`` contains
                varargs) in the model's :meth:`~.ModelMixin.create_builder` method.
            override_kwargs: Optional keyword override arguments.  These arguments
                replace any additional named arguments not overriden by
                ``override_args``.

        Returns:
            The newly created model.
        """
        return self._create(*override_args, **override_kwargs)

    @classmethod
    def _create_subclass_from_model(cls, model_cls):
        """
        Creates a :class:`.ModelConfig` for a model class which implements
        create_builder(*args, **kwargs)
        """
        config_cls = super()._create_subclass_from_module_cls(model_cls)
        config_cls.__doc__ = (
            "A :class:`.ModelConfig` subclass for configuring "
            f":class:`.{model_cls.__name__}` models.  Use the alias "
            f":attr:`.{model_cls.__name__}.Config` to access this class.  Please check "
            f":meth:`.{model_cls.__name__}.create_builder` for more "
            f"details about the  signature."
        )
        return config_cls

    def _to_json_dict_impl(self):
        result = super()._to_json_dict_impl()
        if self.metadata.is_empty:
            result.pop("metadata", None)
        return result

    @classmethod
    def _from_json_dict_impl(cls, **obj):
        obj.pop("__model_config_cls__", None)
        return super()._from_json_dict_impl(**obj)
