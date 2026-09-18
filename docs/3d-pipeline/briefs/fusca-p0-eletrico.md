# Brief 3D-EL-P0 — elétrico Type 1 (P0 TEC)

**Status:** unpublished · Hotmart STOP · n8n Active STOP  
**ID:** `3D-EL-P0` · filename `3D-EL-P0-*`  
**Voz:** Oliver

TEC: [Brief 3D Fusca BR P0 · caixa·massa·bandeja](https://app.notion.com/p/3df7d36bae648163a85ec037aa7543cd)  
COM: [Brief 1º projeto 3D · módulo 3D-EL-P0](https://app.notion.com/p/3df7d36bae64811db8ebd95f02dbb21a)

Cânon: **12 V BR = 1968** · **12 V ≠ alternador** · **T1 ≠ T3** · tipada ≥100 KB.

## VO capa

> Sou o Oliver. Aqui você vê o Fusca Type 1 por dentro — chassi, motor a ar e elétrica — com critério, não com achismo.

## COM · o aluno vê (3D-EL-P0)

- Bateria
- Caixa 8 **ou** 12 pólos
- Chicote simplificado
- Massa CS-1

Não entra: Ω completo · bitola cobrada · preço.

## TEC · ordem P0 de modelagem

| # | Asset | Tipada | Textura | Letterform |
|---|-------|--------|---------|------------|
| 1 | **Caixa fusíveis** 8 ou 12 | N0 caixa8/12 · F-P0 caixa PASS | Liberada se PASS | **Obrigatório** se o slot exige código (cite da face, ex. `111 937 505 M` só se lido na tipada 12p — não inventar) |
| 2 | **Ponto massa CS-1** | metal limpo no chassi | **GAP** — bloqueia textura até tipada PASS | Parafuso / área limpa discriminável · sem cabo solto |
| 3 | **Bandeja bateria** | F-P0-1 PASS soft (cip1 tray no repo) | Soft-reuse só com veredito TEC | Bandeja + flanges + hold-down · bornes in situ = upgrade |

## Escopo L0 (TEC)

- Geometria: caixa · bornes de massa · bandeja (proporção T1).
- Materiais genéricos. Sem decalque de código inventado.
- LOD: close-up de aula N0 / F-P0 — não motor completo nesta leva.
- Proibido no mesh/textura: placa · preço · «12 V = alt» · T3.

## Fora deste P0 TEC

Dínamo / alternador · tinware · loom completo · GEN-F fábrica · faces de cliente.

## Checklist letterform (gate TEC antes de texturizar)

| Check | PASS | FAIL |
|-------|------|------|
| ≥100 KB tipada-fonte | bytes OK | <100 KB |
| Slot certo | caixa / massa limpa / bandeja | cabo-malha ≠ CS-1 · pan ≠ bandeja · bay genérico |
| Letterform se o slot exige código | código lido na face (caixa) | sem letterform no slot de código |
| T1 ≠ T3 | peça T1 | T3 / Variante na Mestra T1 |
| Cânon tensão | 1968 · 12 V ≠ alt | «12 V = alt» / ano 1967 |
| Soft-reuse | veredito TEC citado | reuse sem veredito |
| Produto limpo | sem placa / documento de pessoa | identificador vivo |

## Arco (Oliver)

1. **O quê** — caixa, massa limpa, bandeja.
2. **Por quê** — slot errado mente o critério.
3. **Como** — 1–3 callouts no modelo (nesta ordem TEC).
4. **Cheque** — tipada ≥100 KB; letterform só se lido.
5. **Erro** — «12 V ≠ alternador automático» invertido; pan no lugar da bandeja.
6. **Próximo** — ponte N0-A4 / F-P0-1 / F-P0-5.

## Entregáveis

- [ ] Blockout caixa (8 **ou** 12 — não misturar no mesmo mesh)
- [ ] Blockout bandeja
- [ ] Massa CS-1: geometria ok; **textura HOLD**
- [ ] Cutaway ≤5 · explodido 1–6 (legenda vazia ACE)
- [ ] Caption cite-only

## TODO · TEC / COM

- [ ] TEC: veredito letterform da caixa escolhida (8 ou 12).
- [ ] TEC: tipada PASS de massa limpa — até lá, sem textura CS-1.
- [ ] COM: callouts PT-BR (sem jargão interno).
- [ ] ACE: `3D-EL-P0-caixa-*` · `3D-EL-P0-bandeja-*` · `3D-EL-P0-massa-*` após PASS.

Sem binário neste PR. Sem n8n Active.
