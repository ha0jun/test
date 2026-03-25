"""Template subtraction baselines for periodic DBS artifacts."""

from __future__ import annotations

import numpy as np


def estimate_period_samples(fs: float, stim_freq_hz: float) -> int:
    return max(1, int(round(fs / stim_freq_hz)))


def build_phase_template(x: np.ndarray, period: int) -> np.ndarray:
    n = len(x)
    phases = np.arange(n) % period
    template = np.zeros(period)
    counts = np.zeros(period)
    np.add.at(template, phases, x)
    np.add.at(counts, phases, 1)
    counts = np.maximum(counts, 1)
    return template / counts


def subtract_global_phase_template(x: np.ndarray, fs: float, stim_freq_hz: float) -> np.ndarray:
    period = estimate_period_samples(fs, stim_freq_hz)
    template = build_phase_template(x, period)
    phases = np.arange(len(x)) % period
    return x - template[phases]


def subtract_sliding_template(
    x: np.ndarray,
    fs: float,
    stim_freq_hz: float,
    window_periods: int = 50,
) -> np.ndarray:
    period = estimate_period_samples(fs, stim_freq_hz)
    n = len(x)
    y = np.zeros_like(x)

    for i in range(n):
        phase = i % period
        start = max(0, i - window_periods * period)
        idx = np.arange(start + phase, i + 1, period)
        if len(idx) == 0:
            y[i] = x[i]
            continue
        tmpl = np.mean(x[idx])
        y[i] = x[i] - tmpl
    return y
