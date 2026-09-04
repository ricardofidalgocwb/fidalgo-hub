# Upload binário no Drive — regra SSOT

**Status:** ferramenta unpublished. **Não publicar site. Não ativar n8n. Sem placeholder stub.**

Agentes de Operações, Entrega e Comunicação leem este arquivo antes de qualquer foto de evidência (G-FOTO / Passaporte Digital / Antes).

---

## Proibição dura — MCP Drive

**Proibido** usar Google Drive MCP `create_file` (ou qualquer upload em base64 via MCP) para imagem ou vídeo que vá servir de evidência.

O MCP trunca o binário e grava um **stub** de ~3–9 KB. Isso **não** é foto. COM-PDF-02 (PR 12, texto) e o Passaporte / G-FOTO recusam stub.

Não inventar arquivo. Não commitar credencial. Não escrever no Notion a partir deste fluxo. Não disparar webhook n8n.

---

## Aceite só peso real

Depois do drop, o arquivo no Drive tem de ter **`size` > 100 000 bytes** (metadado `files.get`, campo `size`).

| Resultado | Ação |
|---|---|
| `size` ≤ 100 000 | **Recusar.** É stub ou lixo. Não embutir, não citar como prova. |
| `size` > 100 000 | Aceitável como evidência (ainda falta o Ricardo / mesa validar o conteúdo). |

Cem kilobytes aqui = **100 000 bytes** (decimal), não 102 400. O script e o teste usam o mesmo limiar.

---

## Destino vivo — OS-34 / `00_Antes`

Pasta: **`00_Antes`**  
ID Drive (público, não é secret): `1pYlbPeFcp2RyB1ZqEn9RNFBZ8Y7YccE-`

Audit **2026-09-04** (America/Sao_Paulo): `00_Antes` tem **17 solid** e **0 stubs**; caixa `AIW3138_00_Antes_10_caixa_fusiveis_print_zap.png` ~2.8 MB. Inbox `00_Cliente_envia` vazia de ficheiros. IDs e catálogo de tipagem: [`config/drive_ids.json`](../config/drive_ids.json). COM-PDF-02 embed fotográfico continua **HOLD** até follow-up explícito — slots no HTML seguem AUSENTE. Allowlist MCP: [`docs/mcp-drive-allowlist.md`](mcp-drive-allowlist.md).

---

## Path A — preferido (até existir auth do script)

Ricardo faz o drop **manual no browser** direto em `00_Antes`.

1. Abrir a pasta no Drive (conta que já tem acesso).
2. Enviar os JPEG/PNG/MP4 originais da câmera (não export MCP, não screenshot de stub).
3. Conferir tamanho na UI ou em *Detalhes* — cada arquivo **> 100 KB**.
4. Só então avisar Comunicação / Entrega que o drop existe.

Path A não precisa de service account, OAuth, n8n nem agente. É o caminho certo enquanto o Path B não tiver credencial local do Ricardo.

---

## Path B — script resumable (local)

Script: [`scripts/drive_resumable_upload.py`](../scripts/drive_resumable_upload.py). Auth e variáveis: [`scripts/README.md`](../scripts/README.md).

Usa a API Drive **resumable** (`uploadType=resumable` / `MediaFileUpload(resumable=True)`). **Não** é single-shot base64. **Não** passa pelo MCP.

```bash
# Recusa local se o arquivo tiver ≤ 100 KB (exit ≠ 0). Sem rede.
python scripts/drive_resumable_upload.py \
  --parent 1pYlbPeFcp2RyB1ZqEn9RNFBZ8Y7YccE- \
  --file /caminho/local/antes_caixa_fusiveis.jpg \
  --dry-run

# Upload de verdade (exige credencial local — ver scripts/README.md)
python scripts/drive_resumable_upload.py \
  --parent 1pYlbPeFcp2RyB1ZqEn9RNFBZ8Y7YccE- \
  --file /caminho/local/antes_caixa_fusiveis.jpg \
  --name "OS-34_Antes_caixa_fusiveis.jpg"
```

Depois do upload o script busca metadados e exige `size` > 100 000. Se falhar, **move o arquivo para a lixeira do Drive** e sai com erro. Sem stub no lugar da prova.

Dry-run **só imprime o plano** (pasta, nome, bytes locais, se passaria no portão). Não chama a API.

---

## O que este repo não faz

- Não clona nem commita JSON de service account / OAuth / token.
- Não escreve Notion.
- Não publica site (Heros / Eletro / proposta).
- Não liga n8n (`N8N_AVANCAR_ENABLED` permanece 0).
- Não gera placeholder, stock, render nem ID de stub antigo.

Embed em COM-PDF-02 = **PR posterior**, só com arquivos reais já no Drive.
