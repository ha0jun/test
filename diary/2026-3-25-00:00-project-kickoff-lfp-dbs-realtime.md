# Project Kickoff — LFP + DBS + Real-time Artifact Removal

## Scope confirmed
- Signal modality: LFP
- Stimulation setting: Deep Brain Stimulation (DBS)
- Priority: real-time/causal artifact removal
- Implementation stack: Python ecosystem

## Immediate plan
1. Build structured literature table in `literature/`
2. Define synthetic data generator with controllable artifact knobs
3. Implement baseline methods:
   - template subtraction
   - adaptive filtering
   - ICA/PCA
   - sparse/BSS-style methods
   - deep learning baselines
4. Define metrics:
   - KL divergence on auto-spectra
   - SNR improvement
   - signal distortion metrics (phase/coherence)
   - downstream utility metrics where feasible

## New required outputs
- Keep all plots in `plots/`
- Maintain a concise conference-style markdown report in `paper/report.md`
