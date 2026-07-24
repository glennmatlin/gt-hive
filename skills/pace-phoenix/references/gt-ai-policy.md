# Georgia Tech AI Policy — User Guidance

This is general Georgia Tech institutional AI guidance. It applies to
anyone using AI tools as a Georgia Tech member, not just Phoenix users.
Verify against current Georgia Tech Office of Information Security and
Office of Research policies — see "Where to verify" at the bottom of this
file. The agent-side rules that mirror these expectations live in this
skill's `SKILL.md` under safety; this file is the user-facing summary.

## Data you should not paste into AI tools

When you ask an AI assistant for help with PACE work (or any GT work):

- Do **not** paste personally identifiable information (PII) — names paired
  with student IDs, SSNs, dates of birth, etc.
- Do **not** paste protected or regulated data — FERPA-protected student
  records, HIPAA-protected health information, ITAR/EAR-controlled
  research, sponsor-controlled data, IRB-restricted study data.
- Do **not** paste Georgia Tech organizational data the institute treats
  as internal — unpublished proposals, unannounced personnel decisions,
  unreleased research outputs, internal financial figures.
- Do **not** paste secrets — passwords, API keys, SSH private keys,
  database credentials, signed tokens.

If you are unsure whether a specific dataset falls into one of these
categories, treat it as protected until you have checked the current GT
data classification policy (link below).

## How to think about AI assistants on GT work

Helpful framing to keep in mind:

- Treat the assistant as a draft generator and explainer, not as the final
  authority. Verify AI-generated content against trusted local
  documentation and your own subject-matter judgment before acting on it.
- Verify site-specific Slurm values (account names, partitions, QOS, GPU
  types, module versions) against PACE documentation and `pace-quota` /
  `module avail`, not from assistant memory.
- Tool approval and review matter for institutional integrations. Before
  connecting an AI tool to a GT system or storage location, check whether
  the integration has been reviewed by the relevant office.

## Where to verify (current GT policy lives off this repo)

Policies change. This file is a summary; do not treat it as the live
policy of record. To check the current GT position:

- For current GT data classification and protected-data definitions, see
  the **Georgia Tech Office of Information Security** policies.
- For current AI-tool guidance for research and institute work, see the
  **Georgia Tech Office of Research** and the **Office of the CTO**.
- For sponsor-specific or contract-specific restrictions on AI tool use,
  consult your PI and the responsible administrative office for that
  award.

When in doubt, ask before pasting.
