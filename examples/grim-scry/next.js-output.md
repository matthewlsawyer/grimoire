# Example scry run: projects/next.js

| Field | Value |
| --- | --- |
| Target | [next.js](https://github.com/vercel/next.js) |
| Model | Composer 2.5 |
| Ran with | Cursor |
| workspace_data | [next.js-model.yaml](next.js-model.yaml) |

Chat-facing output from a scry of the [next.js](https://github.com/vercel/next.js) repository.

Lenses rendered from the sibling workspace_data [next.js-model.yaml](next.js-model.yaml).

## Directory hierarchy

```text
next.js/ ◀─ pnpm monorepo for the Next.js React framework and related npm packages
├─ packages/ ◀─ Published npm packages
│  ├─ next/ ◀─ Main Next.js framework (published as next)
│  │  └─ src/
│  ├─ create-next-app/ ◀─ create-next-app CLI tool
│  ├─ next-swc/ ◀─ Native Rust SWC bindings
│  ├─ font/ ◀─ next/font implementation
│  ├─ eslint-plugin-next/ ◀─ ESLint rules for Next.js
│  └─ third-parties/ ◀─ Third-party script integrations
├─ turbopack/ ◀─ Turbopack bundler (Rust git subtree)
├─ crates/ ◀─ Rust crates for Next.js SWC bindings
├─ rspack/
├─ test/ ◀─ All test suites
│  ├─ e2e/
│  ├─ development/ ◀─ Dev server tests
│  ├─ production/ ◀─ Production build tests
│  └─ unit/ ◀─ Unit tests (fast, no browser)
├─ examples/ ◀─ Example Next.js applications
├─ docs/ ◀─ Documentation
│  ├─ 01-app/
│  └─ 02-pages/
├─ scripts/ ◀─ Build and maintenance scripts
├─ evals/ ◀─ Agent evals for Next.js
├─ bench/
├─ apps/
├─ errors/
├─ .agents/
└─ .github/
```

## Conceptual hierarchy

```text
pnpm monorepo ◀─ pnpm workspaces spanning packages, turbopack, crates, test, and tooling
├─ packages/
├─ turbopack/
└─ crates/

Next.js framework ◀─ Full-stack React framework published as the next npm package
├─ packages/next/
└─ Turbopack ◀─ Default bundler for next dev and next build

Agent evals ◀─ Sandbox coding-agent fixtures to test Next.js guidance quality
└─ evals/
```

## Workflow hierarchy

```text
Local development
├─▶ pnpm --filter=next dev ◀─ watch build for core Next.js edits
├─▶ pnpm build
└─▶ pnpm build-all ◀─ JS and Rust; bootstrap after branch switch

Integration testing
├─▶ pnpm test-dev-turbo
├─▶ pnpm test-dev-webpack
├─▶ pnpm test-start-turbo
├─▶ pnpm test-start-webpack
└─▶ pnpm test-unit ◀─ fast unit tests, no browser

Quality and scaffolding
├─▶ pnpm lint
├─▶ pnpm types
└─▶ pnpm new-test ◀─ mandatory for new test suites

PR and agent evals
├─▶ node scripts/pr-status.js ◀─ CI failure and review triage
└─▶ pnpm eval

CLI entrypoints
├─▶ next dev ◀─ packages/next/src/cli/next-dev.ts
├─▶ next start ◀─ packages/next/src/cli/next-start.ts
└─▶ next build ◀─ packages/next/src/cli/next-build.ts

Instructions
├─ AGENTS.md ◀─ primary agent instruction
└─ .github/AGENTS.md
```

## Summary

pnpm monorepo for the Next.js React framework and related npm packages. Core framework in `packages/next`; Rust tooling in `turbopack/`, `crates/`, and `packages/next-swc`. Turbopack is the default dev and build bundler.

## Observations

- Very large monorepo; depth-4 reveal still omits most of `examples/` and `turbopack/crates/`.
- `AGENTS.md` is the primary agent instruction surface; `.github/AGENTS.md` mirrors it.
- Turbopack is default bundler; webpack and rspack remain selectable for tests and builds.
- Integration tests are mode- and bundler-specific (dev vs start, turbo vs webpack vs rspack).
- `evals/` runs coding-agent fixtures via `@vercel/agent-eval` and `run-evals.js`.
