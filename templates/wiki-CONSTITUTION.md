# LLM Wiki — constitution (__REPO_NAME__)

Single memory contour at **the root of this repository**. See [Karpathy LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f): **ingest** → `raw/`, **query** → `wiki/` + code, **lint** → verify against code.

## Layers

| Layer | Purpose |
|------|---------|
| `raw/` | Long captures and raw material. |
| `wiki/` | Compressed base, `index.md`, topics, optional `log.md`. |
| `CONTEXT.md` | Short handoff between sessions and tools. |
| `AGENTS.md` / `CLAUDE.md` | Single schema for agents. |
| `graphify-out/` | Optional: auto structure over code. |

## Tools

- **Cursor:** `.cursor/rules/`
- **Claude Code:** `.claude/settings.json`
- **Codex:** `.codex/hooks.json`

All of the above are listed in `.gitignore` — local machine only.

## Obsidian

Open **this repository folder** as a vault when focusing on this project, or use a parent vault that contains multiple repos (team convention).

## When to update

Refresh `CONTEXT.md` and, when needed, `wiki/log.md` after sign-off, focus changes, or long sessions.
