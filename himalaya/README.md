# Himalaya Email Plugin

Email management skill for Claude Code using the [himalaya](https://github.com/pimalaya/himalaya) CLI.

## Features

- Search, read, and organize emails
- Compose, reply, and forward messages (non-interactive via template system)
- Create and manage drafts
- Download attachments
- Manage folders and flags
- MML syntax for rich content: attachments, HTML, inline images, PGP
- Multi-account support
- Full envelope query language (filter by date, sender, subject, body, flags; sort results)
- Safety hook: requires user approval before sending emails or deleting messages/folders

## Prerequisites

- [himalaya](https://github.com/pimalaya/himalaya) CLI installed and configured
- At least one email account configured in `~/.config/himalaya/config.toml`

## Installation

Install from the Claude Code plugin marketplace, or add locally:

```bash
claude --plugin-dir /path/to/himalaya
```

## Usage

The skill activates automatically when you mention email-related tasks:

- "Check my inbox for emails from Alice"
- "Send an email to bob@example.com about the meeting"
- "Reply to the last message from the team"
- "Download attachments from message 42"
- "Search for emails about the Q1 report"
- "Create a draft reply to message 15"

## Safety Hook

This plugin includes a PreToolUse hook that requires manual user approval before executing destructive himalaya operations:

- `himalaya template send` / `himalaya message send` (sending email)
- `himalaya message delete` (deleting messages)
- `himalaya folder delete` / `purge` / `expunge` (destructive folder operations)

All other himalaya commands (reading, listing, searching, flagging, moving, etc.) execute without prompting.
