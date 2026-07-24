# no-trigger prompts

Human-readable test list for prompts that should NOT activate any layered HPC skill (slurm-core, pace-phoenix, pace-ice). These prompts are unrelated to Slurm or PACE clusters.

## Should NOT activate any HPC skill

(general programming, ML/AI concepts, unrelated technical topics)

- "Explain CUDA streams." (CUDA topic, not Slurm)
- "What is gradient descent?" (ML concept)
- "Help me write a Python decorator."
- "How does PyTorch DataLoader work?"
- "Explain Docker container networking."
- "What's the difference between TCP and UDP?"
- "How do I sort a pandas DataFrame by multiple columns?"
- "Write a regex to match email addresses."
- "How do I configure GitHub Actions for a Python project?"

## Why this matters

False activation costs context. If `slurm-core` activates on "what is gradient descent?", the user wastes attention on irrelevant Slurm context, and the assistant may give worse answers because it's anchored to the wrong domain. The trigger contract in each SKILL.md description should make clear what's NOT in scope.
