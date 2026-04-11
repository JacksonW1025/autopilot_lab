# Contract Audit

## Raw Manifest
- required_contract_keys_present_in_both: `true`
- px4_only_keys: clock_bridge, injector_report, px4_log_path, recorder_summary, ros_topics_recorded, sim_world, telemetry_backfill
- ardupilot_only_keys: ardupilot_bin_log_path, ardupilot_tlog_path, bin_extract_summary, frame, master_uri, runtime_report, vehicle

## Acceptance Keys
- exact_match: `true`
- px4_only_keys: none
- ardupilot_only_keys: none

## Prepared Sample Table
- identity_columns_match: `true`
- identity_columns: sample_id, run_id, backend, mode, scenario, config_profile, research_tier, research_acceptance, seed, timestamp, logical_step
- prefix_contract_ok: `true`
- prefix `backend_` present: `true`
- prefix `mode_` present: `true`
- prefix `scenario_` present: `true`
- prefix `config_profile_` present: `true`
- prefix `param_` present: `true`

## Schema Naming
- px4: `commands_plus_state -> delta_state`
- ardupilot: `commands_plus_state -> delta_state`
- exact_match: `true`

## Conclusion
- contract_ok: `true`
- Cross-backend contract audit passed on manifest contract keys, acceptance keys, prepared identity columns, prefixes, and schema naming.