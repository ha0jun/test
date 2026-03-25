# Project Plan: Real-time Artifact Removal for Simultaneous DBS + LFP

## Objective
Develop and evaluate statistical + machine-learning methods for real-time suppression of stimulation artifacts in simultaneously recorded LFP.

## Constraints
- Real-time/causal emphasis
- DBS-oriented artifact morphology
- Controlled synthetic benchmark first, then transition to real data

## Workstreams
1. Literature map and taxonomy
2. Synthetic data generator with controllable artifact factors
3. Baseline methods implementation
4. Evaluation metrics + experiment harness
5. Figure/report generation pipeline

## Milestones
- M1: Reproducible synthetic benchmark scaffold
- M2: Baseline comparisons + plots
- M3: Iterative improvements and ablations
- M4: Conference-style concise report

## Initial Method Taxonomy
- Classical: template subtraction, adaptive filtering
- Blind source methods: PCA/ICA variants
- Sparse/structured decomposition
- Deep models: causal conv or sequence denoisers

## Evaluation Core
- Artifact suppression quality (PSD KL divergence, residual power)
- Neural fidelity (signal distortion / phase effects)
- Runtime feasibility (latency, throughput)
