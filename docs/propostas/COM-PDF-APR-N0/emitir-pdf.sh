#!/usr/bin/env bash
# Regenera o PDF unpublished desta pasta. Não baixa foto. Não publica. Não envia.
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
OUT="${DIR}/COM-PDF-APR-N0-aprendiz.pdf"
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

USER_DATA="$(mktemp -d)"
cleanup() { rm -rf "${USER_DATA}"; }
trap cleanup EXIT

"${CHROME}" --headless --disable-gpu --no-pdf-header-footer \
  --user-data-dir="${USER_DATA}" \
  --print-to-pdf="${OUT}" \
  "file://${HTML}"

echo "Gerado: ${OUT}"
