| Field | Value |
| --- | --- |
| Target | [omarchy](https://github.com/basecamp/omarchy) |
| Model | Composer 2.5 |
| Ran with | Cursor |
| Prompt | `/grim-scry https://github.com/basecamp/omarchy` |
| Runtime | 19s including git clone |
| Date | 2026-07-24 |

# Grim Scry: Omarchy

Opinionated Arch Linux desktop (Hyprland + Quickshell shell) shipped as a git-managed system tree with a unified `omarchy` CLI and plugin-hosted UI.

```text
Omarchy
├─ⓘ Arch + Hyprland distro; runtime via $OMARCHY_PATH (uwsm session)
╞══════════════════◆
├─ CLI
│  ├─ bin/omarchy
│  │  └─ⓘ Routes omarchy-*; GROUP_DESCRIPTIONS is authoritative
│  ├─ bin/
│  │  └─ⓘ # omarchy: metadata in first 80 lines (group, summary, args, ...)
│  └─▶ omarchy commands
│     └─ⓘ Discovery for users and agents
│
├─ Omarchy shell
│  ├─ shell/
│  │  ├─ shell.qml
│  │  ├─ services/
│  │  │  ├─ PluginRegistry.qml
│  │  │  └─ BarWidgetRegistry.qml
│  │  └─ plugins/
│  │     ├─ bar/
│  │     ├─ panels/
│  │     ├─ menu/
│  │     └─ ...
│  ├─ⓘ One Quickshell process per session; Hyprland autostart quickshell -p
│  ├─▶ omarchy-shell shell ping
│  ├─▶ omarchy-restart-shell
│  └─▶ omarchy plugin add | update | clone
│
├─ Bar & widgets
│  ├─ shell/plugins/bar/
│  ├─ shell/plugins/panels/
│  │  └─ tailscale/
│  │     └─ⓘ omarchy.tailscale bar-widget + panel
│  └─▶ omarchy bar plugin add
│
├─ Config & themes
│  ├─ config/
│  │  └─ⓘ Defaults copied to ~/.config/
│  ├─ default/themed/*.tpl
│  ├─ themes/*/colors.toml
│  └─▶ omarchy-refresh-config
│
├─ Install & upgrade
│  ├─ install/
│  ├─▶ omarchy-setup-system
│  ├─▶ omarchy-setup-hardware
│  ├─▶ omarchy-finalize-user
│  └─▶ omarchy-upgrade-to-quattro
│
├─ Migrations
│  ├─ migrations/
│  └─▶ omarchy-migrate
│
├─ Quality
│  ├─▶ ./test/all
│  ├─▶ ./test/cli
│  └─▶ ./test/shell
│
├─ End-user skill
│  └─ default/omarchy-skill/SKILL.md
│     └─ⓘ ~/.config customization; not source dev
│
└─ Guidance
   └─ AGENTS.md
      └─ⓘ Bash style, helpers, shell IPC, acceptance via omarchy-iso
```

# Summary

[basecamp/omarchy](https://github.com/basecamp/omarchy) is the source tree for Omarchy: a polished Arch-based desktop built around Hyprland and a single long-running Quickshell shell. User-facing behavior is exposed through `bin/omarchy` and many `omarchy-*` helpers (packages, themes, capture, refresh/restart, plugins). The desktop UI is not a sprawl of separate Quickshell apps; bar, menus, panels, overlays, and services load as plugins under `shell/`, configured primarily via `~/.config/omarchy/shell.json` with first-party code in `shell/plugins/`. Defaults and theming live under `config/`, `default/`, and `themes/`; installation and per-user finalization are orchestrated from `install/` and dedicated setup binaries. `AGENTS.md` is the contributor contract (command naming, metadata, migrations, tests, visual verification). Shipped `default/omarchy-skill/SKILL.md` targets installed-system customization, not hacking this repo.

Observations:

- The shell architecture is the structural bet: one process, plugin manifests, `omarchy-shell` IPC (`summon`, `hide`, `listPlugins`, ...) instead of cold-starting Quickshell per surface.
- CLI surface is intentionally wide but routed: prefix groups in `bin/omarchy` plus comment metadata on each command; contributors are told not to duplicate prefix lists in docs.
- Seeds under-read the repo (only seven markdown entry points at budget 25); most of `applications/`, `docs/`, and `install/` detail never entered the crawl - shape above leans on `AGENTS.md` and shell README depth.
