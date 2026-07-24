---
name: pace-guide
description: Interactive guide to PACE HPC tasks (job, GPUs, storage, troubleshooting, connection, specs)
---

# PACE HPC Interactive Router

You are helping a user with Georgia Tech's PACE HPC clusters. Present the routing
options below using `AskUserQuestion`, then load the appropriate layered skills
based on their selection.

This command routes between three skills:

- `slurm-core` -- generic Slurm job control, scripting, and debugging.
- `pace-phoenix` -- Phoenix-specific charge accounts, QOS, GPU types, storage paths.
- `pace-ice` -- ICE-specific instructional defaults, GPU types, storage paths.

## Step 1: Ask What They Need

Use `AskUserQuestion` with these options:

| Option | Label | Description |
|--------|-------|-------------|
| 1 | Submit a job | Get Slurm job script templates and submission guidance |
| 2 | Request GPUs | GPU syntax, types, and cluster-specific availability |
| 3 | Storage / file transfer | Storage tiers, quotas, Globus, SCP, OnDemand |
| 4 | Troubleshoot a job | Diagnose pending, failed, or OOM jobs |
| 5 | Connect to a cluster | SSH, VPN, OnDemand portal links |
| 6 | Explore cluster specs | Node types, partitions, QOS limits |

## Step 2: Cluster Routing

For options 1, 2, 3, and 6, ask which cluster the user is working with (Phoenix
or ICE) using `AskUserQuestion` -- unless context already makes it clear.

**Phoenix indicators:** charge account (`gts-*`), inferno/embers QOS, research context,
PI mention, project storage paths.

**ICE indicators:** course-related work, AI Makerspace, instructional context,
`<gt-login-host-redacted>`.

If the user is working with a generic Slurm cluster (not PACE) or has not
identified a specific cluster, fall back to loading `slurm-core` only.

## Step 3: Load Skills

Pick the layered skills based on cluster:

- **Phoenix** -> load `slurm-core` + `pace-phoenix`.
- **ICE** -> load `slurm-core` + `pace-ice`.
- **Generic Slurm / unknown cluster** -> load `slurm-core` only.

Within each loaded skill, consult its `SKILL.md` and `references/` directory for
the specific topic the user asked about.

### Submit a job
- From `slurm-core`: read `references/core-workflows.md` for the base sbatch
  template, common directives, and submission patterns.
- From `pace-phoenix` (if Phoenix): read `references/workflows.md` and
  `references/cost-model.md` for charge-account, QOS, and GPU-type adaptations.
  Read `references/phoenix-local-notes.md` for storage paths.
- From `pace-ice` (if ICE): read `references/workflows.md` for instructional
  defaults (no `-A`, no `-q`) and `references/ice-local-notes.md` for storage
  paths.

### Request GPUs
- From `slurm-core`: read `references/core-workflows.md` for the GPU directive
  syntax (`--gres=gpu:...`, `--gpus-per-node`).
- From `pace-phoenix` (if Phoenix): read `references/workflows.md` for the
  Phoenix GPU types (H100, H200, L40S, RTX 6000) and core-per-GPU ratios.
- From `pace-ice` (if ICE): read `references/workflows.md` for the ICE GPU
  types and instructional GPU access patterns.

### Storage / file transfer
- From the cluster-specific skill (`pace-phoenix` or `pace-ice`): read
  `references/*-local-notes.md` for storage paths and quotas. Summarize the
  tiers (home, scratch, project/local) and file transfer options (Globus, SCP,
  OnDemand).

### Troubleshoot a job
- From `slurm-core`: read `references/debugging.md` and
  `references/shell-hygiene.md`.
- Ask the user for the job ID or error message, then walk through diagnostics.

### Connect to a cluster
- Provide connection info directly (no extra files needed):
  - Phoenix SSH: `ssh <user>@<gt-login-host-redacted>`
  - Phoenix OnDemand: `https://ondemand-phoenix.pace.gatech.edu/`
  - ICE SSH: `ssh <user>@<gt-login-host-redacted>`
  - ICE OnDemand: `https://ondemand-ice.pace.gatech.edu/`
  - Remind: Georgia Tech VPN (GlobalProtect) is required before connecting

### Explore cluster specs
- From the cluster-specific skill (`pace-phoenix` or `pace-ice`): read its
  `SKILL.md` and `references/workflows.md`. Summarize node types, partitions,
  QOS policies, and resource limits.

## Key Rules

- Never suggest running compute on login nodes.
- Never use `mpirun`/`mpiexec` with Slurm -- use `srun` instead.
- Phoenix requires a charge account (`-A gts-<pi>`). If unknown, instruct the
  user to run `pace-quota` on the cluster.
- ICE does not require a charge account.
- Scratch is not backed up. Remind users to move important results to project storage.
