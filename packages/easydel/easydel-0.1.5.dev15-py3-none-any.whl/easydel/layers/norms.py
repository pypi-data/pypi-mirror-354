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


import jax
from flax import nnx as nn
from jax import lax
from jax import numpy as jnp

float8s = [
    jnp.float8_e4m3b11fnuz,
    jnp.float8_e4m3fn,
    jnp.float8_e4m3fnuz,
    jnp.float8_e5m2,
    jnp.float8_e5m2fnuz,
]


class RMSNorm(nn.Module):
    def __init__(
        self,
        dim: int,
        eps: float = 1e-6,
        dtype: jnp.dtype = jnp.bfloat16,
        param_dtype: jnp.dtype = jnp.bfloat16,
        *,
        rngs: nn.Rngs | None = None,
    ) -> None:
        if rngs is None:
            rngs = nn.Rngs(0)
        self.dim = dim
        self.eps = eps
        self.dtype = dtype
        self.param_dtype = param_dtype
        self.kernel = nn.Param(
            nn.initializers.ones(
                rngs.params(),
                (self.dim,),
                self.param_dtype,
            ),
        )

    def _norm(self, x: jnp.ndarray) -> jnp.ndarray:
        return x * lax.rsqrt(jnp.square(x).mean(-1, keepdims=True) + self.eps)

    @jax.named_scope("easydel-rmsnorm")
    def __call__(self, x: jnp.ndarray) -> jnp.ndarray:
        org_dtype = x.dtype
        if self.param_dtype in float8s or self.dtype in float8s:
            x = x.astype(jnp.float32)
        else:
            x = x.astype(jnp.promote_types(self.dtype, jnp.float32))
        output = self._norm(x).astype(self.dtype)
        weight = self.kernel.astype(self.dtype)
        return (weight * output).astype(org_dtype)
