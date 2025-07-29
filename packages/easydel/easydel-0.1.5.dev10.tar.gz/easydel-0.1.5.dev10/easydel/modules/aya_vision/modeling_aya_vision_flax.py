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


import typing as tp

import chex
import jax
import jax.numpy as jnp
from eformer import common_types
from eformer.pytree import auto_pytree
from flax import nnx as nn

from easydel.infra.base_module import EasyDeLBaseModule
from easydel.infra.factory import TaskType, register_module
from easydel.infra.modeling_outputs import ModelOutput
from easydel.infra.utils import ACT2FN
from easydel.layers.caching import (
    PagedAttentionCache,
    PagedAttentionMetadata,
    TransformerCache,
    TransformerMetadata,
)
from easydel.layers.linear import ParallelLinear
from easydel.modules.auto.auto_modeling import (
    AutoEasyDeLModelForCausalLM,
    AutoEasyDeLVisionModel,
)
from easydel.utils.helpers import get_logger

from .aya_vision_configuration import AyaVisionConfig

logger = get_logger(__name__)


@auto_pytree
class AyaVisionCausalLMOutputWithPast(ModelOutput):
    """
    Base class for AyaVision causal language model (or autoregressive) outputs.

    Args:
        loss (`chex.Array` of shape `(1,)`, *optional*, returned when `labels` is provided):
            Language modeling loss (for next-token prediction).
        logits (`chex.Array` of shape `(batch_size, sequence_length, config.vocab_size)`):
            Prediction scores of the language modeling head (scores for each vocabulary token before SoftMax).
        past_key_values (`tuple(tuple(chex.Array))`, *optional*, returned when `use_cache=True` is passed or
            when `config.use_cache=True`):
            Tuple of `tuple(chex.Array)` of length `config.n_layers`, with each tuple having 2 tensors of shape
            `(batch_size, num_heads, sequence_length, embed_size_per_head)`)

            Contains pre-computed hidden-states (key and values in the self-attention blocks) that can be used (see
            `past_key_values` input) to speed up sequential decoding.
        hidden_states (`tuple(chex.Array)`, *optional*, returned when `output_hidden_states=True` is passed or
            when `config.output_hidden_states=True`):
            Tuple of `chex.Array` (one for the output of the embeddings, if the model has an embedding layer, +
            one for the output of each layer) of shape `(batch_size, sequence_length, hidden_size)`.

            Hidden-states of the model at the output of each layer plus the optional initial embedding outputs.
        attentions (`tuple(chex.Array)`, *optional*, returned when `output_attentions=True` is passed or
            when `config.output_attentions=True`):
            Tuple of `chex.Array` (one for each layer) of shape `(batch_size, num_heads, sequence_length,
            sequence_length)`.

            Attentions weights after the attention softmax, used to compute the weighted average in the self-attention
            heads.
        image_hidden_states (`chex.Array`, *optional*):
            A `chex.Array` of size (batch_size * num_patches, num_images, sequence_length, hidden_size)`.
            image_hidden_states of the model produced by the vision encoder and after projecting the last hidden state.
    """

    loss: chex.Array | None = None
    logits: chex.Array = None
    past_key_values: TransformerCache | None = None
    hidden_states: tuple[chex.Array] | None = None
    attentions: tuple[chex.Array] | None = None
    image_hidden_states: chex.Array | None = None


class AyaVisionMultiModalProjector(nn.Module):
    """
    A multi-modal projector module for AyaVision that processes image features.
    It applies pixel shuffling, layer normalization, and linear transformations.

    Attributes:
        config (AyaVisionConfig): Configuration object.
        dtype (jnp.dtype): Data type for computation.
        param_dtype (jnp.dtype): Data type for parameters.
        precision (jax.lax.PrecisionLike): JAX precision level.
        rngs (nn.Rngs): Random number generators.
    """

    def __init__(
        self,
        config: AyaVisionConfig,
        dtype: jnp.dtype = jnp.bfloat16,
        param_dtype: jnp.dtype = jnp.bfloat16,
        precision: jax.lax.PrecisionLike = None,
        *,
        rngs: nn.Rngs,
    ):
        """Initializes the AyaVisionMultiModalProjector."""
        self.config = config
        self.dtype = dtype
        self.param_dtype = param_dtype
        self.precision = precision
        self.rngs = rngs

        self.downsample_factor = config.downsample_factor
        self.alignment_intermediate_size = getattr(
            config,
            "alignment_intermediate_size",
            config.text_config.hidden_size,
        )

        self.layernorm = nn.LayerNorm(
            config.vision_config.hidden_size * (config.downsample_factor**2),
            epsilon=config.adapter_layer_norm_eps,
            dtype=dtype,
            param_dtype=param_dtype,
            rngs=rngs,
        )

        self.linear_1 = ParallelLinear(
            config.vision_config.hidden_size * (config.downsample_factor**2),
            self.alignment_intermediate_size,
            use_bias=True,
            kernel_init=nn.initializers.normal(0.02),
            param_dtype=param_dtype,
            dtype=dtype,
            precision=precision,
            rngs=rngs,
        )

        self.act = ACT2FN["silu"]
        self.linear_2 = ParallelLinear(
            self.alignment_intermediate_size // 2,
            config.text_config.hidden_size,
            use_bias=True,
            kernel_init=nn.initializers.normal(0.02),
            param_dtype=param_dtype,
            dtype=dtype,
            precision=precision,
            rngs=rngs,
        )

    def __call__(self, image_features: jax.Array) -> jax.Array:
        """Forward pass through the projector.

        Args:
            image_features (jax.Array): Input image features.

        Returns:
            jax.Array: Processed hidden states.
        """
        image_features = self.pixel_shuffle(image_features)
        image_features = self.layernorm(image_features)
        hidden_states = self.linear_1(image_features)
        x, gate = jnp.split(hidden_states, 2, axis=-1)
        hidden_states = self.act(gate) * x

        hidden_states = self.linear_2(hidden_states)
        return hidden_states

    def pixel_shuffle(self, image_features: jax.Array) -> jax.Array:
        """Performs pixel shuffling on the image features based on the downsample factor.

        Args:
            image_features (jax.Array): Input image features (batch_size, seq_length, hidden_size).

        Returns:
            jax.Array: Image features after pixel shuffling.
        """
        batch_size, seq_length, _ = image_features.shape
        height = width = int(seq_length**0.5)
        image_features = image_features.reshape(
            image_features.shape[0],
            width,
            height,
            -1,
        )
        channels = image_features.shape[-1]
        image_features = image_features.reshape(
            batch_size,
            width,
            int(height / self.downsample_factor),
            int(channels * self.downsample_factor),
        )
        image_features = jnp.transpose(image_features, (0, 2, 1, 3))
        image_features = image_features.reshape(
            batch_size,
            int(height / self.downsample_factor),
            int(width / self.downsample_factor),
            -1,
        )
        image_features = jnp.transpose(image_features, (0, 2, 1, 3))
        return image_features


@register_module(TaskType.IMAGE_TEXT_TO_TEXT, config=AyaVisionConfig, model_type="aya_vision")
class AyaVisionForConditionalGeneration(EasyDeLBaseModule):
    """
    AyaVision model for conditional text generation based on image inputs.
    Combines a vision tower and a language model with a multi-modal projector.

    Attributes:
        config (AyaVisionConfig): Configuration object.
        dtype (jnp.dtype): Data type for computation.
        param_dtype (jnp.dtype): Data type for parameters.
        precision (jax.lax.PrecisionLike): JAX precision level.
        rngs (nn.Rngs): Random number generators.
    """

    loss_type = "ForCausalLM"

    def __init__(
        self,
        config: AyaVisionConfig,
        dtype: jnp.dtype = jnp.bfloat16,
        param_dtype: jnp.dtype = jnp.bfloat16,
        precision: jax.lax.PrecisionLike = None,
        *,
        rngs: nn.Rngs,
    ):
        """Initializes the AyaVisionForConditionalGeneration model."""
        super().__init__(
            config=config,
            dtype=dtype,
            param_dtype=param_dtype,
            precision=precision,
            rngs=rngs,
        )
        self.vision_tower = AutoEasyDeLVisionModel.from_config(
            config=config.vision_config,
            dtype=dtype,
            param_dtype=param_dtype,
            precision=precision,
            rngs=rngs,
        )
        self.multi_modal_projector = AyaVisionMultiModalProjector(
            config,
            dtype=dtype,
            param_dtype=param_dtype,
            precision=precision,
            rngs=rngs,
        )
        self.vocab_size = config.text_config.vocab_size
        self.language_model = AutoEasyDeLModelForCausalLM.from_config(
            config=config.text_config,
            dtype=dtype,
            param_dtype=param_dtype,
            precision=precision,
            rngs=rngs,
        )

        self.pad_token_id = self.config.pad_token_id if self.config.pad_token_id is not None else -1
        self.vision_feature_layer = config.vision_feature_layer
        self.vision_feature_select_strategy = getattr(
            config,
            "vision_feature_select_strategy",
            "default",
        )

    def get_image_features(self, pixel_values: chex.Array) -> chex.Array:
        """Extracts and projects image features from the vision tower.

        Args:
            pixel_values (chex.Array): Input pixel values for the images.

        Returns:
            chex.Array: Processed image features ready for the language model.
        """
        image_features = self.vision_tower(pixel_values, output_hidden_states=True)
        selected_image_feature = image_features.hidden_states[self.vision_feature_layer]
        if self.vision_feature_select_strategy == "default":
            selected_image_feature = selected_image_feature[:, 1:]
        elif self.vision_feature_select_strategy == "full":
            selected_image_feature = selected_image_feature
        image_features = self.multi_modal_projector(selected_image_feature)

        return image_features

    def __call__(
        self,
        input_ids: chex.Array = None,
        pixel_values: chex.Array = None,
        attention_mask: chex.Array | None = None,
        position_ids: chex.Array | None = None,
        segment_ids: chex.Array | None = None,
        mode: common_types.RUNTIME_MODE_TYPES | None = None,  # type:ignore
        past_key_values: TransformerCache | PagedAttentionCache | None = None,
        cache_metadata: TransformerMetadata | PagedAttentionMetadata | None = None,
        inputs_embeds: chex.Array | None = None,
        output_attentions: bool | None = None,
        output_hidden_states: bool | None = None,
        **lm_kwargs,
    ):
        """Forward pass for the AyaVision model.

        Args:
            input_ids (chex.Array): Input token IDs. (batch_size, sequence_length)
            pixel_values (chex.Array): Input pixel values for images. (batch_size, num_channels, height, width)
            attention_mask (Optional[chex.Array]): Mask for text attention.
            position_ids (Optional[chex.Array]): Position IDs for text.
            segment_ids (Optional[chex.Array]): Segment IDs (if applicable).
            past_key_values (Optional[TransformerCache | PagedAttentionCache]): Cached keys/values for language model.
            cache_metadata (Optional[TransformerMetadata | PagedAttentionMetadata]): Metadata for paged attention.
            inputs_embeds (Optional[chex.Array]): Input embeddings (alternative to input_ids).
            output_attentions (Optional[bool]): Whether to output attentions.
            output_hidden_states (Optional[bool]): Whether to output hidden states.
            **lm_kwargs: Additional arguments passed to the language model.

        Returns:
            AyaVisionCausalLMOutputWithPast: Model outputs including logits and potentially past key/values,
                hidden states, attentions, and image hidden states.
        """
        if (input_ids is None) ^ (inputs_embeds is not None):
            raise ValueError("You must specify exactly one of input_ids or inputs_embeds")

        output_attentions = output_attentions if output_attentions is not None else self.config.output_attentions
        output_hidden_states = (
            output_hidden_states if output_hidden_states is not None else self.config.output_hidden_states
        )
        if input_ids is not None and self.config.image_token_index >= self.vocab_size:
            special_image_mask = input_ids == self.config.image_token_index
            llm_input_ids = input_ids
            llm_input_ids = jnp.where(special_image_mask, 0, llm_input_ids)
        else:
            llm_input_ids = input_ids

        if inputs_embeds is None:
            inputs_embeds = self.language_model.model.embed_tokens(llm_input_ids)

        if pixel_values is not None:
            image_features = self.get_image_features(pixel_values)

            special_image_mask = jnp.expand_dims((input_ids == self.config.image_token_index), -1)
            special_image_mask = jnp.broadcast_to(special_image_mask, inputs_embeds.shape)
            image_features = image_features.astype(inputs_embeds.dtype)
            inputs_embeds = jnp.place(
                inputs_embeds,
                special_image_mask,
                image_features,
                inplace=False,
            )
        outputs = self.language_model(
            attention_mask=attention_mask,
            position_ids=position_ids,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            mode=mode,
            past_key_values=past_key_values,
            cache_metadata=cache_metadata,
            inputs_embeds=inputs_embeds,
            segment_ids=segment_ids,
            **lm_kwargs,
        )

        return AyaVisionCausalLMOutputWithPast(
            loss=None,
            logits=outputs.logits,
            past_key_values=outputs.past_key_values,
            hidden_states=outputs.hidden_states,
            attentions=outputs.attentions,
            image_hidden_states=image_features if pixel_values is not None else None,
        )

    def init_cache(
        self,
        batch_size,
        max_length,
        starts=None,
        shardings=None,
        pad_token_id=None,
    ):
        return self.language_model.init_cache(
            batch_size,
            max_length,
            starts,
            shardings,
            pad_token_id,
        )

    def _get_compile_model_kwargs(
        self,
        batch_size: int,
        input_tokens_length: int,
        input_sharding: jax.sharding.PartitionSpec,
        rngs: jax.random.PRNGKey,
        vision_included: bool = False,
        vision_batch_size: int = 1,
        vision_channels: int = 3,
        vision_height: int | None = None,
        vision_width: int | None = None,
        required_props: tp.Mapping[str, dict[str, tp.Any]] | None = None,
        **kwargs,
    ):
        """Helper function to get keyword arguments for model compilation, potentially including vision inputs.

        Args:
            batch_size (int): Batch size for text inputs.
            input_tokens_length (int): Sequence length for text inputs.
            input_sharding (jax.sharding.PartitionSpec): Sharding specification for text inputs.
            rngs (jax.random.PRNGKey): Random number generator key.
            vision_included (bool): Whether to include dummy vision inputs. Defaults to False.
            vision_batch_size (int): Batch size for vision inputs. Defaults to 1.
            vision_channels (int): Number of channels for vision inputs. Defaults to 3.
            vision_height (Optional[int]): Height for vision inputs (defaults to config).
            vision_width (Optional[int]): Width for vision inputs (defaults to config).
            required_props (Optional[Mapping[str, Dict[str, Any]]]): Required properties.
            **kwargs: Additional arguments passed to the language model's compile kwargs method.

        Returns:
            dict: Keyword arguments for model compilation.
        """
        basics = self.language_model._get_compile_model_kwargs(
            batch_size=batch_size,
            input_tokens_length=input_tokens_length,
            input_sharding=input_sharding,
            rngs=rngs,
            vision_included=vision_included,
            vision_batch_size=vision_batch_size,
            vision_channels=vision_channels,
            vision_height=vision_height,
            vision_width=vision_width,
            required_props=required_props,
            **kwargs,
        )

        if vision_included:
            pixel_values = jnp.ones(
                (
                    vision_batch_size or 1,
                    vision_channels or 3,
                    self.config.vision_config.image_size,
                    self.config.vision_config.image_size,
                ),
                dtype="f4",
            )
            basics.update({"pixel_values": pixel_values})
        return basics

    def prepare_inputs_for_generation(
        self,
        input_ids: chex.Array,
        max_length: int,
        pad_token_id: int,
        starts: int | None = None,
        pixel_values: chex.Array | None = None,
        attention_mask: chex.Array | None = None,
    ):
        """Prepares inputs for text generation, including pixel values if provided.

        Args:
            input_ids (chex.Array): Initial input token IDs.
            max_length (int): Maximum generation length.
            pixel_values (Optional[chex.Array]): Pixel values for image input.
            attention_mask (Optional[chex.Array]): Attention mask.

        Returns:
            dict: Model inputs ready for generation.
        """
        model_inputs = self.language_model.prepare_inputs_for_generation(
            input_ids=input_ids,
            max_length=max_length,
            pad_token_id=pad_token_id,
            starts=starts,
            attention_mask=attention_mask,
        )
        model_inputs["pixel_values"] = pixel_values
        return model_inputs

    def update_inputs_for_generation(self, model_outputs, model_kwargs):
        """Updates model inputs for the next step of generation, removing pixel values after the first step.

        Args:
            model_outputs: Outputs from the previous generation step.
            model_kwargs: Current keyword arguments for the model.

        Returns:
            dict: Updated model keyword arguments.
        """
        model_kwargs = self.language_model.update_inputs_for_generation(model_outputs, model_kwargs)
        model_kwargs.pop("pixel_values", None)  # only effect first iter
        return model_kwargs
