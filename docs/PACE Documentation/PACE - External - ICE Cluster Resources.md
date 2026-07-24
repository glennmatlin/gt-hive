---
created: 2026-02-26T19:46:48 (UTC -08:00)
tags: []
author:
---

# PACE - External - ICE Cluster Resources

---

## ICE Cluster Resources

Most ICE nodes are available to everyone on ICE! Some nodes have priority for students in College of Computing (CoC) courses and some have priority for students in College of Engineering (CoE) courses, while others have priority for students in courses and workshops in other colleges. This priority is handled automatically, so students can request needed resources and be routed behind the scenes to available nodes.

Each node is connected via an InfiniBand HDR100 (100 Gbps) interface to our high-performance network fabric.

## Structure of a Computational Cluster

-   **Head Nodes (Login Nodes)**

    -   Where you log in
    -   Submit jobs from here
    -   Can edit and compile small-scale programs
    -   Access storage
    -   Login nodes are shared by all. Please do not use the login nodes for any resource-intensive activities, as it prevents other students from using the cluster. PACE will stop processes that continue for too long or use too many resources, in order to ensure functionality of the login node. Please use a compute node for all computational work. An [interactive job](https://gatech.service-now.com/home?id=kb_article_view&sysparm_article=KB0042096#interactive-jobs) provides an interactive environment on a compute node for debugging and other resource-intensive activities.
-   **Compute Nodes**

    -   For running all computations
    -   Assigned by the scheduler and accessed only when assigned
    -   Access storage
    -   May vary in their computational capability
-   **Storage Servers**

    -   See details on the [ICE storage](https://gatech.service-now.com/home?id=kb_article_view&sysparm_article=KB0042094) page.
-   **Scheduler**

    -   Manages compute job requests and assigns resources on compute nodes
    -   Ensures a fair use of shared resources

## ICE Compute Nodes

| Quantity | CPU | Memory | GPU | Local Scratch |
| --- | --- | --- | --- | --- |
| 30 | Dual Xeon Gold 6226 (24 cores/node, 2.70 GHz) | 192GB DDR4 2933 MHz |   | 1.6TB NVMe SSD |
| 22 | Dual Xeon Gold 6226 (24 cores/node, 2.70 GHz) | 192GB DDR4 2933 MHz |   | 1.9TB NVMe SSD |
| 1 | Dual Xeon Gold 6226 (24 cores/node, 2.70 GHz) | 384GB DDR4 2933 MHz |   | 8TB SAS HDD RAID |
| 5 | Dual Xeon Gold 6226 (24 cores/node, 2.70 GHz) | 768GB DDR4 2933 MHz |   | 1.6TB NVMe SSD |
| 2 | Dual Xeon Gold 6226 (24 cores/node, 2.70 GHz) | 768GB DDR4 2933 MHz |   | 1.9TB NVMe SSD |
| 3 | Dual Xeon Gold 6248 (40 cores/node, 2.50 GHz) | 192GB DDR4 2933 MHz | 1x Tesla V100 PCIe 32GB | 512GB SATA SSD |
| 4 | Dual Xeon Gold 6248 (40 cores/node, 2.50 GHz) | 192GB DDR4 2933 MHz | 4x Tesla V100 PCIe 32GB | 512GB SATA SSD |
| 2<sup>[1]</sup> | Dual Xeon Gold 6226 (24 cores/node, 2.70 GHz) | 384GB DDR4 2933 MHz | 4x Quadro Pro RTX6000 24GB | 1.9TB NVMe SSD |
| 11 | Dual Xeon Gold 6226 (24 cores/node, 2.70 GHz) | 384GB DDR4 2933 MHz | 2x Tesla V100 PCIe 16GB | 1.9TB SATA SSD |
| 4 | Dual AMD EPYC 7513 (64 cores/node, 2.60 GHz) | 512GB DDR4 3200 MHz |   | 1.9TB NVMe SSD |
| 2 | Dual AMD EPYC 7513 (64 cores/node, 2.60 GHz) | 512GB DDR4 3200 MHz | 2x A100 PCIe 40GB | 1.9TB NVMe SSD |
| 2 | Dual AMD EPYC 7452 (64 cores/node, 2.20 GHz) | 512GB DDR4 3200 MHz | 2x A100 PCIe 80GB | 1.9TB NVMe SSD |
| 2 | Dual AMD EPYC 7452 (64 cores/node, 2.20 GHz) | 512GB DDR4 3200 MHz | 2x A40 PCIe 48GB | 1.9TB NVMe SSD |
| 2 | Dual AMD EPYC 7452 (64 cores/node, 2.20 GHz) | 512GB DDR4 3200 MHz | 2x MI210 PCIe 64GB |
1.9TB NVMe SSD

 |
| 4 | Dual Xeon Gold 6548Y+ (64 cores/node, 2.50 GHz) | 768GB DDR5 5600 MHz | 8x L40S PCIe 48GB |

3x 3.84TB NVMe SSD

 |
| 20<sup>[2]</sup> | Dual Xeon Platinum 8462Y+ (64 cores/node, 2.8GHz) | 2048GB DDR5 4800 MHz | 8x H100 SXM5 80GB |

3x 3.84TB NVMe SSD

 |
| 18<sup>[3]</sup> | Dual Xeon Platinum 8462Y+ (64 cores/node, 2.8GHz) | 2048GB DDR5 4800 MHz | 8x H200 SXM5 142GB |

8x 3.84TB NVMe SSD

 |
| 3 | Dual Intel(R) Xeon(R) 6740P (96 cores/node, 2.1 GHz) | 2048GB DDR5 4800 MHz | 16x RTX6000 Pro Blackwell 48GB |

2 x 7.68TB NVMe SSD

 |
| 1 | Dual Intel Xeon 6972P (192 cores/node, 2.4 GHz) | 1.5 TiB DDR5 |   |

3.84TB NVMe SSD

 |

\[1\] 8 4xRTX6000 GPU nodes were retired during PACE's May 2024 Maintenance Period.
\[2\] 14 8xH100 GPU nodes reserved for CoE/AI Makerspace users.
\[3\] 12 8xH200 GPU nodes reserved for CoE/AI Makerspace users.

> **Tip:** The scheduler reserves 8GB of memory for system processes, so the total available memory for jobs on a given node is reduced accordingly.

### Partitions

-   Jobs are assigned to Slurm partitions automatically based on your course (CoC, CoE, or other) and whether a GPU has been requested. **Please do not request a partition.**
-   Everyone has access to the `ice-cpu` and `ice-gpu` partitions, which have lower priority.
-   CoC courses have access to `coc-cpu` and `coc-gpu` partitions for higher priority.
-   CoE courses and AI Makerspace users have access to the `pace-cpu` and`coe-gpu` partitions for access to an additional 14 H100 GPU nodes.
-   Non-CoC/CoE courses have access to `pace-cpu` and `pace-gpu` partitions for higher priority.
-   Jobs are automatically submitted to both a priority partition and a general ICE partition and run on available resources. Users do not need to specify a partition, as all eligible partitions are always included.

