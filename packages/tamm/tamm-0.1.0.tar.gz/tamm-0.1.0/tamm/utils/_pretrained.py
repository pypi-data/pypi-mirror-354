import logging
from pathlib import Path as _Path

from tamm import _helpers
from tamm.utils.uri import _URIHandler

_logger = logging.getLogger(__name__)


def fetch_file(
    remote_path: str,
) -> _Path:
    """
    Fetch large artifacts (e.g., model checkpoints, and tokenizer vocabs) from remote
    storage. Utilizes local diskcache as per implementation selected by URI handler.

    Args:
        remote_path: URI in string

    Returns: Local file path of the first successfully fetched remote path

    """

    return _URIHandler(use_cache=True).map_to_local(remote_path)


def fetch_checkpoint(remote_path: str, *, map_location=None) -> dict:
    """
    Fetch Pytorch checkpoint from remote storage. Utilizes local diskcache as per
    implementation selected by URI handler.

    Args:
        remote_path: URI of remote checkpoint e.g., s3://bucket/ckpt.pt

    Returns: Pytorch state dictionary

    """

    with _URIHandler(use_cache=True).open(remote_path, mode="rb") as fptr:
        state_dict = _helpers.safe_torch_load(fptr, map_location=map_location)
    _logger.info("State dictionary is loaded into memory from the checkpoint file.")
    return state_dict
