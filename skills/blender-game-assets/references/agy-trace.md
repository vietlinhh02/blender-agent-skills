# Trace Antigravity CLI token usage

Use separate user turns with labels such as [phase: build], [phase: preview], and [phase: export]. After Antigravity saves the transcript, run:

    python scripts/trace_agy.py CONVERSATION_ID_OR_PREFIX

Run from the skill folder. The parser reads saved local logs, ranks model calls and separates input, output, and cache reads. It does not call a model, print prompt text, or upload logs. This helper applies to Antigravity CLI transcripts that expose the supported fields. For other agents, use the host's own usage reporting.
