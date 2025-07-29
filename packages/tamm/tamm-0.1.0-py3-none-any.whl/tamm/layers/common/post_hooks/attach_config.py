from torch import nn as _nn


class AttachConfigPostHook:
    def __init__(self, config):
        self.config = config

    def __call__(self, model: _nn.Module) -> None:
        model.config = self.config
