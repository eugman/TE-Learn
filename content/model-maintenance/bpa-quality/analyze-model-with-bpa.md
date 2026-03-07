---
uid: analyze-model-with-bpa
title: Analyze your Model with BPA
eo_id: MAINT-E01
to_id: MAINT-T01
blooms_level: Analyze
edition_minimum: te3_desktop
prerequisites: []
status: draft
author: emeidinger
updated: 2026-03-07
exercise:
---
# Analyze your Model with BPA

> **Time to learn**: ~15 minutes | **Time saved**: 5-15 minutes per week

## The Problem

Semantic models accumulate quality issues over time — hidden foreign key columns without proper settings, measures missing format strings, unused objects cluttering the model. Finding these manually is tedious and inconsistent.

## The Solution

The Best Practice Analyzer (BPA) scans your entire model against a set of rules and reports every violation. Tabular Editor ships with built-in rules covering the most common issues.

## Step by Step

### Step 1: Open the BPA Pane

<!-- View → Best Practice Analyzer, or the keyboard shortcut -->

### Step 2: Run the Built-In Rules

<!-- Click Analyze, walk through the results -->

### Step 3: Interpret Results and Prioritize Fixes

<!-- Severity levels, grouping by rule, filtering -->

## Key Takeaways

- BPA scans your entire model for quality issues in seconds
- Built-in rules cover common problems (hidden keys, format strings, naming)
- Results are grouped by rule and can be filtered by severity
- Run BPA regularly as part of your development workflow

## Next Steps

- [Apply Quick Fixes with Code Actions and BPA](apply-quick-fixes-code-actions.md)
