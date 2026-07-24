# PACE Docs Map

ICE-scoped map from task family to the canonical doc(s) in
`docs/PACE Documentation/`. Phoenix entries are intentionally excluded —
they live in the `pace-phoenix` skill.

## Table of Contents

- [How to use this map](#how-to-use-this-map)
- [Refresh the local index](#refresh-the-local-index)
- [Canonical docs by task](#canonical-docs-by-task)
- [Supplemental docs by task](#supplemental-docs-by-task)
- [Known caveats in this doc export](#known-caveats-in-this-doc-export)
- [High-signal grep patterns](#high-signal-grep-patterns)

## How to use this map

1. This overlay is ICE-only. If the user is actually on the research
   cluster, switch to `pace-phoenix`.
2. Pick the task family.
3. Open only the mapped file(s), then answer from those.
4. Cite the doc you used, so the user can verify if upstream content
   has drifted.

Instructional-priority rule:

- Prefer task-direct docs (Slurm-on-ICE, ICE Cluster Resources,
  Storage-on-ICE) over generic workshop pages.
- De-prioritize workshop/training pages unless explicitly requested.

## Refresh the local index

Run this whenever the upstream PACE docs change:

```bash
uv run python scripts/pace_doc_pipeline.py rebuild
```

Generated outputs (full corpus, both clusters; this file is ICE-curated):

- `references/cleaned_docs/` (cleaned markdown)
- `references/doc-index.json` (machine-readable ranking/duplicate metadata)
- `references/doc-index.md` (human-readable canonical map)

All paths below are relative to the repository root.

## Canonical docs by task

### Login and access

- `PACE Documentation/PACE - [GT-login-only] - Log on to ICE.md` (ICE SSH
  endpoint `<gt-login-host-redacted>`, GlobalProtect VPN requirement,
  password prompt behavior)
- `PACE Documentation/PACE - External - Getting Started with ICE.md`
  (ICE access flow, instructor application path, AI Makerspace mention)

### Slurm and job submission

- `PACE Documentation/PACE - External - Using Slurm on ICE.md` (the
  primary ICE workhorse: salloc/sbatch/srun examples, partition/QOS
  auto-routing, college-priority and grading QOS, CPU-architecture
  constraints, full GPU-request syntax for V100/RTX6000/A40/A100/H100/
  H200/L40S/RTX6000 Pro Blackwell/MI210, local-disk constraints, the
  18 h CPU / 16 h GPU walltime caps and 512 CPU-h / 16 GPU-h per-job
  caps)

### Cluster hardware and partitions

- `PACE Documentation/PACE - External - ICE Cluster Resources.md` (full
  hardware inventory, partition routing rules — CoC vs CoE/AI Makerspace
  vs other-college vs everyone — and the AI Makerspace H100/H200
  reservation footnotes)

### Storage and quotas

- `PACE Documentation/PACE - External - Storage on ICE.md` (home 30 GB
  with daily snapshot, scratch 300 GB Lustre with 120-day cleanup, local
  disk via `${TMPDIR}` + `localSAS`/`localNVMe` constraints, course
  shared directories on VAST/Lustre, file transfer pointers)
- `PACE Documentation/PACE - External - Use Job-Specific Local Scratch Storage.md`
  (`${TMPDIR}` + `--tmp` behavior; common to both clusters)

### Open OnDemand

- `PACE Documentation/PACE - External - Open OnDemand Guide.md` (ICE
  web portal at `https://ondemand-ice.pace.gatech.edu/`, GT VPN
  required, Jupyter and graphical-interactive jobs)

### Data transfer

- `PACE Documentation/PACE - [GT-login-only] - Using Globus to Transfer Files.md`
  (preferred for large transfer; `PACE ICE access` collection)
- `PACE Documentation/PACE - [GT-login-only] - File Transfer with SCP (LinuxMac).md`
  (scp usage to/from `<gt-login-host-redacted>`)

### Software stack and modules

- `PACE Documentation/PACE - External - Getting Started with ICE.md`
  references a RHEL9 Software Stack KB article. The surveyed docs do
  not enumerate ICE module names; use `module avail` on the cluster
  as ground truth.

## Supplemental docs by task

### Filesystem convenience and workflow helpers

- `PACE Documentation/PACE - [GT-login-only] - Create Symlinks.md`
- `PACE Documentation/PACE - [GT-login-only] - Use Git on Cluster.md`
- `PACE Documentation/PACE - External - Working with TarfilesTarballs on the Cluster.md`
- `PACE Documentation/PACE - External - Helpful Commands Cheatsheet.md`

### Training and workshop pages

- `PACE Documentation/PACE - External - Workshop Linux 101.md` (mentions
  PACE-ICE in passing for an SSH learning objective; not authoritative
  for ICE)
- `PACE Documentation/PACE - External - Workshop Linux 102.md`
- `PACE Documentation/PACE - External - Workshop Optimization 101.md`
- `PACE Documentation/PACE - External - Workshop PACE Clusters Orientation.md`

## Known caveats in this doc export

- Many raw files include ServiceNow footer noise (cleaned automatically by
  the pipeline):
  - `Was this article helpful?`
  - `ASC Most Viewed Articles`
  - `ASC Most Useful Articles`
  - `Copy Permalink`
- Some files include older examples with placeholder usernames
  (`gburdell3`) or legacy wording; do not copy them verbatim as
  user-specific commands.
- The `Using Slurm on ICE.md` doc only includes a fully worked example
  for H100 GPUs. Other GPU families (V100, A40, A100, L40S, H200,
  RTX6000 Pro Blackwell, MI210) are documented at the directive level
  but not as end-to-end examples.

## High-signal grep patterns

Use these patterns before reading full docs:

```bash
rg -n "salloc|sbatch|srun|--mem-per-gpu|--tmp|--gres|--constraint|-q coc-|-q coe-|-q pace-" "docs/PACE Documentation"
rg -n "ice-cpu|ice-gpu|coc-cpu|coc-gpu|coe-gpu|pace-cpu|pace-gpu" "docs/PACE Documentation"
rg -n "<gt-login-host-redacted>|ondemand-ice.pace.gatech.edu|VPN|GlobalProtect" "docs/PACE Documentation"
rg -n "home|scratch|TMPDIR|localSAS|localNVMe|shared director|VAST|Lustre" "docs/PACE Documentation"
rg -n "AI Makerspace|H100|H200|grade|grading" "docs/PACE Documentation"
```
