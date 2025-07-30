# Copyright 2023 The EASYDEL Author @erfanzar (Erfan Zare Chavoshi).
# Copyright 2024 The Improved Version Contributors.
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

import jax.numpy as jnp
from eformer import escale as es
from eformer.pytree import auto_pytree
from flax import nnx as nn
from flax.nnx.nn.dtypes import promote_dtype
from jax import lax
from jax.experimental.shard_map import shard_map
from jax.sharding import Mesh
from jax.sharding import PartitionSpec as Ps
from jaxtyping import Array, Shaped

from easydel.kernels.collective_matmul import (
    MatrixMultiplyMethod,
    create_distributed_matmul,
    prepare_matrix_for_all_gather,
    prepare_matrix_for_reduce_scatter,
)
from easydel.kernels.tpu_ops.grouped_matmul_pallas import pallas_grouped_matmul_sharded

Dtype = jnp.dtype
Initializer = nn.initializers.Initializer
PrecisionLike = lax.PrecisionLike
Shape = tp.Sequence[int]
AxisNames = str | tp.Sequence[str] | tuple[str, ...]

# Default initializers
default_kernel_init = nn.initializers.lecun_normal()
default_bias_init = nn.initializers.zeros


def get_sharding(arr: Shaped[Array, "..."]) -> Ps | None:
    """Gets the sharding of an array.

    Args:
            arr: Array to get sharding from.

    Returns:
            Sharding of the array.
    """
    sharding = getattr(arr, "sharding", None)
    if sharding is not None:
        return sharding.spec
    return None


def get_output_partition_spec(
    lhs: Shaped[Array, "..."],
    rhs: Shaped[Array, "..."],
    method: MatrixMultiplyMethod,
    axis_name: str,
) -> Ps | None:
    """Calculate output partition spec based on input arrays and matmul method.

    Args:
        lhs: Left-hand side array (inputs)
        rhs: Right-hand side array (weights)
        method: Matrix multiplication method
        axis_name: Axis name for sharding

    Returns:
        Output partition specification
    """
    from jax.sharding import PartitionSpec as P

    lhs_spec = get_sharding(lhs)
    rhs_spec = get_sharding(rhs)

    if lhs_spec is None or rhs_spec is None:
        return None

    if lhs.ndim == 2:
        return P(rhs_spec[1], rhs_spec[0])
    else:
        return P(*(None,) * (lhs.ndim - 1) + (axis_name,))


def get_matmul_output_sharding(lhs_pspec, rhs_pspec):
    """
    Determine the output sharding PartitionSpec for a matrix multiplication
    based on the partition specs of the input matrices.

    For matrix multiplication X @ W:
    - The contracting dimensions get reduced during matmul
    - The non-contracting dimensions of X and W determine the output sharding
    - Ensures no duplicate sharding dimensions in the output
    - Ensures correct output dimensionality with None padding if needed

    Args:
        lhs_pspec: PartitionSpec for the left-hand side matrix X
        rhs_pspec: PartitionSpec for the right-hand side matrix W

    Returns:
        PartitionSpec for the output of X @ W
    """
    if lhs_pspec is None or rhs_pspec is None:
        return Ps()
    lhs_output_dims = lhs_pspec[:-1] if len(lhs_pspec) > 1 else ()
    if len(rhs_pspec) >= 2:
        rhs_output_dims = (rhs_pspec[-1],)
    else:
        rhs_output_dims = (rhs_pspec[-1],) if rhs_pspec else ()

    all_shard_dims = set()
    output_dims = []
    for dim in lhs_output_dims:
        if isinstance(dim, tuple):
            filtered_tuple = tuple(d for d in dim if d not in all_shard_dims)
            for d in dim:
                all_shard_dims.add(d)
            if filtered_tuple:
                output_dims.append(filtered_tuple)
            elif dim:
                output_dims.append(None)
        else:
            if dim not in all_shard_dims:
                output_dims.append(dim)
                all_shard_dims.add(dim)
            else:
                output_dims.append(None)
    for dim in rhs_output_dims:
        if isinstance(dim, tuple):
            filtered_tuple = tuple(d for d in dim if d not in all_shard_dims)
            for d in dim:
                all_shard_dims.add(d)
            if filtered_tuple:
                output_dims.append(filtered_tuple)
            elif dim:
                output_dims.append(None)
        else:
            if dim not in all_shard_dims:
                output_dims.append(dim)
                all_shard_dims.add(dim)
            else:
                output_dims.append(None)
    while len(output_dims) < (len(lhs_pspec) - 1 + 1):
        output_dims.append(None)
    return Ps(*output_dims)


@auto_pytree
class TensorParallelConfig:
    """Configuration for Tensor Parallelism.

    Attributes:
        mesh: The JAX device mesh.
        axis_name: The name of the mesh axis to use for tensor parallelism.
        matmul_type: The type of matmul (MatrixMultiplyMethod).
        reduce_scatter_output: If True and parallel_type is COLUMN,
            use reduce-scatter instead of all-gather for the output.
            This keeps the output sharded (useful for sequence parallelism
            or subsequent RowParallel layers). Defaults to False.
    """

    mesh: Mesh = None
    axis_name: str = "tp"
    matmul_method: MatrixMultiplyMethod | None = None
    reduce_output: bool = False
    reduce_scatter_output: bool = False

    def __post_init__(self):
        msg = None
        if self.matmul_method is not None:
            if self.mesh is None:
                self.mesh = es.get_incontext_mesh()
            if self.axis_name not in self.mesh.axis_names:
                msg = f"axis_name '{self.axis_name}' not found in mesh axis names: {self.mesh.axis_names}"
        if msg is not None:
            raise ValueError(msg)


class ParallelLinear(nn.Module):
    """A Linear layer with optional parallelism.

    Behaves like `nnx.Linear` but can distribute computation and parameters
    across devices based on the `TensorParallelConfig`.

    Attributes:
        in_features: Number of input features.
        out_features: Number of output features.
        use_bias: Whether to include a bias term. Default is True.
        dtype: The dtype of the computation (defaults to inferred from input).
        param_dtype: The dtype of the parameters. Default is float32.
        precision: JAX precision for the dot product. Default is None.
        kernel_init: Initializer for the kernel weights.
        bias_init: Initializer for the bias.
        parallel_config: Configuration for tensor parallelism. If None,
          the layer behaves like a standard non-parallel Linear layer.
    """

    _direction: tp.Literal["row", "column"] | None = None

    def __init__(
        self,
        in_features: int,
        out_features: int,
        *,
        use_bias: bool = True,
        dtype: Dtype | None = None,
        param_dtype: Dtype = jnp.float32,
        precision: PrecisionLike = None,
        kernel_init: Initializer = default_kernel_init,
        bias_init: Initializer = default_bias_init,
        parallel_config: TensorParallelConfig | None = None,
        rngs: nn.Rngs | None = None,
    ):
        if rngs is None:
            rngs = nn.Rngs(0)
        self.in_features = in_features
        self.out_features = out_features
        self.use_bias = use_bias
        self.dtype = dtype
        self.param_dtype = param_dtype
        self.precision = precision
        self.kernel_init = kernel_init
        self.bias_init = bias_init
        self.parallel_config = parallel_config
        self.rngs = rngs

        self.tp_merged = len(out_features) if isinstance(out_features, tp.Sequence) else 1
        out_features_sum = sum(out_features) if self.tp_merged > 1 else out_features
        kernel_key = rngs.params()
        kernel_shape = (in_features, out_features_sum)
        self.kernel = nn.Param(kernel_init(kernel_key, kernel_shape, param_dtype))

        if use_bias:
            bias_key = rngs.params()
            bias_shape = (out_features,)
            self.bias = nn.Param(bias_init(bias_key, bias_shape, param_dtype))
        else:
            self.bias = None
        self.distributed_matmul = None
        if parallel_config is not None and parallel_config.matmul_method is not None:
            self.distributed_matmul = create_distributed_matmul(
                parallel_config.matmul_method,
                parallel_config.axis_name,
            )

    def collective_forward(self, inputs: Shaped[Array, "... in_features"]) -> Shaped[Array, "... out_features"]:
        kernel = self.kernel.value
        bias = self.bias.value if self.use_bias else None

        if bias is not None:
            inputs, kernel, bias = promote_dtype((inputs, kernel, bias), dtype=self.dtype)
        else:
            inputs, kernel = promote_dtype((inputs, kernel), dtype=self.dtype)

        # Ensure inputs are 2D
        orig_shape = inputs.shape
        inputs_2d = inputs.reshape(-1, inputs.shape[-1])

        # Get partition specs
        input_spec = get_sharding(inputs_2d)
        kernel_spec = get_sharding(kernel)
        output_spec = get_output_partition_spec(
            inputs_2d,
            kernel,
            self.parallel_config.matmul_method,
            self.parallel_config.axis_name,
        )

        if self.parallel_config.matmul_method == MatrixMultiplyMethod.REDUCE_SCATTER:
            kernel = prepare_matrix_for_reduce_scatter(
                kernel,
                self.parallel_config.mesh,
                self.parallel_config.axis_name,
            )
        elif self.parallel_config.matmul_method == MatrixMultiplyMethod.ALL_GATHER:
            kernel = prepare_matrix_for_all_gather(
                kernel,
                self.parallel_config.mesh,
                self.parallel_config.axis_name,
            )

        output_2d = shard_map(
            self.distributed_matmul,
            mesh=self.parallel_config.mesh,
            in_specs=(input_spec, kernel_spec),
            out_specs=output_spec,
            check_rep=False,
        )(inputs_2d, kernel)

        output = output_2d.reshape(orig_shape[:-1] + (self.out_features,))

        if bias is not None:
            output = output + jnp.reshape(bias, (1,) * (output.ndim - 1) + (-1,))

        return output

    def native_forward(self, inputs: Shaped[Array, "... in_features"]) -> Shaped[Array, "... out_features"]:
        """Applies the linear transformation with optional tensor parallelism.

        Args:
            inputs: The input array. Shape: (..., in_features).
                    For ROW parallelism, the input is expected to be sharded
                    along the feature dimension (`axis_name`).

        Returns:
            The transformed output array.
            Shape: (..., out_features).
            Output is sharded for COLUMN parallelism if `reduce_scatter_output` is True.
            Otherwise, output is fully replicated.
        """
        kernel = self.kernel.value
        bias = self.bias.value if self.use_bias else None

        if bias is not None:
            inputs, kernel, bias = promote_dtype((inputs, kernel, bias), dtype=self.dtype)
        else:
            inputs, kernel = promote_dtype((inputs, kernel), dtype=self.dtype)

        subscript = "...ik,...kj->...ij" if inputs.ndim > 1 else "...k,...kj->...j"

        y = jnp.einsum(
            subscript,
            inputs,
            kernel,
            precision=self.precision,
            optimize=True,
        )

        if bias is not None:
            y = y + jnp.reshape(bias, (1,) * (y.ndim - 1) + (-1,))

        return y

    def __call__(self, inputs: Shaped[Array, "... in_features"]) -> Shaped[Array, "... out_features"]:
        if self.distributed_matmul is None:
            return self.native_forward(inputs=inputs)
        return self.collective_forward(inputs=inputs)


class RowParallelLinear(ParallelLinear):
    _direction = "row"


class ColumnParallelLinear(ParallelLinear):
    _direction = "column"


class MoELinear(nn.Module):
    def __init__(
        self,
        num_experts: int,
        in_features: int,
        out_features: int,
        *,
        use_bias: bool = True,
        dtype: Dtype | None = None,
        param_dtype: Dtype = jnp.float32,
        precision: PrecisionLike = None,
        kernel_init: Initializer = default_kernel_init,
        bias_init: Initializer = default_bias_init,
        tile_size: tuple[int, int, int] = (512, 1024, 1024),
        do_hostsync: bool = False,
        expert_axes: str = "ep",
        sync_axes: str = "tp",
        rngs: nn.Rngs | None = None,
    ):
        if rngs is None:
            rngs = nn.Rngs(0)
        self.num_experts = num_experts
        self.in_features = in_features
        self.out_features = out_features
        self.use_bias = use_bias
        self.dtype = dtype
        self.param_dtype = param_dtype
        self.precision = precision
        self.kernel_init = kernel_init
        self.bias_init = bias_init
        self.rngs = rngs
        self.tile_size = tile_size
        self.do_hostsync = do_hostsync
        self.expert_axes = expert_axes
        self.sync_axes = sync_axes
        self.tp_merged = len(out_features) if isinstance(out_features, tp.Sequence) else 1
        out_features_sum = sum(out_features) if self.tp_merged > 1 else out_features
        kernel_key = rngs.params()
        kernel_shape = (num_experts, in_features, out_features_sum)
        self.kernel = nn.Param(kernel_init(kernel_key, kernel_shape, param_dtype))

        if use_bias:
            bias_key = rngs.params()
            bias_shape = (out_features,)
            self.bias = nn.Param(bias_init(bias_key, bias_shape, param_dtype))
        else:
            self.bias = None

    def native_forward(
        self,
        inputs: Shaped[Array, "num_tokens in_features"],
        group_sizes: Array,
    ) -> Shaped[Array, "num_tokens out_features"]:
        """Applies the linear transformation with optional tensor parallelism.

        Args:
            inputs: The input array. Shape: (..., in_features).
                    For ROW parallelism, the input is expected to be sharded
                    along the feature dimension (`axis_name`).

        Returns:
            The transformed output array.
            Shape: (..., out_features).
            Output is sharded for COLUMN parallelism if `reduce_scatter_output` is True.
            Otherwise, output is fully replicated.
        """
        kernel = self.kernel.value
        bias = self.bias.value if self.use_bias else None

        if bias is not None:
            inputs, kernel, bias = promote_dtype((inputs, kernel, bias), dtype=self.dtype)
        else:
            inputs, kernel = promote_dtype((inputs, kernel), dtype=self.dtype)

        y = pallas_grouped_matmul_sharded(
            lhs=inputs,
            rhs=kernel,
            group_sizes=group_sizes,
            tile_size=self.tile_size,
            do_hostsync=self.do_hostsync,
            sync_axes=self.sync_axes,
        )

        if bias is not None:
            y = y + jnp.reshape(bias, (1,) * (y.ndim - 1) + (-1,))

        return y

    def __call__(
        self, inputs: Shaped[Array, "num_tokens in_features"], group_sizes: Array
    ) -> Shaped[Array, "num_tokens out_features"]:
        return self.native_forward(inputs=inputs, group_sizes=group_sizes)
