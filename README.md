# xthezealot Claude Code Plugins

A collection of Claude Code plugins by xthezealot.

## Installation

Add this marketplace to Claude Code:

```
/plugin marketplace add xthezealot/claude-plugins
```

Then install the plugins you want:

```
/plugin install bun-migrate@thezealot-plugins
/plugin install youtube-transcript@thezealot-plugins
```

## Available Plugins

### bun-migrate

Migrate JavaScript projects from npm/pnpm/yarn to Bun as the package manager.

**Usage:**
```
/bun-migrate:pm
/bun-migrate:pm --dry-run
```

This migrates the **package manager only**, not the runtime. Your scripts will still use `node` - only package management commands are changed to use `bun`.

### youtube-transcript

Fetch YouTube video transcripts and analyze them with Claude - summarize content, answer questions, or extract specific information.

**Usage:**
```
/youtube VIDEO_ID summarize this video
/youtube https://www.youtube.com/watch?v=VIDEO_ID what are the main points?
/youtube https://youtu.be/VIDEO_ID list all products mentioned
```

Dependencies are installed automatically when Claude Code starts a session with this plugin enabled.

## License

MIT
