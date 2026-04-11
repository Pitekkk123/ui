Run the macro snapshot pipeline and review the output.

Steps:
1. Run `python -m macro_snapshot.cli --print-only` to generate and display the snapshot
2. Review the output JSON for:
   - Any metrics with status "error" or "no_data"
   - Stale metrics (is_stale = true)
   - The environment_score value and whether it's based on sufficient Tier A metrics
   - Proxy flags and stale flags
3. Summarize findings: which layers are healthy, which need attention
