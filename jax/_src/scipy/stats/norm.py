# Copyright 2018 The JAX Authors.
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


import numpy as np
import scipy.stats as osp_stats

from jax import lax
from jax._src.lax.lax import _const as _lax_const
from jax._src.numpy import lax_numpy as jnp
from jax._src.numpy.util import _wraps
from jax._src.numpy.lax_numpy import _promote_args_inexact
from jax.scipy import special

@_wraps(osp_stats.norm.logpdf, update_doc=False)
def logpdf(x, loc=0, scale=1):
  x, loc, scale = _promote_args_inexact("norm.logpdf", x, loc, scale)
  scale_sqrd = lax.square(scale)
  log_normalizer = lax.log(lax.mul(_lax_const(x, 2 * np.pi), scale_sqrd))
  quadratic = lax.div(lax.square(lax.sub(x, loc)), scale_sqrd)
  return lax.div(lax.add(log_normalizer, quadratic), _lax_const(x, -2))


@_wraps(osp_stats.norm.pdf, update_doc=False)
def pdf(x, loc=0, scale=1):
  return lax.exp(logpdf(x, loc, scale))


@_wraps(osp_stats.norm.cdf, update_doc=False)
def cdf(x, loc=0, scale=1):
  x, loc, scale = _promote_args_inexact("norm.cdf", x, loc, scale)
  return special.ndtr(lax.div(lax.sub(x, loc), scale))


@_wraps(osp_stats.norm.logcdf, update_doc=False)
def logcdf(x, loc=0, scale=1):
  x, loc, scale = _promote_args_inexact("norm.logcdf", x, loc, scale)
  return special.log_ndtr(lax.div(lax.sub(x, loc), scale))


@_wraps(osp_stats.norm.ppf, update_doc=False)
def ppf(q, loc=0, scale=1):
  return jnp.asarray(special.ndtri(q) * scale + loc, float)
