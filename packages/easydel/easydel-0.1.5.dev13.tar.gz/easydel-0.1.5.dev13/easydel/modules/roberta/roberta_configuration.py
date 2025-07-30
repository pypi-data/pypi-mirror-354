# Copyright 2023 The EASYDEL Author @erfanzar (Erfan Zare Chavoshi).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from eformer.common_types import ColumnWise, Replicated, RowWise

from easydel.infra.base_module import EasyDeLBaseConfig
from easydel.infra.factory import register_config


@register_config("roberta")
class RobertaConfig(EasyDeLBaseConfig):
    """
    Configuration objects inherit from [`EasyDeLBaseConfig`] and can be used to control the model outputs. Read
    the documentation from [`EasyDeLBaseConfig`] for more information.
    Args:
        vocab_size (:obj:`int`, *optional*, defaults to 50265):
            Vocabulary size of the RoBERTa model. Defines the number of different tokens that can be represented by
            the :obj:`inputs_ids` passed when calling :class:`~easydel.modules.RobertaModel`.
        hidden_size (:obj:`int`, *optional*, defaults to 768):
            Dimensionality of the encoder layers and the pooler layer.
        num_hidden_layers (:obj:`int`, *optional*, defaults to 12):
            Number of hidden layers in the Transformer encoder.
        num_attention_heads (:obj:`int`, *optional*, defaults to 12):
            Number of attention heads for each attention layer in the Transformer encoder.
        intermediate_size (:obj:`int`, *optional*, defaults to 3072):
            Dimensionality of the "intermediate" (i.e., feed-forward) layer in the Transformer encoder.
        hidden_act (:obj:`str` or :obj:`function`, *optional*, defaults to :obj:`"gelu"`):
            The non-linear activation function (function or string) in the encoder and pooler. If string, :obj:`"gelu"`,
            :obj:`"relu"`, :obj:`"swish"` and :obj:`"gelu_new"` are supported.
        hidden_dropout_prob (:obj:`float`, *optional*, defaults to 0.1):
            The dropout probability for all fully connected layers in the embeddings, encoder, and pooler.
        attention_probs_dropout_prob (:obj:`float`, *optional*, defaults to 0.1):
            The dropout ratio for the attention probabilities.
        max_position_embeddings (:obj:`int`, *optional*, defaults to 514):
            The maximum sequence length that this model might ever be used with. Typically set this to something large
            just in case (e.g., 512 or 1024 or 2048).
        type_vocab_size (:obj:`int`, *optional*, defaults to 1):
            The vocabulary size of the :obj:`token_type_ids` passed when calling
            :class:`~easydel.modules.RobertaModel`.
        initializer_range (:obj:`float`, *optional*, defaults to 0.02):
            The standard deviation of the truncated_normal_initializer for initializing all weight matrices.
        layer_norm_eps (:obj:`float`, *optional*, defaults to 1e-5):
            The epsilon used by the layer normalization layers.
        position_embedding_type (:obj:`str`, *optional*, defaults to :obj:`"absolute"`):
            Type of position embedding. Choose one of :obj:`"absolute"`, :obj:`"relative_key"`,
            :obj:`"relative_key_query"`. For positional embeddings use :obj:`"absolute"`. For more information on
            :obj:`"relative_key"`, please refer to [Self-Attention with Relative Position Representations (Shaw et
            al.)](https://arxiv.org/abs/1803.02155). For more information on :obj:`"relative_key_query"`, please
            refer to *Method 4* in [Improve Transformer Models with Better Relative Position Embeddings (Huang et
            al.)](https://arxiv.org/abs/2009.13658).
        use_cache (:obj:`bool`, *optional*, defaults to :obj:`True`):
            Whether or not the model should return the last key/values attentions (not used by all models). Only
            relevant if ``config.is_decoder=True``.
        classifier_dropout (:obj:`float`, *optional*):
            The dropout ratio for the classification head.
        gradient_checkpointing (:obj:`str`, *optional*, defaults to :obj:`"nothing_saveable"`):
            What to save during gradient checkpointing. Choose one of :obj:`"nothing_saveable"`,
            :obj:`"first_half_saveable"`, :obj:`"full_saveable"`.
    """

    model_type: str = "roberta"

    def __init__(
        self,
        vocab_size=50265,
        hidden_size=768,
        num_hidden_layers=12,
        num_attention_heads=12,
        intermediate_size=3072,
        hidden_act="gelu",
        hidden_dropout_prob=0.1,
        attention_probs_dropout_prob=0.1,
        max_position_embeddings=514,
        type_vocab_size=1,
        initializer_range=0.02,
        layer_norm_eps=1e-5,
        pad_token_id=1,
        bos_token_id=0,
        eos_token_id=2,
        position_embedding_type="absolute",
        use_cache=True,
        classifier_dropout=None,
        gradient_checkpointing="nothing_saveable",
        **kwargs,
    ):
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
        self.num_hidden_layers = num_hidden_layers
        self.num_attention_heads = num_attention_heads
        self.hidden_act = hidden_act
        self.intermediate_size = intermediate_size
        self.hidden_dropout_prob = hidden_dropout_prob
        self.attention_probs_dropout_prob = attention_probs_dropout_prob
        self.max_position_embeddings = max_position_embeddings
        self.type_vocab_size = type_vocab_size
        self.initializer_range = initializer_range
        self.layer_norm_eps = layer_norm_eps
        self.position_embedding_type = position_embedding_type
        self.use_cache = use_cache
        self.classifier_dropout = classifier_dropout
        self.gradient_checkpointing = gradient_checkpointing
        super().__init__(
            pad_token_id=pad_token_id,
            bos_token_id=bos_token_id,
            eos_token_id=eos_token_id,
            **kwargs,
        )

    def get_partition_rules(self, *args, **kwargs):
        """
        Get the partition rules for the RoBERTa model.
        Returns:
            `tp.Tuple[tp.Tuple[str, PartitionSpec]]`: The partition rules.
        """
        pmag = self.partition_manager
        return (
            (r"embeddings/word_embeddings/embedding", pmag.resolve(ColumnWise)),
            (r"embeddings/position_embeddings/embedding", pmag.resolve(Replicated)),
            (r"embeddings/token_type_embeddings/embedding", pmag.resolve(Replicated)),
            (r"attention/self/(query|key|value)/kernel", pmag.resolve(ColumnWise)),
            (r"attention/output/dense/kernel", pmag.resolve(RowWise)),
            (r"intermediate/dense/kernel", pmag.resolve(ColumnWise)),
            (r"output/dense/kernel", pmag.resolve(RowWise)),
            (r"pooler/dense/kernel", pmag.resolve(ColumnWise)),
            (r"lm_head/dense/kernel", pmag.resolve(ColumnWise)),
            (r"lm_head/decoder/kernel", pmag.resolve(ColumnWise)),
            (r"classifier/dense/kernel", pmag.resolve(ColumnWise)),
            (r"classifier/out_proj/kernel", pmag.resolve(RowWise)),
            (r"qa_outputs/kernel", pmag.resolve(RowWise)),
            (r".*LayerNorm/scale", pmag.resolve(Replicated)),
            (r".*LayerNorm/bias", pmag.resolve(Replicated)),
            (
                r".*/(query|key|value|dense|fc1|fc2|c_attn|q_attn|c_proj|c_fc|lm_head|classifier|qa_outputs)/bias",
                pmag.resolve(Replicated),
            ),
            (r"lm_head/bias", pmag.resolve(Replicated)),
            (r".*", pmag.resolve(Replicated)),
        )
