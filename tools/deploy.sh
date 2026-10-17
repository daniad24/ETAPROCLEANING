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
cp -R "$ROOT/site/." "$STAGE/"
rm -f "$STAGE/preview.html" "$STAGE/assets/img/POZE-NECESARE.md"
cp "$ROOT/tools/vercel/project.json" "$STAGE/.vercel/project.json"
# TODO la lansare: șterge acest header ca Google să poată indexa site-ul.
cat > "$STAGE/vercel.json" <<'JSON'
{ "headers": [ { "source": "/(.*)", "headers": [ { "key": "X-Robots-Tag", "value": "noindex, nofollow" } ] } ] }
JSON
cd "$STAGE" && "$VERCEL" deploy --prod --yes
