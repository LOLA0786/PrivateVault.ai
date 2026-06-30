#!/usr/bin/env bash
set -euo pipefail
TITLE="${1:?Usage: ./new-post.sh \"Your Post Title\"}"
DATE=$(date +%F)
SLUG=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | sed -e 's/[^a-z0-9]/-/g' -e 's/-\{2,\}/-/g' -e 's/^-//' -e 's/-$//')
DIR="${REPO:-$HOME/PrivateVault.ai/ui/privatevault-control}/src/blog/posts"
FILE="$DIR/${DATE}-${SLUG}.md"
cat > "$FILE" <<POST
---
title: ${TITLE}
date: ${DATE}
excerpt: One line that shows on the blog index. Keep it sharp.
---

Write the post here. No em-dashes. Short paragraphs. One idea per piece.
POST
echo "Created $FILE  ->  /blog/${SLUG}"
