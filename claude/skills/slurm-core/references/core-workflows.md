# Core Slurm Workflows

Worked examples for the four canonical job shapes: batch, interactive, array, and dependency chains. These templates expand on the patterns introduced in `SKILL.md`. Site-local values (account, partition, module names) are left as `VERIFY_ON_SITE`. User-supplied placeholders use `<angle_brackets>`.

## Batch

Long-form skeleton for a single-process Python or shell program with N threads:

```bash
#!/bin/bash
#SBATCH --job-name=<job_name>
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --account=VERIFY_ON_SITE
#SBATCH --partition=VERIFY_ON_SITE
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
#SBATCH --time=02:00:00

mkdir -p logs
module purge
module load VERIFY_ON_SITE

srun python <script.py> --threads "${SLURM_CPUS_PER_TASK}"
```

Submit and monitor:

```bash
sbatch <job_name>.sbatch
squeue -u "${USER}"
```

Notes on the non-obvious directives:

- `--output` / `--error` split stdout and stderr into separate files. `%x` expands to the job name and `%j` to the job ID. Create `logs/` before submitting (`mkdir -p logs` covers this).
- `--ntasks=1` plus `--cpus-per-task=N` is the canonical shape for a single-process program that internally uses N threads. Do not mix with `--ntasks-per-node` for non-MPI work.
- `--mem=8G` requests total memory for the job. Alternative: `--mem-per-cpu=2G` scales with `--cpus-per-task`. Pick one form per script.
- `--time=hh:mm:ss` is required by most schedulers. Estimate generously on the first run, then tighten once you see real `Elapsed` from `sacct`.
- Pass `${SLURM_CPUS_PER_TASK}` into the program so thread counts stay in sync with the allocation.

## Interactive

Use an interactive allocation when validating environments, debugging module/path issues, or smoke-testing a script before committing it to a long batch job.

```bash
salloc --account=VERIFY_ON_SITE \
       --partition=VERIFY_ON_SITE \
       --nodes=1 \
       --ntasks=1 \
       --cpus-per-task=2 \
       --mem=4G \
       --time=00:30:00
srun --pty bash
```

Inside the shell, validate before scaling:

```bash
module purge
module load VERIFY_ON_SITE
python -c "import <package>; print(<package>.__version__)"
python <script.py> --smoke-test
```

Exit (`exit` in the shell) to release the allocation.

When to prefer `salloc` over `sbatch`: iterating on `module load`, diagnosing import or path errors, running a small smoke subset, or inspecting GPU visibility (`nvidia-smi`) on a real compute node. Prefer `sbatch` once the workflow is stable, runs longer than a single sitting, or needs to chain via dependencies.

## Array

Use a job array when a shell loop runs the same program over many parameters. One array task per parameter; the scheduler handles the fan-out.

```bash
#!/bin/bash
#SBATCH --job-name=<array_job>
#SBATCH --output=logs/%x_%A_%a.out
#SBATCH --error=logs/%x_%A_%a.err
#SBATCH --account=VERIFY_ON_SITE
#SBATCH --partition=VERIFY_ON_SITE
#SBATCH --array=0-9%5
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G
#SBATCH --time=00:20:00

mkdir -p logs
module purge
module load VERIFY_ON_SITE

PARAMS=(0.001 0.003 0.01 0.03 0.1 0.3 1.0 3.0 10.0 30.0)
LR="${PARAMS[${SLURM_ARRAY_TASK_ID}]}"

srun python <train.py> --learning-rate "${LR}" \
                      --output "results/run_${SLURM_ARRAY_TASK_ID}.json"
```

Notes:

- `--array=0-9%5` runs ten tasks (indices `0..9`) with at most five running concurrently. The `%N` cap protects shared scheduling and storage from being flooded.
- `%A` is the array job ID; `%a` is the per-task index. Use both in log filenames so output files do not collide.
- Inside the script, `${SLURM_ARRAY_TASK_ID}` indexes into the parameter list. Keep the parameter array in the script for reproducibility, or read from a file: `LR=$(sed -n "$((SLURM_ARRAY_TASK_ID + 1))p" params.txt)`.

## Dependencies

Chain jobs with `--dependency=`. Common forms:

- `afterok:<jobid>` — downstream runs only after the upstream succeeds (exit 0).
- `afterany:<jobid>` — downstream runs after the upstream completes regardless of exit code (useful for cleanup or post-mortem steps that should run even on failure).
- `afternotok:<jobid>` — downstream runs only if the upstream failed (alerting, retry-with-different-params).
- `singleton` — only one job with the same name and user runs at a time (good for serializing periodic tasks).

Worked example — preprocess, then train, then evaluate:

```bash
PREP=$(sbatch --parsable preprocess.sbatch)
TRAIN=$(sbatch --parsable --dependency=afterok:${PREP} train.sbatch)
sbatch --dependency=afterok:${TRAIN} evaluate.sbatch
```

Add a cleanup step that always runs after training:

```bash
sbatch --dependency=afterany:${TRAIN} cleanup.sbatch
```

Add an alert step that only runs on failure:

```bash
sbatch --dependency=afternotok:${TRAIN} notify_failure.sbatch
```

Notes:

- `sbatch --parsable` prints just the numeric job ID, which is easy to capture in a shell variable. Without it, you would need to parse `Submitted batch job <id>`.
- Keep each pipeline stage in its own script. Monolithic stages obscure which step failed and force re-running unrelated work.
- A pending job whose dependency is never satisfied stays in the queue with `REASON=DependencyNeverSatisfied`. Inspect with `squeue -j <jobid>` and cancel with `scancel <jobid>` once you decide not to wait.
