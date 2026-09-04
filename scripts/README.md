# scripts/ — ferramentas locais unpublished

Nada daqui publica site, escreve Notion ou liga n8n. Auth **nunca** vai para o git.

## `drive_resumable_upload.py`

Upload **resumable** para o Google Drive (não MCP, não base64). Regra SSOT: [`docs/drive-binary-upload.md`](../docs/drive-binary-upload.md).

Portão duro: arquivo local **≤ 100 000 bytes** é recusado (exit ≠ 0). Depois do upload, `files.get` tem de devolver `size` > 100 000; senão o script manda o arquivo para a lixeira.

### Dependências (só Path B)

O portão de tamanho e o `--dry-run` rodam com as deps do Hub (`requirements.txt`). Upload ao vivo precisa extra:

```bash
pip install google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2
```

Não commitar esses wheels nem JSON de credencial.

### Auth — escolha uma, local only

**Não** commite os JSON. **Não** cole o conteúdo no chat. Coloque o caminho no `.env` (já no `.gitignore`) ou exporte no shell.

#### Opção 1 — service account

```bash
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/.config/fidalgo-hub/drive-sa.json"
```

A pasta destino (`00_Antes` ou outra) precisa estar **compartilhada** com o e-mail da service account (`client_email` no JSON), com permissão de editor. Sem esse share o upload falha; o script não inventa ACL.

#### Opção 2 — OAuth (cliente instalado + token)

```bash
export GOOGLE_DRIVE_OAUTH_CLIENT_SECRETS="$HOME/.config/fidalgo-hub/client_secret.json"
export GOOGLE_DRIVE_OAUTH_TOKEN="$HOME/.config/fidalgo-hub/drive_token.json"
```

Na primeira corrida o script abre o fluxo OAuth local e grava o token **só** em `GOOGLE_DRIVE_OAUTH_TOKEN` (fora do repo). Escopo: `https://www.googleapis.com/auth/drive.file`.

`GOOGLE_APPLICATION_CREDENTIALS` ganha se as duas opções estiverem definidas.

### Uso

```bash
# Plano apenas — não chama Drive. Recusa se o ficheiro local for stub (≤ 100 KB).
python scripts/drive_resumable_upload.py \
  --parent 1pYlbPeFcp2RyB1ZqEn9RNFBZ8Y7YccE- \
  --file ./foto.jpg \
  --dry-run

# Upload resumable (auth obrigatória)
python scripts/drive_resumable_upload.py \
  --parent 1pYlbPeFcp2RyB1ZqEn9RNFBZ8Y7YccE- \
  --file ./foto.jpg \
  --name "OS-34_Antes_caixa_fusiveis.jpg"
```

`--parent` é o ID da pasta Drive (OS-34 `00_Antes` = `1pYlbPeFcp2RyB1ZqEn9RNFBZ8Y7YccE-`). `--name` é opcional; o padrão é o basename do `--file`.

### O que não fazer

- Não apontar `GOOGLE_APPLICATION_CREDENTIALS` para um ficheiro dentro do clone.
- Não usar MCP `create_file` “para testar”.
- Não ligar n8n para compensar a falta de auth.
