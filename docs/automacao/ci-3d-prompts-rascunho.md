# CI rascunho — prompts + pipeline 3D + apparel

**GitHub CI draft only.** **n8n Active = STOP.** Sem secrets. Dry-run / guarda de árvore.

HUB: [tubo 3D + prompts](https://app.notion.com/p/3df7d36bae6481508231cbdfbede618a) · [apparel](https://app.notion.com/p/3df7d36bae64810f98a3db032d989d1f)

## O que este rascunho **não** é

- Não é workflow n8n.
- Não liga `N8N_AVANCAR_ENABLED`.
- Não publica, não faz deploy, não abre Hotmart, não aponta domínio.
- Não commita binário 3D nem foto de produto.

## Proposta (checks)

O workflow já existente [`.github/workflows/founder_panel_tests.yml`](../../.github/workflows/founder_panel_tests.yml) corre `pytest tests/` em **todo pull request**. A guarda deste rascunho entra por `tests/test_prompts_3d_scaffold.py` — sem workflow novo «ativo» que confunda.

Checks humanos que o pytest espelha:

1. Existem `prompts/` + `docs/3d-pipeline/` + `apparel/`.
2. `prompts/README.md` indexa taxonomia N0-A | F-P0 | C2 | GEN-F | HA-E | 3D | CI, fluxo COM→VIS→ENT, gates **Hotmart STOP**, estilo base + negativo + 5 eixos.
3. Briefs `fusca-p0-chassi|motor|eletrico.md` com IDs `3D-CH|MO|EL-P0` e URLs Notion.
4. Apparel: 5 pastas SKU + **8 TEE** + **2 UNI**.
5. Sem `.glb` / `.fbx` / `.obj` nas pastas placeholder.
6. `N8N_AVANCAR_ENABLED` permanece `0` no job (já no YAML).

## Workflow novo?

**Não habilitar.** Se um YAML extra for preciso no futuro, nomear `*-draft.yml` e deixar `on: workflow_dispatch` comentado. Preferir o pytest acima.

## Dry-run local

```bash
python -m pytest tests/test_prompts_3d_scaffold.py -q
```

*ENT · CI rascunho · n8n Active STOP · Hotmart STOP*
