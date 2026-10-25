#!/bin/bash
# Publică site/ pe Vercel (https://etaprocleaning.vercel.app), cu Google blocat (noindex) cât e în test.
#   bash tools/deploy.sh
# Necesită Vercel CLI autentificat (`vercel login`). Variabila VERCEL poate indica binarul CLI.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VERCEL="${VERCEL:-vercel}"
STAGE="$(mktemp -d "${TMPDIR:-/tmp}/etapro.XXXXXX")/etaprocleaning"
mkdir -p "$STAGE/.vercel"
python3 "$ROOT/tools/build.py"
mkdir -p "$STAGE/site"
cp -R "$ROOT/site/." "$STAGE/site/"
cp -R "$ROOT/api" "$STAGE/api"
rm -f "$STAGE/site/preview.html" "$STAGE/site/assets/img/POZE-NECESARE.md"
cp "$ROOT/tools/vercel/project.json" "$STAGE/.vercel/project.json"
# vercel.json (în rădăcina repo-ului) conține și headerul noindex. TODO la lansare: scoate-l ca Google să poată indexa site-ul.
cp "$ROOT/vercel.json" "$STAGE/vercel.json"
cd "$STAGE" && "$VERCEL" deploy --prod --yes
