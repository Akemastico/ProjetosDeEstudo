# ProjetosDeEstudo Repository Setup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish the existing `AgendadorDeTarefas` project as the first subproject in a public GitHub repository rooted at `~/Documentos/ProjetosDeEstudo/`.

**Architecture:** Promote the existing Git metadata from `AgendadorDeTarefas/` to the parent directory, so the parent is the only repository root. Keep the project files in place, add a root-level ignore file, require the Django signing key from the environment, and publish only source/configuration files that pass the local safety checks.

**Tech Stack:** Git, GitHub CLI (`gh`), Python 3.14, uv, Django 6.1, Django Ninja.

**Spec:** `docs/superpowers/specs/2026-10-06-projetos-de-estudo-design.md`

## Global Constraints

- Root repository and remote name: `ProjetosDeEstudo`.
- GitHub visibility: public.
- `AgendadorDeTarefas/` remains a subdirectory of the root.
- Do not create or edit README files; the user will create the root README later, and subprojects have no README.
- Keep the existing empty `AgendadorDeTarefas/README.md` local and out of the published commit.
- Do not publish `.venv`, Python caches, `.env` files, SQLite databases, or the existing fixed Django key.
- Preserve the local SQLite database and other untracked project files; do not remove project data.
- Do not overwrite or force-push to an existing GitHub repository.

## Review Focus

- Missing `DJANGO_SECRET_KEY`: Django must fail with a clear missing-variable error; verify by running a check with the variable unset.
- Configured `DJANGO_SECRET_KEY`: Django's system check must pass with a temporary test value.
- Local artifacts (`.venv`, `*.sqlite3`, `__pycache__`, `.env`): verify each representative path is ignored.
- Nested Git metadata: verify both the root and project resolve to the parent repository, and no `.git` remains inside the subproject.
- GitHub unavailable or repository name already taken: check authentication and remote name before creation; stop without overwriting if creation cannot proceed safely.

---

### Task 1: Make `ProjetosDeEstudo` the single local repository root

**Files:**
- Move Git metadata: `AgendadorDeTarefas/.git` → `.git`
- Create: `.gitignore`
- Preserve unchanged: `AgendadorDeTarefas/.gitignore`, all project source files, local SQLite database, and local empty project README

**Interfaces:**
- Consumes: Existing Git metadata with one design-spec commit and no configured remote.
- Produces: A single repository whose root is `~/Documentos/ProjetosDeEstudo/`.

- [x] **Step 1: Move the existing `.git` directory to the parent root** without moving or deleting project files; append `AgendadorDeTarefas/README.md` to `.git/info/exclude` so the existing empty project README remains local but untracked.
- [x] **Step 2: Create the root `.gitignore`** with these patterns: `.venv/`, `__pycache__/`, `*.py[cod]`, `*.sqlite3`, `.env`, `.env.*`, `build/`, `dist/`, `*.egg-info/`.
- [x] **Step 3: Verify the repository root from both directories.** Run `git rev-parse --show-toplevel` at the parent and `git -C AgendadorDeTarefas rev-parse --show-toplevel`; both must resolve to `~/Documentos/ProjetosDeEstudo/`.
- [x] **Step 4: Verify local artifacts are ignored.** Run `git check-ignore -v AgendadorDeTarefas/.venv AgendadorDeTarefas/backend/db.sqlite3 AgendadorDeTarefas/backend/api/__pycache__ AgendadorDeTarefas/.env`; each path must match an ignore rule.

### Task 2: Remove the fixed Django key from public source

**Files:**
- Modify: `AgendadorDeTarefas/backend/backend/settings.py`

**Interfaces:**
- Consumes: Environment variable `DJANGO_SECRET_KEY`.
- Produces: Django setting `SECRET_KEY` sourced only from `os.environ["DJANGO_SECRET_KEY"]`.

- [x] **Step 1: Replace the hard-coded `SECRET_KEY`** with `os.environ["DJANGO_SECRET_KEY"]`, adding `import os` if needed.
- [x] **Step 2: Verify the missing-variable behavior.** From `AgendadorDeTarefas/backend`, run `env -u DJANGO_SECRET_KEY uv run python manage.py check`; it must fail and mention `DJANGO_SECRET_KEY`.
- [x] **Step 3: Verify configured behavior.** From the same directory, run `DJANGO_SECRET_KEY=test-only-key uv run python manage.py check`; it must report no Django system-check issues.

### Task 3: Audit, commit, and publish

**Files:**
- Include: project source/configuration, root `.gitignore`, approved design and plan documents.
- Exclude: `AgendadorDeTarefas/README.md`, `.venv`, caches, `.env` files, SQLite databases, and local-only state.

**Interfaces:**
- Consumes: Safe local repository from Tasks 1–2.
- Produces: Public GitHub repository `ProjetosDeEstudo`, local remote `origin`, and published branch `main`.

- [x] **Step 1: Audit the staging set.** Confirm the existing key, `db.sqlite3`, `.venv`, Python caches, `.env` files, and project README are absent from the set to be committed; do not use an unrestricted add if it would include the local README.
- [x] **Step 2: Run the Django verification** with `DJANGO_SECRET_KEY=test-only-key uv run python manage.py check` from `AgendadorDeTarefas/backend`; stop and report any unrelated project failure rather than silently changing application behavior.
- [x] **Step 3: Check GitHub authentication and repository availability.** Use `gh auth status` and `gh repo view Akemastico/ProjetosDeEstudo`; if unauthenticated or the repository already exists, stop before remote creation and report the blocker.
- [x] **Step 4: Rename the local branch to `main`, stage only the approved files, and create the repository commit.** Verify `git status --short` shows no publishable local artifacts.
- [x] **Step 5: Create the public GitHub remote** named `ProjetosDeEstudo`, set it as `origin`, and push `main`. Do not force-push.
- [x] **Step 6: Verify publication** with `git remote -v`, `git status --short --branch`, and `gh repo view --json name,visibility,url`; expected visibility is `PUBLIC`, branch is `main`, and the worktree has no publishable changes.
