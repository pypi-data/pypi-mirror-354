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

import chex
import jax.lax
from chex import Array
from eformer import common_types
from eformer.escale import apply_logical_sharding
from flax import nnx as nn
from jax import numpy as jnp
from jax.sharding import PartitionSpec

from easydel.infra.base_module import EasyDeLBaseModule
from easydel.infra.factory import TaskType, register_module
from easydel.infra.modeling_outputs import (
    AttentionLayerOutput,
    BaseModelOutput,
    CausalLMOutput,
)
from easydel.infra.utils import (
    ACT2FN,
    auto_remat,
    block_wise_ffn,
    get_dot_general_by_bits,
    with_sharding_constraint,
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
from easydel.layers.norms import RMSNorm as RMSNorm

from .phimoe_configuration import PhiMoeConfig


class PhiMoEBlockSparseTop2MLP(nn.Module):
    """PhiMoE Block Sparse Top-2 MLP module.

    This module implements the feed-forward network (MLP) for a single expert
    in the PhiMoE model's Mixture of Experts layer. It uses a Gated Linear Unit (GLU)
    structure with SiLU activation.

    Attributes:
        config (PhiMoeConfig): Configuration object for the model.
        dtype (jnp.dtype): Data type for computations.
        param_dtype (jnp.dtype): Data type for parameters.
        precision (jax.lax.PrecisionLike): Precision setting for JAX operations.
        w1 (ParallelLinear): First linear layer (part of the GLU gate).
        w2 (ParallelLinear): Second linear layer (down-projection).
        w3 (ParallelLinear): Third linear layer (part of the GLU value).
        act_fn (callable): Activation function (SiLU).
    """

    def __init__(
        self,
        config: PhiMoeConfig,
        dtype: jnp.dtype = jnp.bfloat16,
        param_dtype: jnp.dtype = jnp.bfloat16,
        precision: jax.lax.PrecisionLike = None,
        *,
        rngs: nn.Rngs,
    ):
        """Initializes the PhiMoEBlockSparseTop2MLP module.

        Args:
            config (PhiMoeConfig): The configuration object for the PhiMoE model.
            dtype (jnp.dtype): Data type for computation. Defaults to jnp.float32.
            param_dtype (jnp.dtype): Data type for parameters. Defaults to jnp.float32.
            precision (jax.lax.PrecisionLike): Precision setting for JAX operations. Defaults to None.
            rngs (nn.Rngs): Random number generators.
        """
        self.config = config
        self.dtype = dtype
        self.param_dtype = param_dtype
        self.precision = precision
        linear_class = functools.partial(
            ParallelLinear,
            dtype=dtype,
            param_dtype=param_dtype,
            use_bias=False,
            kernel_init=jax.nn.initializers.normal(config.initializer_range),
            precision=precision,
            rngs=rngs,
            **get_dot_general_by_bits(config.bits, config.easy_method),
        )
        ffn_dim = config.intermediate_size
        hidden_dim = config.hidden_size

        self.w1 = linear_class(hidden_dim, ffn_dim, rngs=rngs)
        self.w2 = linear_class(ffn_dim, hidden_dim, rngs=rngs)
        self.w3 = linear_class(hidden_dim, ffn_dim, rngs=rngs)
        self.act_fn = ACT2FN[self.config.hidden_act]

    def __call__(self, hidden_states: Array) -> Array:
        """Forward pass of the expert MLP module.

        Args:
            hidden_states (Array): Input hidden states for this expert.
                Shape: (num_tokens_routed_to_expert, hidden_size).

        Returns:
            Array: Output hidden states after processing by the expert.
                Shape: (num_tokens_routed_to_expert, hidden_size).
        """
        return self.w2(self.act_fn(self.w1(hidden_states)) * self.w3(hidden_states))


class PhiMoEAttention(AttentionModule):
    """PhiMoE Attention module.

    This module implements the multi-head attention mechanism used in the PhiMoE model,
    which is similar to the one in Phi-3. It supports Grouped Query Attention (GQA)
    and Rotary Position Embeddings (RoPE), including scaling options.

    Attributes:
        config (PhiMoeConfig): Configuration object for the model.
        layer_idx (int): Index of the current layer.
        dtype (jnp.dtype): Data type for computations.
        param_dtype (jnp.dtype): Data type for parameters.
        precision (jax.lax.PrecisionLike): Precision setting for JAX operations.
        rngs (nn.Rngs): Random number generators.
        attention_dropout (float): Dropout probability for attention scores.
        hidden_size (int): Dimensionality of the hidden states.
        num_heads (int): Number of attention query heads.
        head_dim (int): Dimensionality of each attention head.
        num_key_value_heads (int): Number of attention key/value heads (for GQA).
        num_key_value_groups (int): Number of query head groups for each key/value head.
        max_position_embeddings (int): Maximum sequence length supported by RoPE.
        original_max_position_embeddings (int): Original max sequence length for RoPE scaling.
        rope_theta (float): Base value for RoPE frequency calculation.
        rope_scaling (dict): Configuration for RoPE scaling.
        is_causal (bool): Whether the attention is causal (always True for this implementation).
        q_proj (ParallelLinear): Linear layer for query projection.
        k_proj (ParallelLinear): Linear layer for key projection.
        v_proj (ParallelLinear): Linear layer for value projection.
        o_proj (ParallelLinear): Linear layer for the output projection.
        attention_performer (FlexibleAttentionModule): Module to perform the core attention computation.
        rotary (RoPE): Rotary position embedding module.
    """

    def __init__(
        self,
        config: PhiMoeConfig,
        layer_idx: int,
        dtype: jnp.dtype = jnp.bfloat16,
        param_dtype: jnp.dtype = jnp.bfloat16,
        precision: jax.lax.PrecisionLike = None,
        *,
        rngs: nn.Rngs,
    ):
        """Initializes the PhiMoEAttention module.

        Args:
            config (PhiMoeConfig): The configuration object for the PhiMoE model.
            layer_idx (int): Index of the current layer.
            dtype (jnp.dtype): Data type for computation. Defaults to jnp.float32.
            param_dtype (jnp.dtype): Data type for parameters. Defaults to jnp.float32.
            precision (jax.lax.PrecisionLike): Precision setting for JAX operations. Defaults to None.
            rngs (nn.Rngs): Random number generators.

        Raises:
            ValueError: If `hidden_size` is not divisible by `num_heads`.
        """
        super().__init__(config=config)
        self.layer_idx = layer_idx
        self.dtype = dtype
        self.param_dtype = param_dtype
        self.precision = precision
        self.rngs = rngs
        self.attention_dropout = config.attention_dropout
        self.hidden_size = config.hidden_size
        self.num_heads = config.num_attention_heads
        self.head_dim = self.hidden_size // self.num_heads
        self.num_key_value_heads = config.num_key_value_heads
        self.num_key_value_groups = self.num_heads // self.num_key_value_heads
        self.max_position_embeddings = config.max_position_embeddings
        self.original_max_position_embeddings = config.rope_scaling.get("original_max_position_embeddings", None)
        self.rope_theta = config.rope_theta
        self.rope_scaling = config.rope_scaling
        self.is_causal = True

        if (self.head_dim * self.num_heads) != self.hidden_size:
            raise ValueError(
                f"hidden_size must be divisible by num_heads (got `hidden_size`: {self.hidden_size}"
                f" and `num_heads`: {self.num_heads})."
            )

        linear_class = functools.partial(
            ParallelLinear,
            dtype=dtype,
            param_dtype=param_dtype,
            use_bias=config.attention_bias,
            kernel_init=jax.nn.initializers.normal(config.initializer_range),
            precision=precision,
            **get_dot_general_by_bits(config.bits, config.easy_method),
        )

        self.q_proj = linear_class(
            config.hidden_size,
            config.num_attention_heads * self.head_dim,
            rngs=rngs,
        )
        self.k_proj = linear_class(
            config.hidden_size,
            config.num_key_value_heads * self.head_dim,
            rngs=rngs,
        )
        self.v_proj = linear_class(
            config.hidden_size,
            config.num_key_value_heads * self.head_dim,
            rngs=rngs,
        )
        self.o_proj = linear_class(
            config.num_attention_heads * self.head_dim,
            config.hidden_size,
            rngs=rngs,
        )

        self.attention_performer = FlexibleAttentionModule(
            rngs=rngs,
            base_config=config,
            softmax_scale=self.head_dim**-0.5,
            dropout_prob=config.attention_dropout,
        )

        self.rotary = self.config.get_basic_rope(
            self.dtype,
            head_size=config.hidden_size // config.num_attention_heads,
            rotary_dim=config.hidden_size // config.num_attention_heads,
            is_neox_style=True,
        )

    def __call__(
        self,
        hidden_states: chex.Array,
        attention_mask: chex.Array,
        position_ids: chex.Array,
        causal_mask: chex.Array | bool | None,
        mode: common_types.RUNTIME_MODE_TYPES,  # type:ignore
        cache_view: TransformerCacheView | PagedAttentionCacheView | None = None,
        cache_metadata: TransformerMetadata | PagedAttentionMetadata | None = None,
        segment_ids: chex.Array | None = None,
        output_attentions: bool = False,
        fcm_mask: chex.Array | None = None,
        frequencies: chex.Array | None = None,
    ):
        """Forward pass of the PhiMoEAttention module.

        Args:
            hidden_states (chex.Array): Input hidden states.
            attention_mask (chex.Array): Mask to apply on the attention scores.
            position_ids (chex.Array): Position indices for the tokens. Shape: (batch_size, sequence_length).
            causal_mask (tp.Optional[chex.Array | bool]): Causal mask for ensuring autoregressive behavior.
            cache_view (tp.Optional[TransformerCacheView | PagedAttentionCacheView]): Cache view for attention KVs.
            cache_metadata (tp.Optional[TransformerMetadata | PagedAttentionMetadata]): Metadata for paged attention.
            segment_ids (tp.Optional[chex.Array]): Segment IDs for segment-based attention (optional).
            output_attentions (bool): Whether to return attention weights. Default is False.
            fcm_mask (tp.Optional[chex.Array]): Flash Chunking Mask (FCM) for attention.
            frequencies (tp.Optional[chex.Array]): Precomputed rotary frequency embeddings.

        Returns:
            tp.Union[tp.Tuple[chex.Array, chex.Array], tp.Tuple[chex.Array]]:
                A tuple containing the attention output hidden states. If `output_attentions` is True,
                it also includes the attention weights.
        """
        batch_size, sequence_length = hidden_states.shape[:2]
        (query_states, key_states, value_states) = (
            self.q_proj(hidden_states),
            self.k_proj(hidden_states),
            self.v_proj(hidden_states),
        )

        query_states = query_states.reshape(
            batch_size,
            sequence_length,
            self.config.num_attention_heads,
            self.head_dim,
        )
        key_states = key_states.reshape(
            batch_size,
            sequence_length,
            self.config.num_key_value_heads,
            self.head_dim,
        )
        value_states = value_states.reshape(
            batch_size,
            sequence_length,
            self.config.num_key_value_heads,
            self.head_dim,
        )

        (
            query_states,
            key_states,
            value_states,
        ) = self.apply_qkv_shardings(query_states, key_states, value_states)

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
            fcm_mask=fcm_mask,
        )

        attentions = self.attention_performer.forward(
            query_states=query_states,
            key_states=key_states,
            value_states=value_states,
            mode=mode,
            bias=None,
            cache_metadata=cache_metadata,
            cache_view=cache_view,
            init_bias=init_attention_bias,
            attention_mask=attention_mask,
            segment_ids=segment_ids,
            causal=True,
        )

        attn_output = self._merge_heads(attentions.attention_outputs)
        if self.config.shard_attention_computation:
            attn_output = with_sharding_constraint(
                arr=attn_output,
                sharding=PartitionSpec(
                    self.config.partition_axis.batch_axis,
                    (self.config.partition_axis.sequence_axis if attn_output.shape[1] != 1 else None),
                    self.config.partition_axis.hidden_state_axis,
                ),
            )
        attn_output = self.o_proj(attn_output)

        return AttentionLayerOutput(
            attention_output=attn_output,
            attention_weight=attentions.attention_weights if output_attentions else None,
            cache_view=cache_view,
        )


class PhiMoeSparseMoeBlock(nn.Module):
    """PhiMoE Sparse Mixture of Experts (MoE) Block.

    This module implements the core MoE logic, including the router (gate)
    and the expert layers. It routes each token to the top-k experts based
    on the router logits and combines the expert outputs.

    Attributes:
        config (PhiMoeConfig): Configuration object for the model.
        layer_idx (int): Index of the current layer.
        dtype (jnp.dtype): Data type for computations.
        param_dtype (jnp.dtype): Data type for parameters.
        precision (jax.lax.PrecisionLike): Precision setting for JAX operations.
        rngs (nn.Rngs): Random number generators.
        gate (ParallelLinear): Linear layer for the router gate.
        experts (tp.List[PhiMoEBlockSparseTop2MLP]): List of expert MLP modules.
    """

    def __init__(
        self,
        config: PhiMoeConfig,
        layer_idx: int,
        dtype: jnp.dtype = jnp.bfloat16,
        param_dtype: jnp.dtype = jnp.bfloat16,
        precision: jax.lax.PrecisionLike = None,
        *,
        rngs: nn.Rngs,
    ):
        """Initializes the PhiMoeSparseMoeBlock module.

        Args:
            config (PhiMoeConfig): The configuration object for the PhiMoE model.
            layer_idx (int): Index of the current layer.
            dtype (jnp.dtype): Data type for computation. Defaults to jnp.float32.
            param_dtype (jnp.dtype): Data type for parameters. Defaults to jnp.float32.
            precision (jax.lax.PrecisionLike): Precision setting for JAX operations. Defaults to None.
            rngs (nn.Rngs): Random number generators.
        """
        self.config = config
        self.layer_idx = layer_idx
        self.dtype = dtype
        self.param_dtype = param_dtype
        self.precision = precision
        self.hidden_dim = config.hidden_size
        self.ffn_dim = config.intermediate_size
        self.num_experts = config.num_local_experts
        self.top_k = config.num_experts_per_tok
        self.router_jitter_noise = config.router_jitter_noise
        self.input_jitter_noise = config.input_jitter_noise
        self.gate = ParallelLinear(
            self.config.hidden_size,
            self.config.num_local_experts,
            use_bias=False,
            rngs=rngs,
            dtype=dtype,
            param_dtype=param_dtype,
            precision=precision,
            kernel_init=nn.initializers.normal(),
        )

        self.experts = [
            PhiMoEBlockSparseTop2MLP(
                config=config,
                dtype=dtype,
                param_dtype=param_dtype,
                precision=precision,
                rngs=rngs,
            )
            for i in range(self.config.num_local_experts)
        ]

    def __call__(
        self,
        hidden_states: chex.Array,
        deterministic: bool = False,
    ) -> tuple[chex.Array, chex.Array]:
        """Forward pass of the Sparse MoE block.

        Args:
            hidden_states (chex.Array): Input hidden states. Shape: (batch_size * sequence_length, hidden_size).
            deterministic (bool): If True, disables dropout/jitter for deterministic behavior. Defaults to False.

        Returns:
            tp.Tuple[chex.Array, chex.Array]:
                - final_hidden_states: Output hidden states after MoE processing.
                  Shape: (batch_size * sequence_length, hidden_size).
                - router_logits: Logits computed by the router gate.
                  Shape: (batch_size * sequence_length, num_local_experts).
        """
        batch_size, sequence_length, hidden_dim = hidden_states.shape
        hidden_states = hidden_states.reshape(-1, hidden_dim)

        router_logits = self.gate(hidden_states).astype(  # no reshaping is needed
            jnp.promote_types(self.dtype, jnp.float32)
        )
        routing_weights, selected_experts = jax.lax.top_k(router_logits, k=self.config.num_experts_per_tok)
        routing_weights = jax.nn.softmax(routing_weights.astype(jnp.promote_types(self.dtype, jnp.float32)), axis=-1)
        if not deterministic and self.input_jitter_noise > 0:
            final_hidden_state = jax.nn.initializers.uniform(
                1.0 - self.input_jitter_noise,
                1.0 + self.input_jitter_noise,
            )(self.make_rng(), hidden_states.shape, hidden_states.dtype)
        else:
            final_hidden_state = jnp.zeros_like(hidden_states)
        for index in range(self.config.num_local_experts):
            expert_layer_output = (
                block_wise_ffn(
                    self.experts[index],
                    hidden_states,
                    self.config.scan_mlp_chunk_size,
                )
                if self.config.use_scan_mlp
                else self.experts[index](hidden_states)
            )
            expert_layer_output_exp = (
                jnp.sum(jnp.multiply(selected_experts == index, routing_weights), axis=-1)[:, :, None]
                * expert_layer_output
            )
            final_hidden_state += expert_layer_output_exp
        return final_hidden_state, router_logits


class PhiMoeDecoderLayer(nn.Module):
    """PhiMoE Transformer Decoder Layer.

    This module represents a single decoder layer in the PhiMoE model.
    It combines self-attention and a Sparse Mixture of Experts (MoE) block
    (or a standard MLP if not an MoE layer) with residual connections and
    RMS normalization.

    Attributes:
        config (PhiMoeConfig): Configuration object for the model.
        layer_idx (int): Index of the current layer.
        dtype (jnp.dtype): Data type for computations.
        param_dtype (jnp.dtype): Data type for parameters.
        precision (jax.lax.PrecisionLike): Precision setting for JAX operations.
        rngs (nn.Rngs): Random number generators.
        input_layernorm (RMSNorm): RMS normalization applied before the attention layer.
        self_attn (PhiMoEAttention): The self-attention module.
        mlp (PhiMoeSparseMoeBlock): The Sparse MoE block.
        post_attention_layernorm (RMSNorm): RMS normalization applied after the attention layer and before the MoE block.
        dropout (nn.Dropout): Dropout layer (potentially unused, dropout is often handled within submodules).
    """

    def __init__(
        self,
        config: PhiMoeConfig,
        layer_idx: int,
        dtype: jnp.dtype = jnp.bfloat16,
        param_dtype: jnp.dtype = jnp.bfloat16,
        precision: jax.lax.PrecisionLike = None,
        *,
        rngs: nn.Rngs,
    ):
        """Initializes the PhiMoeDecoderLayer.

        Args:
            config (PhiMoeConfig): The configuration object for the PhiMoE model.
            layer_idx (int): Index of the current layer.
            dtype (jnp.dtype): Data type for computation. Defaults to jnp.float32.
            param_dtype (jnp.dtype): Data type for parameters. Defaults to jnp.float32.
            precision (jax.lax.PrecisionLike): Precision setting for JAX operations. Defaults to None.
            rngs (nn.Rngs): Random number generators.
        """
        self.config = config
        self.dtype = dtype
        self.param_dtype = param_dtype
        self.precision = precision
        attn_block = PhiMoEAttention
        mlp_block = PhiMoeSparseMoeBlock
        attn_block, mlp_block = auto_remat(
            attn_block,
            mlp_block,
            policy=config.gradient_checkpointing,
        )
        self.self_attn = attn_block(
            config=config,
            layer_idx=layer_idx,
            dtype=dtype,
            param_dtype=param_dtype,
            precision=precision,
            rngs=rngs,
        )
        self.block_sparse_moe = mlp_block(
            config=config,
            layer_idx=layer_idx,
            dtype=dtype,
            param_dtype=param_dtype,
            precision=precision,
            rngs=rngs,
        )
        self.input_layernorm = nn.LayerNorm(
            config.hidden_size,
            epsilon=config.rms_norm_eps,
            dtype=dtype,
            param_dtype=param_dtype,
            use_bias=True,
            rngs=rngs,
        )

        self.post_attention_layernorm = nn.LayerNorm(
            config.hidden_size,
            epsilon=config.rms_norm_eps,
            dtype=dtype,
            param_dtype=param_dtype,
            use_bias=True,
            rngs=rngs,
        )

    def __call__(
        self,
        hidden_states: chex.Array,
        attention_mask: chex.Array,
        position_ids: chex.Array,
        causal_mask: chex.Array | bool | None,
        mode: common_types.RUNTIME_MODE_TYPES,  # type:ignore
        cache_view: TransformerCacheView | PagedAttentionCacheView | None = None,
        cache_metadata: TransformerMetadata | PagedAttentionMetadata | None = None,
        segment_ids: chex.Array | None = None,
        output_attentions: bool = False,
        output_router_logits: bool = False,
        fcm_mask: chex.Array | None = None,
        frequencies: chex.Array | None = None,
    ):
        """Forward pass of the PhiMoeDecoderLayer module.

        Args:
            hidden_states (chex.Array): Input hidden states.
            attention_mask (chex.Array): Mask to apply on the attention scores.
            position_ids (chex.Array): Position indices for the tokens. Shape: (batch_size, sequence_length).
            causal_mask (tp.Optional[chex.Array | bool]): Causal mask for ensuring autoregressive behavior.
            segment_ids (tp.Optional[chex.Array]): Segment IDs for segment-based attention (optional).
            cache_view (tp.Optional[TransformerCacheView | PagedAttentionCacheView]): Cache view for attention KVs.
            cache_metadata (tp.Optional[TransformerMetadata | PagedAttentionMetadata]): Metadata for paged attention.
            output_attentions (bool): Whether to return attention weights. Default is False.
            output_router_logits (bool): Whether to return router logits from the MoE layer. Default is False.
            fcm_mask (tp.Optional[chex.Array]): Flash Chunking Mask (FCM) for attention.
            frequencies (tp.Optional[chex.Array]): Precomputed rotary frequency embeddings.

        Returns:
            tp.Tuple[chex.Array, tp.Optional[chex.Array], tp.Optional[chex.Array]]:
                A tuple containing:
                - hidden_states: Output hidden states after the decoder layer.
                - self_attn_weights: Attention weights (if `output_attentions` is True).
                - router_logits: Router logits from the MoE layer (if `output_router_logits` is True).
        """
        residual = hidden_states

        hidden_states = self.input_layernorm(hidden_states)
        hidden_states = apply_logical_sharding(
            hidden_states,
            dynamic_axes=common_types.HiddenStateSharding,
            partition_manager=self.config.partition_manager,
        )

        attn_outputs = self.self_attn(
            hidden_states,
            attention_mask,
            position_ids,
            causal_mask,
            mode,
            cache_view,
            cache_metadata,
            segment_ids,
            output_attentions,
            fcm_mask,
            frequencies,
        )
        hidden_states, self_attn_weights = (
            attn_outputs.attention_output,
            attn_outputs.attention_weight,
        )

        hidden_states = residual + hidden_states

        # Fully Connected
        residual = hidden_states
        hidden_states = self.post_attention_layernorm(hidden_states)
        hidden_states, router_logits = self.block_sparse_moe(hidden_states)
        hidden_states = residual + hidden_states

        outputs = (hidden_states,)

        if output_attentions:
            outputs += (self_attn_weights,)

        if output_router_logits:
            outputs += (router_logits,)
        return outputs


@register_module(TaskType.BASE_MODULE, config=PhiMoeConfig, model_type="phimoe")
class PhiMoeModel(EasyDeLBaseModule):
    """The base PhiMoE model transformer.

    This class represents the core transformer architecture of the PhiMoE model,
    consisting of an embedding layer, multiple PhiMoeDecoderLayer layers
    (which include Sparse Mixture of Experts blocks), and a final RMS normalization layer.

    Attributes:
        config (PhiMoeConfig): Configuration object for the model.
        dtype (jnp.dtype): Data type for computation.
        param_dtype (jnp.dtype): Data type for parameters.
        precision (jax.lax.PrecisionLike): Precision setting for JAX operations.
        rngs (nn.Rngs): Random number generators.
        embed_tokens (nn.Embed): Embedding layer for input tokens.
        layers (tp.List[PhiMoeDecoderLayer]): List of decoder layers.
        norm (RMSNorm): Final layer normalization.
        embed_dropout (nn.Dropout): Dropout layer applied after embeddings.
        gradient_checkpointing (EasyDeLGradientCheckPointers): Gradient checkpointing configuration.
    """

    def __init__(
        self,
        config: PhiMoeConfig,
        dtype: jnp.dtype = jnp.bfloat16,
        param_dtype: jnp.dtype = jnp.bfloat16,
        precision: jax.lax.PrecisionLike = None,
        *,
        rngs: nn.Rngs,
    ):
        """Initializes the PhiMoeModel.

        Args:
            config (PhiMoeConfig): The configuration object for the PhiMoE model.
            dtype (jnp.dtype): Data type for computation. Defaults to jnp.float32.
            param_dtype (jnp.dtype): Data type for parameters. Defaults to jnp.float32.
            precision (jax.lax.PrecisionLike): Precision setting for JAX operations. Defaults to None.
            rngs (nn.Rngs): Random number generators.
        """
        super().__init__(
            config=config,
            dtype=dtype,
            param_dtype=param_dtype,
            precision=precision,
            rngs=rngs,
        )
        self.padding_idx = config.pad_token_id
        self.vocab_size = config.vocab_size

        self.embed_tokens = nn.Embed(
            config.vocab_size,
            config.hidden_size,
            dtype=dtype,
            param_dtype=param_dtype,
            rngs=rngs,
        )

        self.embed_dropout = nn.Dropout(config.embd_pdrop)
        self.layers = [
            PhiMoeDecoderLayer(
                config=config,
                layer_idx=idx,
                dtype=dtype,
                param_dtype=param_dtype,
                precision=precision,
                rngs=rngs,
            )
            for idx in range(self.config.num_hidden_layers)
        ]
        self.norm = nn.LayerNorm(
            config.hidden_size,
            epsilon=config.rms_norm_eps,
            dtype=dtype,
            param_dtype=param_dtype,
            use_bias=True,
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
        """Forward pass of the PhiMoeModel.

        Args:
            input_ids (tp.Optional[chex.Array]): Input token IDs. Shape: (batch_size, sequence_length).
            inputs_embeds (tp.Optional[chex.Array]): Input embeddings.
                Either `input_ids` or `inputs_embeds` must be provided.
            attention_mask (tp.Optional[chex.Array]): Mask to avoid performing attention on padding token indices.
                Shape: (batch_size, sequence_length).
            position_ids (tp.Optional[chex.Array]): Position indices for the tokens.
                Shape: (batch_size, sequence_length).
            segment_ids (tp.Optional[chex.Array]): Segment IDs (unused).
            output_attentions (tp.Optional[bool]): Whether to return attention weights.
                Defaults to `config.output_attentions`.
            output_hidden_states (tp.Optional[bool]): Whether to return hidden states for all layers.
                Defaults to `config.output_hidden_states`.
            past_key_values (tp.Optional[TransformerCache | PagedAttentionCache]):
                Precomputed key/value states for attention.
            cache_metadata (tp.Optional[TransformerMetadata | PagedAttentionMetadata]): Metadata for paged attention.

        Returns:
            BaseModelOutput: The model's output.
                returns a `BaseModelOutput` object containing `last_hidden_state`, `hidden_states` (optional),
                `attentions` (optional), and `router_logits` (optional).

        Raises:
            ValueError: If neither `input_ids` nor `inputs_embeds` is provided.
        """
        if (input_ids is None) ^ (inputs_embeds is not None):
            raise ValueError(
                "You cannot specify both input_ids and inputs_embeds at the same time, and must specify either one"
            )
        if inputs_embeds is None:
            inputs_embeds = self.embed_tokens(input_ids.astype("i4"))

        batch_size, sequence_length, _ = inputs_embeds.shape

        all_attentions = () if output_attentions else None
        all_hidden_states = () if output_hidden_states else None
        assert sequence_length <= self.config.max_position_embeddings, (
            f"Maximum Position Embedding Reached ! "
            f"(Excepted <= {self.config.max_position_embeddings} got {sequence_length})"
        )
        if attention_mask is None:
            attention_mask = jnp.ones((batch_size, sequence_length), "b1")
        else:
            if attention_mask.dtype != jnp.bool:
                attention_mask = jnp.astype(attention_mask == 1, "b1")
        if position_ids is None:
            position_ids = jnp.broadcast_to(
                jnp.clip(jnp.cumsum(attention_mask, axis=-1) - 1, a_min=0),
                (batch_size, sequence_length),
            ).astype(jnp.int32)
        if attention_mask.ndim == 2:
            attention_mask = jnp.expand_dims(attention_mask, (1, 2))
        if mode is None:
            mode = (
                common_types.MODE_DECODE
                if sequence_length == 1 and past_key_values is not None
                else common_types.MODE_TRAIN
            )
        if past_key_values is None:
            past_key_values = TransformerCache.init_empty(len(self.layers))

        hidden_states = apply_logical_sharding(
            inputs_embeds,
            dynamic_axes=common_types.HiddenStateSharding,
            partition_manager=self.config.partition_manager,
        )

        for idx, block in enumerate(self.layers):
            if output_hidden_states:
                all_hidden_states += (hidden_states,)

            layer_outputs = block(
                hidden_states=hidden_states,
                attention_mask=attention_mask,
                position_ids=position_ids,
                mode=mode,
                cache_view=past_key_values.views[idx],
                cache_metadata=cache_metadata,
                causal_mask=self.causal_mask,
                output_attentions=output_attentions,
                segment_ids=segment_ids,
                frequencies=self.frequencies,
            )
            hidden_states = layer_outputs.hidden_states

            if output_attentions:
                all_attentions += (layer_outputs.attention_weight,)

            past_key_values[idx] = layer_outputs.cache_view

        hidden_states = self.norm(hidden_states)

        if output_hidden_states:
            all_hidden_states += (hidden_states,)

        return BaseModelOutput(
            last_hidden_state=hidden_states,
            hidden_states=all_hidden_states,
            attentions=all_attentions,
            past_key_values=past_key_values,
        )


@register_module(TaskType.CAUSAL_LM, config=PhiMoeConfig, model_type="phimoe")
class PhiMoeForCausalLM(EasyDeLBaseModule):
    """PhiMoE model with a Causal Language Modeling head.

    This model consists of the base PhiMoE transformer (`PhiMoeModel`) followed by a
    linear layer (`lm_head`) that projects the transformer's output hidden states
    to the vocabulary size, producing logits for next token prediction.
    Optionally, the input token embeddings can be tied to the output projection layer.

    Attributes:
        config (PhiMoeConfig): Configuration object for the model.
        dtype (jnp.dtype): Data type for computation.
        param_dtype (jnp.dtype): Data type for parameters.
        precision (jax.lax.PrecisionLike): Precision setting for JAX operations.
        rngs (nn.Rngs): Random number generators.
        model (PhiMoeModel): The core PhiMoE transformer model.
        lm_head (ParallelLinear): The linear layer for projecting hidden states to vocabulary logits.
    """

    def __init__(
        self,
        config: PhiMoeConfig,
        dtype: jnp.dtype = jnp.bfloat16,
        param_dtype: jnp.dtype = jnp.bfloat16,
        precision: jax.lax.PrecisionLike = None,
        *,
        rngs: nn.Rngs,
    ):
        """Initializes the PhiMoeForCausalLM model.

        Args:
            config (PhiMoeConfig): The configuration object for the PhiMoE model.
            dtype (jnp.dtype): Data type for computation. Defaults to jnp.float32.
            param_dtype (jnp.dtype): Data type for parameters. Defaults to jnp.float32.
            precision (jax.lax.PrecisionLike): Precision setting for JAX operations. Defaults to None.
            rngs (nn.Rngs): Random number generators.
        """
        super().__init__(
            config=config,
            dtype=dtype,
            param_dtype=param_dtype,
            precision=precision,
            rngs=rngs,
        )
        self.model = PhiMoeModel(
            config=config,
            dtype=dtype,
            param_dtype=param_dtype,
            precision=precision,
            rngs=rngs,
        )
        self.vocab_size = self.config.vocab_size
        self.lm_head = ParallelLinear(
            config.hidden_size,
            config.vocab_size,
            use_bias=config.lm_head_bias,
            kernel_init=jax.nn.initializers.normal(config.initializer_range),
            dtype=dtype,
            param_dtype=param_dtype,
            precision=precision,
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
    ) -> CausalLMOutput:
        """Forward pass of the PhiMoeForCausalLM model.

        Args:
            input_ids (tp.Optional[chex.Array]): Input token IDs. Shape: (batch_size, sequence_length).
            inputs_embeds (tp.Optional[chex.Array]): Input embeddings.
                Either `input_ids` or `inputs_embeds` must be provided.
            attention_mask (tp.Optional[chex.Array]): Mask to avoid performing attention on padding token indices.
                Shape: (batch_size, sequence_length).
            position_ids (tp.Optional[chex.Array]): Position indices for the tokens.
                Shape: (batch_size, sequence_length).
            segment_ids (tp.Optional[chex.Array]): Segment IDs (unused).
            output_attentions (tp.Optional[bool]): Whether to return attention weights.
                Defaults to `config.output_attentions`.
            output_hidden_states (tp.Optional[bool]): Whether to return hidden states for all layers.
                Defaults to `config.output_hidden_states`.
            past_key_values (tp.Optional[TransformerCache | PagedAttentionCache]):
                Precomputed key/value states for attention.
            cache_metadata (tp.Optional[TransformerMetadata | PagedAttentionMetadata]): Metadata for paged attention.


        Returns:
            CausalLMOutput: The model's output.
                returns a `CausalLMOutput` object containing `logits`, `hidden_states` (optional),
                `attentions` (optional), and `router_logits` (optional).
        """
        outputs = self.model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            position_ids=position_ids,
            mode=mode,
            past_key_values=past_key_values,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            cache_metadata=cache_metadata,
            inputs_embeds=inputs_embeds,
            segment_ids=segment_ids,
        )
        hidden_states = outputs.last_hidden_state
        if self.config.tie_word_embeddings:
            lm_logits = jax.lax.dot_general(
                hidden_states,
                self.model.embed_tokens.embedding.value.T,
                (((hidden_states.ndim - 1), (0,)), ((), ())),
            )
        else:
            lm_logits = self.lm_head(hidden_states)

        return CausalLMOutput(
            logits=lm_logits,
            hidden_states=outputs.hidden_states,
            attentions=outputs.attentions,
            past_key_values=outputs.past_key_values,
        )
