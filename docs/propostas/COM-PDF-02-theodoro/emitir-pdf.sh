#!/usr/bin/env bash
# Regenera o PDF texto-only desta pasta. Não baixa foto. Não envia a cliente.
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
OUT="${DIR}/COM-PDF-02-theodoro-texto.pdf"
HTML="${DIR}/index.html"

CHROME="$(command -v google-chrome-stable || true)"
if [[ -z "${CHROME}" ]]; then
  CHROME="$(command -v google-chrome || true)"
fi
if [[ -z "${CHROME}" ]]; then
  CHROME="$(command -v chromium || true)"
fi
if [[ -z "${CHROME}" ]]; then
  echo "Chrome/Chromium não encontrado. Use Imprimir → Salvar como PDF no navegador." >&2
  exit 1
fi

"${CHROME}" --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="${OUT}" \
  "file://${HTML}"

echo "Gerado: ${OUT}"
