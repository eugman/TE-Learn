# TE-Learn

Source content for Tabular Editor learning materials. Content is authored in Markdown and published to [EasyGenerator](https://www.easygenerator.com/) (primary) and HubSpot (secondary).

## Content

Content lives at the repo root — each top-level folder is a learning group:

```
getting-started/         Install, connect, and orient yourself
dax-authoring/           Write, refactor, test, and debug DAX
model-maintenance/       BPA, quality checks, optimization
scripting-automation/    C# scripts and macros
```

Within each group: **Group → TO folder → EO file** (one markdown file per enabling objective).

## Authoring Workflow

1. Create a new EO file from `_build/templates/eo-template.md`
2. Write content, add images to `media/` folder alongside the EO
3. Set `status: review` when ready for feedback
4. Publish to EasyGenerator via `python _build/scripts/publish_to_easygenerator.py`
5. Set `status: published` after confirming in LMS

## Tooling

Build tooling lives in `_build/` — content editors can ignore it:

```
_build/
  scripts/       Publishing automation (Playwright)
  templates/     Content templates for new EOs
  tests/         Content convention tests
```

## Exercise Files

Exercise models use PBIP format with TMDL (preferred) or model.bim:

- `exercises/starter/` — Starting-point models for learners
- `exercises/solutions/` — Completed exercise models

## Quick Start

```bash
# Install publishing dependencies
pip install playwright markdown
playwright install chromium

# Generate TOC from frontmatter
python _build/scripts/generate_toc.py --write

# Run content convention tests
python -m pytest _build/tests/
```
