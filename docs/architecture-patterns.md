# Architecture Patterns

This document captures the architecture decisions for the layered-skill rollout
in `gt-hive`. The five patterns below — P01 through P05 — define how skills,
wrappers, triggers, placeholders, and tooling deliverables are structured so
the project remains portable, debuggable, and free of content drift.

For the broader rollout plan and phase-by-phase decomposition, see the master
spec at `docs/superpowers/specs/2026-04-25-skill-layering-design.md`. P01-P04
are synthesized from the workshop's resource library on layered AI agent
content; P05 is a `gt-hive`-specific solution to publishing the same source
file into multiple tool-specific deliverables (Codex, Claude) without
duplication.

Each pattern lists the **problem** it solves, where it is **adopted** in this
repo (with file pointers), and **gotchas** to watch out for.

## P01: Two-layer skill architecture

### Problem

A single skill that mixes portable Slurm knowledge with site-specific
Georgia Tech / PACE facts is hard to reuse, hard to test, and hard to
update. New cluster sites would require either forking the whole skill
(duplication) or polluting it with a growing tangle of conditionals
("on Phoenix do X, on ICE do Y, otherwise do Z"). The portable knowledge
also drifts as site facts change underneath it.

### Adoption

Skills split into a portable core layer plus optional site overlays:

- `skills/slurm-core/SKILL.md` — portable Slurm patterns: `sbatch`, `srun`,
  `salloc`, job arrays, dependency chains, evidence-first debugging. Works
  on any Slurm-managed cluster, not just PACE.
- `skills/slurm-core/references/{core-workflows,debugging,shell-hygiene}.md`
  — depth references for the core layer.
- `skills/pace-phoenix/SKILL.md` — Phoenix-specific overlay: `gts-<PI>` charge
  accounts, `inferno` / `embers` QOS, Phoenix GPU types, `pace-quota` /
  `pace-check-queue` tooling.
- `skills/pace-ice/SKILL.md` — ICE-specific overlay: no `-A` flag, partition
  auto-routing, college-priority QOS, grading QOS, ICE GPU layout.

A request for "generic Slurm help" loads `slurm-core` only. A request that
mentions Phoenix or PACE loads `slurm-core` plus `pace-phoenix`. ICE loads
`slurm-core` plus `pace-ice`. The two overlays are mutually exclusive.

### Gotchas

- Do not pollute `slurm-core` with site-specific terms. The body-only
  forbidden-term test in `tests/test_skill_scaffolding.py`
  (`SlurmCoreContent.test_forbidden_site_specific_terms_in_body`) blocks
  references to `Phoenix`, `ICE`, `PACE`, `Georgia Tech`, `pace-quota`,
  `inferno`, `embers` in the slurm-core body.
- Overlays must reference `slurm-core` for portable patterns rather than
  duplicating them. A `test_delegates_to_slurm_core` check enforces this.
- Resist the urge to merge overlays. Keep `pace-phoenix` and `pace-ice`
  separate — their rules differ enough (account flag vs no account flag,
  manual partition vs auto-routing) that combining them re-creates the
  conditional tangle the split was designed to avoid.

## P02: Thin always-on wrapper + on-demand skill

### Problem

If `CLAUDE.md` and `AGENTS.md` carry the full procedural knowledge for the
project, every conversation pays the always-on token cost — even ones that
have nothing to do with HPC. Procedures also drift faster than facts;
embedding them in always-on context forces a wrapper edit for every
content change.

### Adoption

Wrappers stay thin and route to skills:

- `wrappers/CLAUDE.md` — Claude Code always-on layer for the gt-hive
  workspace. Contains routing guidance ("Phoenix mention → load slurm-core
  + pace-phoenix"), a small set of always-on safety rules, and pointers to
  skills. Target length: 30-60 lines.
- `wrappers/AGENTS.md` — Codex (OpenAI) always-on layer. Same routing and
  safety rules as `CLAUDE.md`, plus a Codex-specific dotfiles pattern for
  approval-policy management. Target length: 30-60 lines.
- Skills (`skills/slurm-core/`, `skills/pace-phoenix/`, `skills/pace-ice/`)
  hold the actual procedures and load on demand when their triggers fire.
  Target length: 100-200 lines per `SKILL.md`, with depth in
  `references/*.md`.

### Gotchas

- If a wrapper grows past ~60 lines, that is a strong signal the new content
  belongs in a skill instead. Audit `wrappers/CLAUDE.md` and
  `wrappers/AGENTS.md` periodically.
- Wrappers should not duplicate skill procedures. They should point at
  skills and rely on the skill loading on demand.
- Routing guidance in wrappers must stay aligned with the trigger contracts
  in skill descriptions (P03). When in doubt, the trigger contract is the
  source of truth and the wrapper should mirror it.

## P03: Trigger contract

### Problem

Without explicit "use this skill when …" and "do not use this skill when …"
phrasing in the skill description, the agent guesses about activation —
loading skills that do not match the request, or failing to load one that
does. The result is wrong-cluster examples (Phoenix syntax for an ICE job),
silently missing context, or noisy over-loading.

### Adoption

Every `SKILL.md` description carries an explicit trigger contract with both
positive and negative phrasing, and a parallel test list in `evals/triggers/`
enumerates the prompts the contract should fire on:

- `skills/slurm-core/SKILL.md` — description includes "use when …" and
  "do not use … alone for Phoenix / ICE — use the appropriate site overlay".
- `skills/pace-phoenix/SKILL.md` — "use when … Phoenix / PACE / `gts-<PI>` /
  `inferno` / `embers` mentioned"; "do not use for ICE — that is pace-ice".
- `skills/pace-ice/SKILL.md` — "use when … ICE / `login-ice` / coursework /
  grading mentioned"; "do not use for Phoenix — that is pace-phoenix".
- `evals/triggers/{slurm-core,pace-phoenix,pace-ice,no-trigger}.md` —
  human-readable test lists. Each file enumerates positive prompts (should
  activate) and negative prompts (should not). `no-trigger.md` collects
  prompts that should activate no HPC skill at all.

The scaffolding test
`tests/test_skill_scaffolding.py::*::test_description_has_trigger_contract`
enforces that every SKILL.md description contains use-when and don't-use-when
phrasing.

### Gotchas

- Don't-use-when phrasing should be specific, not generic. "Do not use for
  ICE — that is pace-ice's overlay" is useful; "do not use for the wrong
  cluster" is not.
- The trigger lists in `evals/triggers/` should grow as new ambiguous
  prompts surface. Treat them as living test cases, not a one-shot draft.
- The wrapper routing (P02) and the trigger contracts must agree. If the
  wrapper says "Phoenix → pace-phoenix" but pace-phoenix's description has
  no Phoenix-specific use-when phrasing, the contract is broken.

## P04: VERIFY_ON_* placeholder convention

### Problem

When the agent generates an example for a value it does not know — a charge
account, a partition name, a group-specific module — there are three
options and only one is safe:

1. Invent a plausible-looking value (unsafe: looks correct, fails on the
   real cluster, and the user may not notice before submission).
2. Use angle-bracket placeholders like `<gt_username>` (good for values the
   user fills in, but visually similar to invented names).
3. Use a literal sentinel string that does not look like a real value and
   is grep-friendly (the safest choice).

### Adoption

Two literal markers are reserved for AI-generated examples:

- `VERIFY_ON_SITE` — used in `skills/slurm-core/` and its references for
  values that vary across any Slurm site. Portable.
- `VERIFY_ON_PACE` — used in `skills/pace-phoenix/`, `skills/pace-ice/`,
  and their reference files for GT/PACE-specific values the user has not
  provided (charge accounts, group module names, course shared dirs).

These are complementary to angle-bracket placeholders (`<gt_username>`,
`<PI>`, `<job_id>`) which mark user-fill-in values. Users can grep for
`VERIFY_ON_PACE` or `VERIFY_ON_SITE` before submitting any AI-generated
script and catch any value the AI was uncertain about.

File pointers:

- `skills/slurm-core/SKILL.md` — establishes the `VERIFY_ON_SITE` convention.
- `skills/slurm-core/references/core-workflows.md` — uses `VERIFY_ON_SITE`
  in worked examples.
- `skills/pace-phoenix/SKILL.md`, `skills/pace-ice/SKILL.md` — establish
  `VERIFY_ON_PACE` for the GT-specific overlays.
- `skills/pace-phoenix/references/{workflows,phoenix-local-notes}.md` and
  `skills/pace-ice/references/{workflows,ice-local-notes}.md` — apply
  `VERIFY_ON_PACE` at the spots most prone to invention (charge accounts,
  group-specific module names, course shared-directory paths, college-QOS
  picks when affiliation is unstated).

### Gotchas

- Do not blacklist documented public constants. Names like `inferno`,
  `embers`, `A100`, `H100`, `anaconda3`, `cuda`, `login-phoenix`,
  `login-ice` are public PACE facts, not site-specific values to verify.
  The marker is for things the AI cannot know without the user telling it
  (or running a discovery command like `pace-quota`).
- The marker must be a literal token, not a description ("verify on PACE"
  in prose does not satisfy the contract). Tests grep for the exact string
  `VERIFY_ON_PACE` / `VERIFY_ON_SITE`.
- Pair the marker with a one-line note pointing at the discovery command
  (e.g. `pace-quota` for accounts, `module avail` for modules) so the user
  knows how to fill it in.

## P05: Canonical-source-of-truth via symlinks

### Problem

The project ships two distinct deliverables — a Codex bundle and a Claude
plugin — that need to share the same skills, the same wrappers, and the
same PACE documentation. Naive duplication (copying files into both
deliverables) causes drift the moment one copy is edited and the other
forgotten. A glob-and-copy build step partially fixes this but creates a
moving target between source and deliverable that is annoying to debug.

### Adoption

Content lives in canonical locations once, and tool deliverables hold
**relative symlinks** pointing into the canonical source:

- Canonical sources: `skills/`, `wrappers/`, `docs/PACE Documentation/`.
- Codex deliverable: `codex/skills/{slurm-core,pace-phoenix,pace-ice}` →
  `../../skills/<name>`; `codex/wrappers/AGENTS.md` →
  `../../wrappers/AGENTS.md`; `codex/PACE Documentation` →
  `../docs/PACE Documentation`.
- Claude deliverable: `claude/skills/{slurm-core,pace-phoenix,pace-ice}` →
  `../../skills/<name>`; `claude/wrappers/CLAUDE.md` →
  `../../wrappers/CLAUDE.md`; `claude/docs` → `../docs/PACE Documentation`.

Because the same file on disk is referenced from both deliverables, drift
is structurally impossible — there is no second copy to forget.

The publish materializer (`scripts/publish_release.py`) resolves symlinks
at publish time and writes real files into the public artifact under
`dist/publish/`, so end-users of the published release receive a
self-contained tree.

### Gotchas

- Symlinks must be **relative** (`../../skills/slurm-core`), not absolute.
  Absolute symlinks break the moment the repo is cloned to a different path,
  and they break the materializer's resolution inside `dist/publish/`.
- Do not edit the symlink target. Edit the canonical source under
  `skills/`, `wrappers/`, or `docs/PACE Documentation/`. Editing through
  the symlink works (it is the same file) but loses the affordance that the
  canonical location is the place to make changes.
- The publish boundary security design — see
  `docs/superpowers/specs/2026-04-24-publish-boundary-security-design.md` —
  inspects the materialized files, not the symlinks. Anything inside the
  canonical source is included in the publish set; double-check what lives
  there before adding files.
- Tests that follow the symlink (e.g. reading `skills/pace-phoenix/SKILL.md`
  from a test file under `tests/`) work transparently; tests that expect a
  file copy in `codex/` or `claude/` should be updated to follow the link
  instead.
