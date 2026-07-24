---
created: 2026-02-26T19:46:50 (UTC -08:00)
tags: []
author:
---

# PACE - External - Storage on ICE

> Each student receives both home and scratch directories. Local disk on compute nodes is accessible inside a compute job.

---
## Storage on ICE

Each student receives both home and scratch directories. Local disk on compute nodes is accessible inside a compute job.

### pace-quota

Running `pace-quota` will report on utilization of your home and scratch storage allocations.

### Home

Upon login, you will be placed in your home directory, which is available from all login and compute nodes. Home directories provide a 30 GB storage quota. A snapshot is taken daily in case data needs to be retrieved after accidental file loss.

Files in home directories are deleted after a user has not had access to ICE or logged in for one year.

Home directories are located on OIT's centralized NetApp storage service.

Users in need of more than 30 GB of storage are encouraged to use scratch or shared directories. If these solutions will not work, instructors and TAs may request additional home directory space on behalf of themselves or students in their course.

### Scratch

Each user is allocated a scratch directory as well, with a 300 GB storage quota on a faster parallel filesystem. Each user may place up to 1 million files or directories on scratch.

**Scratch is not backed up**. Any files lost from scratch are permanently gone. In addition, at the end of each semester, all files in scratch directories not touched in 120 days are deleted.

Scratch is hosted on a Lustre parallel filesystem with an InfiniBand network connection to login and compute nodes. Scratch will provide faster performance than home directories and is ideal for computations requiring faster networked storage.

Users in need of more than 300 GB of storage (or more than 1M files) are encouraged to use shared directories where possible. If these solutions will not work, instructors and TAs may request additional scratch directory space on behalf of themselves or students in their course.

### Local Disk

Every ICE compute node has [local disk](https://gatech.service-now.com/home?id=kb_article_view&sysparm_article=KB0042171) storage available for temporary use in a job, which is automatically cleared upon job completion. Some applications can benefit from this storage for faster I/O than network storage (home and scratch). Most ICE CPU nodes and some GPU nodes have large NVMe local disks, while a few have SAS storage. See [ICE resources](https://gatech.service-now.com/home?id=kb_article_view&sysparm_article=KB0042095) for details.

-   Use the `${TMPDIR}` variable in your Slurm script or interactive session to access the temporary directory for your job on local disk, which is automatically created for every job.
-   When requesting a partial node, guarantee availability of local disk space with `#SBATCH --tmp=<size>[units, default MB]`.
-   To request a node with SAS storage, add `#SBATCH -C localSAS`.
-   To request a node with NVMe storage, add `#SBATCH -C localNVMe`.

### Shared Directories

Courses may request a shared directory on ICE. These shared directories can be used for collaborative work or for distributing course materials and/or software. Instructors or TAs should discuss preferred access permissions on shared directories with PACE, to ensure they can be used for collaboration by a course, for group assignments, or for distribution only. Shared directories are located on VAST storage, and files in them do not count towards individual user quotas. Any shared directories for courses that have not run in the last two years will be removed at the end of the semester. Course shared directories are limited to 2 TB by default, and instructors and TAs may request additional space.

Some courses may request to have their shared directories placed on the Lustre parallel filesystem. These shared directories have no backup, so they are best used for data that could be retrieved from another location if it needed to be recreated. Files in Lustre/scratch shared directories count towards the scratch quota of the user who owns them, even though they are located outside the user's scratch directory.

### File Transfer

Transfer files to/from ICE via [Globus](https://gatech.service-now.com/home?id=kb_article_view&sysparm_article=KB0041890), especially for large quantities of data. 

Small file transfer can also be done via SCP ([Mac/Linux](https://gatech.service-now.com/home?id=kb_article_view&sysparm_article=KB0042172) or [Windows](https://gatech.service-now.com/home?id=kb_article_view&sysparm_article=KB0042173)) or [SFTP](https://gatech.service-now.com/home?id=kb_article_view&sysparm_article=KB0042174) or via the "Upload" and "Download" buttons in the "Files" tab of [Open OnDemand](https://ondemand-ice.pace.gatech.edu/).

