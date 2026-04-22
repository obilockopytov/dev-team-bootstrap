#!/usr/bin/env python3
"""Apply local-only LLM Wiki + agent hooks to every git root under a DevProjects tree."""
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

BOOTSTRAP_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = BOOTSTRAP_ROOT / "templates"


def load_template(name: str) -> str:
    return (TEMPLATES / name).read_text(encoding="utf-8")


def git_roots(dev: Path) -> list[Path]:
    out = subprocess.run(
        ["find", str(dev), "-name", ".git", "-type", "d"],
        capture_output=True,
        text=True,
        check=True,
    )
    return sorted(
        {Path(line.strip()).parent for line in out.stdout.splitlines() if line.strip()}
    )


def ensure_gitignore(repo: Path, block: str) -> None:
    gi = repo / ".gitignore"
    text = gi.read_text(encoding="utf-8") if gi.exists() else ""
    if "AI layer: local only (REBUILD §2.8)" in text or "AI-агенты и IDE (локально)" in text:
        return
    gi.write_text(text.rstrip() + block, encoding="utf-8")


def write_if_missing(path: Path, content: str) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def subst_repo_name(template: str, repo_name: str) -> str:
    return template.replace("__REPO_NAME__", repo_name)


def ensure_rules_dir(repo: Path) -> None:
    rules = repo / ".cursor" / "rules"
    if rules.is_symlink() or (rules.exists() and not rules.is_dir()):
        rules.unlink()
    rules.mkdir(parents=True, exist_ok=True)


def write_always(repo: Path) -> None:
    name = repo.name
    claude_settings = load_template("claude-settings.json")
    codex_hooks = load_template("codex-hooks.json")
    llm_mdc = load_template("llm-wiki-context.mdc")
    workflow_mdc = load_template("repo-llm-workflow.mdc")

    (repo / ".claude").mkdir(parents=True, exist_ok=True)
    (repo / ".codex").mkdir(parents=True, exist_ok=True)
    (repo / ".cursor").mkdir(parents=True, exist_ok=True)
    ensure_rules_dir(repo)
    (repo / ".claude" / "settings.json").write_text(claude_settings, encoding="utf-8")
    (repo / ".codex" / "hooks.json").write_text(codex_hooks, encoding="utf-8")
    write_if_missing(repo / ".cursor" / "rules" / "llm-wiki-context.mdc", llm_mdc)
    if not (repo / ".cursor" / "rules" / "launcher.mdc").exists():
        write_if_missing(repo / ".cursor" / "rules" / "repo-llm-workflow.mdc", workflow_mdc)

    write_if_missing(
        repo / "wiki" / "CONSTITUTION.md",
        subst_repo_name(load_template("wiki-CONSTITUTION.md"), name),
    )
    write_if_missing(repo / "wiki" / "index.md", load_template("wiki-index.md"))
    write_if_missing(repo / "raw" / ".gitkeep", "")
    write_if_missing(repo / "AGENTS.md", subst_repo_name(load_template("AGENTS.md"), name))
    write_if_missing(repo / "CLAUDE.md", load_template("CLAUDE.md"))
    write_if_missing(repo / "CONTEXT.md", subst_repo_name(load_template("CONTEXT.md"), name))


def untrack_tracked_paths(repo: Path) -> None:
    ls = subprocess.run(
        ["git", "-C", str(repo), "ls-files", "-z", "--", "AGENTS.md", "CLAUDE.md", "CONTEXT.md"],
        capture_output=True,
        check=False,
    )
    for p in [x for x in ls.stdout.decode().split("\0") if x]:
        subprocess.run(
            ["git", "-C", str(repo), "rm", "--cached", "-f", "--", p],
            capture_output=True,
            text=True,
        )
    ls_wiki = subprocess.run(
        ["git", "-C", str(repo), "ls-files", "-z", "--", "wiki"],
        capture_output=True,
        check=False,
    )
    if [p for p in ls_wiki.stdout.decode().split("\0") if p]:
        subprocess.run(
            ["git", "-C", str(repo), "rm", "-r", "--cached", "-f", "--", "wiki"],
            capture_output=True,
            text=True,
        )
    ls_raw = subprocess.run(
        ["git", "-C", str(repo), "ls-files", "-z", "--", "raw"],
        capture_output=True,
        check=False,
    )
    if [p for p in ls_raw.stdout.decode().split("\0") if p]:
        subprocess.run(
            ["git", "-C", str(repo), "rm", "-r", "--cached", "-f", "--", "raw"],
            capture_output=True,
            text=True,
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dev-projects",
        type=Path,
        required=True,
        help="Absolute path to folder containing multiple git repositories (e.g. DevProjects)",
    )
    parser.add_argument(
        "--skip-untrack",
        action="store_true",
        help="Do not run git rm --cached for wiki/raw/AGENTS/CLAUDE/CONTEXT",
    )
    args = parser.parse_args()
    dev = args.dev_projects.expanduser().resolve()
    if not dev.is_dir():
        raise SystemExit(f"Not a directory: {dev}")

    block = load_template("gitignore-block.txt")
    if not block.startswith("\n"):
        block = "\n" + block

    roots = git_roots(dev)
    for repo in roots:
        print(repo)
        ensure_gitignore(repo, block)
        write_always(repo)
        if not args.skip_untrack:
            untrack_tracked_paths(repo)
    print("Done:", len(roots), "repos")


if __name__ == "__main__":
    main()
