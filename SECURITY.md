# Segurança — Fidalgo Hub

## Como reportar (privado)

Se encontrar um problema de segurança, **não abra issue pública** e **não publique PoC, payload ou passos de ataque**.

Envie um e-mail privado ao Founder:

**ricardofidalgocwb@gmail.com**

Inclua o que observou e em que arquivo ou ambiente, sem anexar tokens, dumps de `.env` ou credenciais.

## Sites unpublished × repositório público

Os sites em `sites/` (Heros Custom, Eletro Fidalgo e páginas relacionadas) estão **unpublished**: usam `meta robots noindex, nofollow` e não devem ir ao ar sem OK do Founder.

O repositório **é público**. Tudo que entrar no Git fica visível. Não coloque secrets no código.

## Segredos e `.env`

- Nunca commite `.env`, `.env.local` nem arquivos de credencial (JSON de service account, tokens OAuth, etc.).
- Use `.env.example` como modelo e preencha o `.env` local (já no `.gitignore`).

## Padrões seguros (não desligar)

O hub opera em dry-run por omissão:

- `CONFIRM=0` — sem escrita no Notion até `CONFIRM=1` (CLI) ou confirmação explícita na UI, sempre com `NOTION_TOKEN`.
- n8n **desligado**: `N8N_AVANCAR_ENABLED=0`. Aprovar nunca dispara n8n. Avançar só posta webhook se a flag e o webhook estiverem ativos.

Não altere essas portas, não adicione bypasses e não enfraqueça as guardas de dry-run.
