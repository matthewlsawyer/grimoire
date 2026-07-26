| Field | Value |
| --- | --- |
| Target | [ghostty](https://github.com/ghostty-org/ghostty) (local workspace) |
| Model | Composer 2.5 |
| Ran with | Cursor |
| Prompt | `/grimweave zig` |
| Token | `zig` (concept) |
| Runtime | ~12s (docs/build grep + reads) |
| Date | 2026-07-26 |

# Grim Weave: zig

Zig is Ghostty’s implementation language and its primary build/test driver; macOS app packaging is the main exception.

```text
zig
├─ⓘ Language + build system; `src/` core and root `zig build` orchestration
╞══════════════════◆
│
├─≣ Definition
│  ├─ build.zig
│  │  ├─ minimum_zig_version ← build.zig.zon
│  │  └─ buildpkg.requireZig (comptime)
│  ├─ build.zig.zon
│  │  └─ .minimum_zig_version = "0.16.0"
│  ├─ src/build/
│  │  └─ⓘ Config, steps, GhosttyZig modules (via buildpkg)
│  └─ src/
│     └─ⓘ Shared Zig core (AGENTS.md)
│
├─≣ Relationships
│  ├─ Depends On
│  │  ├─ Zig toolchain (released version pinned in build.zig.zon)
│  │  ├─ build.zig.zon dependencies (libxev, zig_objc, …)
│  │  └─ zig-out/ artifacts
│  │
│  └─ Referenced By
│     ├─ AGENTS.md
│     │  └─ zig build | test | fmt | libghostty-vt flags
│     ├─ HACKING.md
│     │  └─ zig build run, test, dist, valgrind, …
│     ├─ PACKAGING.md
│     │  └─ zig build for downstream packagers
│     ├─ example/
│     │  └─ zig build run (C API examples use Zig build, not C toolchain alone)
│     ├─ test/fuzz-libghostty/
│     ├─ src/benchmark/AGENTS.md
│     └─ macos/AGENTS.md
│        └─ⓘ zig build -Demit-macos-app=false for core; app via build.nu
│
├─≣ Provenance
│  ├─ Commits
│  │  ├─● e8525c0 Update to Zig 0.16.0
│  │  ├─● f2a7652 mitchell's touchups
│  │  └─● b513f1b deps: Update iTerm2 color schemes
│  │
│  └─ Documents
│     ├─ AGENTS.md
│     ├─ HACKING.md
│     ├─ PACKAGING.md
│     └─ example/README.md
│
└─≣ Threads
   ├─▶ build.zig.zon
   ├─▶ GhosttyZig
   ├─▶ test-lib-vt
   └─▶ example/zig-vt
```

# Summary

In Ghostty, **zig** names both the language of the shared core (`src/`) and the default developer interface: `build.zig` / `build.zig.zon` pin the compiler (currently **0.16.0**) and wire app, tests, libghostty-vt, fuzz, and bench steps. Continue with `/grimweave build.zig.zon` or `/grimweave GhosttyZig` for the build graph, or `/grimweave test-lib-vt` for the VT test slice.
