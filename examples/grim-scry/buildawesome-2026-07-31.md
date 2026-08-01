| Field | Value |
| --- | --- |
| Target | [buildawesome](https://github.com/11ty/buildawesome) |
| Model | Composer 2.5 |
| Ran with | Cursor |
| Prompt | `/grim-scry` |
| Date | 2026-07-31 |

# Grim Scry: Build Awesome (Eleventy)

A JavaScript static site generator that transforms templates (HTML, Markdown, Liquid, Nunjucks, and more) into HTML — the Eleventy project, rebranded under `@awesome.me/buildawesome` while retaining `@11ty/eleventy` compatibility.

```text
buildawesome/
├─ⓘ Eleventy 4 alpha; Node ≥22.15; npm workspaces monorepo
╞══════════════════◆
│
├─≣ Core SSG
│  ├─ⓘ Template pipeline, engines, plugins, CLI
│  ├─ src/
│  │  ├─ Core.js
│  │  ├─ Engines/
│  │  ├─ Plugins/
│  │  └─ Template.js
│  └─ cmd.cjs
│     └─▶ eleventy
│
├─≣ Workspace packages
│  ├─ packages/build-awesome/
│  │  ├─ⓘ @awesome.me/buildawesome — new brand, depends on root
│  │  └─▶ buildawesome
│  └─ packages/browser/
│     ├─ⓘ @11ty/client — browser-friendly bundles (md, njk, liquid, i18n)
│     └─ packages/browser/test/
│
├─≣ Tests
│  ├─ test/
│  │  ├─ⓘ Primary suite — ava
│  │  └─▶ npm run test:ava
│  ├─ test_node/
│  │  ├─ⓘ Secondary — Node test runner (tsx / MDX worker workaround)
│  │  └─▶ npm run test:node
│  └─▶ npm test
│
├─≣ Docs & CI
│  ├─ docs/
│  └─ .github/
│
└─≣ Agent skills
   └─ .agents/skills/
      ├─ grim-scry/
      ├─ grim-forge/
      └─ grim-repo/
```

# Summary

The repo owns the full Eleventy static-site pipeline: core build logic in `src/`, a CLI (`cmd.cjs` / `eleventy`), and two workspace packages — a rebranded `@awesome.me/buildawesome` wrapper and `@11ty/client` for browser use. Quality is enforced through three test runners (ava, Node test, Vitest browser mode) plus GitHub Actions CI.

Observations:

- **Dual branding**: root publishes as `@11ty/eleventy` while `packages/build-awesome` ships `@awesome.me/buildawesome` with a `buildawesome` binary, both sharing the same core.
- **Test strategy is layered by runtime** — ava for the bulk of integration tests, Node's runner for MDX/tsx edge cases, Vitest for browser bundles.
- **`.agents/skills/`** hosts grim-* tooling (scry, forge, repo) for workspace introspection and history — separate from the SSG itself.
