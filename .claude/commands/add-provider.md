Add a new data provider to the macro snapshot system.

Given provider description "$ARGUMENTS":
1. Determine which fetcher module this belongs in (or create a new one)
2. Implement the fetcher function following the MetricPoint contract:
   - Every return must include: name, value, asof, source, status, is_stale, notes, quality_tier, methodology
   - Use honest naming (proxy labels for proxy data)
   - Handle errors gracefully (return MetricPoint.error, never raise)
3. Register the fetcher in pipeline.py
4. Add unit tests with mocked network calls
5. Update CLAUDE.md if adding a new file
