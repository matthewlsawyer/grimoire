| Field | Value |
| --- | --- |
| Target | [ghostty](https://github.com/ghostty-org/ghostty) (`/Users/matthewlsawyer/Code/test_4/ghostty`) |
| Model | Composer |
| Ran with | Cursor |
| Prompt | `/grim-weave zig` |
| Token | `zig` (concept; weave script `token_kind`: symbol) |
| Runtime | ~10s (weave evidence + closed-set reads) |
| Date | 2026-07-26 |

# Grim Weave: zig

Zig is Ghostty’s primary language and build system: the shared core, `build.zig` orchestration, and pinned toolchain in `build.zig.zon`.

```text
zig
├─ⓘ Primary implementation language and `zig build` entry for the repo
╞══════════════════◆
│
├─≣ Definition
│  ├─ build.zig
│  │  └─ⓘ `build()` root; `requireZig(minimum_zig_version)`; steps run/test/lib-vt/translations
│  ├─ build.zig.zon
│  │  └─ⓘ `.minimum_zig_version` (0.16.0); Zig package deps (libxev, zig_objc, …)
│  └─ src/
│     └─ⓘ Shared Zig core (named in AGENTS.md; `**/*.zig` in CI path filters)
│
├─≣ Relationships
│  ├─ Depends On
│  │  ├─ buildpkg (`src/build/main.zig` via `@import`)
│  │  ├─ build.zig.zon (version + dependencies)
│  │  └─ zig-out / .zig-cache (artifact dirs; gitignored)
│  │
│  └─ Referenced By
│     ├─ CMakeLists.txt (`zig build -Demit-lib-vt`; `zig` on PATH)
│     ├─ .github/workflows/test.yml (zig-fmt, build-examples-zig, `**/*.zig`)
│     ├─ HACKING.md / AGENTS.md (`zig build`, `zig fmt`, test filters)
│     └─ README.md (libghostty as C and Zig library)
│
├─≣ Provenance
│  ├─ Commits
│  │  └─ ./
│  │     ├─● 4c7252 Update VOUCHED list (#13437)
│  │     ├─● d65cb5 build: link libghostty-vt on Apple hosts with native linker
│  │     └─● d97a57 ci: test with Xcode 27
│  │
│  └─ Documents
│     ├─ AGENTS.md
│     ├─ HACKING.md
│     ├─ PACKAGING.md
│     └─ README.md
│
└─≣ Threads
   ├─▶ build.zig.zon
   ├─▶ minimum_zig_version
   └─▶ libghostty-vt
```

# Summary

In this workspace, **zig** names both the language of the large **`src/`** tree and the **build system** centered on **`build.zig`**, which enforces **`minimum_zig_version`** from **`build.zig.zon`** (currently **0.16.0**) and exposes the everyday steps documented in **AGENTS.md** and **HACKING.md** (`zig build`, `zig build test`, `zig fmt`, lib-vt and WASM variants). CI and packaging treat Zig as the source of truth for compilation while **CMake** wraps **`zig build -Demit-lib-vt`** for downstream C consumers who still need **`zig` on PATH**. Evidence hit caps; the closed path set is mostly root build metadata and workflows, not individual `.zig` modules.

Good follow-ups: `/grim-weave build.zig.zon`, `/grim-weave minimum_zig_version`, or `/grim-weave libghostty-vt`.
