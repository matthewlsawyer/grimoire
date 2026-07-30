# Grim Forge: genesis and delta

Illustrative provenance lifecycle for a repository named `acme-api`.

## Genesis

Forge runs `status --bootstrap`, reads focused evidence, then establishes the changelog and history.

```markdown
# Grim Forge: acme-api

## Provenance

- **Repo:** `./`
- **Phase:** genesis
- **Changelog:** `./CHANGELOG.md`
- **History:** `./HISTORY.md`
- **Marker:** none -> 9fd02ae
- **Written:** 2 Unreleased entries; Story and 1 Timeline anchor
- **Status:** `status --bootstrap`
```

The first run creates:

```markdown
# Changelog

...

<!-- marker: 9fd02ae -->

## [Unreleased]

### Added
- Worker queue for billing retries (5a3c8d1, 9fd02ae)
```

```markdown
# History

acme-api provides the internal HTTP boundary for account and billing services.

## Story

### Origins
The service began as a small account API with direct provider calls.

### Refactors
The billing retry redesign moved asynchronous recovery into a worker. See [CHANGELOG.md](./CHANGELOG.md#unreleased).

## Timeline

### 2026-07-29

Worker queue and billing retry redesign ([CHANGELOG.md](./CHANGELOG.md#unreleased)) close the synchronous failure path; see [ADR 004](./docs/adrs/004-billing-retries.md).
```

## Delta

On a later run, Forge runs `status`, examines commits since the marker (each with `date`), then appends Unreleased bullets and optionally one dated Timeline entry. `## Story` stays unchanged.

```markdown
# Grim Forge: acme-api

## Provenance

- **Repo:** `./`
- **Phase:** delta
- **Changelog:** `./CHANGELOG.md`
- **History:** `./HISTORY.md`
- **Marker:** 9fd02ae -> b71d4f0
- **Written:** 1 Unreleased entry; 1 Timeline entry
- **Status:** `status`
```

The updated changelog section:

```markdown
## [Unreleased]

### Fixed
- Billing worker adopts idempotency keys through provider submission (b71d4f0)
```

The dated timeline entry (heading from `commits[-1].date`):

```markdown
## Timeline

### 2026-08-04

The idempotency guard ([CHANGELOG.md](./CHANGELOG.md#unreleased)) closes the duplicate-charge gap left when retries became durable.

### 2026-07-29

Worker queue and billing retry redesign ...
```

CHANGELOG records what changed; HISTORY Timeline records when it landed and links outward for context.

## Nested repos

In a workshop with nested git repositories, forge each repo separately.

- Outer artifacts - Throneroom policy only. No inner repo names or commits.
- Inner `projects/grimoire/` artifacts - spellbook evolution, forged by naming that path.

The collector prunes nested git roots when focusing the outer repo, so inner timelines do not bleed into outer provenance.
