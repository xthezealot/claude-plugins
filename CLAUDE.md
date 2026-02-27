# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a **Claude Code Plugin Marketplace** containing plugins by xthezealot. The marketplace is registered via `/plugin marketplace add xthezealot/claude-plugins` and individual plugins are installed with `/plugin install {name}@thezealot-plugins`.

Four plugins exist: **bun** (package manager migration), **himalaya** (email via CLI), **humanizer** (AI writing pattern removal), and **youtube** (transcript fetching).

## Architecture

### Marketplace Registry

`.claude-plugin/marketplace.json` is the central registry that maps plugin names to their source directories and metadata. Each plugin entry has `name`, `source` (relative path), `description`, `version`, and `author`.

### Plugin Structure

Every plugin follows this layout:

```
{plugin-name}/
├── plugin.json              # Name, version, description
├── README.md                # User-facing documentation
├── skills/{skill-name}/
│   └── SKILL.md             # Skill definition with YAML frontmatter
├── hooks/                   # Optional: PreToolUse/PostToolUse hooks
│   ├── hooks.json           # Hook configuration
│   └── *.sh                 # Hook scripts
├── scripts/                 # Optional: Supporting scripts
└── skills/{skill-name}/references/  # Optional: Reference docs loaded by skill
```

### Skills (Primary Interaction Pattern)

Skills replaced the older "commands" pattern. Each skill is defined in `skills/{name}/SKILL.md` with YAML frontmatter:

```yaml
---
name: skill-identifier
description: >-
  Keywords and context that trigger this skill (used by Claude to
  decide when to activate it).
---
```

The markdown body contains the full implementation instructions, examples, and constraints that Claude follows when the skill is activated.

### Hooks

Hooks intercept tool calls for safety. Defined in `hooks/hooks.json`, they reference shell scripts that receive tool input as JSON on stdin and return a JSON decision (`{"decision": "allow"}` or `{"decision": "block", "reason": "..."}`). The himalaya plugin uses a `PreToolUse` hook on `Bash` to block destructive email operations (sending, deleting) without user confirmation.

### Environment Variables

Plugins use `${CLAUDE_PLUGIN_ROOT}` to reference files relative to their own directory (scripts, references, hooks).

## Skill Development

When creating or editing any skill (including its `SKILL.md`, reference docs, and supporting files), always read and follow the best practices in `.claude/skills/skill-development/SKILL.md` before making changes.

## Conventions

- **Line endings**: LF enforced via `.gitattributes` (`* text=auto eol=lf`)
- **Shell scripts**: Use `#!/bin/bash` and `set -euo pipefail`
- **Python scripts**: Use `#!/usr/bin/env python3` with type hints
- **Skill descriptions**: Write as keyword-rich trigger phrases so Claude activates the skill for the right user intents
- **Reference docs**: Place in `skills/{name}/references/` and load via `${CLAUDE_PLUGIN_ROOT}` paths in SKILL.md
- **Safety-critical operations**: Guard with PreToolUse hooks that block and prompt for confirmation
