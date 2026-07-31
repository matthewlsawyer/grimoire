# HISTORY.md Template

A temporal ledger that captures the story arc of a project through thematic eras.

## Structure

```markdown
# History

{What this project is and why this file exists.}

## Story

{One-liner about the story so far.}

### Origins

{How or why this project was started; a distilled origin story.}

## {YYYY-MM-DD}

{Timeline Entry}

## ...
```

## Rules

- **Timeline entries** capture story beats since last run, how this project has evolved, turning points, large refactors, and provenance that led decisions. Appended to on each skill run using reverse chronological (`YYYY-MM-DD`) headings. Optionally use era date ranges in prose (`2026-06 -> 2026-07`). Link to CHANGELOG entries for _what changed_ and link to ADR files for _how it changed_.
- **Keep the timeline tight**. Skip a timeline entry when narrative adds no temporal context.
- **Human-readable**.
- **Succinct**.
