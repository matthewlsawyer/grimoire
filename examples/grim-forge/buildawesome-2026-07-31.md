| Field | Value |
| --- | --- |
| Target | [buildawesome](https://github.com/11ty/buildawesome) |
| Model | Composer 2.5 |
| Ran with | Cursor |
| Prompt | `/grim-forge` |
| Date | 2026-07-31 |

# Grim Forge: Build Awesome (Eleventy)

```text
buildawesome/HISTORY.md
╞══════════════════◆
│
├─≣ 2026-07-31
│  └─ First grim-forge run; ledger created from ~3,700 commits.
├─≣ 2026-07-27
│  └─ Dependency upgrades, BuildAwesome export, fix #4325 on alpha.10.
├─≣ 2026-07-01
│  └─ v4.0.0-alpha.10; repo pointers to 11ty/buildawesome.
├─≣ 2026-06-09 -> 2026-06-11
│  └─ Build Awesome alias layer and packages/build-awesome workspace.
├─≣ 2026-06-05
│  └─ packages/client renamed to packages/browser.
├─≣ 2026-06-17 -> 2026-06-30
│  └─ Alpha.8–10 arc: dual release tags, async Nunjucks bundle plugin.
├─≣ 2025-07-30
│  └─ v4.0.0-alpha.1 — ESM-first major, @11ty/client browser package.
├─≣ 2024-10-01
│  └─ v3.0.0 third major release.
├─≣ 2023-02-08
│  └─ v2.0.0 second major release.
├─≣ 2022-01-08
│  └─ v1.0.0 first stable semver.
└─≣ 2017-11-26
   └─ Genesis — Jekyll-alternative SSG in JavaScript.
```

Created `HISTORY.md` at the repo root — first ledger run, no prior file. It covers genesis (2017), the v1→v2→v3 major arcs, the v4 alpha and ESM/browser monorepo pivot (2025), the Build Awesome rebranding layer (2026-06), and recent alpha.10 maintenance through July 2026. Commit hashes are inlined as provenance on each beat.

---

## HISTORY.md

```markdown
# History

Eleventy (Build Awesome) is a JavaScript static site generator — templates in many formats become HTML. This ledger records how the project evolved from a one-person experiment into a dual-branded monorepo shipping `@11ty/eleventy`, `@awesome.me/buildawesome`, and `@11ty/client`.

## Story

From a November 2017 Jekyll alternative to a mature SSG with browser bundles and a parallel Build Awesome brand, through four major semver arcs and a long v4 alpha.

### Origins

Zach Leatherman started Eleventy in late 2017 as a simpler static site generator in JavaScript (`00ad9192`). Within weeks it gained subfolder templates, CLI flags, and a pivotal December refactor that introduced asynchronous template rendering and Liquid support (`c14f1fa8`) — the architectural shape that would carry through every later version.

## 2026-07-31

First grim-forge ledger run. No prior `HISTORY.md`; this file distills ~3,700 commits from genesis through current HEAD.

## 2026-07-27

Maintenance beat on `4.0.0-alpha.10`: dependency upgrades (`17210371`), `{ BuildAwesome }` named export on the build-awesome package (`6d2c04d1`), and fix for #4325 (`84654019`).

## 2026-07-01

`v4.0.0-alpha.10` (`f77b4cb3`) and repository pointers moved to `11ty/buildawesome` (`cf3a830e`). Alpha.9 shipped the same day with bundle dep and devdep prep (`9146d8ff`, `6c1d3639`).

## 2026-06-09 -> 2026-06-11

Build Awesome branding layer landed as backward-compatible aliases atop Eleventy: `buildawesome.*` events mirror `eleventy.*`, `BUILDAWESOME_` env aliases `ELEVENTY_`, `buildawesome.config.js` config file, data-cascade `buildawesome.computed`, and `buildawesome` global data (`f60a2a84` through `1c6ae1ef`). `packages/build-awesome` workspace package introduced with its own release script and debug prefix (`f25edfc0`, `a779d77b`). Repo name settled as `buildawesome` without a dash (`9b2d6191`).

## 2026-06-05

`packages/client` renamed to `packages/browser` (`ebc32647`); Vitest browser-mode tests standardized on "browser" naming (`b4dfeeae`).

## 2026-06-17 -> 2026-06-30

Alpha.8 (`9443f0e7`) through alpha.10 prep: separate release tags for Eleventy vs Build Awesome (`4bd80df8`), async Nunjucks with new bundle plugin (#4305, `652e4d26`), schema-error messaging refactor (`efe2bec9`), and `*_SKIP_BUNDLE_PLUGIN` for test isolation (`56946223`).

## 2025-07-30

`v4.0.0-alpha.1` (`d53e956c`) — major semver bump after years on v3. ESM-first codebase, Node ≥22, `@11ty/client` browser package with Vitest browser mode, and monorepo workspaces (`packages/browser`, `packages/build-awesome`). Alpha.2–4 followed through August–October 2025.

## 2024-10-01

`v3.0.0` (`8675d68e`) — third major release; continued template-engine expansion and ecosystem maturity on the v3 line through `v3.1.6`.

## 2023-02-08

`v2.0.0` (`05c62633`) — second major arc; breaking changes and architectural hardening from the v1 era.

## 2022-01-08

`v1.0.0` (`c8741c00`) — first stable semver release, ~four years after genesis.

## 2017-11-26

Initial commit (`00ad9192`). Eleventy exists to transform a directory of templates into HTML — "a simpler static site generator, an alternative to Jekyll."
```
