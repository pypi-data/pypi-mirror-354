"""
tamm.layers
-----------
"""

from tamm.layers import common, functional, init, mixture_of_experts, torch_nn
from tamm.layers.activation import GEGLU, GELU, GLU, QuickGELU, ReLU, SiLU, SwiGLU, Tanh
from tamm.layers.attention import (
    KVReuseTransformerAttention,
    QKNorm,
    QKVLinear,
    RoPETransform,
    ScaledDotProductAttention,
    TransformerAttention,
)
from tamm.layers.basic import (
    ChannelsFirstToLast,
    ChannelsLastToFirst,
    Index,
    Interpolation,
    Map,
    Mean,
    PadToMultiple,
    SelectByKey,
    SoftCap,
    Sum,
    Union,
)
from tamm.layers.convolution import (
    Conv1d,
    Conv2d,
    ResNetBlock,
    ResNetStage,
    SqueezeExcitation,
)
from tamm.layers.decoding import KVCacher
from tamm.layers.dropout import Dropout
from tamm.layers.embedding import (
    ConcatEmbedding,
    ConstantEmbedding,
    ConvEmbedding,
    Embedding,
    LowRankFactorizedEmbedding,
    UnionEmbedding,
)
from tamm.layers.feed_forward import FeedForward, TransformerFeedForward
from tamm.layers.lambda_layer import Lambda
from tamm.layers.linear import (
    FusedMultiOutputLinear,
    Linear,
    MultiOutputLinear,
    SegmentedLinear,
    TiedWeightLinear,
    TiedWeightLinearSequence,
    VectorizedLinear,
)
from tamm.layers.loss import FlattenedCrossEntropyLoss
from tamm.layers.norm import BatchNorm, L2Norm, LayerNorm, RMSNorm
from tamm.layers.pooler import (
    AdaptiveConvPooler,
    CAbstractorPooler,
    ConvPooler,
    SimpleAdaptiveAvgPooler,
)
from tamm.layers.positional_encoding import (
    AbsolutePositionalEmbedding,
    SpatialPositionalEmbedding,
)
from tamm.layers.residual import (
    GatedActivationResidualConnection,
    ResidualAdd,
    ShortcutAddActResidualConnection,
)
from tamm.layers.segmentation import (
    ConcatEmbeddingSegmentation,
    ConstantSegmentation,
    ConvEmbeddingPaddingTransform,
    TokensPaddingMask,
    UnionSegmentation,
)
from tamm.layers.sequential import Sequential
from tamm.layers.side_outputs import OutputWithSideOutputs
from tamm.layers.transformer import (
    ALiBiPositionalEncoding,
    AttentionMask,
    CausalLMTransformer,
    ExtendedTransformerStack,
    KVReuseTransformerLayerSequence,
    NoPositionalEncoding,
    RotaryPositionalEmbedding,
    SecondaryPositionalEncodings,
    SequentialPositionalEncoding,
    SinusoidalPositionalEmbedding,
    SlidingWindowPositionalEncoding,
    TextTransformerEncoder,
    TransformerAbsolutePositionalEmbedding,
    TransformerLayer,
    TransformerLayerSequence,
    TransformerPositionalEncoding,
    TransformerStack,
    TransformerTokenTypeEmbedding,
    TransformerTokenTypeEncoding,
    UniformTransformerLayerSequence,
    VisionTransformerEncoder,
    kv_cache,
)
