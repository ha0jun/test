"""Synthetic LFP generator for DBS artifact-removal benchmarking."""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass
class LFPParams:
    fs: float = 1000.0
    duration_s: float = 10.0
    noise_std: float = 0.2
    oscillations: tuple[tuple[float, float], ...] = ((8.0, 1.0), (20.0, 0.6), (70.0, 0.3))


@dataclass
class StimParams:
    freq_hz: float = 130.0
    amp: float = 5.0
    pulse_width_ms: float = 0.15
    decay_ms: float = 2.0


def generate_clean_lfp(params: LFPParams, seed: int = 0) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    n = int(params.fs * params.duration_s)
    t = np.arange(n) / params.fs

    x = np.zeros_like(t)
    for freq, amp in params.oscillations:
        phase = rng.uniform(0, 2 * np.pi)
        x += amp * np.sin(2 * np.pi * freq * t + phase)

    colored = rng.normal(scale=params.noise_std, size=n)
    x += np.convolve(colored, np.ones(7) / 7.0, mode="same")
    return t, x


def _artifact_kernel(fs: float, pulse_width_ms: float, decay_ms: float, amp: float) -> np.ndarray:
    pw = max(1, int(round((pulse_width_ms / 1000.0) * fs)))
    tail = max(1, int(round((decay_ms / 1000.0) * fs)))
    pulse = np.ones(pw)
    decay = np.exp(-np.arange(tail) / max(1, tail / 4.0))
    kernel = np.concatenate([pulse, decay])
    return amp * kernel / (np.max(np.abs(kernel)) + 1e-12)


def generate_dbs_artifact(n: int, fs: float, stim: StimParams) -> np.ndarray:
    period = max(1, int(round(fs / stim.freq_hz)))
    spike_train = np.zeros(n)
    spike_train[::period] = 1.0
    k = _artifact_kernel(fs, stim.pulse_width_ms, stim.decay_ms, stim.amp)
    return np.convolve(spike_train, k, mode="same")


def mix_signal(clean_lfp: np.ndarray, artifact: np.ndarray, scale: float = 1.0) -> np.ndarray:
    return clean_lfp + scale * artifact


def generate_pair(lfp: LFPParams | None = None, stim: StimParams | None = None, seed: int = 0):
    lfp = lfp or LFPParams()
    stim = stim or StimParams()
    t, clean = generate_clean_lfp(lfp, seed=seed)
    art = generate_dbs_artifact(len(clean), lfp.fs, stim)
    noisy = mix_signal(clean, art)
    return {"t": t, "clean": clean, "artifact": art, "observed": noisy, "fs": lfp.fs}
