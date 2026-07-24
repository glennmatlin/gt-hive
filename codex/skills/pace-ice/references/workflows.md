# ICE Workflows

Worked ICE templates that elaborate on the portable Slurm patterns in
`skills/slurm-core/references/core-workflows.md`. This file does not
re-explain `sbatch`, `srun`, `salloc`, job arrays, or dependency chains —
read those there. Below are ICE-specific elaborations: the no-`-A`-flag
rule, partition auto-routing (do **not** specify `-p` / `--partition`),
optional college-priority and grading QOS, GPU type selection,
job-local `${TMPDIR}` staging, the `PACE ICE access` Globus collection,
and ICE queue-troubleshooting commands.

Login endpoint: `ssh <gt_username>@<gt-login-host-redacted>`. GlobalProtect
VPN is required from off-campus. Open OnDemand for graphical/Jupyter work:
`https://ondemand-ice.pace.gatech.edu/`.

ICE is **free** to GT students and instructors with valid course access.
Jobs do **not** carry an account flag; ICE jobs that include `-A gts-...`
are a routing-time mistake imported from research-cluster habits. Strip
account flags before submitting.

## ICE interactive sessions (salloc)

Use `salloc` for environment validation, module debugging, and short smoke
tests on a real compute node. Default — let auto-routing pick the partition
and QOS:

```bash
salloc -N1 --ntasks-per-node=4 -t1:00:00
srun --pty bash
```

College-priority override (only if default routing is too slow). Pick the
QOS for your enrollment:

```bash
salloc -q coc-ice -N1 --ntasks-per-node=4 -t1:00:00   # CoC users
salloc -q coe-ice -N1 --ntasks-per-node=4 -t1:00:00   # CoE users
salloc -q pace-ice -N1 --ntasks-per-node=4 -t1:00:00  # non-CoC/CoE
```

Inside the shell, validate before scaling: `module avail anaconda3`,
`module load anaconda3`, `python -c "import <package>"`, and on GPU
allocations `nvidia-smi`. Always `exit` to release the allocation. Note
the absence of `-A` and the absence of `-p` / `--partition` — both are
deliberate.

## CPU batch template (ICE)

ICE-specific elements: no account flag, no manual partition, optional
CPU-architecture constraint (`-C intel` / `-C amd` / `-C graniterapids`).
Defaults are 1 core / 1 GB / 1 hour if unspecified.

```bash
#!/bin/bash
#SBATCH -J <job_name>
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

- No `-A` and no `-p` / `--partition` — ICE jobs are free, and partition
  selection is automatic by college affiliation and resource constraints.
- Add `-C intel`, `-C amd`, or `-C graniterapids` only when a code path
  needs a specific CPU family. Granite Rapids nodes are the newest tier
  and host the RTX6000 Pro Blackwell GPUs.
- `module load anaconda3` is the documented base name. Pin a version
  only after confirming with `module avail anaconda3` on the cluster.
  Course-specific or group-specific module names (custom software stacks)
  should be marked `VERIFY_ON_PACE` rather than guessed.
- Per-job caps: 512 CPU-hours, 18-hour CPU walltime. Requests beyond
  that are rejected unless you carry a grading QOS.

## GPU batch template (ICE)

Use `--gres=gpu:<TYPE>:N` for GPU type and per-node count and
`--mem-per-gpu=<size>` for memory. The PACE docs explicitly recommend
`--mem-per-gpu` over total `--mem` for GPU jobs.

```bash
#!/bin/bash
#SBATCH -J <gpu_job>
#SBATCH -N 1
#SBATCH --ntasks-per-node=1
#SBATCH --gres=gpu:H100:1
#SBATCH --mem-per-gpu=224G
#SBATCH -t 01:00:00
#SBATCH -o logs/%x_%j.out

mkdir -p logs
module purge
module load anaconda3
module load cuda

nvidia-smi
srun python <train.py>
```

The `--mem-per-gpu=224G` figure is the PACE-documented recommendation
for HGX H100 servers (8 CPUs/GPU, ample headroom). Adjust per GPU type.

Common GPU `--gres` directives:

| Type | `--gres` | Per-node max | Notes |
|------|----------|--------------|-------|
| V100 | `--gres=gpu:V100:1` | 4 | `-C V100-16GB` or `-C V100-32GB` to pin memory |
| RTX_6000 | `--gres=gpu:RTX_6000:1` | 4 | constraint name `-C RTX6000` |
| A40 | `--gres=gpu:A40:1` | 2 | AMD CPUs |
| A100 | `--gres=gpu:A100:1` | 2 | AMD CPUs; `-C A100-40GB` / `-C A100-80GB` |
| H100 | `--gres=gpu:H100:1` | 8 | 14 nodes reserved for CoE/AI Makerspace |
| H200 | `--gres=gpu:H200:1` | 8 | 12 nodes reserved for CoE/AI Makerspace |
| L40S | `--gres=gpu:L40S:1` | 8 | |
| RTX6000 Pro Blackwell | `--gres=gpu:rtx_pro_6000_blackwell:1` | 16 | Granite Rapids CPUs |
| MI210 | `--gres=gpu:MI210:1` | 2 | AMD CPUs and GPUs; monitor with `rocm-smi` |

`--gres=gpu:N -C HX00` requests the first available H100 *or* H200.
`module load cuda` is the documented base name; pin a version only after
verifying with `module avail cuda`.

Per-job GPU caps: 16 GPU-hours, 16-hour GPU walltime. AI Makerspace
H100/H200 reservations may make those nodes unavailable to general users —
the access path is a known gap (point users at PACE support, do not
fabricate steps).

## Grading QOS template (instructors and TAs)

For grading workloads, request a grading QOS. Walltime extends to 24 h,
caps to 768 CPU-hours / 24 GPU-hours per job, with a 10-job concurrent cap.
ICE-only — there is no analog on the research cluster.

```bash
#!/bin/bash
#SBATCH -J grade_pset3
#SBATCH -q coc-grade            # or coe-grade / pace-grade per course
#SBATCH -N 1
#SBATCH --ntasks-per-node=4
#SBATCH --mem-per-cpu=2G
#SBATCH -t 04:00:00
#SBATCH -o logs/%x_%j.out

mkdir -p logs
module purge
module load anaconda3

srun python grade.py
```

Pick the grading QOS by college:

- `-q coc-grade` — College of Computing courses.
- `-q coe-grade` — College of Engineering courses.
- `-q pace-grade` — non-CoC/CoE courses.

If the user has not stated their college affiliation, leave the QOS as
`-q VERIFY_ON_PACE` so it is grep-visible before submission rather than
silently guessed.

## Local-disk staging template

Stage hot data into job-local NVMe (or SAS) for I/O-heavy steps; copy
results to `~/scratch` before the job ends. ICE compute nodes have either
NVMe or SAS local disk; pin the type with `-C localNVMe` or `-C localSAS`
when needed.

```bash
#!/bin/bash
#SBATCH -J <io_job>
#SBATCH -N 1
#SBATCH --ntasks-per-node=4
#SBATCH --mem-per-cpu=2G
#SBATCH -C localNVMe
#SBATCH --tmp=200G
#SBATCH -t 02:00:00
#SBATCH -o logs/%x_%j.out

cp ~/scratch/<input_file> "${TMPDIR}/"
srun <app> "${TMPDIR}/<input_file>" > "${TMPDIR}/result.out"
cp "${TMPDIR}/result.out" ~/scratch/
```

Plan against the **120-day, semester-end cleanup** on `~/scratch`: copy
keepers off scratch (to home, course shared dir, or off-cluster) before
term end.

## Globus transfers

Globus is the preferred mechanism for moving multi-GB data into or out of
ICE. The ICE collection name is **`PACE ICE access`** (per
`Using Globus to Transfer Files.md`). Workflow:

1. Log into `https://www.globus.org/` with your GT identity.
2. Add the `PACE ICE access` collection on one side; pick a local personal
   endpoint or a peer collection on the other.
3. Start the transfer and monitor from the Activity tab.

For small files or quick command-line copies, use `scp` against
`<gt-login-host-redacted>`. For browser-based file moves, use the
"Files" tab in Open OnDemand.

## Queue troubleshooting (ICE tools)

Generic `squeue` / `sacct` debugging lives in `slurm-core/references/debugging.md`.
The ICE-specific tools are:

- **`pace-check-queue <partition>`** — utilization view of a specific
  partition (e.g. `pace-check-queue ice-cpu`, `pace-check-queue coe-gpu`).
  Use when `squeue` shows your job pending and you need to decide whether
  the partition is saturated or your request is unrealistic.
- **`pace-job-summary <job_id>`** — summary of a finished job (CPU/GPU
  hours, memory peak, exit code) drawn from accounting data. Use after a
  job ends to compare requested vs used resources.
- **`pace-quota`** — discover home and scratch utilization. There is no
  charge account on ICE, so this is a storage-only check.

Order of operations on a stuck job:

1. `squeue -u "${USER}"` — confirm the job is pending or running.
2. `pace-check-queue <partition>` — check whether the relevant partition
   is saturated. Auto-routing means your job may sit in any of the
   partitions you have access to.
3. `pace-job-summary <job_id>` — once it ends, compare requested vs used.
4. `pace-quota` — confirm storage is not the cause.
