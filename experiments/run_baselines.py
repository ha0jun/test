"""Run baseline artifact-removal methods on synthetic DBS-LFP data."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from src.data.synthetic_lfp import LFPParams, StimParams, generate_pair
from src.methods.template_subtraction import subtract_global_phase_template
from src.methods.adaptive_lms import make_reference_from_stim_train, nlms_cancel
from src.methods.decomposition import pca_lowrank_denoise
from src.metrics.signal_metrics import summary_metrics


def run_once(seed: int = 0):
    lfp = LFPParams(fs=1000, duration_s=10)
    stim = StimParams(freq_hz=130, amp=5.0, pulse_width_ms=0.15, decay_ms=2.0)
    data = generate_pair(lfp, stim, seed=seed)

    clean = data["clean"]
    obs = data["observed"]
    fs = data["fs"]

    results = {}

    est_template = subtract_global_phase_template(obs, fs=fs, stim_freq_hz=stim.freq_hz)
    results["template"] = summary_metrics(clean, est_template, fs)

    period = max(1, int(round(fs / stim.freq_hz)))
    X = make_reference_from_stim_train(len(obs), period=period, taps=8)
    est_nlms, _ = nlms_cancel(obs, X, mu=0.5)
    results["nlms"] = summary_metrics(clean, est_nlms, fs)

    est_pca = pca_lowrank_denoise(obs, lag=64, rank=2)
    est_pca = est_pca[: len(clean)]
    results["pca"] = summary_metrics(clean, est_pca, fs)

    return results


def main():
    out = {"seed_0": run_once(seed=0)}
    out_dir = Path("experiments/results")
    out_dir.mkdir(parents=True, exist_ok=True)
    p = out_dir / "baseline_metrics.json"
    p.write_text(json.dumps(out, indent=2))
    print(f"Wrote {p}")


if __name__ == "__main__":
    main()
