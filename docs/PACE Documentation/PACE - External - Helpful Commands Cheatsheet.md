---
created: 2026-02-26T19:44:26 (UTC -08:00)
tags: []
author:
---

# PACE - External - Helpful Commands Cheatsheet

---

## Helpful Commands

### General Information

-   `pace-quota`: returns username, storage access and utilization, and job charge or tracking accounts.
-   `pace-check-queue [-c] [-s] [-m] [-j] [-x] [-h] <queue name>`: gives info on resources available for queue, node names, and status of queue.
    -   `pace-check-queue -c <queue name>`: Will color code each node by availability. Useful to quickly see which nodes are accepting jobs.
    -   `pace-check-queue -s <queue name>`: Shows the feature tags for each node. These tags can be used in your `PBS` script to request certain hardware capabilities, such as intel processors or nvidia gpus.
    -   `pace-check-queue -h`: Opens the man page for `pace-check-queue`
    -   **Additional Flags**: The flags `[-m] [-j] and [-x]` Allow you to simplify the output of `pace-check-queue`, and to print the results in xml or json.

### Modules

-   `module avail <optional module name>`: lists modules (software) available on pace and can provide a module name to search for specific software.
-   `module load <module name>`: loads module into environment.
-   `module purge`: gets rid of any modules loaded.

### Job Submission

-   Visit the [Phoenix Job Submission](https://gatech.service-now.com/home?id=kb_article_view&sysparm_article=KB0041998#job-submission) page for more information on Phoenix job submission.

### Informational Commands

-   Visit the [Phoenix Information Commands](https://gatech.service-now.com/home?id=kb_article_view&sysparm_article=KB0041998#informational-commands) page for more information on helpful commands on Phoenix.

### Check Storage

-   `pace-quota`: gives you a summary of how much storage you have used and how much you have left.

### Troubleshooting

-   `pace-why-inqueue <jobid>`: diagnoses why a job is stuck in the queue (not running).

