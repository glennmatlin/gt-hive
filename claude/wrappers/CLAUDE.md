# CLAUDE.md — gt-hive wrapper

This wrapper is the always-on context layer for Claude Code in the gt-hive
workspace. Keep it short; load procedures from `slurm-core`, `pace-phoenix`,
or `pace-ice` skills on demand.

## Routing guidance

Generic Slurm question (no specific cluster named):
- Load `slurm-core` only.

Georgia Tech / PACE / Phoenix mentioned (Phoenix-specific facts):
- Load `slurm-core` + `pace-phoenix`.

Georgia Tech / PACE / ICE mentioned (instructional cluster, coursework, grading):
- Load `slurm-core` + `pace-ice`.

The agent should never load both `pace-phoenix` and `pace-ice` simultaneously —
they are mutually exclusive site overlays.

## Always-on rules

- Never invent a local account, partition, QOS, module name, or filesystem
  path. Use `VERIFY_ON_SITE` (portable) or `VERIFY_ON_PACE` (GT-specific) for
  values the user has not provided. Pair the marker with the discovery
  command (`pace-quota` for accounts, `module avail` for modules).
- Prefer long-form Slurm directives in beginner-facing examples.
- Debugging starts from evidence: batch script, `sacct`, `squeue`, stdout,
  stderr — not speculation.
- Never include secrets, private keys, API tokens, or credentials in prompts
  or generated scripts.
- Recommend the user review every shell command before running it on a
  shared cluster.
- For Phoenix work, always include the account flag (`-A gts-<PI>`) and an
  explicit QOS (`-q inferno` or `-q embers`). For ICE work, never use `-A`
  (jobs are free) and do not manually specify a partition (auto-routed).

## Where things live

- Skills: `skills/slurm-core/`, `skills/pace-phoenix/`, `skills/pace-ice/`
- Eval test lists (trigger contract): `evals/triggers/`
- Architecture decisions: `docs/architecture-patterns.md`
- Publish boundary: `docs/superpowers/specs/2026-04-24-publish-boundary-security-design.md`
- Skill layering spec: `docs/superpowers/specs/2026-04-25-skill-layering-design.md`

## Resource files

For each skill, see its `references/` subdirectory. Notable shared references:

- `skills/slurm-core/references/shell-hygiene.md` — SSH multiplexing and the
  two-terminal pattern for AI-assisted Slurm work.
- `skills/pace-phoenix/references/cost-model.md` — Phoenix billing model
  (`inferno` paid, `embers` free, charge accounts).
- `skills/pace-phoenix/references/gt-ai-policy.md` — institutional GT AI
  guidance (also relevant for ICE users).
