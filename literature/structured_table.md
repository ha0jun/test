# Structured Literature Table — Artifact Removal for Simultaneous DBS + LFP

| Work (representative) | Modality | Stimulation Type | Method Class | Real-time capable? | Key assumptions | Typical metric(s) | Notes/Gaps |
|---|---|---|---|---|---|---|---|
| Template subtraction (phase-locked averaging) | LFP/ECoG/EEG | Periodic DBS or pulse trains | Classical subtraction | Yes (causal sliding templates) | Artifact highly phase-locked | Residual artifact power, SNR | Can suppress neural components if phase overlaps physiology |
| Adaptive filtering (LMS/NLMS/RLS) | LFP/EEG | Known stimulation timing/reference | Adaptive linear filter | Yes | Reference captures artifact dynamics | SNR gain, spectral distortion, latency | Sensitive to nonstationarity and reference mismatch |
| PCA/ICA/BSS decomposition | Multi-channel LFP/EEG/ECoG | Broad stimulation settings | Blind source separation | Sometimes (often offline) | Artifact occupies dominant subspace/independent source | Correlation, PSD mismatch | Usually needs multichannel data; causality less straightforward |
| Sparse / low-rank decomposition | LFP/ECoG | Pulsatile stimulation | Structured optimization | Usually offline or block-causal | Artifact sparse/structured in transformed domain | Reconstruction error, task metrics | Computational load may challenge strict real-time |
| Deep denoisers (causal CNN/RNN/TCN) | LFP/EEG | Data-driven across paradigms | ML/DL | Potentially yes (causal models) | Training data captures domain shift | SNR, KL-PSD, downstream decode | Generalization + hallucination risk; needs careful controls |

## Notes
- This table is a living synthesis and will be expanded with concrete paper citations in upcoming passes.
- Priority lens: methods that are implementable under strict causal/latency constraints for bidirectional BCI.
