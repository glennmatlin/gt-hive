# ICE Doc Index

Hand-curated index of the highest-signal ICE documentation files in
`docs/PACE Documentation/`. This index is ICE-only — Phoenix entries are
intentionally excluded and live with the `pace-phoenix` skill.

- Profile: `internal` (instructional-first; this overlay defaults to ICE).
- Default cluster for this overlay: ICE.
- Refresh: rerun `uv run python scripts/pace_doc_pipeline.py rebuild`
  whenever the upstream PACE docs change. The pipeline writes
  `references/cleaned_docs/`, `references/doc-index.json`, and a
  generated full-corpus map; this file is the curated ICE subset.

## ICE Canonical Docs (Instructional-First)

- `PACE - External - Getting Started with ICE.md` | topics:
  access flow, instructor application, AI Makerspace mention, OnDemand
  pointer. Read first if you do not know what ICE is or who can use it.
- `PACE - [GT-login-only] - Log on to ICE.md` | topics: SSH endpoint
  (`<gt-login-host-redacted>`), GlobalProtect VPN, password prompt.
  The shortest doc — read for login-time questions.
- `PACE - External - ICE Cluster Resources.md` | topics: full hardware
  inventory (CPU/GPU node tables), partition routing logic, AI Makerspace
  H100/H200 reservation footnotes, "do not request a partition" rule.
- `PACE - External - Storage on ICE.md` | topics: home (30 GB,
  snapshotted), scratch (300 GB Lustre, 120-day cleanup, 1M file cap),
  local disk (`${TMPDIR}` + `localSAS`/`localNVMe`), course shared dirs
  on VAST/Lustre, file-transfer pointers.
- `PACE - External - Using Slurm on ICE.md` | topics: the most detailed
  ICE doc. salloc/sbatch/srun examples, walltime caps (18 h CPU / 16 h
  GPU), per-job caps (512 CPU-h / 16 GPU-h), college-priority and
  grading QOS, CPU-architecture constraints, full GPU-request syntax
  (V100, RTX6000, A40, A100, H100, H200, L40S, RTX6000 Pro Blackwell,
  MI210), and a fully worked H100 batch example.

## Cross-Cluster Docs ICE Users Care About

- `PACE - External - Open OnDemand Guide.md:15` | topics: ICE web portal
  at `https://ondemand-ice.pace.gatech.edu/`, Jupyter and graphical
  interactive jobs.
- `PACE - [GT-login-only] - Using Globus to Transfer Files.md:58` | topics:
  the `PACE ICE access` collection name, Globus workflow, large
  transfers.
- `PACE - External - Use Job-Specific Local Scratch Storage.md` |
  topics: `${TMPDIR}` semantics and `--tmp` directive — same on both
  clusters.

## Workflow Helpers (ICE-applicable)

- `PACE - [GT-login-only] - Create Symlinks.md`
- `PACE - [GT-login-only] - Use Git on Cluster.md`
- `PACE - External - Working with TarfilesTarballs on the Cluster.md`
- `PACE - External - Helpful Commands Cheatsheet.md`

## Known Gaps

- AI Makerspace access semantics (who qualifies, how reservations
  interact with auto-routing) are not fully documented in repo. Point
  users at `pace-support@oit.gatech.edu`.
- ICE module/software-stack inventory is not enumerated in repo;
  `module avail` on the cluster is ground truth.
- Worked GPU examples exist only for H100 in `Using Slurm on ICE.md`;
  other GPU families are documented at the directive level only.
