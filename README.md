# TE-Learn

Source content for Tabular Editor learning materials. Content is authored in Markdown and published to [EasyGenerator](https://www.easygenerator.com/) (primary) and HubSpot (secondary).

## Structure

```
content/           Markdown learning content (Group → TO → EO)
exercises/         PBIP and model.bim files for hands-on exercises
templates/         Content templates for new EOs, TOs, and groups
scripts/           Publishing automation (Playwright)
```

## Content Organization

Content follows the Terminal Objectives (TO) framework from TE-dev-rel:

- **Group** folders represent skill domains (e.g., `authoring-dax/`)
- **TO** subfolders represent terminal objectives (e.g., `debugging-unexpected-dax-results/`)
- **EO** files are individual enabling objectives — the atomic unit of content

Each EO targets a "15 minutes to learn, save 5-15 minutes weekly" value proposition.

## Authoring Workflow

1. Create a new EO file from `templates/eo-template.md`
2. Write content, add images to `media/` folder alongside the EO
3. Set `status: review` when ready for feedback
4. Publish to EasyGenerator via `scripts/publish_to_easygenerator.py`
5. Set `status: published` after confirming in LMS

## Exercise Files

Exercise models use PBIP format with TMDL (preferred) or model.bim:

- `exercises/starter/` — starting-point models for learners
- `exercises/solutions/` — completed exercise models

## Quick Start

```bash
# Install publishing dependencies
pip install playwright markdown
playwright install chromium
```
