# Allowlist MCP Drive — evidência fotográfica

**Status:** regra unpublished. Não publicar. Não ativar n8n. Não escrever Notion a partir deste fluxo.

Bots e agentes podem **ler** metadados de evidência no Google Drive. Não podem **criar** imagem ou vídeo de evidência via MCP.

SSOT de upload: [`docs/drive-binary-upload.md`](drive-binary-upload.md). IDs: [`config/drive_ids.json`](../config/drive_ids.json). Audit offline: [`scripts/drive_evidence_audit.py`](../scripts/drive_evidence_audit.py).

---

## Permitido (leitura)

| Ferramenta MCP | Uso |
|---|---|
| `search` | Achar pasta / ficheiro de evidência (OS-34 `00_Antes`, inbox, G-FOTO). |
| `get_file_metadata` | Confirmar `id`, `name`, `size`, `mimeType`. Aceite só `size` > 100 000. |

Leitura não substitui o portão de peso. Stub ≤ 100 000 bytes continua recusado.

---

## Proibido

- MCP Drive `create_file` para **imagem ou vídeo** de evidência (G-FOTO / Passaporte / Antes). O MCP grava stub de 3–9 KB.
- Upload base64 via MCP “para testar”.
- Inventar ficheiro, placeholder, stock ou ID stub antigo.
- Commitar credencial / token.

---

## Como meter bytes reais

**Path A (preferido):** Ricardo faz o drop **manual no browser** na pasta viva (`00_Antes` OS-34 = `1pYlbPeFcp2RyB1ZqEn9RNFBZ8Y7YccE-`). Sem service account, sem agente.

**Path B:** [`scripts/drive_resumable_upload.py`](../scripts/drive_resumable_upload.py) — API Drive **resumable**, não MCP. Auth só local; ver [`scripts/README.md`](../scripts/README.md).

Embed em COM-PDF-02 continua **HOLD** até follow-up explícito, mesmo com solid no Drive.
