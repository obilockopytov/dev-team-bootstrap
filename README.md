# dev-team-bootstrap

One place for **LLM + Obsidian + local-only wiki** setup across many git repositories under a shared folder (for example `DevProjects`).

## Quick start (human)

1. Clone this repository (or copy it into your Bulls Media tree).
2. Install [Obsidian](https://obsidian.md/) and [graphify](https://github.com/safishamsi/graphify) if you want code graphs.
3. Run:

```bash
chmod +x install.sh
./install.sh --dev-projects "/absolute/path/to/DevProjects"
```

4. Open **one** Obsidian vault rooted at that `DevProjects` folder (see `vault-template/` for a starter `app.json` you can merge).
5. In each repo, after big code changes: `graphify update .` at the repo root.

## Quick start (Claude Code / Cursor agent)

Paste the raw URL of [`ONBOARDING.md`](./ONBOARDING.md) from your git host and ask the agent to execute every step in order, or run `./install.sh` first and use the agent only for troubleshooting.

## What the installer does

For **each git repository** under `--dev-projects`:

- Appends a **local-only** block to `.gitignore` (`.cursor/`, `.claude/`, `wiki/`, `CONTEXT.md`, `graphify-out/`, …).
- Creates minimal **`wiki/`**, **`raw/`**, **`CONTEXT.md`**, **`AGENTS.md`**, **`CLAUDE.md`** if missing.
- Writes **`.claude/settings.json`** and **`.codex/hooks.json`** (graphify hint hooks).
- Ensures **`.cursor/rules/`** exists and adds **`llm-wiki-context.mdc`** + **`repo-llm-workflow.mdc`** (unless `launcher.mdc` already exists).
- If `AGENTS.md` / `CLAUDE.md` / `CONTEXT.md` / `wiki` / `raw` were accidentally tracked, runs **`git rm --cached`** for those paths only.

Nothing here replaces your product code; agent memory stays **local** and out of remote by policy.

## Source repository

Canonical copy: **https://github.com/obilockopytov/dev-team-bootstrap** 

If you cloned without `origin` and want your own remote:

```bash
gh repo create YOUR_USER/dev-team-bootstrap --private --source=. --remote=origin --push
```

## License

Internal team use unless you add a public license.
