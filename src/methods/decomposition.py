"""PCA/ICA-style decomposition baselines for artifact suppression."""

from __future__ import annotations

import numpy as np


def hankel_embed(x: np.ndarray, lag: int = 32) -> np.ndarray:
    n = len(x)
    m = max(2, min(lag, n // 2))
    H = np.zeros((n - m + 1, m))
    for i in range(m):
        H[:, i] = x[i : i + n - m + 1]
    return H


def pca_lowrank_denoise(x: np.ndarray, lag: int = 32, rank: int = 2) -> np.ndarray:
    H = hankel_embed(x, lag)
    U, S, Vt = np.linalg.svd(H, full_matrices=False)
    Sr = np.zeros_like(S)
    Sr[:rank] = S[:rank]
    Hr = (U * Sr) @ Vt

    # Diagonal averaging back to 1D
    n1, n2 = Hr.shape
    out = np.zeros(n1 + n2 - 1)
    cnt = np.zeros_like(out)
    for i in range(n1):
        for j in range(n2):
            out[i + j] += Hr[i, j]
            cnt[i + j] += 1
    return out / np.maximum(cnt, 1)


def ica_denoise_placeholder(x: np.ndarray) -> np.ndarray:
    """Placeholder: ICA needs multichannel mixtures; keep identity for now."""
    return x.copy()
