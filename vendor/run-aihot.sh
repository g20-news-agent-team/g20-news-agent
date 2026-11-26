#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
runtime="$(mktemp -d)"
trap 'rm -rf "$runtime"' EXIT
tar -xzf "$root/vendor/aihot-source.tar.gz" -C "$runtime"
npm --prefix "$runtime" ci --no-audit --no-fund
node "$runtime/scripts/g20-collect.ts" --output "$root/fixtures/raw.sample.jsonl" "$@"
