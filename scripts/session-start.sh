#!/usr/bin/env bash
# Foreman SessionStart hook.
# Reminds Claude of the manager role and surfaces the recent Run Log so past
# work is in context at the start of every session. Output is added to context.
set -euo pipefail

cat <<'EOF'
Foreman active — Claude is the manager, skills and agents are the crew.
- Route each subtask to the cheapest capable coworker: inline -> skill -> agent.
- Run independent subtasks in parallel (batch agent calls into one message).
- After each meaningful action, append a dated line to the "## Run Log" in CLAUDE.md.
EOF

if [ -f CLAUDE.md ]; then
  recent="$(awk '/^## Run Log/{f=1;next} f' CLAUDE.md | grep -v '^[[:space:]]*$' | tail -5)"
  if [ -n "$recent" ]; then
    printf '\nRecent Run Log (from CLAUDE.md):\n%s\n' "$recent"
  fi
fi
