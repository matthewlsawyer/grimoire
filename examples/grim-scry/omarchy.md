| Field | Value |
| --- | --- |
| Target | [omarchy](https://github.com/basecamp/omarchy) |
| Model | Composer 2.5 |
| Ran with | Cursor |
| Date | 2026-07-24 |

# Scry Lantern

Opinionated Arch-based desktop distro: Hyprland compositor, one Quickshell `omarchy-shell`, and an `omarchy-*` CLI over install/config/themes and pluginized UI.

```text
Omarchy
├─ⓘ Beautiful, modern & opinionated Linux (DHH); omarchy.org; MIT
╞══════════════════◈
├─ Product surface
│  ├─ default/omarchy-skill/SKILL.md
│  │  └─ⓘ End-user ~/.config customization; not source dev
│  └─ README.md
│
├─ Contributor guidance
│  └─ AGENTS.md
│     ├─ⓘ omarchy-* commands; metadata in bin/; $OMARCHY_PATH
│     ├─ install/ · config/ · themes/ · migrations/
│     ├─▶ ./test/all
│     ├─▶ ./test/cli
│     ├─▶ ./test/shell
│     └─▶ omarchy-restart-shell
│
├─ Omarchy shell
│  ├─ shell/README.md
│  │  ├─ⓘ Single long-running Quickshell; Hyprland autostart
│  │  ├─ shell.qml · services/ · plugins/
│  │  ├─ ~/.config/omarchy/shell.json
│  │  ├─▶ omarchy-shell shell ping
│  │  ├─▶ omarchy plugin add
│  │  └─▶ omarchy plugin update
│  │
│  ├─ shell/plugins/README.md
│  │  └─ⓘ First-party manifest.json plugins (bar, panels, services, …)
│  │
│  ├─ shell/plugins/bar/README.md
│  │  ├─ⓘ omarchy.bar; layout in shell.json
│  │  └─▶ omarchy bar plugin add
│  │
│  └─ shell/plugins/panels/tailscale/README.md
│     ├─ⓘ omarchy.tailscale bar-widget
│     └─▶ omarchy bar plugin add omarchy.tailscale
│
└─ User CLI (from shipped skill)
   ├─▶ omarchy commands
   ├─▶ omarchy refresh
   ├─▶ omarchy theme set
   └─▶ omarchy update
```

---

# Summary

[Omarchy](https://github.com/basecamp/omarchy) is Basecamp’s opinionated Linux desktop stack: Arch underneath, Hyprland for the compositor, and a single **Quickshell** process (`shell/`) that hosts the bar, menus, overlays, panels, and headless services as **manifest-driven plugins**. User-facing behavior is exposed through the **`omarchy` router** and many `omarchy-*` helpers (themes, refresh, capture, packages, setup, updates); shipped defaults live under `config/` and `themes/`, with install/finalization leaves under `install/` and per-user migrations under `migrations/`. **`AGENTS.md`** is the repo’s engineering contract (bash style, command metadata, tests, visual verification, shell IPC). The bundled **`default/omarchy-skill`** targets **installed-system customization** in `~/.config/`, not hacking `/usr/share/omarchy/`.

**Observations:**

- The shell is deliberately **one process**: panels and menus are **summoned via IPC** (`bin/omarchy-shell` → `shell` target) instead of spawning extra Quickshell instances.
- **Customization splits cleanly**: end users edit `~/.config/` and `shell.json`; first-party QML under `shell/plugins/` is cloned to `~/.config/omarchy/plugins/` when users need forks.
- **Third-party shell plugins** are git checkouts with interactive `omarchy plugin` flows; they run **unsandboxed** inside `omarchy-shell`, so the installer emphasizes review before enable.
