# Debugging Slurm Jobs

Worked debugging procedures expanding the SKILL.md "Evidence checklist for debugging" section. The frame is **evidence over speculation**: collect the artifacts before proposing fixes. Site-local values (account, partition, modules) stay `VERIFY_ON_SITE`; user-supplied values use `<angle_brackets>`.

## Failed jobs

When a job has stopped and the user asks "why did it fail?", inspect in this fixed order. Do not skip ahead — each step rules out a class of cause.

1. **Read the batch script.** Confirm the resource request, module loads, working directory, and the actual command being run. Many "failures" are scripts that ran exactly as written.
2. **Run `sacct` for the job summary.** A first-pass invocation:

   ```bash
   sacct -j <jobid> -X \
     --format=JobID,JobName,State,ExitCode,Elapsed,Timelimit,NodeList,MaxRSS,ReqMem
   ```

   `-X` collapses job steps to one row per job for triage. Add `MaxRSS,ReqMem` when you suspect memory pressure; add `Start,End` when you suspect a timeout.
3. **Read stderr, then stdout.** `logs/<job>.err` is the fastest path to a Python traceback, missing-file error, or CUDA OOM. Only fall back to stdout if stderr is empty.
4. **Check environment setup.** Inspect the `module purge` / `module load` lines, any `conda activate` or `source venv/bin/activate`, and the effective `PATH`. A wrong module version is a common silent failure mode.
5. **Propose the smallest safe fix.** One change at a time — bumping `--mem`, fixing a path, swapping a module — so the next run isolates the variable.

### Reading `ExitCode`

`sacct` reports `ExitCode` as `<script_exit>:<signal>` — read both halves; one being zero does not exonerate the other.

- `ExitCode=0:0` — clean exit code, no signal. If results are missing despite this, suspect the script ran but produced no output (wrong cwd, silent early-return, output redirected to a path that does not exist).
- `ExitCode=N:0` (script exit `N`, no signal) — the program returned a non-zero exit code. stderr is the fastest path to root cause; treat it as an application-level failure (Python traceback, non-zero return from a CLI tool, `set -e` tripping a shell command).
- `ExitCode=0:M` (killed by signal `M`) — the kernel or scheduler terminated the job before it could exit. Common signals:
  - `9` (`SIGKILL`) — almost always the OOM-killer; check `MaxRSS` against `ReqMem` in the `sacct` row.
  - `15` (`SIGTERM`) — usually time-limit hit; compare `Elapsed` against `Timelimit`. Slurm sends `SIGTERM` first, then `SIGKILL` after a grace period.
  - `11` (`SIGSEGV`) — segfault in native code; reproduce under `salloc` with the same module set if possible.

When both halves are non-zero (`N:M`), the script returned `N` *and* the job was killed by signal `M` — usually a child process crashed and the wrapping shell propagated the signal. Investigate the signal first; the exit code is downstream.

### Common failure categories

Run through this list before proposing a fix — most failures fall into one bucket:

- **Missing path** — input file, output dir, or scratch path does not exist on the compute node.
- **Wrong environment** — module not loaded, conda env not activated, or `PATH` clobbered by a stale `~/.bashrc`.
- **Bad resource request** — wrong partition, GPU constraint that does not match the partition, or feature not available on requested nodes.
- **Time too short** — `Elapsed` equals `Timelimit` and `ExitCode=0:15`.
- **Memory too small** — `MaxRSS` near or above `ReqMem`, often paired with `ExitCode=0:9`.
- **Dependency unsatisfied** — parent job failed; child shows `REASON=DependencyNeverSatisfied` until cancelled.
- **Wrong working directory** — relative paths resolved against `$HOME` or the submit dir instead of the expected project root.

### Worked example — OOM kill

User reports: "my training job died after 40 minutes." `sacct` says:

```
JobID  State   ExitCode  Elapsed   Timelimit  MaxRSS  ReqMem
12345  FAILED  0:9       00:40:12  04:00:00   31.8G   32G
```

Reading: `ExitCode=0:9` (signal 9 = `SIGKILL`), `Elapsed << Timelimit` (so not a timeout), `MaxRSS` (31.8 G) is right at `ReqMem` (32 G). Diagnosis: OOM-killer. Fix: bump `--mem` to `48G` and re-run; if it OOMs again, profile peak memory rather than guessing higher.

## Pending jobs

When a job is stuck in `PD` (pending), the scheduler is telling you why — but the default `squeue` output truncates the reason. Use a wide format:

```bash
squeue -j <jobid> -o '%i %T %r %S %M %l %D %R'
```

Field meanings: `%i` JobID, `%T` State, `%r` Reason, `%S` start-time estimate, `%M` time-used, `%l` time-limit, `%D` nodes, `%R` reason-or-nodelist.

### Reason interpretation

- `Priority` / `Resources` — normal queueing; the request is valid, the cluster is busy. Compare `%S` (estimated start) against acceptable wait.
- `Dependency` — waiting on a parent job. Check the parent's state with `sacct -j <parent_jobid>`.
- `DependencyNeverSatisfied` — parent failed and the child will never start. Cancel with `scancel <jobid>` and resubmit after fixing the parent.
- `QOSMaxJobsPerUserLimit` / `AssocMaxJobsLimit` — rate-limited by QOS or association. Wait for running jobs to drain, or reduce concurrency.
- `AssocGrpCPUMinutesLimit` / `AssocGrpGRES` — hit an allocation cap (CPU-minutes, GPU-hours). Check the account's remaining balance with the local quota tool (`VERIFY_ON_SITE`).
- `ReqNodeNotAvail` / `Reservation` — the requested constraint, feature, or reservation does not match available nodes. Re-examine `--constraint=` / `--gres=`.
- `JobHeldUser` / `JobHeldAdmin` — the job is held; release with `scontrol release <jobid>` (user) or contact the admin.

### Walk the request

If the reason is `Resources` and the wait estimate is implausibly long, the request is probably oversized for the partition. Walk through:

1. **Resource realism** — is the GPU type, walltime, or memory request larger than what a single node on this partition can satisfy? `sinfo -p <partition> -o '%P %D %c %m %G %l'` shows per-partition node counts, CPUs, memory, GRES, and time-limit.
2. **Dependency state** — `sacct -j <parent>` to confirm the parent is actually running, not pending behind its own dependency. A chain of pending jobs can hide a single root cause several levels up.
3. **Account / QOS** — does the account have allocation remaining? Is the QOS valid for this partition? Re-read the submission command for typos in `--account=` or `--qos=`.
4. **Time limit** — some partitions cap walltime; a 24h request on a 4h partition will sit forever with `ReqNodeNotAvail` or similar.

## Evidence checklist

When a user asks "why did this fail?" — collect this evidence before proposing fixes. Each item rules out an ambiguity; missing items mean guessing.

1. **The batch script** — full contents, including all `#SBATCH` directives.
2. **`sacct -j <jobid> -X`** — the summary row with `JobID,JobName,State,ExitCode,Elapsed,Timelimit,NodeList,MaxRSS,ReqMem`.
3. **`squeue -j <jobid>`** — only if the job is still pending; include the wide format above so the reason field is not truncated.
4. **stdout** — `logs/<job>.out` (or whatever `--output` resolved to).
5. **stderr** — `logs/<job>.err`. Read this first when triaging.
6. **The exact submission command** — `sbatch <script>` with any CLI overrides; CLI flags override `#SBATCH` directives silently.
7. **Module / env activation lines** — the `module load`, `conda activate`, `source` commands actually run inside the job.
8. **Working directory** — what `pwd` resolves to inside the job (often the submit dir, but not guaranteed).
9. **Inputs the script reads** — paths, contents (or sizes), and whether they exist on the compute node.

If any item is missing, ask for it before guessing. The exit code is a fact; the reason field is a fact; a hypothesis built without them is speculation.
