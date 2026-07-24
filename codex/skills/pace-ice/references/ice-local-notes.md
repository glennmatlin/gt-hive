# ICE Local Notes

Site-specific facts about the ICE cluster, cross-checked against
`docs/PACE Documentation/`. Anything not corroborated by an upstream doc
is flagged inline. Routing and doc-index information lives in
`pace-docs-map.md` and `doc-index.md`, not here.

## Storage

Three distinct storage tiers, each with its own ICE policy
(per `PACE - External - Storage on ICE.md`):

- **Home (`~`):** 30 GB on OIT NetApp; **daily snapshot** for accidental
  recovery; deleted after 1 year of no ICE login. For code, configs,
  small data only — many tools write into `~` and will fail when the
  quota fills.
- **Scratch (`~/scratch`):** 300 GB on a Lustre parallel filesystem with
  InfiniBand; **not backed up**; **120-day cleanup at semester end** —
  any file untouched for 120 days is removed. **1M file/dir cap.**
  Suitable for course datasets and intermediate results that do not need
  to outlive the term.
- **Job-local (`${TMPDIR}`):** per-job NVMe or SAS local disk; freed at
  job exit. Reserve with `#SBATCH --tmp=<size>` and pin the family with
  `-C localNVMe` or `-C localSAS` when needed.
- **Course shared directories:** VAST storage, **2 TB default**, files do
  not count against individual user quotas. Instructors and TAs request
  these from PACE; the request workflow itself is a known gap (point
  users at `pace-support@oit.gatech.edu`). Some courses opt for Lustre
  shared dirs; in that case files count against the owner's scratch quota.
  The exact shared-directory path for a given course is site-specific —
  mark it `VERIFY_ON_PACE` in generated examples rather than guessing.

## Partition mapping (auto-routed)

ICE picks the partition automatically by the user's college affiliation
and the requested resources. Users should **not** name a partition with
`-p` / `--partition`. Five partition pairs exist
(per `PACE - External - ICE Cluster Resources.md`):

- **`ice-cpu` / `ice-gpu`** — open to everyone, lower priority. Always
  considered as a fallback.
- **`coc-cpu` / `coc-gpu`** — College of Computing priority.
- **`pace-cpu` / `coe-gpu`** — College of Engineering / AI Makerspace
  priority. Includes the 14 reserved 8xH100 nodes.
- **`pace-cpu` / `pace-gpu`** — non-CoC/CoE courses.

Multi-college students default to one priority partition; optional
override QOS (`-q coc-ice` / `-q coe-ice` / `-q pace-ice`) can pin the
priority queue.

## GPU per-node maxima

From `PACE - External - ICE Cluster Resources.md` and
`PACE - External - Using Slurm on ICE.md`:

| GPU type | Memory | Per-node max | CPU notes |
|----------|--------|--------------|-----------|
| V100 | 16 GB / 32 GB | 4 | Intel Xeon Gold 6248 |
| Quadro Pro RTX6000 | 24 GB | 4 | Intel Xeon Gold 6226 |
| A40 | 48 GB | 2 | AMD EPYC 7452 |
| A100 | 40 GB / 80 GB | 2 | AMD EPYC 7513/7452 |
| H100 SXM5 | 80 GB | 8 | Intel Xeon Platinum 8462Y+; 14 nodes reserved for CoE/AI Makerspace |
| H200 SXM5 | 142 GB | 8 | Intel Xeon Platinum 8462Y+; 12 nodes reserved for CoE/AI Makerspace |
| L40S | 48 GB | 8 | Intel Xeon Gold 6548Y+ |
| RTX6000 Pro Blackwell | 48 GB | 16 | Intel Granite Rapids 6740P |
| MI210 | 64 GB | 2 | AMD EPYC 7452; AMD GPU — `rocm-smi` and `hipcc --offload-arch=gfx90a` |

Scheduler reserves 8 GB per node for system processes; budget memory
requests accordingly.

## Walltime and per-job caps

From `PACE - External - Using Slurm on ICE.md`:

- **Default request if unspecified:** 1 core, 1 GB/core, 1 hour wallclock.
- **Per-job CPU cap:** 512 CPU-hours.
- **Per-job GPU cap:** 16 GPU-hours.
- **CPU walltime cap:** 18 hours.
- **GPU walltime cap:** 16 hours.

Grading QOS (instructors and TAs only — `-q coc-grade` / `-q coe-grade` /
`-q pace-grade`) bumps these to:

- 24-hour walltime.
- 768 CPU-hours / 24 GPU-hours per job.
- 10 concurrent jobs cap.

## Module conventions

Use base names; pin versions only after `module avail` confirms
availability:

- `module load anaconda3` — base name documented in the Slurm-on-ICE
  examples. Available versions drift each semester.
- `module load cuda` — base name for CUDA. The Slurm-on-ICE GPU example
  loads `cuda` (and `gcc` is loaded by default in interactive sessions).

The ICE software stack page references a "RHEL9 Software Stack" KB article
(per `PACE - External - Getting Started with ICE.md`) but the surveyed
docs do not enumerate the available modules. Use `module avail` on the
cluster as ground truth. Course-specific or group-specific module names
should be marked `VERIFY_ON_PACE` rather than guessed.

## AI Makerspace note

`PACE - External - ICE Cluster Resources.md` (footnotes 2 and 3) reserves
14 of the 8xH100 SXM5 nodes and 12 of the 8xH200 SXM5 nodes for CoE / AI
Makerspace users. The same doc states CoE courses and AI Makerspace
users have access via the `pace-cpu` / `coe-gpu` partition pair.

What is **not** documented in repo: the exact access path — who counts as
an "AI Makerspace user" beyond "CoE student/course," whether enrollment
or a separate ticket is required, how reservations interact with default
auto-routing for the unreserved subset of H100/H200 nodes. Treat this
as a known gap. Point users at PACE support
(`pace-support@oit.gatech.edu`) instead of fabricating steps.

## Notable facts

- **Login endpoint:** `ssh <gt_username>@<gt-login-host-redacted>`.
  GlobalProtect VPN required from off-campus.
- **Open OnDemand:** `https://ondemand-ice.pace.gatech.edu/` (per
  `PACE - External - Open OnDemand Guide.md` and the Storage-on-ICE
  doc).
- **Globus collection:** `PACE ICE access` (per
  `PACE - [GT-login-only] - Using Globus to Transfer Files.md`).
- **No `-A` flag:** ICE jobs do not specify a charge account. Importing
  the `-A gts-...` habit from a research cluster is a routing-time
  mistake to flag and strip.
- **No manual `-p` / `--partition`:** auto-routing handles it. Manual
  partition selection works against the routing logic.
- **GPU memory request convention:** PACE explicitly recommends
  `--mem-per-gpu=<size>` over total `--mem` for GPU jobs.
- **ICE-specific tools:** `pace-quota`, `pace-check-queue <partition>`,
  `pace-job-summary <jobid>`. These ship on ICE login and compute
  nodes; do not assume they exist elsewhere.

## What to verify locally before final submission

- Local module names and available versions (`module avail`).
- Whether the default-routed partition is saturated
  (`pace-check-queue ice-cpu` or the priority-queue equivalent).
- Whether a course has a shared directory you should be writing into
  (course staff usually announces this).
- Whether your enrollment qualifies you for a college-priority QOS
  override or grading QOS.
