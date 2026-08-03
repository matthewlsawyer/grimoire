| Field | Value |
| --- | --- |
| Target | [buildawesome](https://github.com/11ty/buildawesome) |
| Model | Composer 2.5 |
| Ran with | Cursor |
| Prompt | `/grim-forge` |
| Date | 2026-08-02 |

# Grim Forge: Build Awesome (Eleventy)

```text
/Users/matthewlsawyer/Code/buildawesome/HISTORY.md
╞══════════════════◆
│
├─≣ 2026-07-27
│  └─ v4 alpha polish: named export, fixes, dependency bumps.
├─≣ 2026-07-01
│  └─ alpha.10 ships; repo URLs point to 11ty/buildawesome.
├─≣ 2026-06-09
│  └─ Build Awesome rebrand: dual naming, new package, browser rename, alpha.8.
├─≣ 2026-05-15
│  └─ Incremental build queue coalescing and multi-file support.
├─≣ 2025-07-30
│  └─ v4.0.0-alpha.1: monorepo, @11ty/client browser bundle, Vitest.
├─≣ 2024-10-01
│  └─ v3.0.0: ESM migration ships.
├─≣ 2023-02-08
│  └─ v2.0.0: dev server, incremental builds, i18n.
└─≣ 2018-08-14
   └─ v0.5.1 caps year one; core SSG foundation in place.
```

Created `HISTORY.md` from scratch — no prior ledger existed. The file traces the full arc from the 2017 Eleventy prototype through v2/v3 milestones, the v4 alpha and browser-client monorepo work, and the June 2026 Build Awesome rebrand, with eight reverse-chronological timeline entries.

---

## HISTORY.md

```markdown
# History

Build Awesome (Eleventy) is a JavaScript static site generator — a simpler alternative to Jekyll that transforms templates into HTML. This ledger records the project's story arc: from a weekend prototype in 2017, through years of Eleventy growth, into the v4 era and the Build Awesome rebrand.

## Story

Eight years of incremental craft on a beloved SSG, now entering a dual-named v4 alpha under the Build Awesome banner while preserving full Eleventy compatibility.

### Origins

Zach Leatherman started the project in November 2017 as a minimal static site generator (`00ad9192`). Within days it gained subfolder templates, CLI flags, and underscore-prefixed file ignores. By early December the name settled on **Eleventy** (`d041111c`), async rendering landed (`c14f1fa8`), and Liquid became the default data engine. Pagination, the `_data` directory, and multi-engine support (Nunjucks, Handlebars, Pug, EJS, Markdown) followed in rapid succession through 2017–2018, establishing the Jekyll-inspired mental model that would define the project.

## 2026-07-27

Dependency maintenance and API polish on the v4 alpha line. A `{ BuildAwesome }` named export was added alongside the default export (`6d2c04d1`), and assorted fixes landed (`84654019`, `562c399f`). The project remains at **v4.0.0-alpha.10**.

## 2026-07-01

**v4.0.0-alpha.10** shipped (`f77b4cb3`). Issue and release URLs now point to the `11ty/buildawesome` repository (`cf3a830e`), completing the public-facing repo migration started during the June rebrand.

## 2026-06-09

The **Build Awesome** rebrand landed as a compatibility layer over Eleventy (`f60a2a84`). `buildawesome.*` events mirror `eleventy.*`; `BUILDAWESOME_` env vars alias `ELEVENTY_`; config files prefer `buildawesome.config.js`; the data cascade resolves `buildawesome.computed` ahead of `eleventyComputed`. A sibling npm package `@awesome.me/buildawesome` was scaffolded in `packages/build-awesome`, with its own CLI binary and release script (`f25edfc0`). The browser workspace package was renamed from `client` to `browser` (`ebc32647`), Vitest browser tests standardized (`b4dfeeae`), and error classes/methods were renamed for the new identity (`2cf42805`, `792108c2`). **v4.0.0-alpha.8** released mid-month (`9443f0e7`), with separate release tags for Eleventy and Build Awesome (`4bd80df8`) and npm staged publish (`49c2f614`). Async Nunjucks and the new bundle plugin integrated by month-end (`652e4d26`).

## 2026-05-15

Incremental build reliability improved: multiple incremental files per build (`d3c5c261`), smarter queue coalescing when two or more pending changes include non-template files (`d84477af`, `53e13be2`), and SIGINT handling to prevent queued rebuilds after interrupt (`9c84d981`).

## 2025-07-30

**v4.0.0-alpha.1** marked the start of the v4 line (`d53e956c`). The monorepo gained `@11ty/client` — a browser-runnable bundle of the core (`29f34648`, Vitest browser mode) — plus automated release scripting for co-publishing client and core (`9818691d`). Chokidar v4 config-reset bugs were fixed (`e664d230`). Alphas .2–.4 followed through August.

## 2024-10-01

**v3.0.0** shipped (`8675d68e`), completing the ESM migration. Node 18+ required; the codebase moved to `"type": "module"` with dynamic imports for the dev server and a modern dependency tree.

## 2023-02-08

**v2.0.0** released (`05c62633`), a major version after a long canary/beta cycle. Incremental builds, the Eleventy Dev Server (replacing BrowserSync), and I18n support were headline features of the v2 era.

## 2018-08-14

**v0.5.1** (`d4b7b9a8`) capped the frantic first year. By then Eleventy had collections, layouts, permalinks, passthrough copy, and a growing plugin ecosystem — the foundation everything since has built on.
```
