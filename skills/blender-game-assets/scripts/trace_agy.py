"""Summarize saved AGY CLI token telemetry without printing prompts."""

import argparse
from collections import deque
from dataclasses import dataclass
import json
from pathlib import Path
import re
import sys

LOG_PATH = Path(".system_generated/logs/transcript_full.jsonl")
CHILD = re.compile(
    r'Created the following subagent:\s*\{\s*"conversationId"\s*:\s*"([0-9a-f-]+)"',
    re.IGNORECASE,
)
PHASE = re.compile(r"\[phase:\s*([\w /-]{1,40})\]", re.IGNORECASE)


@dataclass
class Usage:
    calls: int = 0
    input: int = 0
    output: int = 0
    cache: int = 0

    @property
    def recorded(self):
        return self.input + self.output

    def add(self, other):
        self.calls += other.calls
        self.input += other.input
        self.output += other.output
        self.cache += other.cache


def read_log(path):
    with path.open(encoding="utf-8-sig") as stream:
        for number, line in enumerate(stream, 1):
            if line.strip():
                try:
                    yield json.loads(line)
                except json.JSONDecodeError:
                    print(f"Skipping unreadable line {number} in {path}", file=sys.stderr)


def print_breakdown(title, entries):
    print(f"\n{title}")
    print(f"{'Scope':<66} {'Calls':>6} {'Input':>12} {'Output':>12}"
          f" {'Input+output':>13} {'Cache read':>13}")
    for label, counts in entries:
        print(f"{label[:66]:<66} {counts.calls:>6,} {counts.input:>12,} {counts.output:>12,}"
              f" {counts.recorded:>13,} {counts.cache:>13,}")


def report(brain, root_id, top):
    queue = deque([(root_id, "Root")])
    seen = {root_id}
    agents, turns, calls = [], [], []
    models = {}
    while queue:
        conversation_id, role = queue.popleft()
        path = brain / conversation_id / LOG_PATH
        if not path.is_file():
            print(f"No full transcript for {conversation_id} ({role})", file=sys.stderr)
            continue

        usage = Usage()
        turn_usage = None
        pending_roles = deque()
        for row in read_log(path):
            step = row.get("step_index")
            row_type = row.get("type")
            content = row.get("content") or ""
            if row_type == "USER_INPUT" and conversation_id == root_id:
                phase = PHASE.search(content.split("</USER_REQUEST>", 1)[0])
                turn_usage = Usage()
                label = phase.group(1).strip() if phase else "User turn"
                turns.append((f"#{step} {label}", turn_usage))

            if row_type == "PLANNER_RESPONSE":
                tools = row.get("tool_calls") or []
                pending_roles = deque(
                    (call.get("args") or {}).get("Role") or "Subagent"
                    for call in tools if call.get("name") == "invoke_subagent"
                )
                if "input_tokens" in row:
                    counts = Usage(
                        1, row["input_tokens"], row.get("output_tokens", 0),
                        row.get("cache_read_tokens", 0),
                    )
                    usage.add(counts)
                    models.setdefault(row.get("model") or "Unknown model", Usage()).add(counts)
                    if turn_usage is not None:
                        turn_usage.add(counts)
                    names = ", ".join(call["name"] for call in tools) or "text"
                    calls.append((counts, conversation_id, step, names))
            elif row_type == "GENERIC":
                match = CHILD.search(content)
                if match:
                    child = match.group(1)
                    child_role = pending_roles.popleft() if pending_roles else "Subagent"
                    if child not in seen:
                        seen.add(child)
                        queue.append((child, child_role))
                elif "failed to create subagent conversation" in content and pending_roles:
                    pending_roles.popleft()

        agents.append((conversation_id[:8] + " " + role, usage))

    total = Usage()
    for _, counts in agents:
        total.add(counts)
    print(f"Root: {root_id} | transcripts found: {len(agents)}")
    print("Input+output is a log subtotal; cache reads are separate.")
    print_breakdown("By conversation", [("TOTAL", total)] + sorted(
        agents, key=lambda item: item[1].recorded, reverse=True,
    ))
    print_breakdown("By model", sorted(models.items(), key=lambda item: item[1].recorded,
                                       reverse=True))
    print_breakdown("By user turn (root only)", [item for item in turns if item[1].calls])
    print_breakdown("Largest model calls", [
        (f"{conversation_id[:8]} #{step} {names}", counts)
        for counts, conversation_id, step, names in sorted(
            calls, key=lambda item: item[0].recorded, reverse=True,
        )[:top]
    ])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("conversation", help="Conversation UUID or unique prefix")
    parser.add_argument("--brain", type=Path,
                        default=Path.home() / ".gemini/antigravity-cli/brain")
    parser.add_argument("--top", type=int, default=8, help="Number of model calls to rank")
    args = parser.parse_args()
    if not re.fullmatch(r"[0-9a-f-]{4,36}", args.conversation, re.IGNORECASE):
        parser.error("provide a conversation UUID or prefix with at least four characters")
    if args.top < 0:
        parser.error("--top must be nonnegative")
    matches = [
        path.name for path in args.brain.glob(args.conversation.lower() + "*")
        if (path / LOG_PATH).is_file()
    ]
    if len(matches) != 1:
        parser.error(f"expected one transcript for {args.conversation}; found {len(matches)}")
    report(args.brain, matches[0], args.top)


if __name__ == "__main__":
    main()
