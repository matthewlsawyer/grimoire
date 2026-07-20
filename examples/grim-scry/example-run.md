# Example scry run: vercel/next.js

| Field | Value |
| --- | --- |
| Target | [vercel/next.js](https://github.com/vercel/next.js) |
| Model | GPT-5.4 Nano Medium |
| workspace_data | [example-workspace-data.yaml](example-workspace-data.yaml) |

Chat-facing output from a scry of that repo. Lenses render from the sibling workspace_data example; model not re-embedded here.

## Directory hierarchy

```text
next.js/
├─ packages/ -> Published npm packages (including core `next`)
├─ turbopack/ -> Turbopack bundler (Rust) subtree
├─ crates/ -> Rust crates (SWC bindings)
├─ test/ -> Test suites across modes
├─ examples/ -> Example Next.js applications
├─ docs/ -> Documentation
└─ scripts/ -> Build and maintenance scripts
```

## Conceptual hierarchy

```text
next.js
└─ Monorepo -> pnpm workspaces that ship Next.js and related packages
   ├─ Core Next.js package -> The main `next` framework package (and its CLI entrypoints)
   │  └─ packages/ -> Published npm packages (including core `next`)
   ├─ Bundler & runtime tooling -> Turbopack (default) plus Rust-based JS tooling
   │  └─ turbopack/ -> Turbopack bundler (Rust) subtree
   └─ Build / Dev / Test workflow -> Documented dev, build, and test pipelines with mode-specific commands
      ├─ scripts/ -> Build and maintenance scripts
      └─ test/ -> Test suites across modes
```

## Workflow hierarchy

```text
next.js
├─ AGENTS.md
│  ├─ uses ─▶ dev (watch): `pnpm --filter=next dev`
│  ├─ uses ─▶ build-all: `pnpm build-all`
│  └─ uses ─▶ test-dev-turbo: `pnpm test-dev-turbo test/path/to/test.ts`
├─ `pnpm --filter=next dev` ─▶ next dev server (packages/next/src/cli/next-dev.ts)
├─ `pnpm build-all` ─▶ next build (packages/next/src/cli/next-build.ts)
├─ `pnpm test-dev-turbo test/path/to/test.ts` (depends on `pnpm --filter=next dev`) ─▶ next dev server (packages/next/src/cli/next-dev.ts)
└─ .github/workflows/build_and_test.yml
```

## Summary

A pnpm monorepo for the Next.js framework and related packages, including the core `next` package, the Turbopack bundler, Rust/SWC bindings, test suites, examples, and build/maintenance scripts.

## Observations

- `AGENTS.md` documents the monorepo layout and the core CLI entrypoints for dev/build/start.
- The root `package.json` scripts expose mode-specific commands (e.g. `test-dev-turbo`, `test-start-*`) and `build-all` pipelines.
- Turbopack is called out as the default bundler for both `next dev` and `next build`.
- The workflow surface is centralized around `packages/next/src/cli/` entrypoints and scripts in `package.json` / `scripts/`.
- CI is configured via `.github/workflows/build_and_test.yml` (build + test automation).
