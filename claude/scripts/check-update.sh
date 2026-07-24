#!/usr/bin/env bash
# Refresh the gt-hive marketplace and update plugins at session start.
# Runs silently; failures are non-blocking but logged.
set -euo pipefail

marketplace="gt-hive"
log_dir="${HOME}/.cache/gt-hive"
log_file="${log_dir}/check-update.log"

if ! command -v claude >/dev/null 2>&1; then
  exit 0
fi

mkdir -p "$log_dir"
if ! claude plugin marketplace update "$marketplace" >>"$log_file" 2>&1; then
  echo "$(date -u +%FT%TZ) WARN: marketplace update failed" >>"$log_file"
fi
