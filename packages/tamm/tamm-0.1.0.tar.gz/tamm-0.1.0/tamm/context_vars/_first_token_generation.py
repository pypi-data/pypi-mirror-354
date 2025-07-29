import contextlib as _contextlib
from contextvars import ContextVar

first_token_generation = ContextVar("first_token_generation", default=False)


def get_first_token_generation_flag() -> bool:
    """
    Returns whether we are currently generating the first token in a sequence.

    Returns:
        bool: ``True`` if we're generating the first token, ``False`` otherwise
    """
    return first_token_generation.get()


@_contextlib.contextmanager
def first_token_generation_context():
    """
    Context manager for indicating first token generation.

    Sets a flag ``True`` indicating that we're generating the first token in a sequence.
    The flag is automatically reset to ``False`` when exiting the context.

    Example:
        >>> with first_token_generation_context():
        ...     first_token_logits = model(input_ids, ...)
    """
    token = first_token_generation.set(True)
    try:
        yield
    finally:
        first_token_generation.reset(token)
