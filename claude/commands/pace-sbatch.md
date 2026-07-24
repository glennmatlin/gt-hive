---
name: pace-sbatch
description: Interactive wizard that drafts a Slurm sbatch script for PACE Phoenix, ICE, or generic Slurm
---

# sbatch wizard

Draft a Slurm batch script through structured questions. Use this command
when the user wants a runnable sbatch file fast and is happier clicking
through options than describing every directive in prose.

## Step 1: cluster

Use `AskUserQuestion` with these options:

| Option | Label | Description |
|--------|-------|-------------|
| 1 | Phoenix | Georgia Tech research cluster (`gts-*` accounts, `inferno`/`embers` QOS) |
| 2 | ICE | Georgia Tech instructional cluster (no `-A`, no manual partition) |
| 3 | Generic Slurm | A non-PACE Slurm site |

## Step 2: workload

Use `AskUserQuestion`:

| Option | Label | Description |
|--------|-------|-------------|
| 1 | CPU | CPU-only batch job |
| 2 | Single GPU | One GPU on one node |
| 3 | Multi-GPU | Multiple GPUs (single node or multi-node) |
| 4 | Array | Array of independent tasks |
| 5 | MPI | Distributed MPI workload (uses `srun`, never `mpirun`) |

## Step 3: basic params

Use a single grouped `AskUserQuestion` to collect cores, memory (GB), and
walltime (HH:MM:SS). Provide sensible defaults: 4 cores, 16 GB, 02:00:00.

## Step 4: GPU type (only if Step 2 was GPU)

Look up the cluster's available GPU types:

- Phoenix: read `pace-phoenix/references/workflows.md` for the H100 / H200 /
  L40S / RTX 6000 / Blackwell list and the per-GPU core ratios.
- ICE: read `pace-ice/references/workflows.md` for the ICE GPU list.

Present those GPUs as `AskUserQuestion` options.

## Step 5: load skills and draft the script

Load skills based on cluster:

- **Phoenix** -> `slurm-core` + `pace-phoenix`.
- **ICE** -> `slurm-core` + `pace-ice`.
- **Generic Slurm** -> `slurm-core` only.

Read `slurm-core/references/core-workflows.md` for the base sbatch template
and the cluster overlay's `references/workflows.md` for site-specific
directives.

Draft a complete `.sbatch` file with long-form Slurm directives. For values
the agent cannot know, emit the `VERIFY_ON_PACE` marker pattern from the
overlay paired with the discovery command:

- Charge account on Phoenix: `#SBATCH -A VERIFY_ON_PACE   # run pace-quota to find your gts-* account`
- Module names: `module load VERIFY_ON_PACE   # run module avail to find the module name`

Phoenix jobs must include both `-A` and `-q`. ICE jobs must omit `-A` and
must not specify a partition manually. Generic Slurm jobs use only the
portable `slurm-core` directives — and use `VERIFY_ON_SITE` (not
`VERIFY_ON_PACE`) for unknown values, since the GT-specific marker would
leak a site name into a portable script.

## Step 6: submission reminder

Print the script in a fenced code block, then a one-line reminder:

> Save as `<name>.sbatch`, review every directive, then submit with `sbatch <name>.sbatch`. On Phoenix, double-check the QOS (`inferno` is paid, `embers` is free). Scratch is not backed up — move important results to project storage.

## Key rules

- Never suggest running compute on login nodes.
- Never use `mpirun`/`mpiexec` with Slurm — use `srun` instead.
- Never invent a Phoenix `gts-*` account, a module name, or a filesystem
  path. Use `VERIFY_ON_PACE` markers for anything user-specific.
