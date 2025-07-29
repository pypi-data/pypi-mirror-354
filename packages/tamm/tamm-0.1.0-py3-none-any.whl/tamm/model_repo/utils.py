import copy
import logging as _logging

from tamm.model_repo._warning import _warn_deprecated_published_config

logger = _logging.getLogger(__name__)


def get_model_config_from_any_tamm_object(any_tamm_object):
    model_config = any_tamm_object
    if any_tamm_object.__class__.__name__ == "PublishedModelConfig":
        _warn_deprecated_published_config(any_tamm_object)
        model_config = any_tamm_object.model_config
    # pylint: disable=import-outside-toplevel
    from tamm.models.common import ModelConfig

    if not isinstance(model_config, ModelConfig):
        raise ValueError(
            f"Unsupported model config type: {type(model_config).__name__}"
        )
    return copy.deepcopy(model_config)
