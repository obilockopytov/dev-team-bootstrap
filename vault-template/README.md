# Obsidian vault snippet

Use this when **one vault** covers many repositories under a single parent folder (for example `DevProjects`).

## Setup

1. In Obsidian: **Open folder as vault** → select the parent folder (e.g. `DevProjects`), not each repo separately.
2. Copy or merge `.obsidian/app.json` from this template into your vault’s `.obsidian/` folder.
3. Adjust **`userIgnoreFilters`** to match your stack (build outputs, large assets, etc.).

Heavy paths are excluded so Obsidian stays fast; Cursor/Claude still open individual repo roots for coding.
