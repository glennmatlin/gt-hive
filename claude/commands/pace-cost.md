---
name: pace-cost
description: Estimate the Phoenix charge for a job (GPU or CPU, hours, optional QOS). Args or wizard.
---

# cost estimator

Compute the Phoenix charge for a job. The command is a hybrid: it accepts
positional arguments for fast use, and falls into a wizard if invoked with
no arguments.

## Step 1: parse the arguments

`$ARGUMENTS` is the user's invocation tail. Two cases:

**Case A — `$ARGUMENTS` is non-empty.** Parse it as
`<gpu-or-cpu> <hours> [qos] [rate]`. Examples:

- `/gt-hive-pace:pace-cost h100 4` -> 1× H100, 4 hours, default QOS, no rate
  supplied (returns billed usage hours only).
- `/gt-hive-pace:pace-cost cpu 24 embers` -> CPU job, 24 hours, free `embers` QOS
  (always $0).
- `/gt-hive-pace:pace-cost h200 0.5 inferno 2.50` -> 1× H200, 30 minutes
  (fractional hours are supported), paid QOS, $2.50/GPU-hour user-supplied
  rate.

If the args do not parse, ask the user to clarify and skip to Case B.

**Case B — `$ARGUMENTS` is empty.** Use `AskUserQuestion` to collect four
inputs: resource (GPU type or CPU), hours (fractional allowed), QOS
(`inferno` paid / `embers` free / unsure), and optional per-hour rate.

## Step 2: redirect ICE callers

If the user mentions ICE, the answer is one line: ICE jobs are free —
there is no charge model and no estimator. Stop.

## Step 3: load `pace-phoenix` and read the cost model

Load the `pace-phoenix` skill. Read
`pace-phoenix/references/cost-model.md` for the cost **formula**
(`usage-hours = (resource count) * (walltime hours)`,
`estimated cost = usage-hours * user-supplied rate`), the `inferno` paid
vs `embers` free rules, and the `--rate-cpu-hour` / `--rate-gpu-hour`
inputs the model expects.

The cost model intentionally externalizes hourly rates because PACE
pricing changes; do not hard-code a rate. The user must supply one (in
`$ARGUMENTS` or via the wizard) or this command falls back to
usage-hours only.

## Step 4: compute and report

Compute usage hours from the cost-model formula. Two cases for the
report:

**With a user-supplied rate:** `estimate = usage-hours * rate`. Report:

> **Estimate:** $X.XX for <hours> h on <resource> (QOS: <qos>, rate $<rate>/h).
>
> <free or paid line>: `embers` is free; `inferno` is paid against your
> `gts-*` charge account.
>
> Rates change. If accuracy matters, re-check `cost-model.md` and
> `pace-quota` on the cluster.

**Without a rate:** report usage hours only and prompt for a rate:

> **Usage:** <usage-hours> billed hours for <hours> h on <resource>
> (QOS: <qos>).
>
> No rate supplied — re-run with a rate (e.g. `/gt-hive-pace:pace-cost <res>
> <hours> <qos> <rate>`) or check current PACE pricing for a $ figure.

If the user supplied no QOS, default to `inferno` for the estimate but
flag both options in the response. `embers` always reports $0 regardless
of rate.
