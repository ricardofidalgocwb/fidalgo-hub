# Biblioteca de prompts — unpublished

**HUB-tubo-3d-pesquisa-1709** · rascunho interno · **Hotmart STOP** · **n8n Active STOP**.

Voz: **Oliver** (tutor, não bot). Gold `#C9A227` ≤15%. Base `#0D0D0D` · Ivory `#F5F0E6`.
Zero preço · checkout · placa · documento de pessoa · endereço de oficina no miolo gerado.

SSOT COM: [Biblioteca prompts N0-A/F-P0/GEN-F/3D/CI · 5 eixos](https://app.notion.com/p/3df7d36bae6481e59c12d47f39391e95)

Pai: [HUB- · Tubo 3D + prompts + pesquisa clássicos · 17/09](https://app.notion.com/p/3df7d36bae6481508231cbdfbede618a)

Todo prompt = **rascunho**. Tipada real ≥100 KB vence still gerado. Type 1 only nas trilhas de aula; Type 3 / Variante técnica = módulo aparte (merch cultural ≠ Mestra).

## Taxonomia

| Código | Trilha | Pasta | Prompts |
|--------|--------|-------|---------|
| **N0-A** | Elétrica simples A1–A6 | [`n0-a/`](n0-a/) | `P-N0-*` |
| **F-P0** | Cap.2 / Fusca Passaporte | [`f-p0/`](f-p0/) | `P-FP-*` |
| **C2** | Cap.2 anatomia (e-book) | — | reusa F-P0 + pack Cap.2 |
| **GEN-F** | Gênese Fusca | [`gen-f/`](gen-f/) | `P-GF-*` |
| **HA-E** | Catálogo elétrico | — | reusa CI + pack Peças |
| **3D** | Fusca air-cooled | [`3d/`](3d/) | `P-3D-*` |
| **CI** | Guardas pytest | [`ci/`](ci/) | `P-CI-*` |

## Gates

- **Hotmart STOP** — sem checkout, sem anúncio, sem ir ao ar.
- Sem domínio / sem publish / sem filmar sem tipada.
- **n8n Active STOP** — automação só rascunho GitHub CI. Ver [`docs/automacao/ci-3d-prompts-rascunho.md`](../docs/automacao/ci-3d-prompts-rascunho.md).
- Sem PN / Ω / torque inventados.

## Fluxo

```
COM → VIS → ENT
```

COM escreve prompt/roteiro → VIS tipa ou modela (cite-only) → ENT empacota **unpublished**.
Tubo 3D irmão: [`docs/3d-pipeline/README.md`](../docs/3d-pipeline/README.md).

## 5 eixos (colar na meta de cada prompt)

| Eixo | Meta no output |
|------|----------------|
| **Instrução** | O quê → Por quê → Como → Cheque → Erro → Próximo |
| **Interativo** | 1 pergunta **ou** 1 checklist ≤5 |
| **Formação** | Ponte clara N0-A ↔ F-P0 ↔ GEN-F ↔ 3D |
| **Visual** | Gold ≤15% · tipada/cite · sem placa |
| **Métricas** | 1 critério verificável (ex.: 1968 · 8 vs 12 pólos) |

## Estilo base (sempre)

```
Heros Custom educational asset, Type 1 VW Beetle aircooled, dark #0D0D0D, ivory #F5F0E6, gold #C9A227 max 15%, didactic Oliver tutor tone, no license plate, no price, no WhatsApp, no Hotmart, photoreal or clean CAD, unpublished draft
```

## Negativo (sempre)

```
license plate, CPF, price tag, shopping cart, Hotmart, WhatsApp logo, Staff jargon, OS number, Path A, Type 3 Variant mixed with Type 1 lesson, influencer smile, cash, checkout QR
```

## Índice

| ID | Ficheiro | Uso curto |
|----|----------|-----------|
| P-N0-capa | [`n0-a/p-n0-capa.md`](n0-a/p-n0-capa.md) | Title card aula A1–A6 |
| P-N0-still | [`n0-a/p-n0-still.md`](n0-a/p-n0-still.md) | Close-up cite-ready |
| P-N0-check | [`n0-a/p-n0-check.md`](n0-a/p-n0-check.md) | Overlay checklist |
| P-N0-mito | [`n0-a/p-n0-mito.md`](n0-a/p-n0-mito.md) | Quadro «não faça» |
| — | [`n0-a/roteiro-a1-a6.md`](n0-a/roteiro-a1-a6.md) | Roteiro videoaula arco Oliver |
| P-FP-capa | [`f-p0/p-fp-capa.md`](f-p0/p-fp-capa.md) | Title card Passaporte |
| P-FP-still | [`f-p0/p-fp-still.md`](f-p0/p-fp-still.md) | Peça / bay didático |
| P-FP-flatlay | [`f-p0/p-fp-flatlay.md`](f-p0/p-fp-flatlay.md) | Conjunto evidência |
| P-FP-antesdepois | [`f-p0/p-fp-antesdepois.md`](f-p0/p-fp-antesdepois.md) | Split só com tipada PASS |
| — | [`f-p0/roteiro-cap2-passaporte.md`](f-p0/roteiro-cap2-passaporte.md) | Exemplo Cap.2 / Passaporte |
| P-GF-capa | [`gen-f/p-gf-capa.md`](gen-f/p-gf-capa.md) | Chapter card gênese |
| P-GF-hist | [`gen-f/p-gf-hist.md`](gen-f/p-gf-hist.md) | Still histórico cite-only |
| P-GF-ponte | [`gen-f/p-gf-ponte.md`](gen-f/p-gf-ponte.md) | Ponte gênese → N0 |
| P-3D-blockout | [`3d/p-3d-blockout.md`](3d/p-3d-blockout.md) | CAD limpo T1 |
| P-3D-cutaway | [`3d/p-3d-cutaway.md`](3d/p-3d-cutaway.md) | Corte didático ≤5 |
| P-3D-explod | [`3d/p-3d-explod.md`](3d/p-3d-explod.md) | Explodido 1–6 |
| P-3D-tex | [`3d/p-3d-tex.md`](3d/p-3d-tex.md) | Preview material |
| P-CI-guard | [`ci/p-ci-guard.md`](ci/p-ci-guard.md) | Revisar guarda pytest |
| P-CI-copy | [`ci/p-ci-copy.md`](ci/p-ci-copy.md) | Diff miolo (defensivo) |
| P-CI-slot | [`ci/p-ci-slot.md`](ci/p-ci-slot.md) | Mapear ficheiro → taxonomia |

*COM · Biblioteca prompts tubo 3D · unpublished · Hotmart STOP*
