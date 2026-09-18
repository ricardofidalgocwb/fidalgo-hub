# Pipeline 3D Fusca air-cooled — unpublished

**HUB-tubo-3d-pesquisa-1709** · rascunho de pastas · **sem binários 3D** · **Hotmart STOP** · **n8n Active STOP**.

Voz capa (Oliver):

> Sou o Oliver. Aqui você vê o Fusca Type 1 por dentro — chassi, motor a ar e elétrica — com critério, não com achismo.

SSOT:

- Pai: [HUB- · Tubo 3D + prompts](https://app.notion.com/p/3df7d36bae6481508231cbdfbede618a)
- COM brief: [1º projeto 3D chassi·motor·elétrico](https://app.notion.com/p/3df7d36bae64811db8ebd95f02dbb21a)
- TEC brief: [3D Fusca BR P0 · caixa·massa·bandeja](https://app.notion.com/p/3df7d36bae648163a85ec037aa7543cd)
- Prompts âncora: [`../../prompts/3d/`](../../prompts/3d/)

Cânon: **12 V BR = 1968** · **12 V ≠ alternador** · **T1 ≠ T3** · tipada ≥100 KB · soft-reuse só com veredito TEC · sem PN / Ω / torque inventados.

## Tubo

```
Pesquisa/VIS → Ops tip ≥100KB → TEC PASS|HOLD → ACE slot → ENT unpublished → APR
```

COM escreve brief + prompt → VIS/3D modela e texturiza → TEC PASS ou HOLD → ACE indexa o slot → ENT empacota unpublished → APR prova os 5 eixos.

## Estágios (asset)

Ordem: brief → modelo → textura → slot ACE.

1. **Brief** — [`briefs/`](briefs/) (TEC/COM preenchem; TODOs visíveis).
2. **Modelo** — blockout / cutaway / explodido (pasta placeholder).
3. **Textura** — PBR fosco; letterform só se lido na tipada PASS.
4. **Slot ACE** — filename taxonomia; Mestra só depois de PASS.

## Módulos P0

| ID | Brief | Aluno vê | Não entra |
|----|-------|----------|-----------|
| **3D-CH-P0** | [`briefs/fusca-p0-chassi.md`](briefs/fusca-p0-chassi.md) | Assoalho · canais · bandeja · massa visível | Solda cobrada · PN de funilaria |
| **3D-MO-P0** | [`briefs/fusca-p0-motor.md`](briefs/fusca-p0-motor.md) | Bloco · tinware · correia · dínamo ≠ alt (volumes) | Torque · folga · PN de kit |
| **3D-EL-P0** | [`briefs/fusca-p0-eletrico.md`](briefs/fusca-p0-eletrico.md) | Bateria · caixa 8/12 · chicote simples · massa CS-1 | Ω completo · bitola cobrada |

TEC P0 **primeiro mesh**: caixa → massa CS-1 (textura GAP) → bandeja. Motor/tinware/dínamo completos = fora desta leva de elétrico.

## Convenção de nomes (sem placa)

Taxonomia: `3D-CH|MO|EL-P0-*`

```
3D-{CH|MO|EL}-P0-{slot}-{vista}.{ext}
```

Exemplos (não commitar o binário):

- `3D-EL-P0-caixa-ortho.glb`
- `3D-EL-P0-bandeja-34.png`
- `3D-CH-P0-assoalho-explod.glb`
- `3D-MO-P0-bloco-cutaway.png`

Proibido no nome e no mesh: placa · documento de pessoa · preço · «12 V = alt».

## Pastas placeholder (sem binário)

| Pasta | Função |
|-------|--------|
| `briefs/` | Texto TEC/COM |
| `assets/3d-ch-p0/` | Slot chassi — só `.gitkeep` |
| `assets/3d-mo-p0/` | Slot motor — só `.gitkeep` |
| `assets/3d-el-p0/` | Slot elétrico — só `.gitkeep` |

Não commitar `.glb` / `.fbx` / `.obj` / texturas grandes neste rascunho.

## Entregáveis (quando modelar)

Blockout (ortho + ¾) · cutaway ≤5 callouts · explodido 1–6 com legenda vazia ACE · still 16:9 + 4:3 · caption cite-only.

## CI

Guarda: `tests/test_prompts_3d_scaffold.py`.
Rascunho: [`../automacao/ci-3d-prompts-rascunho.md`](../automacao/ci-3d-prompts-rascunho.md).

*ENT · pipeline 3D unpublished · Hotmart STOP*
