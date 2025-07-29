from torch import nn as _nn


class AttachMetadataPostHook:
    def __init__(self, metadata):
        self.metadata = metadata

    def __call__(self, model: _nn.Module) -> None:
        model.metadata = self.metadata
