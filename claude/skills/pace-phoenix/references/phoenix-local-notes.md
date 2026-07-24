# Phoenix Local Notes

Site-specific facts about the Phoenix cluster, cross-checked against
`docs/PACE Documentation/`. Anything not corroborated by an upstream doc
is flagged inline. Routing and doc-index information lives in
`pace-docs-map.md` and `doc-index.md`, not here.

## Storage

Three distinct storage tiers, each with its own policy
(per `PACE - [GT-login-only] - Storage Guide.md` and
`PACE - External - Use Job-Specific Local Scratch Storage.md`):

- **Home (`~`):** 20 GB quota, 1M file/dir cap, **backed up**. Symlinks to
  project storage and scratch are created here. Do not store large datasets
  in home; many tools write into `~` and will fail when the quota fills.
- **Network scratch (`~/scratch`):** 15 TB quota, 1M file/dir cap,
  **not backed up**. Files older than 60 days are deleted automatically each
  month. Use for inputs/outputs that must outlive a single job but do not
  need long-term retention.
- **Project storage:** group-shared directory funded per PI; symlinks
  appear in home as `p-<pi-username>-<n>` or `r-<pi-username>-<n>`. New
  accounts since April 2025 use the `r-...` form pointing at
  `/storage/project/p-<pi-username>-<n>/<username>`. Project storage has no
  per-user file count limit and is the right home for long-term datasets.
- **Job-local scratch (`${TMPDIR}`):** per-job local disk, fast, freed at
  job exit. Reserve with `#SBATCH --tmp=<size>`. Use the `trap` pattern to
  copy results out before the job ends.

## Charge accounts

Phoenix charge accounts follow the `gts-<PI UID>[-<descriptor>]` taxonomy
(per `PACE - [GT-login-only] - Using Slurm on Phoenix.md`):

- `gts-<PI UID>` — institute-sponsored free-tier account; resets monthly.
- `gts-<PI UID>-CODA20` — credits from the 2020 Coda hardware refresh.
- `gts-<PI UID>-FY20PhaseN` — credits for hardware purchased in FY20.
- `gts-<PI UID>-<group>` — child of a shared multi-PI or school account.
- `gts-<PI UID>-<custom>` — postpaid (billed monthly on actual usage).
- `gts-<group>-CODA20` — parent shared account; cannot submit jobs to it
  directly, only its children.

Discover yours with `pace-quota`. Do not invent an account name; substitute
`<PI>` only after `pace-quota` confirms the account exists. If the user has
not provided a charge account, leave the literal token `VERIFY_ON_PACE` in
the example (e.g. `-A VERIFY_ON_PACE`) so it is grep-visible before submission.

## Module names (base names, no version pinning)

- `module load anaconda3` — documented base name. Pin a version
  (e.g. `anaconda3/2024.06`) only after confirming with
  `module avail anaconda3` on the cluster, since available versions drift.
- `module load cuda` — documented base name for CUDA on Phoenix. Same rule:
  `module avail cuda` first if you need a specific CUDA version.

The PACE docs themselves contain example versions (e.g. `anaconda3/2022.05`)
that are now stale; treat versioned examples in this skill as illustrative.
Group-specific module names (per-lab software stacks beyond `anaconda3` and
`cuda`) should be marked `VERIFY_ON_PACE` rather than guessed.

## Notable facts

- **Login endpoint:** `ssh <gt_username>@<gt-login-host-redacted>`.
- **Open OnDemand:** `https://ondemand-phoenix.pace.gatech.edu/` (requires
  GT VPN — see `PACE - External - Open OnDemand Guide.md`).
- **Free backfill QOS:** `embers` — preemptible after 1 hour, max 8 h
  wallclock; useful when work can checkpoint.
- **Paid QOS:** `inferno` — predictable runtime, billed against the charge
  account.
- **AMD CPU targeting:** `-C amd` is documented as the public constraint
  flag for AMD nodes.
- **GPU memory request convention:** PACE explicitly recommends
  `--mem-per-gpu=<size>` over total `--mem` for GPU jobs.
- **Phoenix-specific tools:** `pace-quota`, `pace-check-queue <q>`,
  `pace-job-summary <jobid>`. These ship on Phoenix login and compute
  nodes; do not assume they exist elsewhere.

## What to verify locally before final submission

- Whether a specific account is required (`pace-quota`).
- Whether a specific partition or QOS is required (`sinfo`,
  `pace-check-queue`).
- Local module names and available versions (`module avail`).
- Whether a lab or course has additional conventions not captured here.
