# humanizer

Claude Code plugin to remove signs of AI-generated writing from text.

## Installation

This plugin is installed at `~/.claude/plugins/humanizer`.

To use in Claude Code, ensure the plugin directory is recognized by Claude Code.

## Skills

### `/humanizer`

Identifies and removes AI writing patterns to make text sound natural and human-written.

**Usage:**
```
/humanizer
```

**What it does:**
1. Scans text for 24 categories of AI writing patterns (significance inflation, promotional language, vague attributions, em dash overuse, sycophantic tone, etc.)
2. Rewrites problematic sections while preserving meaning and intended tone
3. Adds genuine voice and personality — not just pattern removal
4. Runs a final anti-AI audit pass to catch remaining tells

**Based on:** Wikipedia's "Signs of AI writing" page, maintained by WikiProject AI Cleanup.

## Notes

- Works on any text: articles, emails, documentation, blog posts
- Preserves the core message while making it sound like a person wrote it
- Outputs a draft rewrite, identifies remaining tells, then delivers a final version
