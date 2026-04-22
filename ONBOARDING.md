# Agent runbook — team LLM + Obsidian bootstrap

Execute these steps **in order**. If a step fails, stop and report the error output.

## Preconditions

- macOS or Linux with `bash`, `python3`, `git`, and `find` available.
- User has cloned **`dev-team-bootstrap`** and knows the **absolute path** to their **`DevProjects`** root (folder that contains multiple git repos).

## Step 1 — Verify clone

1. `cd` into the `dev-team-bootstrap` repository root (where `install.sh` lives).
2. Confirm `install.sh` and `scripts/apply_llm_wiki_scaffold.py` exist.

## Step 2 — Run the installer

Run (replace the path with the user’s real `DevProjects` path):

```bash
chmod +x install.sh
./install.sh --dev-projects "/absolute/path/to/DevProjects"
```

Expected: one line printed per repository processed, ending with `Done: N repos`.

## Step 3 — Obsidian

1. Install Obsidian if missing: https://obsidian.md/
2. **Open folder as vault** → choose the **same** `DevProjects` directory used above.
3. Optional: merge `vault-template/.obsidian/app.json` **`userIgnoreFilters`** into the vault’s `app.json` so heavy folders are excluded.

## Step 4 — graphify (optional but recommended)

If `graphify` is installed, for **each** git repo root under `DevProjects`:

```bash
graphify update "/absolute/path/to/ThatRepo"
```

Confirm `graphify-out/graph.json` and `GRAPH_REPORT.md` exist after the run.

## Step 5 — Cursor / Claude Code usage

- Open the **individual git repo** as the workspace when coding (not the whole `DevProjects` tree), so `.cursor/rules` and roots resolve correctly.
- Obsidian can still use the **single** vault rooted at `DevProjects` for cross-repo notes.

## Step 6 — Git remote policy

Do **not** commit `wiki/`, `raw/`, `CONTEXT.md`, `AGENTS.md`, `CLAUDE.md`, `.claude/`, `.cursor/`, `graphify-out/` to remote; they should remain ignored locally. If the installer printed `git rm --cached` warnings, the user should review `git status` and commit only intentional code changes.

## Done

Report: number of repos found, any failures, and whether Obsidian opens the vault without errors.
