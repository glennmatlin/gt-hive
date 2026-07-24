# Phoenix Workflows

Worked Phoenix templates that elaborate on the portable Slurm patterns in
`skills/slurm-core/references/core-workflows.md`. This file does not
re-explain `sbatch`, `srun`, `salloc`, job arrays, or dependency chains —
read those there. Below are Phoenix-specific elaborations: account/QOS
routing (`-A gts-<PI>`, `-q inferno`/`-q embers`), GPU type selection,
storage-tier staging, Globus collections, and Phoenix queue-troubleshooting
commands.

Login endpoint: `ssh <gt_username>@<gt-login-host-redacted>`. Discover
your charge account before submitting:

```bash
pace-quota
```

Do not invent an account; substitute `<PI>` with your PI's GT username only
after `pace-quota` confirms it. If the user has not provided a charge account,
keep the literal token `VERIFY_ON_PACE` (e.g. `--account=VERIFY_ON_PACE`) in
generated examples so the user grep-finds it before submission.

## Phoenix interactive sessions (salloc)

Use `salloc` for environment validation, module debugging, and short smoke
tests on a real compute node. Inferno (paid, predictable):

```bash
salloc -A gts-<PI> -q inferno -N 1 --ntasks-per-node=4 -t 01:00:00
srun --pty bash
```

Embers (free, preemptible after 1 hour, max 8h wallclock) — useful for
quick interactive checks where preemption is acceptable:

```bash
salloc -A gts-<PI> -q embers -N 1 --ntasks-per-node=4 -t 01:00:00
```

Inside the shell, validate before scaling: `module avail anaconda3`,
`module load anaconda3`, `python -c "import <package>"`, and on GPU
allocations `nvidia-smi`. Always `exit` to release the allocation.

## CPU batch template (Phoenix)

Phoenix-specific elements layered onto the generic batch skeleton: the
`-A gts-<PI>` account directive, the `-q inferno` QOS, optional `-C amd`
constraint for AMD CPU nodes, and the documented `module load anaconda3`
base name.

```bash
#!/bin/bash
#SBATCH -J <job_name>
#SBATCH -A gts-<PI>
#SBATCH -q inferno
#SBATCH -C amd
#SBATCH -N 1
#SBATCH --ntasks-per-node=4
#SBATCH --mem-per-cpu=2G
#SBATCH -t 01:00:00
#SBATCH -o logs/%x_%j.out
#SBATCH -e logs/%x_%j.err

mkdir -p logs
module purge
module load anaconda3

hostname
srun python <script.py>
```

Notes:

- Drop `-C amd` if you do not need AMD silicon. To target the new
  Granite Rapids partition added Oct 2025, use the partition directive
  (`#SBATCH -p cpu-gnr`) and verify availability with `sinfo` first.
- `module load anaconda3` is the documented base name. Pin a version
  (`anaconda3/2024.06`) only after confirming with `module avail anaconda3`
  on the cluster. Group-specific or per-lab software stacks (custom module
  trees) should be marked `VERIFY_ON_PACE` rather than guessed.
- `hostname` in the body confirms which compute node ran the job — useful
  when correlating with `sacct` and the inventory in `Phoenix Cluster Resources.md`.
- For free-tier work that can checkpoint, swap `-q inferno` to `-q embers`.
  Embers preempts after 1 hour of runtime; design the job to resume.

## GPU batch template (Phoenix)

Use `--gres=gpu:<TYPE>:N` for GPU type and count and `--mem-per-gpu=<size>`
for memory. The PACE docs explicitly recommend `--mem-per-gpu` over total
`--mem` for GPU jobs.

```bash
#!/bin/bash
#SBATCH -J <gpu_job>
#SBATCH -A gts-<PI>
#SBATCH -q inferno
#SBATCH -N 1
#SBATCH --gres=gpu:H100:1
#SBATCH --mem-per-gpu=80G
#SBATCH -t 04:00:00
#SBATCH -o logs/%x_%j.out

mkdir -p logs
module purge
module load anaconda3
module load cuda

nvidia-smi
srun python <train.py>
```

Common GPU types and constraint examples:

| Type | `--gres` | Constraint examples |
|------|----------|---------------------|
| V100 | `--gres=gpu:V100:1` | `-C V100-32GB` or `-C V100-16GB` to pin memory tier |
| RTX_6000 | `--gres=gpu:RTX_6000:1` | |
| A100 | `--gres=gpu:A100:1` | up to 32 CPUs/GPU via `--ntasks-per-node` |
| H100 | `--gres=gpu:H100:1` | `-C gpu-h100` |
| H200 | `--gres=gpu:H200:1` | |
| L40S | `--gres=gpu:L40S:1` | |
| rtx_pro_6000_blackwell | `--gres=gpu:rtx_pro_6000_blackwell:1` | recent addition; verify with `module avail` and `sinfo` |

`module load cuda` is the documented base name for CUDA on Phoenix. Pin a
version only after verifying with `module avail cuda`.

## Scratch path conventions

Three storage tiers, each with a different Phoenix policy:

- **Home (`~`):** small persistent quota; for code, configs, small data.
- **Network scratch (`~/scratch`):** 15 TB / 1M-file cap, 60-day cleanup
  (per `Storage Guide.md`). Run inputs/outputs that must outlive one job.
- **Job-local scratch (`${TMPDIR}`):** per-job NVMe, fast, freed at job exit.

Pattern: stage hot data into `${TMPDIR}` for I/O-heavy steps, copy results
back to `~/scratch` before the job ends so they survive. Request node-local
space with `--tmp=`:

```bash
#!/bin/bash
#SBATCH -J <io_job>
#SBATCH -A gts-<PI>
#SBATCH -q inferno
#SBATCH -N 1
#SBATCH --tmp=200G
#SBATCH -t 02:00:00

cp ~/scratch/<input_file> "${TMPDIR}/"
srun <app> "${TMPDIR}/<input_file>" > "${TMPDIR}/result.out"
cp "${TMPDIR}/result.out" ~/scratch/
```

Plan against the 60-day cleanup on `~/scratch`: anything that must persist
longer belongs on a project storage tier, not scratch.

## Globus transfers

Globus is the preferred mechanism for moving multi-GB datasets in or out
of Phoenix. The Phoenix collection name is **`PACE Phoenix`** (per
`Using Globus to Transfer Files.md`). Workflow:

1. Log into `https://www.globus.org/` with your Georgia Tech identity.
2. Add the `PACE Phoenix` collection on one side; pick a local personal
   endpoint or a peer collection on the other.
3. Start the transfer and monitor from the Activity tab.

When to choose Globus vs `scp`:

- **Globus:** datasets larger than a few GB, transfers that need restart on
  failure, scheduled overnight moves, or anything traversing flaky networks.
- **`scp`/`rsync`:** small files, quick command-line copies, ad-hoc fixes.
  See `Using Globus to Transfer Files.md` for current collection names and
  endpoint registration steps.

## Queue troubleshooting (Phoenix tools)

Generic `squeue` / `sacct` debugging lives in `slurm-core/references/debugging.md`.
The Phoenix-specific tools are:

- **`pace-check-queue <partition_or_qos>`** — Phoenix's view of partition or
  QOS state (free vs busy, pending vs running breakdown). Use when `squeue`
  shows your job pending and you need to decide whether the partition is
  saturated or your request is unrealistic.
- **`pace-job-summary <job_id>`** — summary of a finished job (CPU/GPU
  hours, memory peak, exit code) drawn from accounting data. Use after a
  job ends to compare requested vs used resources before tightening the
  next submission.
- **`pace-quota`** — discover charge accounts and quota state on home and
  scratch. Use before submission to confirm the account exists and there is
  storage headroom; use after a storage-related failure to confirm whether
  you tripped a 15 TB or 1M-file cap.

Order of operations on a stuck job:

1. `squeue -u "${USER}"` — confirm the job is pending or running.
2. `pace-check-queue inferno` (or `embers`) — check whether the QOS is
   saturated.
3. `pace-job-summary <job_id>` — once it ends, compare requested vs used.
4. `pace-quota` — confirm account and storage are not the cause.
