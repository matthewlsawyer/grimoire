# Example scry run: vercel/next.js

| Field | Value |
| --- | --- |
| Target | [vercel/next.js](https://github.com/vercel/next.js) |
| Model | Composer 2.5 |
| workspace_data | [example-workspace-data.yaml](example-workspace-data.yaml) |

Chat-facing output from a scry of that repo (run in Composer 2.5). Lenses render from the sibling workspace_data example; model not re-embedded here.

## Directory hierarchy

```text
next.js/
├─ packages/ -> Published npm packages (core `next` and siblings)
│  └─ next/
├─ turbopack/ -> Turbopack bundler (Rust) subtree
├─ rspack/ -> Rspack bundler integration (alternate)
├─ crates/ -> Rust crates for Next.js / SWC bindings
├─ test/ -> Integration and mode-matrix test suites
├─ examples/ -> Example Next.js applications
├─ docs/ -> Product documentation (app/pages/architecture)
├─ scripts/ -> Build and maintenance scripts
├─ .agents/skills/ -> Contributor agent skills
└─ skills/ -> Product adoption agent skills
```

## Conceptual hierarchy

```text
next.js
└─ Monorepo -> pnpm workspaces plus Cargo workspace shipping Next.js
   ├─ Core Next.js package -> Main `next` framework and CLI entrypoints
   │  └─ next/
   ├─ Bundler tooling -> Turbopack default; Webpack and Rspack still selectable
   │  ├─ turbopack/
   │  └─ rspack/
   ├─ Native / SWC layer -> Rust crates and NAPI bindings behind transforms
   │  └─ crates/
   └─ Dev / build / test loop -> Watch build, mode-specific tests, full bootstrap builds
      ├─ scripts/
      └─ test/
```

## Workflow hierarchy

```text
next.js
├─ AGENTS.md
│  ├─▶ pnpm --filter=next dev
│  │  └─▶ next-dev
│  ├─▶ pnpm build-all
│  │  └─▶ next-build
│  └─▶ pnpm test-dev-turbo
│     ├─▶ next-dev
│     └─ depends_on -> pnpm --filter=next dev
└─ build_and_test (.github/workflows/build_and_test.yml)
   └─▶ pnpm build-all
      └─▶ next-build
```

## Summary

A pnpm + Cargo monorepo for the Next.js framework: core `next` package, Turbopack (default bundler), Rust/SWC bindings, tests, examples, docs, and contributor agent skills / CI automation.

## Observations

- AGENTS.md is the primary contributor map; CLAUDE.md symlinks to it.
- Turbopack is the default bundler for `next dev` and `next build`; Webpack/Rspack remain selectable.
- Core CLI lives under `packages/next/src/cli/` (`next-dev`, `next-build`, `next-start`).
- Dev loop favors `pnpm --filter=next dev` plus mode-specific `test-*-turbo|webpack|rspack` scripts.
- Dual skill surfaces: `.agents/skills/` (contributor) and root `skills/` (product adoption).
- CI hub workflow is `.github/workflows/build_and_test.yml` on canary push and PRs.
