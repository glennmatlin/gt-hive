# gt-hive-pace

Claude Code plugin in the `gt-hive` marketplace, for Georgia Tech PACE HPC clusters (Phoenix and ICE). Provides Slurm job scripting, storage navigation, GPU resource selection, troubleshooting, and ready-made templates.

## Skills

The plugin auto-activates one or more layered skills based on what you ask:

- **slurm-core** — portable Slurm guidance.
- **pace-phoenix** — Phoenix-specific overlay (charge accounts, QOS, GPU types).
- **pace-ice** — ICE-specific overlay (instructional defaults, storage paths).

## Commands

Slash commands. The picker shorthand (e.g., `/pace-guide`) is what you'll see in the Claude Code TUI; the full namespace (`/gt-hive-pace:pace-guide`) is the canonical form.

- `/gt-hive-pace:pace-guide` (`/pace-guide`) — interactive guide for common HPC tasks (job scripts, storage, GPUs, troubleshooting). Start here if you don't know what to ask.
- `/gt-hive-pace:pace-sbatch` (`/pace-sbatch`) — wizard that drafts a runnable Slurm sbatch script for Phoenix, ICE, or generic Slurm.
- `/gt-hive-pace:pace-cost` (`/pace-cost`) — Phoenix charge estimator. Args: `/pace-cost <gpu-or-cpu> <hours> [qos] [rate]`. Bare invocation falls into a wizard.

Conventions for commands (and how to add your own) live in `claude/COMMANDS.md`.

## Auto-update

A SessionStart hook checks for plugin updates at the beginning of each session. Updated plugins take effect on the next session.

## Full documentation

See the [gt-hive README](https://github.com/glennmatlin/gt-hive) for installation, usage, and maintenance details.
