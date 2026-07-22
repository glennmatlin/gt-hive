---
name: slurm-core
description: Portable Slurm guidance for batch scripts (sbatch/srun/salloc), job arrays, dependencies, sacct/squeue monitoring, and debugging pending or failed jobs. Pair with a site overlay (pace-phoenix or pace-ice) when a specific cluster is named; not for a named cluster alone.
---

# Slurm Core

This skill teaches a terminal AI assistant how to help with **portable Slurm workflows** without inventing site-local facts.

## What this skill is for

Use this skill when the user needs help with:

- CPU, Python, or GPU batch scripts
- `sbatch`, `srun`, or `salloc`
- job arrays
- dependency pipelines
- monitoring and debugging
- accounting and exit-code interpretation
- converting ad hoc shell loops into repeatable Slurm workflows

Before drafting anything, build context:

1. Identify the task type (`job submission`, `resource selection`, `monitoring`, `troubleshooting`).
2. Identify the workload profile (`CPU`, `GPU`, `MPI`, `array`, `interactive debugging`, `I/O-heavy`).
3. State assumptions explicitly and continue unless cluster policy or data handling forces a clarifying question.

## What this skill must not guess

Do **not** invent any of the following:

- cluster-specific `--account`
- `--partition`
- `--qos`
- module names
- filesystem paths
- conda environment names
- site policy
- GPU type names that the cluster may not actually provide

If a value is unknown, mark it `VERIFY_ON_SITE` and explain what local doc or command should confirm it. The literal string `VERIFY_ON_SITE` is the convention readers grep for: it tells humans "the AI refused to invent this — fill it in yourself before submitting." Use it everywhere a site-local fact would otherwise be hallucinated (for example `--account=VERIFY_ON_SITE`, `module load VERIFY_ON_SITE`).

For reader-supplied values that are not site-secret (a job name, a script path), use angle-bracket placeholders like `<job_name>` or `<script.py>`.

## Operating principles

1. Prefer **long-form Slurm directives** (`--cpus-per-task=4`, not `-c 4`) so scripts read as teaching material.
2. Prefer **explicit resource requests** to implicit defaults.
3. Keep explanations beginner-friendly but technically correct.
4. Separate portable Slurm ideas from site-local details. Portable goes in this skill; site-local goes in the overlay.
5. When the user is debugging, start from evidence rather than speculation.

## Remote Cluster Deployment

- Treat local-to-cluster source transfer as a software release operation,
  never as a routine job-submission step.
- Prefer, in order: an existing verified remote deployment, an authorized
  remote checkout of an exact Git revision, reusable parameterized launchers,
  and one consolidated release transfer.
- Treat a checkout as verified only when it is detached at the requested full
  SHA, clean, and covered by a machine-readable receipt binding its origin,
  path, revision, and tracked bootstrap or dependency identity.
- Never create or upload one-off local wrappers, sbatch files, patches,
  contracts, configurations, or content-addressed bundles for individual
  jobs. Generate job-specific configuration on the cluster from code and
  artifacts already present there.
- Prepare complete Slurm dependency chains before unattended runs. Do not
  insert user approval boundaries between stages using the same deployment.
- If new source bytes truly must cross systems, consolidate all changes into
  one tested release and request one exact approval at the phase boundary.

## Core patterns

### 1. Batch job skeleton

Canonical portable shape — Python-style single-process workload, long-form directives, `VERIFY_ON_SITE` for anything site-local:

```bash
#!/bin/bash
#SBATCH --job-name=<job_name>
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --account=VERIFY_ON_SITE
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=4G
#SBATCH --time=00:10:00

mkdir -p logs
module purge
module load VERIFY_ON_SITE

srun python <script.py>
```

Notes:

- `--mem=4G` requests total memory for the job. Alternatives: `--mem-per-cpu=2G` scales with `--cpus-per-task`; `--mem-per-gpu=12G` scales with allocated GPUs. Pick one and stick with it.
- `--ntasks=1` plus `--cpus-per-task=N` is the canonical shape for a single-process Python or shell program that uses N threads. Do not mix with `--ntasks-per-node` for non-MPI work.
- `--output` and `--error` are split into separate files inside `logs/`. `%x` expands to the job name and `%j` to the job ID. Create `logs/` before submitting (the skeleton's `mkdir -p logs` covers this).
- `module purge && module load <module_name>` is the safe pattern for environment setup. Real module names (anaconda, cuda, gcc, etc.) are site-specific, so the placeholder is `VERIFY_ON_SITE`.

### 2. Interactive debugging pattern

When users are exploring environments, module issues, path issues, or quick validation, recommend an interactive allocation before finalizing the batch script:

```bash
salloc --nodes=1 --ntasks=1 --cpus-per-task=2 --mem=4G --time=00:15:00
srun --pty bash
```

Inside the shell, validate `module load`, `python -c "import ..."`, and small smoke runs before submitting a long batch job.

### 3. Job-array pattern

When a shell loop runs the same program over many parameters, prefer a Slurm job array:

```bash
#SBATCH --array=0-99%10
#SBATCH --output=logs/%x_%A_%a.out
#SBATCH --error=logs/%x_%A_%a.err
```

Defaults that pay off:

- one task per array element
- separate logs per task (`%A` = array job ID, `%a` = array task ID)
- explicit concurrency cap like `%10` to avoid flooding the scheduler
- inside the script, use `${SLURM_ARRAY_TASK_ID}` to index into the parameter list

### 4. Dependency pattern

Chain jobs with `--dependency=`:

- `afterok:<jobid>` — downstream runs only after success
- `afterany:<jobid>` — downstream runs after completion regardless of exit
- `afternotok:<jobid>` — downstream runs only after failure (cleanup, alerting)
- `singleton` — only one job of a given name+user runs at a time

```bash
JOB1=$(sbatch --parsable stage1.sbatch)
sbatch --dependency=afterok:${JOB1} stage2.sbatch
```

Keep pipeline stages as separate scripts when it improves clarity over a monolithic script.

### 5. GPU job pattern

The most portable way to request a GPU is the count-only form:

```bash
#SBATCH --gres=gpu:1
```

If a specific GPU type is needed, the form is `--gres=gpu:<TYPE>:1` with `<TYPE>=VERIFY_ON_SITE` because GPU type names (e.g. specific architectures and SKUs) are site-specific. Some sites also accept the newer `--gpus=1` syntax. Pair the GPU request with `--mem-per-gpu=` if memory should scale with GPUs, and load the cluster's CUDA/driver module via `module load VERIFY_ON_SITE`.

### 6. MPI sidebar

For MPI workloads, replace the canonical resource shape with `--ntasks-per-node=N` (and optionally `--nodes=K`) so each rank is a Slurm task. Launch with `srun <mpi_program>` — `srun` integrates with Slurm's process manager, so an explicit `mpirun` is rarely needed. This sidebar is intentionally short; tune ranks-per-node and the binding flags to the cluster's interconnect.

## Safety

- Never include secrets, private keys, API tokens, or credentials in prompts, scripts, or logs.
- Never invent local site policy. If the user does not provide an account, partition, QOS, module name, or path, mark the value `VERIFY_ON_SITE` and explain what local doc or command should confirm it.
- Never propose heavy compute on login nodes — route the user to `salloc` or `sbatch`.
- Recommend the user review every shell command before running it on a shared cluster.

## Evidence checklist for debugging

For **failed jobs**, inspect in this order:

1. the batch script
2. `sacct -j <jobid> -X --format=JobID,JobName,State,ExitCode,Elapsed,MaxRSS,ReqMem` — `-X` collapses job steps for first-pass triage
3. stdout / stderr in `logs/`
4. environment / module activation lines
5. only then propose the smallest safe fix

For **pending jobs**, inspect:

1. `squeue -j <jobid>` (or `squeue -u <user>` to see all of a user's jobs)
2. the `REASON` field
3. the resource request — walltime, memory, GPU type, partition fit
4. dependency, account, or time-limit issues

Interpretation heuristics:

- `ExitCode=0:0` usually means the script exited cleanly; look elsewhere (timeout, OOM, signal) for the cause if results are missing.
- `ExitCode=N:0` (first number non-zero) means the script's own exit code was non-zero; stderr is usually the fastest path to root cause.
- `ExitCode=0:M` (second number non-zero) means the job was killed by signal `M` (e.g. `9` = OOM-killer, `15` = timeout via `SIGTERM`).

Common failure categories worth checking up front:

- missing file or wrong path
- wrong environment / package missing
- bad resource request
- time limit too short
- memory too small
- dependency never satisfied
- wrong working directory

## Output conventions

When you write examples:

- use readable log names (`logs/%x_%j.{out,err}`, or `logs/%x_%A_%a.{out,err}` for arrays)
- explain each non-obvious directive
- state explicitly which fields are portable and which are site-local
- mark unknown site fields `VERIFY_ON_SITE`
- distinguish network scratch (a persistent shared path, e.g. `<network_scratch>=VERIFY_ON_SITE`) from job-local scratch (`${TMPDIR}`, universal across Slurm sites — node-local, fast, freed at job exit). Stage hot data into `${TMPDIR}` for I/O-heavy steps and copy results back to the network path before the job ends.
- keep commands copy-editable

## Resource files

Load these references when needed:

- `references/core-workflows.md` — minimal mental model, batch script checklist, arrays, dependencies.
- `references/debugging.md` — first-pass commands, exit-code heuristics, common failure categories.
- `references/shell-hygiene.md` — SSH multiplexing (`ControlMaster`/`ControlPath`/`ControlPersist`) and the two-terminal operator/assistant pattern. Portable across sites; load when the user asks about persistent SSH or how to organize terminals for AI-assisted Slurm.

User-facing prompt-coaching templates live in `docs/prompt-templates.md` (tier-2 deferred). They are deliberately *not* part of this skill: prompt coaching is for humans authoring prompts, not for the AI agent reading the skill at runtime.
