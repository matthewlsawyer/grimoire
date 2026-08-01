# History

Grimoire is a spellbook of at-a-glance agent skills — Grim Scry (conceptual shape), Grim Repo (nested git census), and Grim Forge (historical ledger). This file records how the spellbook evolved from a single scry spell into a three-spell toolkit with script-backed evidence and a simplified distill-and-template workflow.

## Story

From a July 2026 rename off "skillit" through hyphenated spell ids, a brief grim-weave experiment, and a July refactor that traded verbose skill contracts for template-driven distill workflows.

### Origins

The repo began July 6, 2026 as a skills collection (`cb12339`), renamed to skillit the next day (`786ce80`) and grimoire on July 8 (`451261f`). Grim Scry arrived July 20 (`a031701`) as the first spell — canonical repo models distilled into session viewports. `install.sh` copied spells into invoking `.agents/skills/` (`0b5c1c5`); README framed spellbook axioms and roadmap (`82c236b`).

## 2026-07-31

Genesis `HISTORY.md` ledger established for the spellbook via grim-forge. Refactor branch merged to `main` (`5939fc2`). All three spells slimmed: shorter headings (`Forge`, `Repo`, `Scry`), report templates for session output, grim-forge drops `status.py` and CHANGELOG contract — HISTORY-only distill via git log (`426c27b`). grim-scry `discover.py` collects ADR dirs and drops `--budget` (`ea7050b`). Examples refreshed for buildawesome, ghostty, and throneroom (`0fe6bc6`, `165dcbe`, `5399f50`); README examples table updated (`65887a4`).

## 2026-07-30

grim-forge gained `status.py` collector capped at 250 commits (`7b1abbf`, `604bdf7`); spell examples and README expanded (`2d0258b`, `4391752`).

## 2026-07-29

grim-forge introduced as provenance spell with CHANGELOG + HISTORY artifacts (`e56d601`). grim-weave dropped (`f4d6db3`); grim-scry and grim-repo scripts trimmed and output clarified (`b3e9c23`).

## 2026-07-27

Spell ids hyphenated: grim-scry, grim-repo (`bdb5838`). grim-weave refactored to flat path stdout (`cbb756b`). README reworked for hyphenated spells (`cd631b4`).

## 2026-07-26

Script layer landed: `census.py` for grim-repo (`074fa77`), `discover.py` for grim-scry (`a550d14`), `weave.py` for grim-weave (`823d28f`). Skills wired to scripts with policy sections (`352b78e`, `fe946a5`, `c78f7eb`). Unittest harness and examples (`453636c`, `e879e92`).

## 2026-07-20 -> 2026-07-22

grim-scry matured: schema/viewport split (`183c279`), ASCII lantern shipped (`bad5b16`), at-a-glance README framing (`a03b5e8`), tailscale and next.js example runs. Scry discover PR merged (`4c3d05e`).
