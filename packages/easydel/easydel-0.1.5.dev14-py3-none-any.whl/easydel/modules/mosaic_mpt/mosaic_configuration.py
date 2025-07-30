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
from easydel.infra.etils import EasyDeLGradientCheckPointers
from easydel.infra.factory import register_config


class MptAttentionConfig(EasyDeLBaseConfig):
    """
    This is the configuration class to store the attention related configuration of a [`MptModel`].

    Args:
        attn_type (`str`, *optional*, defaults to `"multihead_attention"`):
            The type of attention to use. Can be either `"multihead_attention"` or `"multiquery_attention"`.
        attn_pdrop (`float`, *optional*, defaults to 0.0):
            The dropout probability applied to the attention output.
        attn_impl (`str`, *optional*, defaults to `"torch"`):
            The implementation of the attention mechanism. Can be either `"torch"` or `"flash"`.
        clip_qkv (`float`, *optional*):
            The clip value applied to the query, key, and value tensors.
        softmax_scale (`float`, *optional*):
            The scale factor applied to the softmax function in the attention layer.
        prefix_lm (`bool`, *optional*, defaults to `False`):
            Whether to use a prefix LM.
        qk_ln (`bool`, *optional*, defaults to `False`):
            Whether to apply layer normalization to the query and key tensors.
        attn_uses_sequence_id (`bool`, *optional*, defaults to `False`):
            Whether the attention layer uses sequence IDs.
        alibi (`bool`, *optional*, defaults to `True`):
            Whether to use the ALiBi (Attention with Linear Biases) method.
        alibi_bias_max (`int`, *optional*, defaults to 8):
            The maximum value for the ALiBi bias.
    """

    def __init__(
        self,
        attn_type="multihead_attention",
        attn_pdrop=0,
        attn_impl="torch",
        clip_qkv=None,
        softmax_scale=None,
        prefix_lm=False,
        qk_ln=False,
        attn_uses_sequence_id=False,
        alibi=True,
        alibi_bias_max=8,
        **kwargs,
    ):
        """Initializes an MptAttentionConfig object.

        Args:
            attn_type (str, optional): Type of attention mechanism. Defaults to "multihead_attention".
            attn_pdrop (float, optional): Dropout probability for attention output. Defaults to 0.
            attn_impl (str, optional): Implementation of attention ("torch" or "flash"). Defaults to "torch".
            clip_qkv (float, optional): Clipping value for QKV projections. Defaults to None.
            softmax_scale (float, optional): Scale factor for softmax. Defaults to None.
            prefix_lm (bool, optional): Whether to use prefix language modeling. Defaults to False.
            qk_ln (bool, optional): Whether to apply LayerNorm to Q and K. Defaults to False.
            attn_uses_sequence_id (bool, optional): Whether attention uses sequence IDs. Defaults to False.
            alibi (bool, optional): Whether to use ALiBi positional bias. Defaults to True.
            alibi_bias_max (int, optional): Maximum ALiBi bias value. Defaults to 8.
            **kwargs: Additional keyword arguments.
        """
        super().__init__()
        self.attn_type = attn_type
        self.attn_pdrop = attn_pdrop
        self.attn_impl = attn_impl
        self.clip_qkv = clip_qkv
        self.softmax_scale = softmax_scale
        self.prefix_lm = prefix_lm
        self.attn_uses_sequence_id = attn_uses_sequence_id
        self.alibi = alibi
        self.qk_ln = qk_ln
        self.alibi_bias_max = alibi_bias_max

        if attn_type not in ["multihead_attention", "multiquery_attention"]:
            raise ValueError(
                f"`attn_type` has to be either `multihead_attention` or `multiquery_attention`. Received: {attn_type}"
            )

    @classmethod
    def from_pretrained(cls, pretrained_model_name_or_path, **kwargs) -> "EasyDeLBaseConfig":
        """Loads attention configuration from a pretrained model configuration file.

        Args:
            cls (type): The class itself.
            pretrained_model_name_or_path (str): Path or identifier of the pretrained model.
            **kwargs: Additional keyword arguments passed to `get_config_dict` and `from_dict`.

        Returns:
            EasyDeLBaseConfig: An instance of MptAttentionConfig loaded from the pretrained model.
        """
        cls._set_token_in_kwargs(kwargs)
        config_dict, kwargs = cls.get_config_dict(pretrained_model_name_or_path, **kwargs)
        if config_dict.get("model_type") == "mpt":
            config_dict = config_dict["attn_config"]
        return cls.from_dict(config_dict, **kwargs)


@register_config("mpt")
class MptConfig(EasyDeLBaseConfig):
    """
    Configuration objects inherit from [`EasyDeLBaseConfig`] and can be used to control the model outputs. Read
    the documentation from [`EasyDeLBaseConfig`] for more information.

    Args:
        d_model (`int`, *optional*, defaults to 2048):
            Dimensionality of the encoder layers and the pooler layer.
        n_heads (`int`, *optional*, defaults to 16):
            Number of attention heads for each attention layer in the Transformer encoder.
        n_layers (`int`, *optional*, defaults to 24):
            Number of hidden layers in the Transformer encoder.
        expansion_ratio (`int`, *optional*, defaults to 4):
            Expansion ratio of the feed-forward layer.
        max_seq_len (`int`, *optional*, defaults to 2048):
            The maximum sequence length that this model might ever be used with. Typically set this to something large
            just in case (e.g., 2048 or 4096).
        vocab_size (`int`, *optional*, defaults to 50368):
            Vocabulary size of the MPT model. Defines the number of different tokens that can be represented by the
            `inputs_ids` passed to the forward method.
        resid_prob_drop (`float`, *optional*, defaults to 0.0):
            The dropout probability for all fully connected layers in the embeddings, encoder, and pooler.
        layer_norm_epsilon (`float`, *optional*, defaults to 1e-5):
            The epsilon used by the layer normalization layers.
        emb_prob_drop (`float`, *optional*, defaults to 0.0):
            The dropout ratio for the embeddings.
        learned_pos_emb (`bool`, *optional*, defaults to `True`):
            Whether to learn positional embeddings.
        attn_config ([`MptAttentionConfig`], *optional*):
            The configuration of the attention layer.
        init_device (`str`, *optional*, defaults to `"cpu"`):
            The device to initialize the model on.
        logit_scale (`float` or `str`, *optional*):
            The logit scale. If set to `"inv_sqrt_d_model"`, the logit scale is calculated as `1 / math.sqrt(d_model)`.
        no_bias (`bool`, *optional*, defaults to `True`):
            Whether to use bias in the linear layers.
        verbose (`int`, *optional*, defaults to 0):
            The verbosity level.
        embedding_fraction (`float`, *optional*, defaults to 1.0):
            The fraction of the embedding matrix to use.
        norm_type (`str`, *optional*, defaults to `"low_precision_layernorm"`):
            The type of layer normalization to use.
        use_cache (`bool`, *optional*, defaults to `False`):
            Whether or not the model should return the last key/values attentions (not used by all models). Only
            relevant if `config.is_decoder=True`.
        initializer_range (`float`, *optional*, defaults to 0.02):
            The standard deviation of the truncated_normal_initializer for initializing all weight matrices.
        alibi (`bool`, *optional*, defaults to `True`):
            Whether to use ALiBi (Attention with Linear Biases) method.
        use_bias (`bool`, *optional*, defaults to `False`):
            Whether to use bias in the linear layers.
        act_fn (`str`, *optional*, defaults to `"gelu"`):
            The activation function to use.
        qk_ln (`bool`, *optional*, defaults to `False`):
            Whether to apply layer normalization to the query and key tensors.
        use_lm_head (`bool`, *optional*, defaults to `False`):
            Whether to use a language modeling head.
        use_norm_bias (`bool`, *optional*, defaults to `False`):
            Whether to use bias in the layer normalization layers.
        gradient_checkpointing (`str`, *optional*, defaults to `"nothing_saveable"`):
            The gradient checkpointing configuration.
        bits (`int`, *optional*):
            The number of bits to quantize the model to.
    """

    model_type = "mpt"
    attribute_map = {
        "num_attention_heads": "n_heads",
        "hidden_size": "d_model",
        "num_hidden_layers": "n_layers",
        "max_position_embeddings": "max_seq_len",
        "tie_word_embeddings": "use_lm_head",
    }

    def __init__(
        self,
        d_model: int = 2048,
        n_heads: int = 16,
        n_layers: int = 24,
        expansion_ratio: int = 4,
        max_seq_len: int = 2048,
        vocab_size: int = 50368,
        resid_prob_drop: float = 0.0,
        layer_norm_epsilon: float = 1e-5,
        emb_prob_drop: float = 0.0,
        learned_pos_emb: bool = True,
        attn_config: MptAttentionConfig | None = None,
        init_device: str = "cpu",  # Ignored by EasyDeL.
        logit_scale: float | str | None = None,
        no_bias: bool = True,
        verbose: int = 0,
        embedding_fraction: float = 1.0,
        norm_type: str = "low_precision_layernorm",
        use_cache: bool = False,
        initializer_range=0.02,
        alibi: bool = True,
        use_bias: bool = False,
        act_fn: str = "gelu",
        qk_ln: bool = False,
        use_lm_head: bool = False,
        use_norm_bias: bool = False,
        gradient_checkpointing: EasyDeLGradientCheckPointers = EasyDeLGradientCheckPointers.NONE,
        bits: int | None = None,
        **kwargs,
    ):
        """Initializes an MptConfig object.

        Args:
            d_model (int, optional): Hidden size. Defaults to 2048.
            n_heads (int, optional): Number of attention heads. Defaults to 16.
            n_layers (int, optional): Number of hidden layers. Defaults to 24.
            expansion_ratio (int, optional): Expansion ratio for MLP. Defaults to 4.
            max_seq_len (int, optional): Maximum sequence length. Defaults to 2048.
            vocab_size (int, optional): Vocabulary size. Defaults to 50368.
            resid_prob_drop (float, optional): Residual dropout probability. Defaults to 0.0.
            layer_norm_epsilon (float, optional): Epsilon for layer normalization. Defaults to 1e-5.
            emb_prob_drop (float, optional): Embedding dropout probability. Defaults to 0.0.
            learned_pos_emb (bool, optional): Whether to learn positional embeddings. Defaults to True.
            attn_config (MptAttentionConfig, optional): Attention configuration. Defaults to None.
            init_device (str, optional): Device for initialization (ignored). Defaults to "cpu".
            logit_scale (float | str, optional): Logit scaling factor. Defaults to None.
            no_bias (bool, optional): Whether to disable bias in linear layers. Defaults to True.
            verbose (int, optional): Verbosity level (ignored). Defaults to 0.
            embedding_fraction (float, optional): Embedding fraction (ignored). Defaults to 1.0.
            norm_type (str, optional): Type of layer normalization. Defaults to "low_precision_layernorm".
            use_cache (bool, optional): Whether to use KV cache. Defaults to False.
            initializer_range (float, optional): Initializer range. Defaults to 0.02.
            alibi (bool, optional): Whether to use ALiBi positional bias. Defaults to True.
            use_bias (bool, optional): Whether to use bias in linear layers. Defaults to False.
            act_fn (str, optional): Activation function. Defaults to "gelu".
            qk_ln (bool, optional): Whether to apply LayerNorm to Q and K. Defaults to False.
            use_lm_head (bool, optional): Whether to use a language modeling head (tied embeddings). Defaults to False.
            use_norm_bias (bool, optional): Whether to use bias in layer normalization. Defaults to False.
            gradient_checkpointing (EasyDeLGradientCheckPointers, optional): Gradient checkpointing strategy.
                Defaults to EasyDeLGradientCheckPointers.NONE.
            bits (tp.Optional[int], optional): Quantization bits. Defaults to None.
            **kwargs: Additional keyword arguments.
        """
        if attn_config is None:
            self.attn_config = MptAttentionConfig(**kwargs)
        elif isinstance(attn_config, dict):
            self.attn_config = MptAttentionConfig(**attn_config | kwargs)
        else:
            self.attn_config = attn_config
        self.d_model = d_model
        self.use_norm_bias = use_norm_bias
        self.use_lm_head = use_lm_head
        self.n_heads = n_heads
        self.n_layers = n_layers
        self.expansion_ratio = expansion_ratio
        self.max_seq_len = max_seq_len
        self.vocab_size = vocab_size
        self.resid_prob_drop = resid_prob_drop
        self.use_bias = use_bias
        self.emb_prob_drop = emb_prob_drop
        self.gradient_checkpointing = gradient_checkpointing
        self.norm_type = norm_type
        self.learned_pos_emb = learned_pos_emb
        self.act_fn = act_fn
        self.logit_scale = logit_scale
        self.no_bias = no_bias
        self.qk_ln = qk_ln
        self.alibi = alibi
        self.verbose = verbose
        self.initializer_range = initializer_range
        self.embedding_fraction = embedding_fraction
        self.init_device = init_device
        self.use_cache = use_cache
        self.bits = bits
        self.layer_norm_epsilon = layer_norm_epsilon
        self.from_pt = False

        super().__init__(bits=bits, **kwargs)

    @staticmethod
    def _set_config_defaults(config, config_defaults):
        """Sets default values for missing configuration parameters.

        Args:
            config (dict): The configuration dictionary to update.
            config_defaults (dict): A dictionary containing default values.

        Returns:
            dict: The updated configuration dictionary.
        """
        for k, v in config_defaults.items():
            if k not in config:
                config[k] = v
        return config

    def get_partition_rules(self, *args, **kwargs):
        """
        Get the partition rules for the model.
        Returns:
            `tp.Tuple[tp.Tuple[str, PartitionSpec]]`: The partition rules.
        """
        pmag = self.partition_manager
        return (
            (r"wte/embedding", pmag.resolve(ColumnWise)),
            (r"attn/Wqkv/kernel", pmag.resolve(ColumnWise)),
            (r"attn/out_proj/kernel", pmag.resolve(RowWise)),
            (r"ffn/up_proj/kernel", pmag.resolve(ColumnWise)),
            (r"ffn/down_proj/kernel", pmag.resolve(RowWise)),
            (r".*/(norm_1|norm_2|norm_f)/scale", pmag.resolve(Replicated)),
            (r".*/(norm_1|norm_2|norm_f)/bias", pmag.resolve(Replicated)),
            (r"lm_head/kernel", pmag.resolve(ColumnWise)),
            (r".*(Wqkv|out_proj|up_proj|down_proj|lm_head)/bias", pmag.resolve(Replicated)),
            (r".*", pmag.resolve(Replicated)),
        )
