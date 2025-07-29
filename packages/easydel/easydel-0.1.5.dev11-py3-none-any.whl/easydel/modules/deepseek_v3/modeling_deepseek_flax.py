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
import typing as tp
from functools import partial

import chex
import jax
import jax.numpy as jnp
from eformer import common_types
from eformer.escale import apply_logical_sharding
from flax import nnx as nn

from easydel.infra.base_module import EasyDeLBaseModule
from easydel.infra.factory import TaskType, register_module
from easydel.infra.modeling_outputs import (
    AttentionLayerOutput,
    BaseModelOutput,
    CausalLMOutput,
    DecoderLayerOutput,
)
from easydel.infra.utils import (
    ACT2FN,
    ModuleCaches,
    auto_remat,
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
from easydel.layers.norms import RMSNorm

from .deepseek_configuration import DeepseekV3Config


def yarn_find_correction_dim(
    num_rotations,
    dim,
    base=10000,
    max_position_embeddings=2048,
):
    return (dim * math.log(max_position_embeddings / (num_rotations * 2 * math.pi))) / (2 * math.log(base))


def yarn_find_correction_range(
    low_rot,
    high_rot,
    dim,
    base=10000,
    max_position_embeddings=2048,
):
    low = math.floor(yarn_find_correction_dim(low_rot, dim, base, max_position_embeddings))
    high = math.ceil(yarn_find_correction_dim(high_rot, dim, base, max_position_embeddings))
    return max(low, 0), min(high, dim - 1)  # Clamp values just in case


def yarn_get_mscale(scale=1.0, mscale=1.0):
    if scale <= 1:
        return 1.0
    return 0.1 * mscale * math.log(scale) + 1.0


def yarn_linear_ramp_mask(min_, max_, dim):
    if min_ == max_:
        max_ += 0.001  # Prevent singularity

    linear_func = (jnp.arange(dim, dtype=jnp.float32) - min_) / (max_ - min_)
    return jnp.clip(linear_func, 0, 1)


def init_deepseek_rotary_embedding(
    dim,
    max_position_embeddings=2048,
    base=10000,
    method: tp.Literal["linear", "yarn", "dynamic", None] = None,
    kwargs: dict | None = None,
):
    if method is None:
        inv_freq = 1.0 / (base ** (jnp.arange(0, dim, 2).astype("float32") / dim))
        t = jnp.arange(max_position_embeddings, dtype=inv_freq.dtype)
        freqs = jnp.outer(t, inv_freq)
        emb = jnp.concatenate((freqs, freqs), axis=-1)
        return jnp.sin(emb), jnp.cos(emb)
    elif method == "linear":
        assert kwargs is not None
        inv_freq = 1.0 / (base ** (jnp.arange(0, dim, 2).astype("float32") / dim))
        t = jnp.arange(max_position_embeddings, dtype=inv_freq.dtype) / kwargs.get("scaling_factor")
        freqs = jnp.outer(t, inv_freq)
        emb = jnp.concatenate((freqs, freqs), axis=-1)
        return jnp.sin(emb), jnp.cos(emb)
    elif method == "dynamic":
        assert kwargs is not None
        targeted_len = kwargs.get("targeted_len", max_position_embeddings)
        if targeted_len > max_position_embeddings:
            base = base * (
                (kwargs.get("scaling_factor") * targeted_len / max_position_embeddings)
                - (kwargs.get("scaling_factor") - 1)
            ) ** (dim / (dim - 2))
            inv_freq = 1.0 / (base ** (jnp.arange(0, dim, 2).astype("float32") / dim))

        else:
            inv_freq = 1.0 / (base ** (jnp.arange(0, dim, 2).astype("float32") / dim))
        t = jnp.arange(max_position_embeddings, dtype=inv_freq.dtype) / kwargs.get("scaling_factor")

        freqs = jnp.outer(t, inv_freq)
        emb = jnp.concatenate((freqs, freqs), axis=-1)
        return jnp.sin(emb), jnp.cos(emb)
    elif method == "yarn":
        scaling_factor = kwargs.get("scaling_factor", 1.0)
        original_max_position_embeddings = kwargs.get("original_max_position_embeddings", 4096)
        beta_fast = kwargs.get("beta_fast", 32)
        beta_slow = kwargs.get("beta_slow", 1)
        mscale = kwargs.get("mscale", 1)
        mscale_all_dim = kwargs.get("mscale_all_dim", 0)
        freq_extra = 1.0 / (base ** (jnp.arange(0, dim, 2, dtype=jnp.float32) / dim))
        freq_inter = 1.0 / (scaling_factor * base ** (jnp.arange(0, dim, 2, dtype=jnp.float32) / dim))

        low, high = yarn_find_correction_range(
            beta_fast,
            beta_slow,
            dim,
            base,
            original_max_position_embeddings,
        )
        inv_freq_mask = 1.0 - yarn_linear_ramp_mask(low, high, dim // 2).astype("float32")
        inv_freq = freq_inter * (1 - inv_freq_mask) + freq_extra * inv_freq_mask
        t = jnp.arange(max_position_embeddings, dtype=jnp.float32)

        freqs = jnp.outer(t, inv_freq)

        _mscale = float(yarn_get_mscale(scaling_factor, mscale) / yarn_get_mscale(scaling_factor, mscale_all_dim))

        emb = jnp.concatenate((freqs, freqs), axis=-1)
        return (jnp.sin(emb) * _mscale).astype("float32"), (jnp.cos(emb) * _mscale).astype("float32")


def rotate_half(x):
    x1 = x[..., : x.shape[-1] // 2]
    x2 = x[..., x.shape[-1] // 2 :]
    return jnp.concatenate((-x2, x1), axis=-1)


def apply_rotary_pos_emb(q, k, cos, sin, position_ids, unsqueeze_dim=1):
    cos = jnp.expand_dims(cos[position_ids], unsqueeze_dim)
    sin = jnp.expand_dims(sin[position_ids], unsqueeze_dim)
    b, h, s, d = q.shape
    q = q.reshape(b, h, s, d // 2, 2).transpose(0, 1, 2, 4, 3).reshape(b, h, s, d)
    b, h, s, d = k.shape
    k = k.reshape(b, h, s, d // 2, 2).transpose(0, 1, 2, 4, 3).reshape(b, h, s, d)
    q_embed = (q * cos) + (rotate_half(q) * sin)
    k_embed = (k * cos) + (rotate_half(k) * sin)
    return q_embed, k_embed


class DeepseekV3MLP(nn.Module):
    def __init__(
        self,
        config: DeepseekV3Config,
        dtype: jnp.dtype = jnp.bfloat16,
        param_dtype: jnp.dtype = jnp.bfloat16,
        precision: jax.lax.PrecisionLike = None,
        hidden_size=None,
        intermediate_size=None,
        *,
        rngs: nn.Rngs,
    ):
        self.config = config
        self.dtype = dtype
        self.param_dtype = param_dtype
        self.precision = precision
        self.hidden_size = config.hidden_size if hidden_size is None else hidden_size
        self.intermediate_size = config.intermediate_size if intermediate_size is None else intermediate_size
        linear_class = partial(
            ParallelLinear,
            dtype=dtype,
            param_dtype=param_dtype,
            use_bias=False,
            kernel_init=jax.nn.initializers.normal(config.initializer_range),
            precision=precision,
            rngs=rngs,
            **get_dot_general_by_bits(config.bits, config.easy_method),
        )
        self.gate_proj = linear_class(self.hidden_size, self.intermediate_size)
        self.down_proj = linear_class(self.intermediate_size, self.hidden_size)
        self.up_proj = linear_class(self.hidden_size, self.intermediate_size)
        self.act_fn = ACT2FN[config.hidden_act]

    def __call__(self, hidden_states: jnp.ndarray) -> jnp.ndarray:
        if hidden_states.ndim == 3:  # if not in moe infer
            hidden_states = apply_logical_sharding(
                hidden_states,
                dynamic_axes=common_types.HiddenStateSharding,
                partition_manager=self.config.partition_manager,
            )
        gate = self.act_fn(self.gate_proj(hidden_states))
        up = self.up_proj(hidden_states)
        hidden_states = self.down_proj(gate * up)
        if hidden_states.ndim == 3:  # if not in moe infer
            hidden_states = apply_logical_sharding(
                hidden_states,
                dynamic_axes=common_types.HiddenStateSharding,
                partition_manager=self.config.partition_manager,
            )
        return hidden_states


class MoEGate(nn.Module):
    def __init__(
        self,
        config: DeepseekV3Config,
        dtype: jnp.dtype = jnp.bfloat16,
        param_dtype: jnp.dtype = jnp.bfloat16,
        precision: jax.lax.PrecisionLike = None,
        *,
        rngs: nn.Rngs,
    ):
        self.config = config
        self.dtype = dtype
        self.param_dtype = param_dtype
        self.precision = precision
        self.top_k = self.config.num_experts_per_tok
        self.n_routed_experts = self.config.n_routed_experts
        self.routed_scaling_factor = self.config.routed_scaling_factor
        self.scoring_func = self.config.scoring_func
        self.seq_aux = self.config.seq_aux
        self.topk_method = self.config.topk_method
        self.n_group = self.config.n_group
        self.topk_group = self.config.topk_group
        self.norm_topk_prob = self.config.norm_topk_prob
        self.gating_dim = self.config.hidden_size
        kernel = nn.initializers.kaiming_uniform()(
            rngs.param(),
            (self.gating_dim, self.n_routed_experts),
            param_dtype,
        )

        self.kernel = nn.Param(kernel)
        if self.topk_method == "noaux_tc":
            self.e_score_correction_bias = nn.Param(
                nn.initializers.zeros(
                    rngs.params(),
                    (self.n_routed_experts,),
                    param_dtype,
                )
            )

    def __call__(self, hidden_states):
        bsz, seq_len, h = hidden_states.shape
        hidden_states = hidden_states.reshape(-1, h)
        logits = jnp.dot(
            hidden_states.astype(jnp.float32),
            self.kernel.value.astype(jnp.float32),
            precision=self.precision,
        )

        if self.scoring_func == "sigmoid":
            scores = jax.nn.sigmoid(logits)
        else:
            raise NotImplementedError(f"insupportable scoring function for MoE gating: {self.scoring_func}")

        if self.topk_method == "noaux_tc":
            scores_for_choice = scores + self.e_score_correction_bias
            group_scores = scores_for_choice.reshape(bsz * seq_len, self.n_group, -1)
            top2_scores = jax.lax.top_k(group_scores, k=2)[0]
            group_scores = jnp.sum(top2_scores, axis=-1)

            group_idx = jax.lax.top_k(group_scores, k=self.topk_group)[1]

            group_mask = jnp.zeros_like(group_scores)
            indices = jnp.arange(group_mask.shape[0])[:, None]
            group_mask = group_mask.at[indices, group_idx].set(1.0)

            score_mask = jnp.repeat(group_mask[:, :, None], self.n_routed_experts // self.n_group, axis=2).reshape(
                bsz * seq_len, -1
            )

            masked_scores = jnp.where(score_mask > 0, scores_for_choice, 0.0)
            topk_weight, topk_idx = jax.lax.top_k(masked_scores, k=self.top_k)
        else:
            raise NotImplementedError(f"insupportable TopK function for MoE gating: {self.topk_method}")

        if self.top_k > 1 and self.norm_topk_prob:
            denominator = jnp.sum(topk_weight, axis=-1, keepdims=True) + 1e-20
            topk_weight = topk_weight / denominator

        topk_weight = topk_weight * self.routed_scaling_factor
        return topk_idx, topk_weight


class DeepseekV3MoE(nn.Module):
    def __init__(
        self,
        config: DeepseekV3Config,
        dtype: jnp.dtype = jnp.bfloat16,
        param_dtype: jnp.dtype = jnp.bfloat16,
        precision: jax.lax.PrecisionLike = None,
        *,
        rngs: nn.Rngs,
    ):
        self.config = config
        self.dtype = dtype
        self.param_dtype = param_dtype
        self.precision = precision
        self.num_experts_per_tok = self.config.num_experts_per_tok
        self.experts_per_rank = config.n_routed_experts
        self.deterministic = False
        self.experts = [
            DeepseekV3MLP(
                config=self.config,
                dtype=dtype,
                param_dtype=param_dtype,
                precision=precision,
                intermediate_size=config.moe_intermediate_size,
                rngs=rngs,
            )
            for i in range(config.n_routed_experts)
        ]

        self.gate = MoEGate(
            config=self.config,
            dtype=dtype,
            param_dtype=param_dtype,
            precision=precision,
            rngs=rngs,
        )
        if config.n_shared_experts is not None:
            self.shared_experts = DeepseekV3MLP(
                config=self.config,
                dtype=dtype,
                param_dtype=param_dtype,
                precision=precision,
                intermediate_size=self.config.moe_intermediate_size * self.config.n_shared_experts,
                rngs=rngs,
            )

    def __call__(self, hidden_states):
        identity = hidden_states
        orig_shape = hidden_states.shape
        topk_idx, topk_weight = self.gate(hidden_states)
        hidden_states = hidden_states.reshape(-1, hidden_states.shape[-1])
        if self.deterministic:
            y = self.moe_infer(hidden_states, topk_idx, topk_weight).reshape(*orig_shape)
        if self.config.n_shared_experts is not None:
            y = y + self.shared_experts(identity)
        return y

    def moe_infer(
        self,
        x: jnp.ndarray,
        topk_ids: jnp.ndarray,
        topk_weight: jnp.ndarray,
    ) -> jnp.ndarray:
        """
        Args:
                x: Input tensor of shape [batch_size, hidden_dim]
                topk_ids: Tensor of expert assignments [batch_size, top_k]
                topk_weight: Tensor of expert weights [batch_size, top_k]
        Returns:
                Output tensor of shape [batch_size, hidden_dim]
        """
        final_hidden_state = jnp.zeros_like(x)
        for expert_idx, expert in enumerate(self.experts):
            expert_mask = jnp.sum(
                jnp.multiply(topk_ids == expert_idx, topk_weight),
                axis=-1,
                keepdims=True,
            )
            final_hidden_state = final_hidden_state + (expert_mask * expert(x))
        return final_hidden_state


class DeepseekV3Attention(AttentionModule):
    def __init__(
        self,
        config: DeepseekV3Config,
        dtype: jnp.dtype = jnp.bfloat16,
        param_dtype: jnp.dtype = jnp.bfloat16,
        precision: str | jax.lax.Precision | None = None,
        *,
        rngs: nn.Rngs,
    ):
        super().__init__(config=config)
        self.config = config
        self.dtype = dtype
        self.param_dtype = param_dtype
        self.precision = precision
        self.rngs = rngs

        self.attention_dropout = config.attention_dropout
        self.hidden_size = config.hidden_size
        self.num_heads = config.num_attention_heads

        self.max_position_embeddings = config.max_position_embeddings
        self.rope_theta = config.rope_theta
        self.q_lora_rank = config.q_lora_rank
        self.qk_rope_head_dim = config.qk_rope_head_dim
        self.kv_lora_rank = config.kv_lora_rank
        self.v_head_dim = config.v_head_dim
        self.qk_nope_head_dim = config.qk_nope_head_dim
        self.q_head_dim = config.qk_nope_head_dim + config.qk_rope_head_dim

        self.is_causal = True

        linear = functools.partial(
            ParallelLinear,
            dtype=dtype,
            param_dtype=param_dtype,
            precision=precision,
            rngs=rngs,
        )
        if self.config.q_lora_rank is None:
            self.q_proj = ParallelLinear(
                self.hidden_size,
                self.num_heads * self.q_head_dim,
                use_bias=False,
            )
        else:
            self.q_a_proj = linear(
                self.hidden_size,
                config.q_lora_rank,
                use_bias=config.attention_bias,
            )
            self.q_a_layernorm = RMSNorm(
                config.q_lora_rank,
                eps=1e-6,
                dtype=dtype,
                param_dtype=param_dtype,
                rngs=rngs,
            )
            self.q_b_proj = linear(
                config.q_lora_rank,
                self.num_heads * self.q_head_dim,
                use_bias=False,
            )

        self.kv_a_proj_with_mqa = linear(
            self.hidden_size,
            config.kv_lora_rank + config.qk_rope_head_dim,
            use_bias=config.attention_bias,
        )
        self.kv_a_layernorm = RMSNorm(
            config.kv_lora_rank,
            dtype=dtype,
            eps=1e-6,
            param_dtype=param_dtype,
            rngs=rngs,
        )
        self.kv_b_proj = linear(
            config.kv_lora_rank,
            self.num_heads * (self.q_head_dim - self.qk_rope_head_dim + self.v_head_dim),
            use_bias=False,
        )

        self.o_proj = linear(
            self.num_heads * self.v_head_dim,
            self.hidden_size,
            use_bias=config.attention_bias,
        )

        softmax_scale = self.q_head_dim**-0.5
        if self.config.rope_scaling is not None:
            mscale_all_dim = self.config.rope_scaling.get("mscale_all_dim", 0)
            scaling_factor = self.config.rope_scaling["factor"]
            if mscale_all_dim:
                mscale = yarn_get_mscale(scaling_factor, mscale_all_dim)
                softmax_scale = softmax_scale * mscale * mscale
        self.attention_performer = FlexibleAttentionModule(
            rngs=rngs,
            base_config=config,
            softmax_scale=softmax_scale,
            dropout_prob=config.attention_dropout,
        )

    def __call__(
        self,
        hidden_states: chex.Array,
        frequencies: tuple[chex.Array, chex.Array],
        attention_mask: chex.Array,
        position_ids: chex.Array,
        causal_mask: chex.Array | bool | None,
        mode: common_types.RUNTIME_MODE_TYPES,  # type:ignore
        cache_view: TransformerCacheView | PagedAttentionCacheView | None = None,
        cache_metadata: TransformerMetadata | PagedAttentionMetadata | None = None,
        segment_ids: chex.Array | None = None,
        output_attentions: bool = False,
        fcm_mask: chex.Array | None = None,
    ):
        """
        Forward pass of the attention module.

        Args:
            hidden_states (chex.Array): Input hidden states.
            frequencies (tp.Tuple[chex.Array, chex.Array]): Cosine and sine components for rotary embeddings.
            attention_mask (chex.Array): Mask to apply on the attention scores.
            position_ids (chex.Array): Position indices for the tokens.
            causal_mask (chex.Array): Causal mask for ensuring autoregressive behavior.
            segment_ids (tp.Optional[chex.Array]): Segment IDs for segment-based attention (optional).
            deterministic (bool): If True, disables dropout for deterministic behavior.
            init_cache (bool): If True, initializes cache for caching keys and values.
            output_attentions (bool): If True, outputs attention weights alongside the hidden states.
            fcm_mask (tp.Optional[chex.Array]): fcm mask to be combined with attn mask and causal mask.
        Returns:
            tp.Tuple[chex.Array, chex.Array]: A tuple containing the attention output and the attention weights.
        """
        bsz, q_len, _ = hidden_states.shape

        if self.config.q_lora_rank is None:
            q = self.q_proj(hidden_states)
        else:
            q = self.q_b_proj(self.q_a_layernorm(self.q_a_proj(hidden_states)))
        q = q.reshape(bsz, q_len, self.num_heads, self.q_head_dim).transpose(0, 2, 1, 3)
        # Split into nope and pe parts
        q_nope, q_pe = q[..., : self.qk_nope_head_dim], q[..., self.qk_nope_head_dim :]
        # Key and Value projections with MQA (Multi-Query Attention) considerations
        compressed_kv = self.kv_a_proj_with_mqa(hidden_states)
        k_pe = compressed_kv[..., self.kv_lora_rank :]
        compressed_kv = compressed_kv[..., : self.kv_lora_rank]

        k_pe = k_pe.reshape(bsz, q_len, 1, self.qk_rope_head_dim).transpose(0, 2, 1, 3)
        kv = (
            self.kv_b_proj(
                self.kv_a_layernorm(compressed_kv),
            )
            .reshape(bsz, q_len, self.num_heads, self.qk_nope_head_dim + self.v_head_dim)
            .transpose(0, 2, 1, 3)
        )

        k_nope = kv[..., : self.qk_nope_head_dim]
        value_states = kv[..., self.qk_nope_head_dim : self.qk_nope_head_dim + self.v_head_dim]

        sin, cos = frequencies

        q_pe, k_pe = apply_rotary_pos_emb(
            q=q_pe,
            k=k_pe,
            cos=cos,
            sin=sin,
            position_ids=position_ids,
        )

        query_states = jnp.zeros((bsz, self.num_heads, q_len, self.q_head_dim), q_pe.dtype)
        query_states = query_states.at[..., : self.qk_nope_head_dim].set(q_nope)
        query_states = query_states.at[..., self.qk_nope_head_dim :].set(q_pe)

        key_states = jnp.zeros((bsz, self.num_heads, q_len, self.q_head_dim), k_pe.dtype)
        key_states = key_states.at[..., : self.qk_nope_head_dim].set(k_nope)
        key_states = key_states.at[..., self.qk_nope_head_dim :].set(k_pe)

        query_states = query_states.transpose(0, 2, 1, 3)
        key_states = key_states.transpose(0, 2, 1, 3)
        value_states = value_states.transpose(0, 2, 1, 3)

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

        attn_output = self.shard_attention_prod(self._merge_heads(attentions.attention_outputs))
        attn_output = self.o_proj(attn_output)

        return AttentionLayerOutput(
            attention_output=attn_output,
            attention_weight=attentions.attention_weights if output_attentions else None,
            cache_view=cache_view,
        )


class DeepseekV3DecoderLayer(nn.Module):
    def __init__(
        self,
        config: DeepseekV3Config,
        layer_idx: int,
        dtype: jnp.dtype = jnp.bfloat16,
        param_dtype: jnp.dtype = jnp.bfloat16,
        precision: str | jax.lax.Precision | None = None,
        *,
        rngs: nn.Rngs,
    ):
        super().__init__()
        self.config = config
        self.dtype = dtype
        self.param_dtype = param_dtype
        self.precision = precision
        self.rngs = rngs
        self.layer_idx = layer_idx
        self.hidden_size = config.hidden_size

        attn_block = DeepseekV3Attention
        mlp_block = DeepseekV3MLP
        mlp_moe_block = DeepseekV3MoE

        attn_block, mlp_block, mlp_moe_block = auto_remat(
            attn_block,
            mlp_block,
            mlp_moe_block,
            policy=config.gradient_checkpointing,
        )
        self.self_attn = attn_block(
            config=config,
            dtype=dtype,
            param_dtype=param_dtype,
            precision=precision,
            rngs=rngs,
        )

        self.mlp = (
            mlp_moe_block(
                config=config,
                dtype=dtype,
                param_dtype=param_dtype,
                precision=precision,
                rngs=rngs,
            )
            if (
                config.n_routed_experts is not None
                and layer_idx >= config.first_k_dense_replace
                and layer_idx % config.moe_layer_freq == 0
            )
            else mlp_block(
                config=config,
                dtype=dtype,
                param_dtype=param_dtype,
                precision=precision,
                rngs=rngs,
            )
        )
        self.input_layernorm = RMSNorm(
            config.hidden_size,
            eps=config.rms_norm_eps,
            dtype=dtype,
            param_dtype=param_dtype,
            rngs=rngs,
        )
        self.post_attention_layernorm = RMSNorm(
            config.hidden_size,
            eps=config.rms_norm_eps,
            dtype=dtype,
            param_dtype=param_dtype,
            rngs=rngs,
        )

    def __call__(
        self,
        hidden_states: chex.Array,
        frequencies: tuple[chex.Array, chex.Array],
        attention_mask: chex.Array,
        position_ids: chex.Array,
        causal_mask: chex.Array | bool | None,
        mode: common_types.RUNTIME_MODE_TYPES,  # type:ignore
        cache_view: TransformerCacheView | PagedAttentionCacheView | None = None,
        cache_metadata: TransformerMetadata | PagedAttentionMetadata | None = None,
        segment_ids: chex.Array | None = None,
        output_attentions: bool = False,
        fcm_mask: chex.Array | None = None,
    ):
        """
        Forward pass of the module block.

        Args:
            hidden_states (chex.Array): Input hidden states.
            frequencies (tp.Tuple[chex.Array, chex.Array]): Cosine and sine components for rotary embeddings.
            attention_mask (chex.Array): Mask to apply on the attention scores.
            position_ids (chex.Array): Position indices for the tokens.
            causal_mask (chex.Array): Causal mask for ensuring autoregressive behavior.
            segment_ids (tp.Optional[chex.Array]): Segment IDs for segment-based attention (optional).
            deterministic (bool): If True, disables dropout for deterministic behavior.
            init_cache (bool): If True, initializes cache for caching keys and values.
            output_attentions (bool): If True, outputs attention weights alongside the hidden states.
            fcm_mask (tp.Optional[chex.Array]): fcm mask to be combined with attn mask and causal mask.
        Returns:
            tp.Tuple[chex.Array, chex.Array]: A tuple containing the attention output and the attention weights.
        """
        residual = hidden_states

        hidden_states = self.input_layernorm(hidden_states)
        hidden_states = apply_logical_sharding(
            hidden_states,
            dynamic_axes=common_types.HiddenStateSharding,
            partition_manager=self.config.partition_manager,
        )

        # Self Attention
        attn_out = self.self_attn(
            hidden_states,
            frequencies,
            attention_mask,
            position_ids,
            causal_mask,
            mode,
            cache_view,
            cache_metadata,
            segment_ids,
            output_attentions,
            fcm_mask,
        )
        hidden_states = attn_out.attention_output
        hidden_states = residual + hidden_states

        # Fully Connected
        residual = hidden_states
        hidden_states = self.post_attention_layernorm(hidden_states)

        feed_forward_hidden_states = self.mlp(hidden_states)
        hidden_states = residual + feed_forward_hidden_states
        hidden_states = apply_logical_sharding(
            hidden_states,
            dynamic_axes=common_types.HiddenStateSharding,
            partition_manager=self.config.partition_manager,
        )
        return DecoderLayerOutput(
            hidden_states=hidden_states,
            attention_weight=attn_out.attention_weight,
            cache_view=attn_out.cache_view,
        )


@register_module(TaskType.BASE_MODULE, DeepseekV3Config, model_type="deepseek_v3")
class DeepseekV3Model(EasyDeLBaseModule):
    def __init__(
        self,
        config: DeepseekV3Config,
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
        self.embed_tokens = nn.Embed(
            self.config.vocab_size,
            self.config.hidden_size,
            embedding_init=jax.nn.initializers.normal(stddev=self.config.initializer_range),
            dtype=dtype,
            param_dtype=param_dtype,
            rngs=rngs,
        )

        self.layers = [
            DeepseekV3DecoderLayer(
                config=config,
                dtype=dtype,
                param_dtype=param_dtype,
                precision=precision,
                layer_idx=i,
                rngs=rngs,
            )
            for i in range(self.config.num_hidden_layers)
        ]
        self.norm = RMSNorm(
            self.config.hidden_size,
            eps=self.config.rms_norm_eps,
            dtype=dtype,
            param_dtype=param_dtype,
            rngs=rngs,
        )

    @functools.cached_property
    def frequencies(self):
        initial_rope_kwargs = {}
        method = None
        if self.config.rope_scaling is not None:
            scaling_type = self.config.rope_scaling["type"]
            method = scaling_type
            if scaling_type != "yarn":
                initial_rope_kwargs = dict(scaling_factor=self.config.rope_scaling["factor"])
            else:
                initial_rope_kwargs = {
                    key: self.config.rope_scaling[key]
                    for key in [
                        "original_max_position_embeddings",
                        "beta_fast",
                        "beta_slow",
                        "mscale",
                        "mscale_all_dim",
                    ]
                    if key in self.config.rope_scaling
                }
                initial_rope_kwargs["scaling_factor"] = self.config.rope_scaling["factor"]
        return ModuleCaches(
            init_deepseek_rotary_embedding(
                dim=self.config.qk_rope_head_dim,
                max_position_embeddings=self.config.granted_freq_max_position_embedding,
                base=self.config.rope_theta,
                method=method,  # type:ignore
                kwargs=initial_rope_kwargs,
            )
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
        Forward pass through the Deepseekv3 module.

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

        hidden_states = inputs_embeds

        if mode is None:
            mode = (
                common_types.MODE_DECODE
                if sequence_length == 1 and past_key_values is not None
                else common_types.MODE_TRAIN
            )
        if past_key_values is None:
            past_key_values = TransformerCache.init_empty(len(self.layers))

        hidden_states = apply_logical_sharding(
            hidden_states,
            dynamic_axes=common_types.HiddenStateSharding,
            partition_manager=self.config.partition_manager,
        )

        for idx, layer in enumerate(self.layers):
            if output_hidden_states:
                all_hidden_states += (hidden_states,)
            output = layer(
                hidden_states=hidden_states,
                frequencies=self.frequencies,
                attention_mask=attention_mask,
                position_ids=position_ids,
                causal_mask=self.causal_mask,
                output_attentions=output_attentions,
                segment_ids=segment_ids,
                mode=mode,
                cache_view=past_key_values.views[idx],
                cache_metadata=cache_metadata,
            )
            hidden_states = output.hidden_states

            if output_attentions:
                all_attentions += (output.attention_weight,)

            past_key_values[idx] = output.cache_view

        hidden_states = self.norm(hidden_states)

        if output_hidden_states:
            all_hidden_states += (hidden_states,)

        return BaseModelOutput(
            last_hidden_state=hidden_states,
            hidden_states=all_hidden_states,
            attentions=all_attentions,
            past_key_values=past_key_values,
        )


@register_module(TaskType.CAUSAL_LM, DeepseekV3Config, model_type="deepseek_v3")
class DeepseekV3ForCausalLM(EasyDeLBaseModule):
    """
    DeepseekV3 model with a language modeling head for causal language modeling tasks.

    This model extends the base DeepseekV3Model by adding a linear language modeling head
    on top of the transformer model. It incorporates Mixture of Experts (MoE) architecture
    and is designed for generative tasks and text generation.
    """

    def __init__(
        self,
        config: DeepseekV3Config,
        dtype: jnp.dtype = jnp.bfloat16,
        param_dtype: jnp.dtype = jnp.bfloat16,
        precision: jax.lax.PrecisionLike = None,
        *,
        rngs: nn.Rngs,
    ):
        """Initialize the DeepseekV3ForCausalLM model.

        Args:
            config (DeepseekV3Config): The model configuration.
            dtype (jnp.dtype, optional): The data type for computation. Defaults to jnp.float32.
            param_dtype (jnp.dtype, optional): The data type for parameters. Defaults to jnp.float32.
            precision (jax.lax.PrecisionLike, optional): The precision to use for matrix multiplication.
                Defaults to None.
            rngs (nn.Rngs): The random number generators.
        """
        super().__init__(
            config=config,
            dtype=dtype,
            param_dtype=param_dtype,
            precision=precision,
            rngs=rngs,
        )
        self.model = DeepseekV3Model(
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
            use_bias=False,
            kernel_init=nn.initializers.normal(config.initializer_range),
            rngs=rngs,
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
        Forward pass of the causal language model.

        Args:
            input_ids (Optional[chex.Array], optional): Token IDs to process. Defaults to None.
            inputs_embeds (Optional[chex.Array], optional): Pre-computed input embeddings. Defaults to None.
            attention_mask (Optional[chex.Array], optional): Mask to avoid attention on padding tokens. Defaults to None.
            position_ids (Optional[chex.Array], optional): Position IDs. Defaults to None.
            segment_ids (Optional[chex.Array], optional): Segment IDs for segment-based attention. Defaults to None.
            output_attentions (Optional[bool], optional): Whether to output attention weights. Defaults to None.
            output_hidden_states (Optional[bool], optional): Whether to output hidden states. Defaults to None.
            past_key_values (Optional[TransformerCache | PagedAttentionCache], optional): Cached key/values.
                Defaults to None.
            cache_metadata (Optional[TransformerMetadata | PagedAttentionMetadata], optional): Cache metadata.
                Defaults to None.


        Returns:
                CausalLMOutput: The model outputs, either as a named tuple or a standard tuple.
        """
        outputs = self.model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            position_ids=position_ids,
            inputs_embeds=inputs_embeds,
            mode=mode,
            past_key_values=past_key_values,
            cache_metadata=cache_metadata,
            segment_ids=segment_ids,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
        )

        hidden_states = outputs.last_hidden_state

        hidden_states = apply_logical_sharding(
            hidden_states,
            dynamic_axes=common_types.HiddenStateSharding,
            partition_manager=self.config.partition_manager,
        )

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
