"""Adaptive filtering baselines using reference artifact regressors."""

from __future__ import annotations

import numpy as np


def make_reference_from_stim_train(n: int, period: int, taps: int = 8) -> np.ndarray:
    u = np.zeros(n)
    u[::period] = 1.0
    X = np.zeros((n, taps))
    for k in range(taps):
        X[k:, k] = u[: n - k]
    return X


def lms_cancel(x: np.ndarray, X: np.ndarray, mu: float = 0.01) -> tuple[np.ndarray, np.ndarray]:
    n, d = X.shape
    w = np.zeros(d)
    y = np.zeros(n)
    e = np.zeros(n)

    for i in range(n):
        y[i] = X[i] @ w
        e[i] = x[i] - y[i]
        w = w + 2.0 * mu * e[i] * X[i]
    return e, w


def nlms_cancel(x: np.ndarray, X: np.ndarray, mu: float = 0.5, eps: float = 1e-6):
    n, d = X.shape
    w = np.zeros(d)
    y = np.zeros(n)
    e = np.zeros(n)

    for i in range(n):
        xi = X[i]
        y[i] = xi @ w
        e[i] = x[i] - y[i]
        denom = eps + np.dot(xi, xi)
        w = w + (mu / denom) * e[i] * xi
    return e, w
