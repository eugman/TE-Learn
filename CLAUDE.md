# TE-Learn Project Guidelines

## This Project

Markdown source content for Tabular Editor learning materials (TE Learn). Content is organized as Group → Terminal Objective (TO) → Enabling Objective (EO) and published to EasyGenerator LMS.

### Related Repositories

| Location | Purpose |
|----------|---------|
| `C:\Users\eugme\Documents\GitHub\TE-dev-rel` | Dev rel tooling, terminal objectives data, content analysis |
| `C:\Users\eugme\Documents\GitHub\TE-dev-rel\data\terminal_objectives.json` | Canonical TO/EO definitions (v3.0) |
| `C:\Users\eugme\Documents\GitHub\TabularEditorDocs` | Official TE docs (fork worktrees) |

### Content Conventions

- **One file per EO** — the atomic unit of content
- **Frontmatter is required** — see `templates/eo-template.md` for schema
- **uid = filename** (sans .md) — kebab-case, human-readable slug
- **eo_id/to_id in frontmatter only** — folder names are human-readable, never codes
- **Images** go in `media/` subfolder within the TO folder
- **Status field**: `draft | review | published`

### Folder Naming

Group and TO folders use human-readable kebab-case names, not ID codes:
- `getting-started/` not `INTRO/`
- `authoring-dax/` not `DAX/`

### Exercise Files

- Prefer TMDL format (separate files per table/measure) over model.bim
- Each exercise has a `.gitignore` excluding `.pbi/cache.abf` and `.pbi/localSettings.json`
- `exercises/starter/` = what learner opens; `exercises/solutions/` = expected end state

### Publishing

- Primary target: EasyGenerator (no API — use Playwright automation in `scripts/`)
- Secondary target: HubSpot (no KB API — manual or browser automation)
- Run: `python scripts/publish_to_easygenerator.py --eo <uid>`

### Commands

| Task | Command |
|------|---------|
| Publish single EO | `python scripts/publish_to_easygenerator.py --eo <uid>` |
| List unpublished | `grep -rl "status: draft" content/` |
| List ready for review | `grep -rl "status: review" content/` |

## Environment

- **OS**: Windows. Use Git Bash with forward slashes.
- **Python**: Use venv if adding dependencies.
