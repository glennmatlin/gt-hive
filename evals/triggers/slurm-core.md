# slurm-core triggers

Human-readable test list for the trigger contract on `skills/slurm-core/`. Each prompt is one a user might paste into Claude Code or Codex; the assertion is what skills should activate.

## Should activate slurm-core

(prompts that are portable Slurm — no specific cluster named)

- "Draft a Slurm script for this Python program."
- "Convert this shell loop into a job array."
- "Explain why my Slurm job failed from this sacct output."
- "Create a preprocess/train/evaluate pipeline with dependencies."
- "What does `salloc` do?"
- "How do I read `ExitCode=0:9` in sacct output?"
- "My job is pending — what does the reason field tell me?"

## Should also activate an overlay

(prompts that add a cluster context — slurm-core PLUS pace-phoenix or pace-ice)

- "I'm on Georgia Tech PACE Phoenix. Draft a GPU script."  → slurm-core + pace-phoenix
- "How do I ask for an A100 on Phoenix?"  → slurm-core + pace-phoenix
- "I'm running this for a course on ICE."  → slurm-core + pace-ice
- "How do I submit a grading job on PACE ICE?"  → slurm-core + pace-ice

## v1 vs automation

These are human-readable checklists in v1. Automation (sending each prompt to an LLM and asserting which skill activates) is a future spec.
