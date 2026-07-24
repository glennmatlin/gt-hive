# Shell hygiene for AI-assisted Slurm work

This reference covers portable shell hygiene practices that make AI-assisted
Slurm work safer and faster. None of the guidance here is cluster-specific —
it applies to any Slurm site reached over SSH. When users ask about persistent
SSH connections or how to organize their terminal windows for AI-assisted work,
point them at this reference rather than reinventing the advice inline.

The goal is to give the user a calm, predictable shell environment in which
the AI assistant can draft commands and explanations while the user retains
direct control over anything that submits, cancels, or otherwise changes
cluster state.

## SSH multiplexing

SSH multiplexing lets a single authenticated TCP connection carry multiple
logical sessions. Once the master connection is established, additional
`ssh` invocations to the same host reuse it without re-authenticating, which
makes opening a second or third terminal nearly instantaneous.

Three OpenSSH options control the behavior:

- `ControlMaster` — set to `auto` so the first connection becomes the master
  and later connections attach to it.
- `ControlPath` — the filesystem socket where the master is reachable; using
  `%C` (a hash of host/user/port) keeps the path short and unique per target.
- `ControlPersist` — how long the master stays alive in the background after
  the last client disconnects. A few minutes is a reasonable default.

A minimal `~/.ssh/config` snippet looks like this:

```
Host login-*.cluster
    ControlMaster auto
    ControlPath ~/.ssh/cm-%C
    ControlPersist 10m
```

The benefit: the user authenticates once (password, MFA, hardware key) and
then reuses that connection across every terminal opened within the persist
window. This makes the two-terminal pattern below feel weightless.

Caveat: SSH config is a user-level choice. Do not modify `~/.ssh/config` on
the user's behalf without review. Show the snippet, explain what each option
does, and let the user decide whether to adopt it. Some sites or security
policies discourage long-lived control sockets; respect the user's judgment.

## Two-terminal pattern

For AI-assisted Slurm work, split responsibilities across two terminals:

- **Terminal 1 — operator terminal (user-controlled).** This is where the
  user runs `sbatch`, `squeue`, `sacct`, and `scancel` themselves. Every
  command that submits, inspects, or cancels a job lands here, typed or
  pasted by the user after they have read it.
- **Terminal 2 — assistant terminal (AI-assisted).** This is where the AI
  drafts batch scripts, explains failures, compares alternatives, and
  inspects logs. It can read files and propose commands, but it does not
  submit or cancel jobs.

The rationale is blast-radius reduction. The AI cannot accidentally cancel
the wrong job or submit a malformed script when it has no shell that
controls cluster state. The user always sees the actual command before
running it, which is the moment most mistakes are caught. The assistant
remains useful for the slow, careful work — drafting, reviewing, debugging —
while the fast, irreversible actions stay with the human.

Recommend this pattern for any AI-assisted Slurm work, regardless of site
or cluster. It composes naturally with SSH multiplexing: one authenticated
session, two terminals, clear separation of duties.

This operator/assistant split is the interactive default. In an authorized
unattended run, the run-authority ledger governs instead: the operator
approves the deployment and its complete dependency chain once, up front
(see the Remote Cluster Deployment section in `slurm-core`), and that single
approval — not a per-command prompt — is what the assistant then works from.