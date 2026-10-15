#!/bin/sh
# Reconstruit dev/src.html depuis la source d'avant la vue de côté (commit eb32ca7) en appliquant p01..p08 dans l'ordre.
set -e; cd "$(dirname "$0")/../.."
git show eb32ca7:dev/src.html > src.html
for p in build/vue_cote/p*.py; do python3 "$p"; done
