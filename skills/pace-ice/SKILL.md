---
name: pace-ice
description: Georgia Tech PACE ICE specifics — "ICE", login-ice, instructional or coursework workloads, and grading workflows. Always pair with slurm-core for portable Slurm; not for Phoenix (that's pace-phoenix).
---

# PACE ICE Overlay

This skill is the ICE-specific overlay for Georgia Tech PACE. It adds site
facts that `slurm-core` deliberately does not know.

## What this overlay adds

Load this skill when the user is working on (or asking about) the PACE ICE
cluster — the **instructional** PACE cluster at Georgia Tech for
credit-bearing coursework, TA grading workflows, and GT-hosted workshops.
ICE is **free** to GT students and instructors with a valid GT account; no
charge account is configured and no `-A` flag is required.

The layered model is: **load `slurm-core` for portable Slurm patterns**
(sbatch, srun, salloc, sacct, job arrays, dependencies, debugging
checklists), **plus this overlay for ICE-specific account/QOS/storage/policy
decisions**. Do not duplicate `slurm-core` content here; reference it
instead.

Ground truth for every claim in this skill is `docs/PACE Documentation/`
(an export of the official PACE knowledge base). When in doubt, re-verify
against those docs and cite the specific page used.

## When to use ICE

Route to this overlay when any of the following apply:

- **Credit-bearing course context** — a course Slurm assignment, course
  project, or in-class lab.
- **Teaching/grading workflows** — instructor or TA grading scripts that
  need cluster compute.
- **GT-hosted workshops or training** — short-form classroom sessions
  using PACE.
- **Explicit user mention** of ICE, `<gt-login-host-redacted>`, the
  instructional cluster, or OnDemand at
  `https://ondemand-ice.pace.gatech.edu/`.

Do NOT use this overlay for:

- **Production research workflows** — those go to the `pace-phoenix`
  overlay (paid research cluster with charge accounts and explicit QOS
  selection).
- **Generic Slurm questions without a cluster named** — those use
  `slurm-core` alone, with no site overlay.

## Routing

- **Use this overlay alone** for: ICE login/portal pointers, partition
  auto-routing rules, college-priority and grading QOS choice, GPU type
  selection, storage-tier guidance, semester-cleanup caveats, and the
  no-`-A`-flag rule.
- **Pair with `slurm-core`** for: writing the actual `sbatch` script,
  interactive `salloc`/`srun` workflows, job arrays, dependencies,
  sacct/squeue debugging — anything portable across Slurm clusters.
  ICE-specific values (no `-A`, optional `-q coc-ice`/`coe-ice`/`pace-ice`,
  `--gres=gpu:<TYPE>:N`, `-C intel`/`-C amd`/`-C graniterapids`) come from
  this overlay; the surrounding Slurm scaffolding comes from `slurm-core`.

## Operating defaults

- **Login endpoint:** `<gt-login-host-redacted>`
  (`ssh <gt_username>@<gt-login-host-redacted>`).
- **VPN:** GlobalProtect required from off-campus.
- **OnDemand portal:** `https://ondemand-ice.pace.gatech.edu/`.
- **No `-A` (account) flag** — ICE is free; jobs do not specify a charge
  account. Importing the `-A gts-...` habit from a research cluster is a
  routing-time mistake.
- **Auto-routed partitions** — users should NOT specify `-p` /
  `--partition` manually. ICE picks the partition by college affiliation
  and resource constraints (GPU type, CPU architecture).
- **Default request if unspecified:** 1 core, 1 GB/core, 1 hour wallclock.
- **Per-job caps:** 512 CPU-hours / 16 GPU-hours per job; 18-hour CPU
  walltime / 16-hour GPU walltime.
- **Globus collection:** `PACE ICE access`.

## Cluster facts

### Partitions and QOS

ICE has five partition pairs, all selected automatically:

- **`ice-cpu` / `ice-gpu`** — open to everyone, lower priority.
- **`coc-cpu` / `coc-gpu`** — College of Computing priority.
- **`pace-cpu` / `coe-gpu`** — College of Engineering / AI Makerspace
  priority.
- **`pace-cpu` / `pace-gpu`** — non-CoC/CoE courses.

Users do not name these directly. Auto-routing picks one based on the
user's college and the requested resources.

**Optional priority-override QOS** — use only when the default routing is
not fast enough:

- `-q coc-ice` — CoC-priority queue (CoC users).
- `-q coe-ice` — CoE-priority queue (CoE users).
- `-q pace-ice` — non-CoC/CoE priority queue.

**Grading-priority QOS** (instructors and TAs only):

- `-q coc-grade` / `-q coe-grade` / `-q pace-grade`
- 24-hour walltime, 768 CPU-hours / 24 GPU-hours per job, 10 concurrent
  jobs cap.
- ICE-only — there is no analog on the research cluster.

### CPU partitions and constraints

Pin CPU architecture only when needed:

- `-C intel` — Intel CPUs.
- `-C amd` — AMD CPUs (note: A40/A100/MI210 GPU nodes have AMD CPUs).
- `-C graniterapids` — newest-generation Intel Granite Rapids CPUs.

### GPU types

Available GPU families on ICE, with notable per-node maxima:

| GPU type | Memory | Per-node max | Notes |
|----------|--------|--------------|-------|
| V100 | 16 GB / 32 GB | 4 | |
| Quadro Pro RTX6000 | 24 GB | 4 | |
| A40 | 48 GB | 2 | AMD CPUs |
| A100 | 40 GB / 80 GB | 2 | AMD CPUs |
| H100 SXM5 | 80 GB | 8 | 14 nodes reserved for CoE/AI Makerspace |
| H200 SXM5 | 142 GB | 8 | 12 nodes reserved for CoE/AI Makerspace |
| L40S | 48 GB | 8 | |
| RTX6000 Pro Blackwell | 48 GB | 16 | |
| AMD MI210 | 64 GB | 2 | |

Directive form is `--gres=gpu:<TYPE>:N` (e.g. `--gres=gpu:H100:1`,
`--gres=gpu:V100:2`). AI Makerspace H100/H200 reservations are documented
in `docs/PACE Documentation/PACE - External - ICE Cluster Resources.md`,
but the full **access semantics** (who qualifies, how to opt into the
reservation pool) are a known gap (see safety rules below).

### Storage tiers

- **Home (`~`):** 30 GB on NetApp; daily snapshots; 1-year inactivity
  cleanup. For code, configs, small data only.
- **Shared project volume (`/storage/ice-shared/cs7634/staff/TDA`):** the
  destination for persistent data artifacts and results. This is where
  keepers go.
- **Scratch (`~/scratch`):** 300 GB on Lustre; **no backup**; 120-day
  cleanup at semester end; 1M-file cap. Use for **environments only**
  (venv, uv cache) — not for data artifacts you need to keep.
- **Job-local (`${TMPDIR}`):** per-job NVMe or SAS; request with
  `-C localSAS` or `-C localNVMe`; freed at job exit. Fastest tier for
  I/O-heavy in-job staging.
- **Course shared directories:** VAST, 2 TB default; instructor request
  workflow (the procedure itself is a known gap — point users at
  `pace-support@oit.gatech.edu`).

Stage hot data into `${TMPDIR}` for I/O-heavy steps; copy results and data
artifacts to the shared project volume
(`/storage/ice-shared/cs7634/staff/TDA`) before the job ends. Do **not**
write data to home (`~`) or scratch (`~/scratch`) — scratch is for
environments only. The canonical storage rule lives in the global
`agents/AGENTS.md`.

## ICE-specific safety rules

- **Do not use `-A` (account) flag on ICE.** ICE jobs are free and do not
  charge an account. If a script carries `-A gts-...` from a research
  cluster, strip it before submitting.
- **Do not specify `-p` / `--partition` manually.** ICE auto-routes by
  college and resource constraints. Manual partition selection works
  against the routing logic.
- **For instructor/TA grading workloads, request a grading QOS**
  (`-q coc-grade` / `-q coe-grade` / `-q pace-grade`). Default routing is
  for student work.
- **Use `VERIFY_ON_PACE` for user/group-specific values** that are not in
  PACE docs. Examples:
  - the user's college affiliation if it affects routing:
    `# college=VERIFY_ON_PACE` (auto-routing handles this for you, but
    surface it when relevant)
  - course-shared-directory path: `--chdir=VERIFY_ON_PACE`
  - module versions: `module load VERIFY_ON_PACE`
  Do **not** use `VERIFY_ON_PACE` for documented public constants
  (the login endpoint, public GPU types, partition names, grading QOS
  names). Those are stable and should be named outright.
- **Filter ServiceNow boilerplate** when reading from cleaned PACE docs —
  ignore lines like `Was this article helpful`, `ASC Most Viewed`,
  `Copy Permalink`. They are export artifacts, not content.
- **AI Makerspace reservations affect H100/H200 availability.** 14 of the
  H100 SXM5 nodes and 12 of the H200 SXM5 nodes are reserved for CoE/AI
  Makerspace use. If a job pends on those, the access path is
  institution-specific and not fully documented in repo (known gap — point
  users to PACE support rather than fabricate steps).
- **Scratch is wiped at semester end** (120-day cleanup) and is for
  environments only. Never write data artifacts to scratch or home; copy
  keepers to the shared project volume
  (`/storage/ice-shared/cs7634/staff/TDA`). See the global `agents/AGENTS.md`
  for the canonical storage rule.

> Institutional GT AI guidance is tracked separately, not in this section.
> The policy is institution-wide and identical for both clusters, so it
> lives in a single file: `pace-phoenix/references/gt-ai-policy.md`.

## Phoenix vs ICE

For users unsure which overlay applies — a one-paragraph disambiguation:

- **Phoenix** = research, paid, charge account required (`-A gts-...`),
  explicit QOS (`inferno` / `embers`), login at
  `<gt-login-host-redacted>`. Use for production research workloads.
- **ICE** = instructional, **free**, no `-A` flag, partitions
  auto-routed, login at `<gt-login-host-redacted>`. Use for coursework,
  TA grading, and GT-hosted workshops.

If the request is research production, route to the `pace-phoenix`
overlay. If it is coursework, grading, or workshop, stay here.

## Build responses in this order

1. **Recommend the workflow** with the minimal steps to execute the
   user's task safely (which login host, which QOS if any, where to run
   from). Default to the auto-routed path.
2. **Provide command/script templates** with placeholders
   (`<gt_username>`, paths) and `VERIFY_ON_PACE` markers for
   user/group-specific values the AI must not invent. **No `-A` flag. No
   manual `-p` / `--partition`.**
3. **Include QOS tradeoffs** — default routing vs college-priority
   override vs grading QOS — and call out per-job and walltime caps.
4. **Add caveats** — data-handling per `gt-ai-policy.md`, semester-end
   scratch cleanup, AI Makerspace reservation impact on H100/H200,
   instructor-only grading QOS.
5. **Cite the specific PACE doc(s) used** so the user can verify and
   update if facts have drifted.

## Resource files

The shared institutional AI guidance lives at
`pace-phoenix/references/gt-ai-policy.md` — the same policy applies to both
clusters, so the file is not duplicated.

- `references/workflows.md` — ICE-specific job templates (CPU, GPU,
  grading QOS, OnDemand).
- `references/ice-local-notes.md` — non-routing local facts (semester
  cleanup, scratch caveats, AI Makerspace reservation notes).
- `references/pace-docs-map.md` — routing map into the authoritative ICE
  docs (`Getting Started with ICE`, `Log on to ICE`, `ICE Cluster
  Resources`, `Storage on ICE`, `Using Slurm on ICE`).
