#!/usr/bin/env python3
"""
Generate research-oriented sbatch templates for PACE clusters.

Examples:
  uv run python scripts/generate_sbatch.py --mode cpu --account gts-user --command "python run.py"
  uv run python scripts/generate_sbatch.py --mode gpu --account gts-user --gpus 1 --gpu-type H100 \
    --estimate-cost --rate-gpu-hour 12.5 --out train.sbatch
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def parse_duration_hours(raw: str) -> float:
    raw = raw.strip()
    if raw.isdigit():
        return int(raw) / 60.0

    days = 0
    time_part = raw
    if "-" in raw:
        day_part, time_part = raw.split("-", 1)
        days = int(day_part)

    parts = time_part.split(":")
    if len(parts) == 3:
        hours, minutes, seconds = (int(parts[0]), int(parts[1]), int(parts[2]))
    elif len(parts) == 2:
        hours, minutes, seconds = (int(parts[0]), int(parts[1]), 0)
    elif len(parts) == 1 and parts[0].isdigit():
        return int(parts[0]) / 60.0
    else:
        raise ValueError(f"Unsupported time format: {raw}")

    total_seconds = (days * 24 * 3600) + (hours * 3600) + (minutes * 60) + seconds
    return total_seconds / 3600.0


def fmt_money(value: float) -> str:
    return f"${value:,.2f}"


def ensure_srun(command: str) -> str:
    stripped = command.strip()
    if stripped.startswith("srun "):
        return stripped
    return f"srun {stripped}"


def default_account(cluster: str, account: str | None) -> str:
    if account:
        return account
    if cluster == "phoenix":
        return "<account_name>"
    return ""


def build_summary(
    *,
    cluster: str,
    mode: str,
    qos: str,
    nodes: int,
    ntasks: int | None,
    ntasks_per_node: int,
    gpus: int,
    walltime: str,
    estimate_cost: bool,
    rate_cpu_hour: float | None,
    rate_gpu_hour: float | None,
) -> list[str]:
    lines = [
        f"# Cluster: {cluster}",
        f"# Mode: {mode}",
        f"# Walltime request: {walltime}",
    ]

    hours = parse_duration_hours(walltime)
    cpu_count = ntasks if ntasks else nodes * ntasks_per_node
    cpu_hours = cpu_count * hours
    gpu_count = nodes * gpus if mode == "gpu" else 0
    gpu_hours = gpu_count * hours

    if mode == "gpu":
        lines.append(f"# Estimated billed usage: {gpu_hours:.2f} GPU-hours")
    else:
        lines.append(f"# Estimated billed usage: {cpu_hours:.2f} CPU-hours")

    if not estimate_cost:
        return lines

    if cluster != "phoenix":
        lines.append("# Estimated cost: not modeled for ICE (course/priority model varies).")
        return lines

    if qos == "embers":
        lines.append("# Estimated cost: $0.00 (embers is backfill/preemptible in docs).")
        return lines

    if mode == "gpu":
        if rate_gpu_hour is None:
            lines.append("# Estimated cost: missing --rate-gpu-hour.")
        else:
            lines.append(
                f"# Estimated cost: {fmt_money(gpu_hours * rate_gpu_hour)} "
                f"at {rate_gpu_hour}/GPU-hour."
            )
    else:
        if rate_cpu_hour is None:
            lines.append("# Estimated cost: missing --rate-cpu-hour.")
        else:
            lines.append(
                f"# Estimated cost: {fmt_money(cpu_hours * rate_cpu_hour)} "
                f"at {rate_cpu_hour}/CPU-hour."
            )

    lines.append("# Cost estimate is a planning approximation, not an official bill.")
    return lines


def build_script(args: argparse.Namespace) -> str:
    cluster = args.cluster
    qos = args.qos
    account = default_account(cluster, args.account)

    lines: list[str] = ["#!/bin/bash"]
    lines.extend(
        build_summary(
            cluster=cluster,
            mode=args.mode,
            qos=qos,
            nodes=args.nodes,
            ntasks=args.ntasks,
            ntasks_per_node=args.ntasks_per_node,
            gpus=args.gpus,
            walltime=args.time,
            estimate_cost=args.estimate_cost,
            rate_cpu_hour=args.rate_cpu_hour,
            rate_gpu_hour=args.rate_gpu_hour,
        )
    )
    lines.append(f"#SBATCH -J {args.job_name}")

    if cluster == "phoenix":
        lines.append(f"#SBATCH -A {account}")
        lines.append(f"#SBATCH -q {qos}")
    elif account:
        lines.append(f"#SBATCH -A {account}")
        if qos:
            lines.append(f"#SBATCH -q {qos}")

    lines.append(f"#SBATCH -N {args.nodes}")
    if args.ntasks is not None:
        lines.append(f"#SBATCH --ntasks={args.ntasks}")
    else:
        lines.append(f"#SBATCH --ntasks-per-node={args.ntasks_per_node}")

    if args.mode == "gpu":
        lines.append(f"#SBATCH --gres=gpu:{args.gpu_type}:{args.gpus}")
        lines.append(f"#SBATCH --mem-per-gpu={args.mem_per_gpu}")
    else:
        lines.append(f"#SBATCH --mem-per-cpu={args.mem_per_cpu}")

    if args.mode == "array":
        array_spec = args.array
        if args.array_throttle is not None:
            array_spec = f"{array_spec}%{args.array_throttle}"
        lines.append(f"#SBATCH --array={array_spec}")

    if args.constraint:
        lines.append(f"#SBATCH -C {args.constraint}")

    lines.append(f"#SBATCH -t {args.time}")
    lines.append(f"#SBATCH -o {args.output_pattern}")

    if args.mail_type:
        lines.append(f"#SBATCH --mail-type={args.mail_type}")
    if args.mail_user:
        lines.append(f"#SBATCH --mail-user={args.mail_user}")

    lines.append("")
    lines.append("module purge")
    for module in [m.strip() for m in args.modules.split(",") if m.strip()]:
        lines.append(f"module load {module}")
    lines.append(ensure_srun(args.command))
    lines.append("")

    return "\n".join(lines)


def validate_args(args: argparse.Namespace) -> None:
    if args.nodes <= 0:
        raise ValueError("--nodes must be >= 1")
    if args.ntasks is not None and args.ntasks <= 0:
        raise ValueError("--ntasks must be >= 1")
    if args.ntasks_per_node <= 0:
        raise ValueError("--ntasks-per-node must be >= 1")
    if args.mode == "gpu" and args.gpus <= 0:
        raise ValueError("--gpus must be >= 1 for gpu mode")
    if args.mode != "gpu" and args.gpus != 1:
        raise ValueError("--gpus is only meaningful in gpu mode")
    parse_duration_hours(args.time)
    if args.cluster == "phoenix" and args.qos not in {"inferno", "embers"}:
        raise ValueError("--qos must be inferno or embers for phoenix")
    if args.cluster == "phoenix" and not args.account:
        raise ValueError(
            "--account is required for phoenix cluster (e.g. --account gts-yourpi)"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate sbatch templates for PACE")
    parser.add_argument("--cluster", choices=("phoenix", "ice"), default="phoenix")
    parser.add_argument("--mode", choices=("cpu", "gpu", "array"), default="cpu")
    parser.add_argument("--job-name", default="pace_job")
    parser.add_argument("--account", help="Charge account, usually required for Phoenix")
    parser.add_argument("--qos", default="inferno", help="Phoenix: inferno or embers")

    parser.add_argument("--nodes", type=int, default=1)
    parser.add_argument("--ntasks", type=int, help="Total tasks")
    parser.add_argument("--ntasks-per-node", type=int, default=4)
    parser.add_argument("--mem-per-cpu", default="2G")
    parser.add_argument("--mem-per-gpu", default="12G")

    parser.add_argument("--gpus", type=int, default=1)
    parser.add_argument("--gpu-type", default="V100")
    parser.add_argument("--constraint", help="Optional Slurm constraint")

    parser.add_argument("--time", default="01:00:00")
    parser.add_argument("--array", default="1-10", help="Array range for array mode")
    parser.add_argument("--array-throttle", type=int)

    parser.add_argument("--modules", default="anaconda3")
    parser.add_argument("--command", default="python script.py")
    parser.add_argument("--output-pattern", default="Report-%j.out")
    parser.add_argument("--mail-type")
    parser.add_argument("--mail-user")

    parser.add_argument("--estimate-cost", action="store_true")
    parser.add_argument("--rate-cpu-hour", type=float)
    parser.add_argument("--rate-gpu-hour", type=float)

    parser.add_argument("--out", help="Write output script to file instead of stdout")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        validate_args(args)
    except ValueError as exc:
        print(f"Validation error: {exc}", file=sys.stderr)
        return 2

    script = build_script(args)

    if args.out:
        out_path = Path(args.out)
        try:
            out_path.write_text(script, encoding="utf-8")
        except OSError as exc:
            print(f"Error writing {out_path}: {exc}", file=sys.stderr)
            return 2
        print(f"Wrote {out_path}")
    else:
        print(script)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
