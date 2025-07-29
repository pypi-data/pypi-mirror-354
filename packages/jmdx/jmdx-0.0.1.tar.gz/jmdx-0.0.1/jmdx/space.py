from jax import jit, Array
import jax.numpy as jnp


@jit
def apply_pbc(vec: Array, box: Array) -> Array:
    return jnp.mod(vec, box)
