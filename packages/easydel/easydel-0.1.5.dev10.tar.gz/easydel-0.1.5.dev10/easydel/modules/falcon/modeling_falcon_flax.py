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


import functools
import math

import chex
import jax
from eformer import common_types
from eformer.escale import apply_logical_sharding
from flax import nnx as nn
from jax import numpy as jnp

from easydel.infra.base_module import EasyDeLBaseModule
from easydel.infra.factory import TaskType, register_module
from easydel.infra.modeling_outputs import (
    AttentionLayerOutput,
    BaseModelOutput,
    CausalLMOutput,
    DecoderLayerOutput,
)
from easydel.infra.utils import (
    auto_remat,
    block_wise_ffn,
    get_dot_general_by_bits,
)
from easydel.layers.attention import AttentionModule, FlexibleAttentionModule
from easydel.layers.caching import (
    PagedAttentionCache,
    PagedAttentionCacheView,
    PagedAttentionMetadata,
    TransformerCache,
    TransformerCacheView,
    TransformerMetadata,
)
from easydel.layers.linear import ParallelLinear

from .falcon_configuration import FalconConfig


def built_bloom_alibi(attention_mask, num_attention_heads):
    """The built_bloom_alibi function is used to create a bloom alibi for the attention mask.
    The bloom alibi is used in the Bloom Attention layer to ensure that each token has a unique
    attention vector, even if it's masked out. This ensures that all tokens have an equal chance of being selected as
    the most important token in the sequence, which helps with training stability and performance.

    Args:
        attention_mask: Mask out the padding tokens in the input
            sequence
        num_attention_heads: Determine the number of attention heads in
            the model

    Returns:
        A tensor of shape (batch_size, num_attention_heads, 1,
        sequence_length)
    """
    batch_size, sequence_length = attention_mask.shape
    cp2 = 2 ** math.floor(math.log2(num_attention_heads))
    base = jnp.asarray(2 ** (-(2 ** -(math.log2(cp2) - 3))), dtype=jnp.float32)
    powers = jnp.arange(1, 1 + cp2, dtype=jnp.float32)
    slops = jnp.power(base, powers)
    if cp2 != num_attention_heads:
        extra_base = jnp.asarray(2 ** (-(2 ** -(math.log2(2 * cp2) - 3))), dtype=jnp.float32)
        num_rem_heads = min(cp2, num_attention_heads - cp2)
        extra_power = jnp.arange(1, 1 + 2 * num_rem_heads, 2, dtype=jnp.dtype)
        slops = jnp.concatenate([slops, jnp.power(extra_base, extra_power)], axis=0)
    arange_tensor = (((jnp.cumsum(attention_mask, axis=-1)) - 1) * attention_mask)[:, jnp.newaxis, :]
    alibi = slops[..., jnp.newaxis].astype(jnp.bfloat16) * arange_tensor
    return alibi.reshape(batch_size, num_attention_heads, 1, sequence_length)


def dropout_add(
    nn_drop: nn.Dropout,
    x: chex.Array,
    residual: chex.Array,
) -> chex.Array:
    """The dropout_add function is a helper function that adds the residual to the output of
    the dropout layer. This is necessary because we want to use deterministic=True when
    we are evaluating our model, but we still need to add in the residual. The reason for this
    is that during training, we have two paths through our network: one with dropout and one without.
    The path without dropout (residual) allows us to backpropagate gradients through both paths at once.

    Args:
        nn_drop: nn.Dropout: Specify the dropout layer
        x: chex.Array: Pass in the input to the dropout layer
        residual: chex.Array: Add the residual to the output of
            dropout_add
        deterministic: bool: Determine whether the dropout layer is
            active or not

    Returns:
        A tensor that is the sum of the residual and a dropout layer
    """
    out = nn_drop(inputs=x)
    out = residual + out
    return out


class FalconAttention(AttentionModule):
    def __init__(
        self,
        config: FalconConfig,
        dtype: jnp.dtype = jnp.bfloat16,
        param_dtype: jnp.dtype = jnp.bfloat16,
        precision: jax.lax.PrecisionLike = None,
        *,
        rngs: nn.Rngs,
    ):
        super().__init__(config=config)
        self.dtype = dtype
        self.param_dtype = param_dtype
        self.precision = precision
        self.rngs = rngs
        head_dim = config.hidden_size // config.num_attention_heads
        if config.new_decoder_architecture:
            qkv_out_dim = (config.num_kv_heads * 2 + config.num_attention_heads) * head_dim
        elif config.multi_query:
            qkv_out_dim = config.hidden_size + 2 * head_dim
        else:
            qkv_out_dim = 3 * config.hidden_size

        self.head_dim = head_dim
        assert self.head_dim * config.num_attention_heads == config.hidden_size
        self.num_kv_heads = config.num_kv_heads if (config.new_decoder_architecture or not config.multi_query) else 1
        self.new_decoder_architecture = config.new_decoder_architecture
        self.num_heads = config.num_attention_heads
        self.query_key_value = ParallelLinear(
            config.hidden_size,
            qkv_out_dim,
            rngs=rngs,
            dtype=dtype,
            param_dtype=param_dtype,
            precision=precision,
            use_bias=config.bias,
            **get_dot_general_by_bits(config.bits, config.easy_method),
        )
        self.inv_norm_factor = 1 / math.sqrt(head_dim)
        self.dense = ParallelLinear(
            qkv_out_dim,
            config.hidden_size,
            rngs=rngs,
            dtype=dtype,
            param_dtype=param_dtype,
            use_bias=config.bias,
            precision=self.precision,
            **get_dot_general_by_bits(config.bits, config.easy_method),
        )
        if not self.config.alibi:
            self.rotary = self.config.get_basic_rope(
                rotary_dim=self.config.hidden_size // self.config.num_attention_heads,
                head_size=self.config.hidden_size // self.config.num_attention_heads,
                base=self.config.rope_theta,
                is_neox_style=True,
                dtype=self.dtype,
            )
        self.attention_performer = FlexibleAttentionModule(
            rngs=rngs,
            base_config=config,
            softmax_scale=self.head_dim**-0.5,
            dropout_prob=config.attention_dropout,
        )

    def _split_heads(self, qkv: chex.Array) -> tuple[chex.Array, chex.Array, chex.Array]:
        """
        Splits the query, key, and value tensors into separate heads.

        Args:
            qkv (chex.Array): Combined query, key, and value tensor.

        Returns:
            tp.Tuple[chex.Array, chex.Array, chex.Array]: A tuple containing the query, key,
                and value tensors split into heads.
        """
        batch_size, sequence_length, _ = qkv.shape

        if self.config.new_decoder_architecture:
            qkv = qkv.reshape(
                batch_size,
                sequence_length,
                -1,
                self.num_heads // self.num_kv_heads + 2,
                self.head_dim,
            )
            query_states = qkv[:, :, :, :-2]
            key_states = qkv[:, :, :, [-2]]
            value_states = qkv[:, :, :, [-1]]
            key_states = jnp.broadcast_to(key_states, query_states.shape)
            value_states = jnp.broadcast_to(value_states, query_states.shape)

            query_states, key_states, value_states = [
                x.reshape(x.shape[:-2] + (x.shape[-2] * x.shape[-1],)) for x in (query_states, key_states, value_states)
            ]

            return query_states, key_states, value_states
        if self.config.multi_query:
            qkv = qkv.reshape(batch_size, sequence_length, self.config.num_attention_heads + 2, -1)
            query_states, key_states, value_states = (
                qkv[..., :-2, :],
                qkv[..., [-2], :],
                qkv[..., [-1], :],
            )

        else:
            query_states, key_states, value_states = jnp.split(qkv, 3, -1)
        return query_states, key_states, value_states

    def _merge_heads(self, x: chex.Array) -> chex.Array:
        """
        Merges the attention heads into a single tensor.

        Args:
            x (chex.Array): Tensor with separate attention heads.

        Returns:
            chex.Array: Tensor with merged attention heads.
        """
        batch_size_and_num_heads, seq_length, _ = x.shape
        batch_size = batch_size_and_num_heads // self.num_heads
        x = x.reshape(batch_size, self.config.num_attention_heads, seq_length, self.head_dim)
        return x.reshape(batch_size, seq_length, self.config.num_attention_heads * self.head_dim)

    def __call__(
        self,
        hidden_states: chex.Array,
        attention_mask: chex.Array,
        position_ids: chex.Array,
        mode: common_types.RUNTIME_MODE_TYPES,  # type:ignore
        cache_view: TransformerCacheView | PagedAttentionCacheView | None = None,
        cache_metadata: TransformerMetadata | PagedAttentionMetadata | None = None,
        causal_mask: chex.Array | bool | None = None,
        segment_ids: chex.Array | None = None,
        alibi: chex.Array | None = None,
        output_attentions: bool = False,
        frequencies: chex.Array | None = None,
    ):
        fused_qkv = self.query_key_value(hidden_states)
        num_kv_heads = self.num_heads if self.new_decoder_architecture else self.num_kv_heads
        # 3 x [batch_size, seq_length, num_heads, head_dim]
        (query_states, key_states, value_states) = self._split_heads(fused_qkv)
        batch_size, query_length, _, _ = query_states.shape
        key_length = query_length
        query_states = query_states.reshape(
            batch_size,
            query_length,
            self.num_heads,
            self.head_dim,
        )
        key_states = key_states.reshape(
            batch_size,
            query_length,
            num_kv_heads,
            self.head_dim,
        )
        value_states = value_states.reshape(
            batch_size,
            query_length,
            num_kv_heads,
            self.head_dim,
        )

        (
            query_states,
            key_states,
            value_states,
        ) = self.apply_qkv_shardings(query_states, key_states, value_states)

        if alibi is None:
            query_states, key_states = self.rotary(
                positions=position_ids,
                query=query_states,
                key=key_states,
                frequencies=frequencies,
            )

        (
            key_states,
            value_states,
            attention_mask,
            init_attention_bias,
            cache_view,
        ) = self.concatenate(
            query=query_states,
            key=key_states,
            value=value_states,
            cache_view=cache_view,
            cache_metadata=cache_metadata,
            attention_mask=attention_mask,
            causal_mask=causal_mask,
            fcm_mask=None,
        )

        if alibi is None:
            attention = self.attention_performer.forward(
                query_states=query_states,
                key_states=key_states,
                value_states=value_states,
                mode=mode,
                bias=init_attention_bias(),
                cache_metadata=cache_metadata,
                cache_view=cache_view,
                init_bias=init_attention_bias,
                attention_mask=None,
                segment_ids=segment_ids,
                causal=True,
            )
            attention_outputs = attention.attention_outputs
            attention_outputs = attention_outputs.reshape(batch_size, query_length, self.num_heads * self.head_dim)
            output_tensor = self.dense(attention_outputs)
            return AttentionLayerOutput(
                attention_output=output_tensor,
                attention_weight=attention.attention_weights if output_attentions else None,
                cache_view=cache_view,
            )

        else:
            attention_scores = jnp.einsum(
                "...qhd,...khd->...hqk",
                query_states,
                key_states,
                precision=self.precision,
            )
            attention_scores = attention_scores.reshape(batch_size, self.num_heads, query_length, key_length)
            attention_scores = attention_scores + alibi.reshape(batch_size, self.num_heads, 1, -1)
            attention_scores *= self.inv_norm_factor
            attention_scores = jax.nn.softmax(
                attention_scores + init_attention_bias(),
                axis=-1,
            )
            attention_scores = attention_scores.reshape(batch_size, self.num_heads, query_length, key_length)
            # matmul: [batch_size * num_heads, q_length, head_dim]
            attn_output = jax.lax.batch_matmul(attention_scores, value_states.transpose(0, 2, 1, 3))
            attn_output = attn_output.reshape((attn_output.shape[1] * attn_output.shape[0],) + attn_output.shape[2:])
            attn_output = self.shard_attention_prod(self._merge_heads(attn_output))

            output_tensor = self.dense(attn_output)

            AttentionLayerOutput(
                attention_output=output_tensor,
                attention_weight=attention.attention_weights if output_attentions else None,
                cache_view=cache_view,
            )


class FalconMlp(nn.Module):
    def __init__(
        self,
        config: FalconConfig,
        dtype: jnp.dtype = jnp.bfloat16,
        param_dtype: jnp.dtype = jnp.bfloat16,
        precision: jax.lax.PrecisionLike = None,
        *,
        rngs: nn.Rngs,
    ):
        super().__init__()
        self.config = config
        self.dtype = dtype
        self.param_dtype = param_dtype
        self.precision = precision
        self.rngs = rngs
        linear = functools.partial(
            ParallelLinear,
            dtype=dtype,
            param_dtype=param_dtype,
            precision=precision,
            use_bias=self.config.bias,
            **get_dot_general_by_bits(config.bits, config.easy_method),
        )
        self.dense_h_to_4h = linear(
            self.config.hidden_size,
            self.config.ff_factor * self.config.hidden_size,
            rngs=rngs,
        )
        self.dense_4h_to_h = linear(
            self.config.ff_factor * self.config.hidden_size,
            self.config.hidden_size,
            rngs=rngs,
        )

    def __call__(self, x: chex.Array, deterministic: bool = True):
        x = apply_logical_sharding(
            x,
            dynamic_axes=common_types.HiddenStateSharding,
            partition_manager=self.config.partition_manager,
        )
        x = self.dense_4h_to_h(nn.gelu(self.dense_h_to_4h(x), approximate=False))
        x = apply_logical_sharding(
            x,
            dynamic_axes=common_types.HiddenStateSharding,
            partition_manager=self.config.partition_manager,
        )
        return x


class FalconBlock(nn.Module):
    def __init__(
        self,
        config: FalconConfig,
        dtype: jnp.dtype = jnp.bfloat16,
        param_dtype: jnp.dtype = jnp.bfloat16,
        precision: jax.lax.PrecisionLike = None,
        *,
        rngs: nn.Rngs,
    ):
        super().__init__()
        self.config = config
        self.dtype = dtype
        self.param_dtype = param_dtype
        self.precision = precision
        self.rngs = rngs

        if config.new_decoder_architecture and config.num_ln_in_parallel_attn == 2:
            self.ln_attn = nn.LayerNorm(
                self.config.hidden_size,
                epsilon=config.layer_norm_epsilon,
                dtype=self.dtype,
                param_dtype=self.param_dtype,
                rngs=rngs,
            )
            self.ln_mlp = nn.LayerNorm(
                self.config.hidden_size,
                epsilon=config.layer_norm_epsilon,
                dtype=self.dtype,
                param_dtype=self.param_dtype,
                rngs=rngs,
            )
        else:
            self.input_layernorm = nn.LayerNorm(
                self.config.hidden_size,
                epsilon=config.layer_norm_epsilon,
                dtype=self.dtype,
                param_dtype=self.param_dtype,
                rngs=rngs,
            )
            if not config.parallel_attn:
                self.post_attention_layernorm = nn.LayerNorm(
                    self.config.hidden_size,
                    epsilon=config.layer_norm_epsilon,
                    dtype=self.dtype,
                    param_dtype=self.param_dtype,
                    rngs=rngs,
                )
        attn_block = FalconAttention
        mlp_block = FalconMlp
        attn_block, mlp_block = auto_remat(
            attn_block,
            mlp_block,
            policy=config.gradient_checkpointing,
        )

        self.mlp = mlp_block(
            config=config,
            dtype=dtype,
            param_dtype=param_dtype,
            precision=precision,
            rngs=rngs,
        )
        self.self_attention = attn_block(
            config=config,
            dtype=dtype,
            param_dtype=param_dtype,
            precision=precision,
            rngs=rngs,
        )

        self.dropout = nn.Dropout(self.config.attention_dropout)
        self.dropout_mlp = nn.Dropout(self.config.hidden_dropout)

    def __call__(
        self,
        hidden_states: chex.Array,
        attention_mask: chex.Array,
        position_ids: chex.Array,
        mode: common_types.RUNTIME_MODE_TYPES,  # type:ignore
        cache_view: TransformerCacheView | PagedAttentionCacheView | None = None,
        cache_metadata: TransformerMetadata | PagedAttentionMetadata | None = None,
        causal_mask: chex.Array | bool | None = None,
        segment_ids: chex.Array | None = None,
        alibi: chex.Array | None = None,
        output_attentions: bool = False,
        frequencies: chex.Array | None = None,
    ):
        """
        Forward pass of the FalconBlock module.

        Args:
            hidden_states (chex.Array): Input hidden states.
            attention_mask (chex.Array): Mask to apply on the attention scores.
            position_ids (chex.Array): Position indices for the tokens.
            causal_mask (chex.Array, optional): Causal mask for ensuring autoregressive behavior.
            segment_ids (tp.Optional[chex.Array], optional): Segment IDs for segment-based attention.
            alibi (tp.Optional[chex.Array], optional): Alibi tensor for adding positional bias.
            init_cache (bool, optional): If True, initializes cache for caching keys and values.
            output_attentions (bool, optional): If True, outputs attention weights alongside the hidden states.
            deterministic (bool, optional): If True, disables dropout for deterministic behavior.

        Returns:
            tp.Union[chex.Array, tp.Tuple[chex.Array, chex.Array]]: The output tensor and optionally
                the attention weights.
        """
        residual = hidden_states

        if self.config.num_ln_in_parallel_attn == 2:
            attention_layernorm_out = self.ln_attn(hidden_states)
            mlp_layernorm_out = self.ln_mlp(hidden_states)
        else:
            attention_layernorm_out = self.input_layernorm(hidden_states)

        attn_outputs = self.self_attention(
            attention_layernorm_out,
            attention_mask,
            position_ids,
            mode,
            cache_view,
            cache_metadata,
            causal_mask,
            segment_ids,
            alibi,
            output_attentions,
            frequencies,
        )

        if self.config.num_ln_in_parallel_attn == 1:
            if self.config.parallel_attn:
                mlp_layernorm_out = attention_layernorm_out
            else:
                residual = dropout_add(self.dropout, attn_outputs.attention_output, residual)
                mlp_layernorm_out = self.post_attention_layernorm(residual)

        if self.config.use_scan_mlp:
            mlp_output = block_wise_ffn(
                self.mlp,
                mlp_layernorm_out,
                self.config.scan_mlp_chunk_size,
            )
        else:
            mlp_output = self.mlp(mlp_layernorm_out)

        if self.config.new_decoder_architecture or self.config.parallel_attn:
            mlp_output += attn_outputs.attention_output

        output = dropout_add(self.dropout_mlp, mlp_output, residual)
        return DecoderLayerOutput(
            hidden_states=output,
            attention_weight=attn_outputs.attention_weight,
            cache_view=attn_outputs.cache_view,
        )


@register_module(TaskType.BASE_MODULE, config=FalconConfig, model_type="falcon")
class FalconModel(EasyDeLBaseModule):
    def __init__(
        self,
        config: FalconConfig,
        dtype: jnp.dtype = jnp.bfloat16,
        param_dtype: jnp.dtype = jnp.bfloat16,
        precision: jax.lax.PrecisionLike = None,
        *,
        rngs: nn.Rngs,
    ):
        super().__init__(
            config=config,
            dtype=dtype,
            param_dtype=param_dtype,
            precision=precision,
            rngs=rngs,
        )
        self.word_embeddings = nn.Embed(
            num_embeddings=config.vocab_size,
            features=config.hidden_size,
            dtype=dtype,
            param_dtype=param_dtype,
            rngs=rngs,
        )
        self.h = [
            FalconBlock(
                config=config,
                dtype=dtype,
                param_dtype=param_dtype,
                precision=precision,
                rngs=rngs,
            )
            for i in range(self.config.num_hidden_layers)
        ]
        self.ln_f = nn.LayerNorm(
            self.config.hidden_size,
            dtype=dtype,
            param_dtype=param_dtype,
            epsilon=config.layer_norm_epsilon,
            rngs=rngs,
        )

    def __call__(
        self,
        input_ids: chex.Array | None = None,
        inputs_embeds: chex.Array | None = None,
        attention_mask: chex.Array | None = None,
        position_ids: chex.Array | None = None,
        segment_ids: chex.Array | None = None,
        output_attentions: bool | None = None,
        output_hidden_states: bool | None = None,
        mode: common_types.RUNTIME_MODE_TYPES | None = None,  # type:ignore
        past_key_values: TransformerCache | PagedAttentionCache | None = None,
        cache_metadata: TransformerMetadata | PagedAttentionMetadata | None = None,
    ) -> BaseModelOutput:
        """
        Forward pass through the Falcon module.

        Args:
            input_ids (chex.Array): Input tensor containing token IDs.
            attention_mask (chex.Array): Mask for attention.
            position_ids (chex.Array): Positional indices.
            segment_ids (tp.Optional[chex.Array]): Segment IDs for different input parts.
            inputs_embeds (tp.Optional[chex.Array]): Embedded input tensor.
            output_attentions (tp.Optional[bool]): If True, output attention weights.
            output_hidden_states (tp.Optional[bool]): If True, output hidden states.
            init_cache (bool): If True, initialize cache for decoding.
            deterministic (bool): If True, disable dropout.

        Returns:
            BaseModelOutput | tp.Tuple: Model output, either as a named tuple or a standard tuple.
        """
        all_hidden_states = () if output_hidden_states else None
        all_attentions = () if output_attentions else None
        if (input_ids is None) ^ (inputs_embeds is not None):
            raise ValueError(
                "You cannot specify both input_ids and inputs_embeds at the same time, and must specify either one"
            )
        if inputs_embeds is None:
            inputs_embeds = self.word_embeddings(input_ids.astype("i4"))

        batch_size, sequence_length, _ = inputs_embeds.shape

        if attention_mask is None:
            attention_mask = jnp.ones((batch_size, sequence_length), dtype="i4")
        alibi = None
        if self.config.alibi:
            alibi = built_bloom_alibi(
                attention_mask,
                self.config.num_attention_heads,
            ).astype(inputs_embeds.dtype)
        elif position_ids is None:
            position_ids = jnp.broadcast_to(
                jnp.clip(jnp.cumsum(attention_mask, axis=-1) - 1, a_min=0),
                (batch_size, sequence_length),
            ).astype(jnp.int32)
        if attention_mask.ndim == 2:
            attention_mask = jnp.expand_dims(attention_mask, (-3, -2))
        if mode is None:
            mode = (
                common_types.MODE_DECODE
                if sequence_length == 1 and past_key_values is not None
                else common_types.MODE_TRAIN
            )
        if past_key_values is None:
            past_key_values = TransformerCache.init_empty(len(self.h))
        hidden_states = inputs_embeds
        for idx, layer in enumerate(self.h):
            layer_outputs = layer(
                hidden_states=hidden_states,
                alibi=alibi,
                attention_mask=attention_mask,
                position_ids=position_ids,
                causal_mask=self.causal_mask,
                mode=mode,
                cache_view=past_key_values.views[idx],
                cache_metadata=cache_metadata,
                output_attentions=output_attentions,
                segment_ids=segment_ids,
                frequencies=self.frequencies,
            )
            hidden_states = layer_outputs.hidden_states
            if output_hidden_states:
                all_hidden_states += (hidden_states,)
            if output_attentions:
                all_attentions += (layer_outputs.attention_weight,)

            past_key_values[idx] = layer_outputs.cache_view

        hidden_states = self.ln_f(hidden_states)

        if all_hidden_states is not None:
            all_hidden_states += hidden_states

        return BaseModelOutput(
            last_hidden_state=hidden_states,
            hidden_states=all_hidden_states,
            attentions=all_attentions,
            past_key_values=past_key_values,
        )


@register_module(TaskType.CAUSAL_LM, config=FalconConfig, model_type="falcon")
class FalconForCausalLM(EasyDeLBaseModule):
    """Falcon model with a language modeling head for causal language modeling tasks.

    This model extends the base FalconModel by incorporating a linear language modeling head on top
    of the base model, designed for generative tasks and text generation. The model can use either
    alibi positional embeddings or rotary position embeddings (RoPE) based on configuration.
    """

    def __init__(
        self,
        config: FalconConfig,
        dtype: jnp.dtype = jnp.bfloat16,
        param_dtype: jnp.dtype = jnp.bfloat16,
        precision: jax.lax.PrecisionLike = None,
        *,
        rngs: nn.Rngs,
    ):
        """Initialize a FalconForCausalLM model.

        Args:
                config (FalconConfig): Configuration object for the model.
                dtype (jnp.dtype, optional): Data type for activations and weights. Defaults to jnp.float32.
                param_dtype (jnp.dtype, optional): Data type for parameters. Defaults to jnp.float32.
                precision (jax.lax.PrecisionLike, optional): Numerical precision for computations. Defaults to None.
                rngs (nn.Rngs): Random number generator keys for initialization.
        """
        super().__init__(
            config=config,
            dtype=dtype,
            param_dtype=param_dtype,
            precision=precision,
            rngs=rngs,
        )
        self.transformer = FalconModel(
            config=config,
            dtype=dtype,
            param_dtype=param_dtype,
            precision=precision,
            rngs=rngs,
        )

        self.lm_head = ParallelLinear(
            config.hidden_size,
            config.vocab_size,
            dtype=dtype,
            param_dtype=param_dtype,
            precision=precision,
            rngs=rngs,
            use_bias=False,
            **get_dot_general_by_bits(config.bits, config.easy_method),
        )

    def __call__(
        self,
        input_ids: chex.Array | None = None,
        inputs_embeds: chex.Array | None = None,
        attention_mask: chex.Array | None = None,
        position_ids: chex.Array | None = None,
        segment_ids: chex.Array | None = None,
        output_attentions: bool | None = None,
        output_hidden_states: bool | None = None,
        mode: common_types.RUNTIME_MODE_TYPES | None = None,  # type:ignore
        past_key_values: TransformerCache | PagedAttentionCache | None = None,
        cache_metadata: TransformerMetadata | PagedAttentionMetadata | None = None,
    ) -> CausalLMOutput:
        """
        Forward pass through the Falcon module.

        Args:
            input_ids (tp.Optional[chex.Array]): Input tensor containing token IDs.
            attention_mask (tp.Optional[chex.Array]): Mask for attention.
            position_ids (tp.Optional[chex.Array]): Positional indices.
            segment_ids (tp.Optional[chex.Array]): Segment IDs for different input parts.
            inputs_embeds (tp.Optional[chex.Array]): Embedded input tensor.
            output_attentions (tp.Optional[bool]): If True, output attention weights.
            output_hidden_states (tp.Optional[bool]): If True, output hidden states.
            init_cache (bool): If True, initialize cache for decoding.
            deterministic (bool): If True, disable dropout.

        Returns:
            CausalLMOutput | tp.Tuple: Model output, either as a named tuple or a standard tuple.
        """
        outputs = self.transformer(
            input_ids=input_ids,
            attention_mask=attention_mask,
            position_ids=position_ids,
            output_attentions=output_attentions,
            mode=mode,
            past_key_values=past_key_values,
            cache_metadata=cache_metadata,
            inputs_embeds=inputs_embeds,
            output_hidden_states=output_hidden_states,
            segment_ids=segment_ids,
        )
        hidden_state = outputs.last_hidden_state

        logits = self.lm_head(hidden_state)

        return CausalLMOutput(
            logits=logits,
            hidden_states=outputs.hidden_states,
            attentions=outputs.attentions,
            past_key_values=outputs.past_key_values,
        )
