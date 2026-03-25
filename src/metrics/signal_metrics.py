"""Evaluation metrics for artifact-removal quality and neural fidelity."""

from __future__ import annotations

import numpy as np


def snr_db(ref: np.ndarray, est: np.ndarray) -> float:
    num = np.mean(ref ** 2)
    den = np.mean((ref - est) ** 2) + 1e-12
    return float(10 * np.log10(num / den))


def _periodogram(x: np.ndarray, fs: float) -> tuple[np.ndarray, np.ndarray]:
    X = np.fft.rfft(x)
    p = (np.abs(X) ** 2) / len(x)
    f = np.fft.rfftfreq(len(x), d=1.0 / fs)
    return f, p


def kl_divergence_psd(ref: np.ndarray, est: np.ndarray, fs: float) -> float:
    _, p = _periodogram(ref, fs)
    _, q = _periodogram(est, fs)
    p = p / (np.sum(p) + 1e-12)
    q = q / (np.sum(q) + 1e-12)
    return float(np.sum(p * np.log((p + 1e-12) / (q + 1e-12))))


def bandpower(x: np.ndarray, fs: float, fmin: float, fmax: float) -> float:
    f, p = _periodogram(x, fs)
    m = (f >= fmin) & (f <= fmax)
    return float(np.trapz(p[m], f[m])) if np.any(m) else 0.0


def corrcoef(ref: np.ndarray, est: np.ndarray) -> float:
    c = np.corrcoef(ref, est)[0, 1]
    return float(c)


def summary_metrics(ref: np.ndarray, est: np.ndarray, fs: float) -> dict:
    return {
        "snr_db": snr_db(ref, est),
        "kl_psd": kl_divergence_psd(ref, est, fs),
        "corr": corrcoef(ref, est),
        "beta_power_ref": bandpower(ref, fs, 13, 30),
        "beta_power_est": bandpower(est, fs, 13, 30),
    }
