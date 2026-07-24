# Commands directory guide

This is meta documentation for `claude/commands/`, the directory that
holds the slash commands shipped with the `gt-hive-pace` plugin (part
of the `gt-hive` marketplace). Each markdown file there becomes
`/gt-hive-pace:<filename-stem>`.

This file lives at `claude/COMMANDS.md` rather than
`claude/commands/README.md` because the Claude Code plugin loader
registers **every** file under `commands/` as a slash command, regardless
of whether the file has YAML frontmatter (observed empirically — a
frontmatter-less `commands/README.md` still appeared in the picker as
`/gt-hive-pace:README`). Keeping the meta doc one directory up makes
the picker show only real commands.

## Commands vs skills

Two execution surfaces in this plugin look similar but are loaded very
differently:

| | `claude/commands/` | `skills/` (linked into `claude/skills/`) |
|---|---|---|
| Triggered by | The user typing `/gt-hive-pace:<name>` | Claude reading the skill `description` and deciding to load it |
| Genre | A prompt-as-script | Reference material the model reads on demand |
| Best for | Structured, deterministic workflows | Knowledge the model pulls in mid-conversation |
| Discoverability | Slash-command picker | Natural-language phrasing |

The dividing line: skills are model-discovered knowledge; commands are
user-invoked prompts-as-scripts. Reach for a command when the workflow
benefits from an `AskUserQuestion` wizard, takes structured arguments,
or is a recurring named handle. Reach for a skill when the model just
needs to know something to answer well.

## Naming convention

The marketplace is `gt-hive`; this plugin is `gt-hive-pace`. The full
slash invocation is `/gt-hive-pace:<command>`, but Claude Code's picker
abbreviates the namespace and shows just the command name. To prevent
generic-looking entries (`/guide`, `/cost`), command names include the
**topic prefix** so the picker shows something descriptive.

Convention: **`<topic>-<action>`**, kebab-case.

- Good: `pace-guide`, `pace-sbatch`, `pace-cost`. Picker shows `/pace-guide` etc.
- Avoid: `guide`, `sbatch`, `cost` (generic — collide with other plugins).
- Avoid: `pace_guide`, `pace.guide`, `paceGuide` (kebab-case is the dominant convention across Claude Code plugins).

If a future plugin in the gt-hive marketplace covers a different topic,
its commands use that topic's prefix — e.g., a hypothetical
`gt-hive-canvas` plugin would have `/canvas-grade`, `/canvas-sync`.

## How to add a command

1. Create `claude/commands/<topic>-<action>.md` with this frontmatter:

   ```markdown
   ---
   name: <topic>-<action>
   description: One-sentence description shown in the slash-command picker.
   ---
   ```

   The `name` field must match the file stem.

2. Write the body as a prompt. When the user types
   `/gt-hive-pace:<name>`, Claude Code interpolates the body (with
   `$ARGUMENTS` for any text after the command name) and runs it as
   a turn.

3. Use `AskUserQuestion` for branching wizards. Use `$ARGUMENTS` for
   commands that take typed args (and consider an args-or-wizard
   hybrid like `pace-cost.md` if both audiences matter).

4. Load skills explicitly in the body. Commands and skills are
   independent; a command that needs `slurm-core` knowledge should say
   so, and Claude will load the skill into the turn.

## Publish-boundary obligations

Every new command must be wired into the publish flow:

- Add a copy entry to `config/publish_manifest.json`. If the command
  body embeds GT login hostnames or other restricted content, the
  source path is `dist/public/variants/claude/commands/<name>.md`;
  otherwise it is the file itself at `claude/commands/<name>.md`.

- If the command needs public-variant rewriting, add it to
  `public_variant_sources` in `config/data_policy.json` so
  `scripts/build_doc_views.py --profile public` regenerates the
  redacted copy.

- Run `python3 scripts/security_policy_check.py --profile public`
  after any change. The publish boundary blocks the release if a
  restricted pattern leaks into the public artifact.

## Testing

The layout contract for the four files in this directory lives in
`tests/test_commands_layout.py`. When you add a command:

- Add a test class asserting the file exists, has correct frontmatter
  (with `name` matching the file stem), and references the skills /
  arguments it depends on.
- Update `REQUIRED_DESTS` in `tests/test_publish_manifest.py` so the
  manifest test fails if you forget to ship the file publicly.

The trigger contract under `evals/triggers/` is for skills, not
commands. Commands are user-invoked, so trigger eval prompts do not
apply — the test surface is layout, frontmatter, and publish wiring.
