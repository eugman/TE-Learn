---
uid: metadata-only-editing
order: 2
title: Saving Time and Avoiding Mistakes with Metadata-only Editing
eo_id: TBD
to_id: INTRO-T02
blooms_level: Understand
edition_minimum: te3_desktop
prerequisites: []
status: draft
author: emeidinger
updated: 2026-03-07
exercise:
---
# Saving Time and Avoiding Mistakes with Metadata-only Editing

> **Time to learn**: ~15 minutes | **Time saved**: 5-15 minutes per week

## The Problem

In Power BI Desktop, every change to a measure triggers a full model validation — even if you're just renaming a folder or fixing a typo in a description. On large models this can mean waiting seconds or minutes between each small edit.

## The Solution

Tabular Editor works with model metadata directly. It doesn't validate the entire model on every DAX change, so edits are instant. Combined with full undo/redo (Ctrl+Z), you can make dozens of changes confidently and only deploy when ready.

## Step by Step

### Step 1: Understanding Metadata-only Mode

<!-- Explain how TE edits the TOM metadata without re-evaluating DAX -->

### Step 2: Making Rapid Edits with Undo/Redo

<!-- Demo Ctrl+Z behavior — show how every property change is undoable -->

### Step 3: Batch Editing Without Validation Overhead

<!-- Show editing multiple measures in sequence, no wait between edits -->

## Key Takeaways

- Tabular Editor edits metadata directly — no full model validation per change
- **Ctrl+Z** undoes any change, including property edits, renames, and deletes
- This makes Tabular Editor dramatically faster for bulk editing tasks
- Changes are only applied to the model when you explicitly save/deploy

## Next Steps

- [Analyzing Your Model with Best Practice Analyzer](../../model-maintenance/bpa-quality/analyze-model-with-bpa.md)
