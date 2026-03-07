---
uid: navigate-complex-dax-peek-goto
title: Navigating Complex DAX with Peek, Go To, and Inline Definition
eo_id: DAX-E01
to_id: DAX-T01
blooms_level: Apply
edition_minimum: te3_desktop
prerequisites: []
status: draft
author: emeidinger
updated: 2026-03-07
exercise:
---
# Navigating Complex DAX with Peek, Go To, and Inline Definition

> **Time to learn**: ~15 minutes | **Time saved**: 5-15 minutes per week

## The Problem

When working with complex models containing dozens or hundreds of measures, understanding how measures reference each other becomes a challenge. You find yourself scrolling through the TOM Explorer, searching for referenced measures, and losing your place constantly.

## The Solution

Tabular Editor 3's DAX editor includes VS Code-style code navigation features — Peek Definition, Go to Definition, and Inline Definition — that let you trace through measure dependencies without leaving your current context.

## Step by Step

### Step 1: Go to Definition

<!-- Ctrl+Click or F12 on a measure reference to jump to its definition -->

### Step 2: Peek Definition

<!-- Alt+F12 to open an inline peek window without navigating away -->

### Step 3: Inline Definition

<!-- Show how inline definition lets you edit the referenced measure in-place -->

## Key Takeaways

- Use **F12** (Go to Definition) to jump to a referenced measure
- Use **Alt+F12** (Peek Definition) to view a measure without losing your place
- These features work for measures, columns, tables, and other DAX references
- Combine with **Ctrl+-** (Go Back) to return to where you were

## Next Steps

- [Working Faster with Intro Hotkeys](../../getting-started/exploring-models/working-faster-te-hotkeys.md)
