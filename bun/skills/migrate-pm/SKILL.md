---
name: migrate-pm
description: This skill should be used when the user asks to "migrate to bun", "switch package manager to bun", "convert from npm to bun", "convert from pnpm to bun", "convert from yarn to bun", "replace npm with bun", or mentions migrating a JavaScript project's package manager to Bun.
---

# Package Manager Migration to Bun

Migrate the current project from npm, pnpm, or yarn to use **Bun as the package manager only**.

## CRITICAL GUARDS

**This migration is for PACKAGE MANAGER only, NOT runtime.**

- DO NOT replace `node` with `bun` in scripts or commands
- DO NOT change runtime configurations
- DO NOT modify how scripts execute (e.g., keep `node server.js`, not `bun server.js`)
- ONLY change package management commands:
  - `npm install` / `pnpm install` / `yarn` → `bun install`
  - `npm add` / `pnpm add` / `yarn add` → `bun add`
  - `npm remove` / `pnpm remove` / `yarn remove` → `bun remove`
  - `npm run <script>` / `pnpm <script>` / `yarn <script>` → `bun run <script>` or `bun <script>`
  - `npx` / `pnpm dlx` / `yarn dlx` → `bunx`

## Migration Steps

### Step 1: Detect Current Package Manager

Check which lockfile exists:
- `package-lock.json` → npm
- `pnpm-lock.yaml` → pnpm
- `yarn.lock` → yarn

Report which package manager was detected.

### Step 2: Clean Up

Remove in this order:
1. **Lockfile**: Remove the detected lockfile (`package-lock.json`, `pnpm-lock.yaml`, or `yarn.lock`)
2. **node_modules**: Remove the `node_modules/` directory
3. **Framework caches**: Remove these directories if they exist:
   - `.next/` (Next.js)
   - `.expo/` (Expo)
   - `.nuxt/` (Nuxt)
   - `.output/` (Nitro/Nuxt)
   - `.turbo/` (Turborepo)
   - `.cache/` (Various tools)
   - `dist/` (Build output - ask user first if non-empty)

Use `rm -rf` for each directory. Report what was removed.

### Step 3: Install Dependencies with Bun

Run `bun install` and capture the output.

**Important**: Watch for blocked lifecycle scripts. Bun blocks postinstall scripts by default for security. The output will show messages like:
```
warn: xyz's postinstall script was blocked. Run `bun pm trust xyz` to allow it.
```

### Step 4: Trust Required Packages

For each package that had its postinstall blocked:
1. List the packages that need trusting
2. Ask the user: "The following packages need postinstall scripts to run: [list]. Trust all of them?"
3. If confirmed, run `bun pm trust <package>` for each one
4. Run `bun install` again to execute the postinstall scripts

### Step 5: Update Documentation

Search and update package manager references in these files:

#### 5a. package.json scripts
Read `package.json` and update the `scripts` section:
- Replace `npm run` with `bun run`
- Replace `pnpm` with `bun` (for script execution)
- Replace `yarn` with `bun`
- Replace `npx` with `bunx`
- Replace `pnpm dlx` with `bunx`
- DO NOT change `node` commands - keep them as-is

#### 5b. CLAUDE.md
If exists, update:
- Package manager commands in code blocks
- Development commands documentation
- Any npm/pnpm/yarn references to bun equivalents
- Update "Package Manager" references if documented

#### 5c. README.md
If exists, update:
- Installation instructions
- Development setup commands
- Any documented npm/pnpm/yarn commands

#### 5d. Other *.md files
Use Glob to find all `*.md` files and Grep to find files containing npm/pnpm/yarn commands. Update relevant documentation files.

### Step 6: Summary

Report:
- Previous package manager
- Files cleaned up
- Packages trusted (if any)
- Files updated
- Any manual steps needed

## Dry Run Mode

If `--dry-run` is passed:
- DO NOT execute any destructive commands
- Only report what WOULD be done
- Show which files would be modified and what changes would be made

## Command Equivalence Reference

| npm | pnpm | yarn | bun |
|-----|------|------|-----|
| `npm install` | `pnpm install` | `yarn` | `bun install` |
| `npm install <pkg>` | `pnpm add <pkg>` | `yarn add <pkg>` | `bun add <pkg>` |
| `npm install -D <pkg>` | `pnpm add -D <pkg>` | `yarn add -D <pkg>` | `bun add -d <pkg>` |
| `npm install -g <pkg>` | `pnpm add -g <pkg>` | `yarn global add <pkg>` | `bun add -g <pkg>` |
| `npm uninstall <pkg>` | `pnpm remove <pkg>` | `yarn remove <pkg>` | `bun remove <pkg>` |
| `npm run <script>` | `pnpm <script>` | `yarn <script>` | `bun <script>` |
| `npx <cmd>` | `pnpm dlx <cmd>` | `yarn dlx <cmd>` | `bunx <cmd>` |
| `npm ci` | `pnpm install --frozen-lockfile` | `yarn --frozen-lockfile` | `bun install --frozen-lockfile` |
| `npm update` | `pnpm update` | `yarn upgrade` | `bun update` |
| `npm outdated` | `pnpm outdated` | `yarn outdated` | `bun outdated` |
