#!/usr/bin/env bash
set -euo pipefail
umask 077
vendor="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
state="${G20_AIHOT_STATE_DIR:-$HOME/.local/share/g20-aihot}"
mkdir -p "$state"
state="$(cd "$state" && pwd)"
runtime="$state/app"
compose=(docker compose --project-name g20-aihot)
command -v docker >/dev/null || { echo '需要在部署机器上安装 Docker 和 Compose。' >&2; exit 1; }
docker compose version >/dev/null
mkdir -p "$runtime"
tar -xzf "$vendor/aihot-source.tar.gz" -C "$runtime"
cp "$vendor/g20-sources.json" "$runtime/industry/sources.json"
cd "$runtime"
if [[ ! -f .env ]]; then
  node scripts/init-env.ts
fi
if ! grep -Eq '^LLM_API_KEY=.+$' .env; then
  echo "请在 $runtime/.env 中配置 LLM_API_KEY、LLM_BASE_URL 和 LLM_MODEL 后重新执行。" >&2
  exit 1
fi
"${compose[@]}" config --quiet
"${compose[@]}" up -d --build
"${compose[@]}" ps
