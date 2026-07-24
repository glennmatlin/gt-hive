# Cost Model (Planning)

This skill uses a planning estimate, not billing data.

## Scope

- Primary target: Phoenix research jobs.
- ICE is treated as backup/fallback; no fixed dollar model is enforced here.

## Phoenix cost assumptions

1. Jobs in `inferno` are billed.
2. Jobs in `embers` are modeled as `$0` (backfill/preemptible guidance from docs).
3. CPU-focused jobs are estimated in CPU-hours.
4. GPU-focused jobs are estimated in GPU-hours.

## Formulas

- `CPU-hours = (requested CPU count) * (walltime in hours)`
- `GPU-hours = (requested GPU count) * (walltime in hours)`
- `Estimated cost = usage-hours * user-supplied rate`

Rates are intentionally externalized because pricing can change.

## Required user inputs for dollar estimates

- `--rate-cpu-hour` for CPU jobs
- `--rate-gpu-hour` for GPU jobs

Without rates, the script still reports estimated billed usage hours.

## Caveats

- The scheduler may place jobs on different partitions/resources than initially expected.
- Policies and rates can change; always verify with current PACE documentation or support.
- This model does not account for failed jobs, reservation policies, or special account agreements.
