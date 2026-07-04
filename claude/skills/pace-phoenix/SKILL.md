---
name: pace-phoenix
description: Georgia Tech PACE Phoenix specifics — "Phoenix", pace-quota, inferno, embers, A100/H100/H200/L40S GPUs, and Phoenix accounts, partitions, or QOS. Always pair with slurm-core for portable Slurm; not for ICE (that's pace-ice).
---

# PACE Phoenix Overlay

This skill is the Phoenix-specific overlay for Georgia Tech PACE. It adds site
facts that `slurm-core` deliberately does not know.

## What this overlay adds

Load this skill when the user is working on (or asking about) the PACE Phoenix
research cluster at Georgia Tech. The overlay supplies Phoenix-specific
account naming, QOS policies, partition and constraint conventions, GPU types,
storage tiers, login/portal endpoints, and cost guidance — plus the
`VERIFY_ON_PACE` discipline for user/group-specific values.

The layered model is: **load `slurm-core` for portable Slurm patterns**
(sbatch, srun, salloc, sacct, job arrays, dependencies, debugging
checklists), **plus this overlay for Phoenix-specific account/QOS/storage/cost
decisions**. Do not duplicate `slurm-core` content here; reference it instead.

Ground truth for every claim in this skill is `docs/PACE Documentation/`
(an export of the official PACE knowledge base). When in doubt, re-verify
against those docs and cite the specific page used.

## Operating defaults

- **Default cluster:** Phoenix.
- **Default QOS:** `inferno` (paid production path; max wallclock 8 days; base
  priority).
- **Free-tier QOS:** `embers` (free; preemptible after 1 hour wallclock; max
  8-hour wallclock; runs as backfill).
- **Account naming pattern:** `gts-<PI_username>[-CODA20|-FY20PhaseN|-paid|-startup]`
  (per `Using Slurm on Phoenix.md`). Substitute `<PI_username>` with the
  user's PI's GT username; suffix variants are optional.
- **Free-tier allowance:** 10k CPU-hours/month on the institute-sponsored
  `gts-<PI_username>` account, billed against base CPU-192GB nodes; credits
  reset on the 1st of each month (per `Using Slurm on Phoenix.md`).
- **Login endpoint:** `<gt-login-host-redacted>`
  (`ssh <gt_username>@<gt-login-host-redacted>`).
- **OnDemand portal:** `https://ondemand-phoenix.pace.gatech.edu/`.
- **Account/quota discovery:** use `pace-quota` on a Phoenix login node to
  discover charge accounts and storage usage. Do not invent an account.
- **Cluster size (stale-sensitive — re-verify against PACE docs):** ~1393 base
  nodes from Phase 1–6 migration completed Feb 2023; plus 54 cpu-gnr (Granite
  Rapids) CPU nodes added Oct 2025; plus 3 gpu-rtxpro-blackwell GPU nodes total
  per current `Phoenix Cluster Resources.md` inventory table (2 of those were
  added Oct 2025 per `Using Slurm on Phoenix.md`; subsequent additions are
  undated in current docs — check the inventory table for the current count).

## Routing

- **Use this overlay alone** for: Phoenix account/QOS choice, partition and
  GPU-type selection, storage-tier guidance, login/Globus/OnDemand pointers,
  cost-vs-priority tradeoffs.
- **Pair with `slurm-core`** for: writing the actual `sbatch` script,
  interactive `salloc`/`srun` workflows, job arrays, dependencies, sacct/squeue
  debugging — anything portable across Slurm clusters. Phoenix-specific values
  (`-A gts-...`, `-q inferno`, `-C amd`, `--gres=gpu:H100:N`) come from this
  overlay; the surrounding Slurm scaffolding comes from `slurm-core`.

## Cluster facts

### CPU partitions and constraints

- Base CPU partition is **CPU-192GB** (the default node class for general
  workloads and free-tier billing).
- Use `#SBATCH -C amd` to request an AMD CPU node.
- **`cpu-gnr`** is the new Granite Rapids partition added October 2025 — flag
  as a recent addition; users targeting newest-generation CPU should prefer
  it but verify availability with `sinfo`.

### GPU types and per-GPU CPU defaults

| GPU type | Default CPUs/GPU | Notes |
|----------|------------------|-------|
| V100 | 12 | use `-C V100-32GB` or `-C V100-16GB` to pin memory tier |
| RTX_6000 | 6 | |
| A100 | 8 (up to 32 by `--ntasks-per-node` request) | |
| H100 | 8 | use `-C gpu-h100` |
| H200 | 8 | |
| L40S | 4 | |
| rtx_pro_6000_blackwell | not documented in current PACE docs; check `module avail` and `sinfo` on the cluster | recent addition (2 Oct 2025 + further per inventory) |

Directive form is `--gres=gpu:<TYPE>:N` (e.g., `--gres=gpu:H100:1`,
`--gres=gpu:A100:2`). Use `--mem-per-gpu=<size>` for memory; the PACE docs
explicitly recommend `--mem-per-gpu` for GPU sizing rather than total `--mem`.
Default per-GPU CPU ratios are documented in
`Using Slurm on Phoenix.md:716-718`.

### Storage tiers

- **Home (`~`):** small, persistent, low quota — for code, configs, and small
  data only.
- **Network scratch (`~/scratch`):** 60-day cleanup; 15 TB / 1M-file cap (per
  `Storage Guide.md`). Suitable for run inputs/outputs that need to outlive
  one job but not be retained long-term.
- **Job-local scratch (`${TMPDIR}`):** per-job NVMe; fast; freed at job exit.
  Documented in `Using Slurm on Phoenix.md` as the per-node temporary path.

Stage hot data into `${TMPDIR}` for I/O-heavy steps; copy results back to
`~/scratch` before the job ends.

### Data transfer

The Globus collection name for Phoenix is **`PACE Phoenix`** (per
`Using Globus to Transfer Files.md`). Globus is the preferred mechanism for
moving large datasets in or out — use it instead of `scp`/`rsync` for
multi-GB transfers. Network scratch has a 60-day cleanup policy, so
schedule transfers around it.

## Cost guidance

Phoenix accounting separates billed (`inferno`) and free (`embers`) work
against published CPU-hour and GPU-hour rates. Plan jobs against the QOS
that matches their priority and fault tolerance.

- **`inferno`:** billed at the CPU-hour and GPU-hour rates published in the
  PACE rate study; use for production-priority work that must complete on a
  predictable wallclock.
- **`embers`:** free; preemptible after 1 hour of runtime; max 8-hour
  wallclock; suitable for backfill and fault-tolerant jobs that can checkpoint
  and resume.
- **Free-tier `gts-<PI_username>` allowance:** 10k CPU-hours per month on
  base CPU-192GB nodes; resets on the 1st.
- See `references/cost-model.md` for the full billing model and the
  rate-study URL.

## Phoenix-specific safety rules

- **No heavy compute on login nodes.** Route to `salloc` (interactive) or
  `sbatch` (batch). Login nodes are for editing, building, and short
  command-line work.
- **Always include account and QOS** for Phoenix jobs: `-A gts-<PI_username>`
  and `-q inferno` (or `-q embers`). If the user has not provided their
  account, point them to `pace-quota` to discover it; do not invent one.
- **Module loads use base names.** `module load anaconda3` and
  `module load cuda` are the documented Phoenix base names; specific
  *versions* drift, so do not pin a version unless the user has verified it
  with `module avail anaconda3` (or equivalent) on the cluster.
- **Filter ServiceNow boilerplate** when reading from cleaned PACE docs —
  ignore lines like `Was this article helpful`, `ASC Most Viewed`,
  `Copy Permalink`, etc. They are export artifacts, not content.
- **Flag stale-sensitive details.** Node inventory, hardware additions
  (Granite Rapids Oct 2025, Blackwell — recent, exact count via inventory
  table), policy limits, and date-bound facts drift over time. Encourage
  re-check against authoritative
  `docs/PACE Documentation/` before relying on a number.
- **Use `VERIFY_ON_PACE` for user/group-specific values** that are not in
  PACE docs. Examples:
  - charge account if user does not provide: `--account=VERIFY_ON_PACE`
  - group-specific module: `module load VERIFY_ON_PACE`
  - allocation balance: not invented; use `pace-quota` to discover

  Do **not** use `VERIFY_ON_PACE` for documented public constants
  (`inferno`, `embers`, `-C amd`, public GPU types, login endpoint). Those
  are stable cluster-wide facts, name them outright.

> Institutional GT AI guidance is tracked in `references/gt-ai-policy.md`,
> not this section. See that file for current language and citation.

## Recommended workflow on Phoenix

1. **Prepare on the login node.** Edit code, build environments, and verify
   small things (`module avail`, syntax checks, dataset paths).
2. **Use `sbatch` for normal execution.** Reach for `salloc` + `srun` only
   for environment validation and quick interactive checks.
3. **Treat the AI as a script-drafter.** Review every generated `sbatch`
   script (account, QOS, partition, GPU type, paths) before submission.
4. **Keep risky operations in an operator-controlled terminal.** Job
   cancellation, requeue, and `scancel` are operator decisions, not
   delegated to background tooling.
5. **Cite the specific PACE doc you used** and re-verify stale-sensitive
   facts (node inventory, dates, hardware deltas) against
   `docs/PACE Documentation/`.

## Build responses in this order

1. **Recommend the workflow** with the minimal steps to execute the user's
   task safely (which QOS, which partition, where to run from).
2. **Provide command/script templates** with placeholders (`<gt_username>`,
   `<account>=gts-<PI_username>`, paths) and `VERIFY_ON_PACE` markers for
   user/group-specific values the AI must not invent.
3. **Include cost/queue tradeoffs** — `inferno` vs `embers`, partition and
   GPU-type implications, free-tier exposure.
4. **Add caveats** that affect data safety, storage cleanup, or institutional
   policy.
5. **Cite the specific PACE doc(s) used** so the user can verify and update
   if the facts have drifted.

## Resource files

- `references/cost-model.md` — billing model and rate-study URL (Task 9).
- `references/workflows.md` — Phoenix-specific job templates (CPU, GPU,
  array, I/O staging) (Task 10).
- `references/pace-docs-map.md` — routing map into authoritative PACE docs,
  Phoenix-only rows (Task 11).
- `references/doc-index.md` — full Phoenix doc index (Task 12).
- `references/phoenix-local-notes.md` — non-routing local facts (Task 13).
- `references/gt-ai-policy.md` — general GT institutional AI guidance
  (relocated from workshop content; kept separate from Phoenix specifics so
  it can be cited or updated independently).
