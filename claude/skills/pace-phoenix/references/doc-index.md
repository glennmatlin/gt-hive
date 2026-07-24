# Phoenix Doc Index

Hand-curated index of the highest-signal Phoenix documentation files in
`docs/PACE Documentation/`. This index is Phoenix-only — ICE entries are
intentionally excluded and live with the `pace-ice` skill.

- Profile: `internal` (research-first; this skill defaults to Phoenix).
- Default cluster: `phoenix`.
- Refresh: rerun `uv run python scripts/pace_doc_pipeline.py rebuild`
  whenever the upstream PACE docs change. The pipeline writes
  `references/cleaned_docs/`, `references/doc-index.json`, and a
  generated full-corpus map; this file is the curated Phoenix subset.

## Phoenix Canonical Docs (Research-First)

- `PACE - [GT-login-only] - Using Slurm on Phoenix.md` | topics: resources, slurm, storage
- `PACE - [GT-login-only] - Phoenix Cluster Resources.md` | topics: migration, resources, slurm, storage
- `PACE - [GT-login-only] - Phoenix Migration to Slurm.md` | topics: migration, ondemand, resources, slurm, storage
- `PACE_PHOENIX_RESOURCES.md` | topics: migration, resources, slurm, storage (duplicate variant of cluster resources)
- `PACE - [GT-login-only] - RHEL9 Migration for Phoenix.md` | topics: migration, ondemand, resources, slurm

## Phoenix Storage and Transfer

- `PACE - [GT-login-only] - Storage Guide.md` | topics: home, scratch, project storage, quotas
- `PACE - External - Use Job-Specific Local Scratch Storage.md` | topics: `${TMPDIR}`, `--tmp` directive
- `PACE - [GT-login-only] - IDEaS Storage on the Cluster.md` | topics: IDEaS-funded storage on Phoenix
- `PACE - [GT-login-only] - Using Globus to Transfer Files.md` | topics: `PACE Phoenix` collection, large transfers
- `PACE - [GT-login-only] - File Transfer with SCP (LinuxMac).md` | topics: small transfers, ad-hoc copies

## Phoenix Web Access

- `PACE - External - Open OnDemand Guide.md` | topics: `ondemand-phoenix.pace.gatech.edu`, web portal, GT VPN

## Workflow Helpers (Phoenix-applicable)

- `PACE - [GT-login-only] - Create Symlinks.md`
- `PACE - [GT-login-only] - Use Git on Cluster.md`
- `PACE - External - Working with TarfilesTarballs on the Cluster.md`
- `PACE - External - Helpful Commands Cheatsheet.md`

## Duplicates Noted

- `PACE - [GT-login-only] - Phoenix Cluster Resources.md` and `PACE_PHOENIX_RESOURCES.md`
  cover the same hardware inventory; prefer the GT-Login titled file as canonical.
