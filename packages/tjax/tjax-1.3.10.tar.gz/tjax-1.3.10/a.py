import jax.numpy as jnp
y = 2.0
jy = jnp.asarray(2.0)
g = {'y': y}
h = {'y': jy}
print(g == h)
