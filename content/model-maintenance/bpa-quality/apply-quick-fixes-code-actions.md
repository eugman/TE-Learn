---
uid: apply-quick-fixes-code-actions
title: Applying Quick Fixes with Code Actions and BPA
eo_id: MAINT-E02
to_id: MAINT-T01
blooms_level: Apply
edition_minimum: te3_desktop
prerequisites:
  - analyze-model-with-bpa
status: draft
author: emeidinger
updated: 2026-03-07
exercise:
---
# Applying Quick Fixes with Code Actions and BPA

> **Time to learn**: ~15 minutes | **Time saved**: 5-15 minutes per week

## The Problem

You've run BPA and found dozens of violations. Fixing them one by one — clicking each object, finding the right property, making the change — is slow and repetitive.

## The Solution

Many BPA rules have auto-fix actions built in. Code Actions (the lightbulb menu) also offer quick fixes for common issues directly in the DAX editor. Together, they let you resolve violations in seconds instead of minutes.

## Step by Step

### Step 1: Auto-Fix from BPA Results

<!-- Right-click a violation → Apply Fix, or select multiple → Apply Fix -->

### Step 2: Use Code Actions in the DAX Editor

<!-- Lightbulb icon, Ctrl+. to trigger, walk through available actions -->

### Step 3: Managing Rule Suppressions

<!-- When a violation is intentional — how to suppress without ignoring -->

## Key Takeaways

- Many BPA violations can be auto-fixed with a single click
- Select multiple violations to batch-fix them at once
- Code Actions (Ctrl+.) offer inline fixes while editing DAX
- Suppress intentional violations rather than ignoring the rule entirely

## Next Steps

- [Apply Bulk Fixes with BPA and C# Scripts](apply-bulk-fixes-bpa-scripts.md)
