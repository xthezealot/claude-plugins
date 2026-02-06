# bun

Claude Code plugin to migrate JavaScript projects from npm/pnpm/yarn to Bun as the package manager.

## Installation

This plugin is installed at `~/.claude/plugins/bun`.

To use in Claude Code, ensure the plugin directory is recognized by Claude Code.

## Skills

### `/bun:migrate-pm`

Migrates your project's package manager to Bun.

**Usage:**
```
/bun:migrate-pm
/bun:migrate-pm --dry-run
```

**What it does:**
1. Detects current package manager (npm, pnpm, or yarn)
2. Removes lockfile, node_modules, and framework cache directories
3. Runs `bun install`
4. Trusts packages that require postinstall scripts (with confirmation)
5. Updates documentation (package.json scripts, CLAUDE.md, README.md, other *.md files)

**Important:** This migrates the **package manager only**, not the runtime. Your scripts will still use `node` - only package management commands are changed to use `bun`.

## Notes

- Always review changes before committing
- Use `--dry-run` to preview what would change
- The command will ask for confirmation before trusting postinstall scripts
