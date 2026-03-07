# Exercise Files

Hands-on exercise models for TE Learn content. Each exercise is a PBIP project that learners can open in Power BI Desktop or Tabular Editor.

## Structure

- `starter/` — Starting-point models (what the learner opens)
- `solutions/` — Completed models (expected end state after the exercise)

## Format

**Preferred: TMDL format**
```
exercise-name/
├── exercise-name.pbip
├── exercise-name.SemanticModel/
│   ├── definition/
│   │   ├── model.tmdl
│   │   ├── tables/
│   │   │   ├── Sales.tmdl
│   │   │   └── Date.tmdl
│   │   └── relationships.tmdl
│   └── definition.pbism
└── .gitignore
```

**Alternative: model.bim (TMSL)**
```
exercise-name/
├── exercise-name.pbip
├── exercise-name.SemanticModel/
│   ├── model.bim
│   └── definition.pbism
└── .gitignore
```

## Conventions

- Keep models minimal — only include tables/measures needed for the exercise
- Each exercise `.gitignore` should exclude `.pbi/cache.abf` and `.pbi/localSettings.json`
- Name exercise folders to match the `exercise:` frontmatter field in the corresponding EO
- Use descriptive names (e.g., `contoso-sales-bpa`, not `exercise-3`)
