# Formal V2 Next-Phase Decision Layer

## Overall Recommendation

- default_entry: A2
- hard_mode: A1
- contrast_only: B1
- boundary_candidates: C1, D1, D2
- recommendation: Use A2 as the next-phase default entry, retain A1 as a hard-mode contrast/backup line, and keep B1/C1/D1/D2 as explanatory non-entry candidates.

## Candidate Board

| priority | candidate | bucket | score | signal | structure | role |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | A2 | primary_entry_ready | 13 | pair_target_ready | direct_control | default_entry_candidate |
| 2 | A1 | mechanism_rich_hard_mode | 8 | targeted_reproduction_ready | state_continuation | hard_mode_backup_line |
| 3 | B1 | contrast_non_entry | 4 | none | state_continuation | contrast_only_candidate |
| 4 | C1 | boundary_or_pathology | -3 | none | autoregressive_blocked | boundary_explainer |
| 5 | D2 | boundary_or_pathology | -5 | none | autoregressive_blocked | boundary_explainer |
| 6 | D1 | boundary_or_pathology | -6 | none | collapse_boundary | failure_boundary_exemplar |

## Why A2 Is The Default Entry

- A2 is the default entry because it is pair-target-ready, low-conditioning, stable_non_empty, and still dominated by a direct-control throttle-to-actuator path.
- evidence_sources: /mnt/nvme/autopilot_lab/artifacts/studies/20260414_064153_formal_v2_anchor_deep_dive/tables/ardupilot_a2_c1_d1_d2_boundary.csv; /mnt/nvme/autopilot_lab/artifacts/studies/20260416_003634_371133_ardupilot_a2_pair_target_readiness/summary/a2_pair_target_readiness.json; artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation/fits/commands_only__actuator_response__pooled/ridge_affine/matrix_f.csv; artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation/fits/commands_only__actuator_response__pooled/ridge_affine/sparsity_mask.csv; artifacts/studies/20260413_070802_ardupilot_real_generalization_ablation/fits/commands_only__actuator_response__pooled/ridge_affine/metrics.json

## Why A1 Is Hard Mode, Not Baseline

- A1 is generalized-supported and targeted-reproduction-ready, but it stays in hard mode because the stable signal is a state-continuation path rather than a low-dimensional direct-control entry.
- downgrade_reasons: state_continuation_not_direct_control; requires_state_feedback_channel_assumption

## Why B1/C1/D1/D2 Are Not Mainline Entries

- B1: B1 remains a contrast-only candidate because its state-continuation template is local rather than scenario-stable, so it explains A1 but does not justify a mainline entry. | downgrade_reasons=supported_but_local_only; primary_driver=stratification
- C1: C1 stays out of the mainline because it is a stable partial + extreme conditioning sample: the raw autoregressive template persists, but formal support never matures into an entry path. | downgrade_reasons=stable_partial_mask_only; extreme_conditioning; primary_driver=feature_collinearity
- D1: D1 is not a mainline entry because it is a diagnostic raw collapse boundary: the mask stays empty and the baseline support template does not survive the diagnostic phase. | downgrade_reasons=empty_mask; diagnostic_raw_collapse; primary_driver=none
- D2: D2 is not a mainline entry because it is a stable raw template + empty mask sample under extreme conditioning, which keeps the structure as boundary evidence rather than a usable entry. | downgrade_reasons=empty_mask; stable_raw_template_but_formally_blocked; primary_driver=feature_collinearity

## Residual Unknowns And Evidence Boundary

- PX4 A1 still depends on a realistic state/feedback perturbation channel; the current artifact only shows reproducible continuation structure.
- ArduPilot state-evolution remains inconclusive; C1 and D2 are boundary evidence, not mature entry paths.
- D1 shows that targeted baseline positives can collapse under diagnostic widening, so localized success should not be promoted to a mainline entry.
