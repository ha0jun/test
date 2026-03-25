"""Create simple comparison plots from baseline metrics JSON."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt


def main():
    metrics_path = Path("experiments/results/baseline_metrics.json")
    if not metrics_path.exists():
        raise FileNotFoundError("Run experiments/run_baselines.py first")

    data = json.loads(metrics_path.read_text())["seed_0"]
    methods = list(data.keys())
    snr = [data[m]["snr_db"] for m in methods]
    kl = [data[m]["kl_psd"] for m in methods]

    out_dir = Path("plots")
    out_dir.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(7, 4))
    plt.bar(methods, snr)
    plt.ylabel("SNR (dB)")
    plt.title("Baseline Comparison: SNR")
    plt.tight_layout()
    plt.savefig(out_dir / "baseline_snr.png", dpi=150)
    plt.close()

    plt.figure(figsize=(7, 4))
    plt.bar(methods, kl)
    plt.ylabel("KL divergence (PSD)")
    plt.title("Baseline Comparison: Spectral KL")
    plt.tight_layout()
    plt.savefig(out_dir / "baseline_kl_psd.png", dpi=150)
    plt.close()

    print("Saved plots to plots/")


if __name__ == "__main__":
    main()
