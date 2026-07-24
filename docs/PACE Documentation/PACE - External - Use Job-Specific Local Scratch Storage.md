---
created: 2026-02-26T19:46:57 (UTC -08:00)
tags: []
author:
---

# PACE - External - Use Job-Specific Local Scratch Storage

---

## How to Use Local Scratch Storage

### What is Local Scratch Storage?

-   Every Node comes with a tmp directory that's local to the node.
-   Since it's a local disk mounted on the node, it's **faster** than network storage (`/project`, `home` etc)
-   A node may be forced to go offline if a large `tmp` directory is created on the node and then not deleted once the job ends. As a solution, temporary directories have been created on nodes to support the use of `tmp` directories. The job-specific `/tmp` directory is **automatically** deleted after the job has finished running

### Scratch Directory on Node Explained

-   Each node has its own `/scratch` directory.

> **Warning:** The /scratch dir on the node is not the same as the ~/scratch directory in your home folder

-   Every job will create a directory on the node under `/scratch` named after the jobID, for example:
    -   `/scratch/20986925`
    -   It is **not possible** to access this path directly. Inside it, another directory is created that is appears to be mounted at `/tmp` while inside a job. **Use this** **`/tmp` to use local disk inside a job.** 
-   This directory will be **automatically deleted** when the job is complete, so you don't have to worry about deleting it yourself
-   `${TMPDIR}` is the variable that is **assigned** to this path. `${TMPDIR}` is how you reference this directory in your code
-   Any places in your code that you require a tmp directory can use `/tmp` or `${TMPDIR}` to access local disk. 

### How to Use Scratch Directory + Example

> **Important:** In your code, use ${TMPDIR} or /tmp to use local scratch storage

-   Since`${TMPDIR}` automatically deletes itself after the job, the problem of a large number of nodes running out of local space will be prevented

### Ensure Local Storage Availability for Job

-   The #SBATCH --tmp=<size>\[units, default MB\] directive allows you to request space for your job. For example, if you need 10gb of space:
    -   `#SBATCH --tmp=10G`. **Remember**: this storage amount is **per node**, not per job.
-   This directive will make sure your job will be allocated on a node that has at least 10gb free on `${TMPDIR}`. This is assuming you only requested 1 node. Since the `#SBATCH --tmp=10G` directive reserves storage **per node**. Requesting for example, 2 nodes would suddenly leave you with 20gb requested storage instead of 10 (10gb per node \* 2 nodes)

### Retrieve Files from Unexpectedly Terminated Jobs

-   Since `{$TMPDIR}` is deleted once a job is finished, you may lose the files stored in it if the job unexpectedly terminates
-   However, you can use the `trap` command to make sure that files are copied over from the `{$TMPDIR}` before the job terminates and the directory is deleted
-   For `trap` to work, it must precede the command that causes the unexpected termination, so the suggested location is right after the PBS directives
-   Here is an example command that can be inserted right after the PBS directives:

```
trap "cp ${TMPDIR}/* ~/data/somewhere_to_store_these/" TERM
```

-   You should make sure to make this command more specific based on where you want to copy your files to
-   A good option is to copy the files over to your global scratch directory `~/scratch/` 
-   Note that this copy will ONLY happen if the job terminates as a failure, so you should make sure that the existing procedure you have for copying files during a normal completion is still a part of the script.

