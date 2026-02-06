# xthezealot Claude Code Plugins

A collection of Claude Code plugins by xthezealot.

## Installation

Add this marketplace to Claude Code:

```
/plugin marketplace add xthezealot/claude-plugins
```

Then install the plugins you want:

```
/plugin install bun@thezealot-plugins
/plugin install himalaya@thezealot-plugins
/plugin install youtube@thezealot-plugins
```

## Available Plugins

### bun

Migrate JavaScript projects from npm/pnpm/yarn to Bun as the package manager.

**Usage:**
```
/bun:migrate-pm
/bun:migrate-pm --dry-run
```

This migrates the **package manager only**, not the runtime. Your scripts will still use `node` - only package management commands are changed to use `bun`.

### himalaya

Email management using the [himalaya](https://github.com/pimalaya/himalaya) CLI — search, read, compose, reply, forward, manage drafts, attachments, folders, and flags. Multi-account support with MML syntax for rich content.

Includes a safety hook that prompts for confirmation before sending emails or deleting messages/folders.

**Requires:** himalaya CLI installed and configured (`~/.config/himalaya/config.toml`).

### youtube

Fetch YouTube video transcripts and analyze them with Claude - summarize content, answer questions, or extract specific information.

**Usage:**
```
/youtube:transcript VIDEO_ID summarize this video
/youtube:transcript https://www.youtube.com/watch?v=VIDEO_ID what are the main points?
/youtube:transcript https://youtu.be/VIDEO_ID list all products mentioned
```

Dependencies are installed automatically when the transcript skill is first invoked.

## License

MIT
