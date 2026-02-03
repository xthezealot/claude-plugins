#!/bin/bash
set -euo pipefail

input=$(cat)
command=$(echo "$input" | jq -r '.tool_input.command // ""')

if echo "$command" | grep -qE 'himalaya\s+(template|message)\s+send|himalaya\s+(message|folder)\s+(delete|purge|expunge)'; then
  echo '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"ask","permissionDecisionReason":"Destructive email command — confirm before executing."}}'
fi
