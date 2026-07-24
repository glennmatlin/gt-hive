# GT Hive

Georgia Tech PACE HPC skills for AI coding tools. Navigate Phoenix and ICE clusters, compose Slurm job scripts, estimate costs, and find storage and transfer workflows.

## Install

### Claude Code

```bash
claude plugin marketplace add github:glennmatlin/gt-hive
claude plugin install gt-hive-pace
```

### Codex

Clone this repository and link the skill:

```bash
git clone https://github.com/glennmatlin/gt-hive.git
cd gt-hive
ln -sfn "$(pwd)/pace-openai" "$HOME/.codex/skills/pace-openai"
ln -sfn "$(pwd)/docs" "$HOME/.codex/skills/docs"
```

## What's inside

- **`claude/`** — `gt-hive-pace` Claude Code plugin: Slurm scripting, storage navigation, GPU resource selection, troubleshooting, templates.
- **`codex/`** — Codex skill view of the same content (skill symlinks + wrappers).
- **`docs/PACE Documentation/`** — PACE documentation references.

## Using the plugin

From Claude Code (picker shows the abbreviated form on the right):

- `/gt-hive-pace:pace-guide` (`/pace-guide`) — interactive guide for cluster tasks. Start here if you're new.
- `/gt-hive-pace:pace-sbatch` (`/pace-sbatch`) — interactive wizard that drafts a Slurm sbatch script.
- `/gt-hive-pace:pace-cost` (`/pace-cost`) — Phoenix charge estimator (`/pace-cost h100 4`).

The skills auto-load when your prompt mentions PACE, Phoenix, ICE, Slurm, sbatch, or HPC.

## Issues and contributions

File issues at https://github.com/glennmatlin/gt-hive/issues.

## License

MIT — see [LICENSE](LICENSE).
