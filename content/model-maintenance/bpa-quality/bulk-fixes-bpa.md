---
uid: bulk-fixes-bpa
order: 3
title: Applying Bulk Fixes with BPA and C# Scripts
eo_id: MAINT-E02b
to_id: MAINT-T01
blooms_level: Apply
edition_minimum: te3_desktop
prerequisites:
  - quick-fixes-code-actions
status: draft
author: emeidinger
updated: 2026-03-07
exercise:
---
# Applying Bulk Fixes with BPA and C# Scripts

> **Time to learn**: ~15 minutes | **Time saved**: 5-15 minutes per week

## The Problem

Some BPA violations can't be auto-fixed — or you need to apply a fix across dozens of objects with specific logic (e.g., set format strings based on measure name patterns). Doing this manually is error-prone at scale.

## The Solution

Combine BPA to identify the violations with a short C# script to fix them in bulk. Tabular Editor's scripting API gives you access to every model object, so you can write targeted fix-it scripts.

## Step by Step

### Step 1: Identify the Pattern from BPA Results

<!-- Use BPA to find all violations of a specific rule -->

### Step 2: Write a C# Script to Fix in Bulk

<!-- Simple script example: iterate matching objects, apply the fix -->

### Step 3: Verify with BPA Re-Run

<!-- Run BPA again to confirm violations are resolved -->

## Key Takeaways

- BPA identifies the problems; C# scripts fix them at scale
- Even simple scripts (5-10 lines) can fix hundreds of objects at once
- Always re-run BPA after applying scripts to verify the fix
- Save useful scripts as macros for reuse (see: Working Faster with C# Macros)

## Next Steps

- [Understanding the DAX Debugger](../../dax-authoring/dax-debugging/understanding-dax-debugger.md)
