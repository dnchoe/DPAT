# -*- coding: utf-8 -*-
import numpy as np
from scipy import optimize #yeo jhonson transformation

def yeojohnson(x, lmbda=None):

    x = np.asarray(x)
    if x.size == 0:
        return x

    if np.issubdtype(x.dtype, np.complexfloating):
        raise ValueError('Yeo-Johnson transformation is not defined for '
                         'complex numbers.')

    if np.issubdtype(x.dtype, np.integer):
        x = x.astype(np.float64, copy=False)

    if lmbda is not None:
        return _yeojohnson_transform(x, lmbda)

    # if lmbda=None, find the lmbda that maximizes the log-likelihood function.
    lmax = yeojohnson_normmax(x)
    y = _yeojohnson_transform(x, lmax)

    return y, lmax

def yeojohnson_normmax(x, brack=(-2, 2)):

    def _neg_llf(lmbda, data):
        return -yeojohnson_llf(lmbda, data)

    return optimize.brent(_neg_llf, brack=brack, args=(x,))

def yeojohnson_llf(lmb, data):
    data = np.asarray(data)
    n_samples = data.shape[0]

    if n_samples == 0:
        return np.nan

    trans = _yeojohnson_transform(data, lmb)

    loglike = -n_samples / 2 * np.log(trans.var(axis=0))
    loglike += (lmb - 1) * (np.sign(data) * np.log(np.abs(data) + 1)).sum(axis=0)

    return loglike

def _yeojohnson_transform(x, lmbda):

    out = np.zeros_like(x)
    pos = x >= 0  # binary mask

    # when x >= 0
    if abs(lmbda) < np.spacing(1.):
        out[pos] = np.log1p(x[pos])
    else:  # lmbda != 0
        out[pos] = (np.power(x[pos] + 1, lmbda) - 1) / lmbda

    # when x < 0
    if abs(lmbda - 2) > np.spacing(1.):
        out[~pos] = -(np.power(-x[~pos] + 1, 2 - lmbda) - 1) / (2 - lmbda)
    else:  # lmbda == 2
        out[~pos] = -np.log1p(-x[~pos])

    return out

