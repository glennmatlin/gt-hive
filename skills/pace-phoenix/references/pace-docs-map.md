# PACE Docs Map

Phoenix-scoped map from task family to the canonical doc(s) in
`docs/PACE Documentation/`. ICE entries are intentionally excluded —
they live in the `pace-ice` skill.

## Table of Contents

- [How to use this map](#how-to-use-this-map)
- [Refresh the local index](#refresh-the-local-index)
- [Canonical docs by task](#canonical-docs-by-task)
- [Supplemental docs by task](#supplemental-docs-by-task)
- [Known caveats in this doc export](#known-caveats-in-this-doc-export)
- [High-signal grep patterns](#high-signal-grep-patterns)

## How to use this map

1. Default to `phoenix`. This overlay is Phoenix-only; if the user is
   actually on ICE, switch skills.
2. Pick the task family.
3. Open only the mapped file(s), then answer from those.

Research-priority rule:

- Prefer production operations docs (Slurm, resources, storage, transfer).
- De-prioritize workshop/training pages unless explicitly requested.

## Refresh the local index

Run this whenever the upstream PACE docs change:

```bash
uv run python scripts/pace_doc_pipeline.py rebuild
```

Generated outputs (full corpus, both clusters; this file is Phoenix-curated):

- `references/cleaned_docs/` (cleaned markdown)
- `references/doc-index.json` (machine-readable ranking/duplicate metadata)
- `references/doc-index.md` (human-readable canonical map)

All paths below are relative to the repository root.

## Canonical docs by task

### Slurm and job submission

- `PACE Documentation/PACE - [GT-login-only] - Using Slurm on Phoenix.md` (phoenix)

### Cluster hardware and partitions

- `PACE Documentation/PACE - [GT-login-only] - Phoenix Cluster Resources.md` (phoenix)
- `PACE Documentation/PACE_PHOENIX_RESOURCES.md` (phoenix duplicate variant)

### Storage and quotas

- `PACE Documentation/PACE - [GT-login-only] - Storage Guide.md` (phoenix home, scratch, project storage)
- `PACE Documentation/PACE - External - Use Job-Specific Local Scratch Storage.md` (`${TMPDIR}` and `--tmp` behavior)
- `PACE Documentation/PACE - [GT-login-only] - IDEaS Storage on the Cluster.md` (phoenix + IDEaS)

### Login and access

- `PACE Documentation/PACE - [GT-login-only] - Phoenix Migration to Slurm.md` (phoenix login endpoint and migration context)

### Open OnDemand

- `PACE Documentation/PACE - External - Open OnDemand Guide.md` (phoenix web access; uses `ondemand-phoenix.pace.gatech.edu`)

### Data transfer

- `PACE Documentation/PACE - [GT-login-only] - Using Globus to Transfer Files.md` (preferred for large transfer; `PACE Phoenix` collection)
- `PACE Documentation/PACE - [GT-login-only] - File Transfer with SCP (LinuxMac).md` (scp usage)

## Supplemental docs by task

### Filesystem convenience and workflow helpers

- `PACE Documentation/PACE - [GT-login-only] - Create Symlinks.md`
- `PACE Documentation/PACE - [GT-login-only] - Use Git on Cluster.md`
- `PACE Documentation/PACE - External - Working with TarfilesTarballs on the Cluster.md`
- `PACE Documentation/PACE - External - Helpful Commands Cheatsheet.md`

### Migrations and platform updates

- `PACE Documentation/PACE - [GT-login-only] - RHEL9 Migration for Phoenix.md`
- `PACE Documentation/PACE - [GT-login-only] - Phoenix Migration to Slurm.md`

### Training and workshop pages

- `PACE Documentation/PACE - External - Workshop Linux 101.md`
- `PACE Documentation/PACE - External - Workshop Linux 102.md`
- `PACE Documentation/PACE - External - Workshop Optimization 101.md`
- `PACE Documentation/PACE - External - Workshop PACE Clusters Orientation.md`

## Known caveats in this doc export

- Many raw files include ServiceNow footer noise (cleaned automatically by the pipeline):
  - `Was this article helpful?`
  - `ASC Most Viewed Articles`
  - `ASC Most Useful Articles`
  - `Copy Permalink`
- Some files include older examples with placeholder usernames (`gburdell3`,
  `puser32`) or legacy wording; do not copy them verbatim as user-specific
  commands.

## High-signal grep patterns

Use these patterns before reading full docs:

```bash
rg -n "pace-quota|--account|-A |qos|inferno|embers" "docs/PACE Documentation"
rg -n "salloc|sbatch|srun|--mem-per-gpu|--tmp|--gres|--constraint" "docs/PACE Documentation"
rg -n "<gt-login-host-redacted>|ondemand-phoenix.pace.gatech.edu|VPN" "docs/PACE Documentation"
rg -n "home|scratch|TMPDIR|local disk|Globus|SCP|project storage" "docs/PACE Documentation"
```
