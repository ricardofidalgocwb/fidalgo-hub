# Sibling-grid site spec

**Status:** written spec in this repo only. Not published. Not a Wix patch, not a live deploy, not an app rewrite.

Three public faces share one information architecture and one chrome. Grupo Fidalgo is an endorsement chip in the footer — not a fourth door.

## Canonical IA (all faces)

`Início` · `Serviços` · `Prova` · `Como` · `Contato`

Do not add extra top-nav items.

## Shared chrome

| Token | Spec |
|---|---|
| Type | **Montserrat** (display / headings) + **Inter** (UI / body) |
| Header | Face wordmark + the five IA links. No Grupo Fidalgo door. |
| Footer | Face NAP (when the face has NAP) + the same five links + **Grupo Fidalgo** endorsement chip |
| Proof photos | **4:3** only |
| Chip | Footer only. Does not navigate to a fourth site. |

## Faces (do not invent extra brands)

| Order | Face | Palette | This spec |
|---|---|---|---|
| 1 | **Eletro Fidalgo (EF)** | Navy `#1C2E4A` / steel | Fully specified below |
| 2 | **FSE / Soluções** | Paint `#1B2430` / teal `#2A6F7A` | Stub only |
| 3 | **Heros Custom** | Gold `#C9A227` / carbon | Out of scope except one line |

Steel (EF) and carbon (Heros) have no hex in this spec — do not invent one.

---

## 1. Eletro Fidalgo — full spec

Live **content source:** [https://www.eletrofidalgo.net/](https://www.eletrofidalgo.net/) (Wix). Snapshot used for this mapping: 2026-08-26.

**`.com.br` stays parked.** [https://eletrofidalgo.com.br/](https://eletrofidalgo.com.br/) is not the live site and must not replace `.net`. Spec it as parked until a later, explicit cutover.

### NAP (EF only — never copy to FSE or Heros)

| Field | Value |
|---|---|
| Address | Rodovia BR 116 - Linha Verde Km 101 nº 13238, Vila Fany, Curitiba – PR |
| Telefone | (41) 3333-8644 |
| WhatsApp | (41) 99979-3395 |

### Wix IA today (7 routes)

Home dump + five service verticals + contact:

| Wix route | What is there now |
|---|---|
| `/` | Home dump: “SOBRE NÓS” (60+ years, comércio e recuperação AT/BT) + bullet list of services |
| `/transformadores` | AT/BT transformers; **proof-in-kVA lives here** |
| `/locacao` | Transformer rental capacities + caminhão MUNK |
| `/ensaios` | NBR-5356 / COPEL / óleo tests + job/fachada photo dump |
| `/motores` | Motor types + comércio / manutenção / recuperação |
| `/geradores` | Geradores / grupos geradores + recovery steps |
| `/contact` | NAP + Wix form |

Home-only bullets with **no own route:** disjuntores, chaves compensadoras, retificadores, filtragem de óleo, manutenção em cabines AT, laudos de óleo. Fold these into `Serviços`; do not create extra top-level brands or doors.

### Map onto sibling IA

| Sibling | Target path | Maps from Wix today | Gap |
|---|---|---|---|
| **Início** | `/` | `/` home dump | — |
| **Serviços** | `/servicos` | `/transformadores`, `/locacao`, `/ensaios`, `/motores`, `/geradores` + home bullets | No single Serviços hub today (five sibling URLs instead) |
| **Prova** | `/prova` | Partial: kVA on `/transformadores`; job photos on `/ensaios` | **No dedicated Prova page** |
| **Como** | `/como` | Partial: ensaio method lists on `/ensaios`; recovery steps on `/motores` and `/geradores` | **No dedicated Como page** |
| **Contato** | `/contato` | `/contact` | — |

Existing Wix slugs may stay as aliases later. This spec does not implement redirects.

### Serviços (what the hub must cover)

1. **Transformadores** — novos e recondicionados; a óleo e a seco; relatório de ensaios; garantia; padrão COPEL / CELESC / concessionárias.
2. **Locação** — transformadores para manutenção ou emergência; classes 15 kV, 25 kV, 34,5 kV; tensões 440/254 V; caminhão MUNK.
3. **Ensaios** — NBR-5356 / COPEL; óleo (rigidez, cromatografia, físico-química, PCB).
4. **Motores** — trifásicos, monofásicos, CC, varimots, vibradores, bombas, motoredutor; comércio / manutenção / recuperação.
5. **Geradores** — comércio / manutenção / recuperação; carvão, anéis, excitatriz estática besides the shared rewind/test steps.

### Proof-in-kVA (from `/transformadores`)

Move the kVA proof onto **Prova** (4:3 photos + numbers). Keep a short pointer from Serviços.

| Família | Faixa (Wix) |
|---|---|
| Trifásicos | 15–2000 kVA |
| Monofásicos | 5–37,5 kVA |
| A seco trifásicos | 3–1000 kVA |
| A seco monofásicos | 3–30 kVA |
| BT sob encomenda trifásicos | 5–500 kVA |

Locação lists 45–1000 kVA at 15 kV (380/220 e 220/127). That is rental stock, not the Prova kVA table.

### Prova / Como (new pages)

- **Prova:** kVA table above + 4:3 crop of current `/ensaios` proof (fachada; obras nomeadas no Wix: Cocelpa, Fundição Tupy, Perfilados Paraná, Darnel).
- **Como:** ensaio sequence (relação, ôhmica, isolamento, tensão induzida/aplicada, excitação, impedância, perdas) + recovery sequence (estufa, rebobinamento, testes, balanceamento, rolamentos). Do not invent a process that is not on Wix.

### Contato

NAP as tabled. WhatsApp CTA uses **(41) 99979-3395** only. Wix form stays a contact form; this spec does not invent extra emails.

---

## 2. FSE / Soluções — stub only

- Paint `#1B2430` / teal `#2A6F7A`.
- Same IA and chrome as EF.
- **No live site in this spec.**
- **NAP = TODO.** Do not copy EF address, telefone, or WhatsApp.

No pages, offers, or proof assets specified here.

---

## 3. Heros Custom — out of scope

Heros Custom (gold `#C9A227` / carbon) is a third face and **shares this grid later**. Do not invent Heros NAP, pages, or copy in this PR.

---

## Hard rules

1. WhatsApp and address **never** cross companies.
2. Grupo Fidalgo chip is footer endorsement only — not a fourth face.
3. Do not add brands beyond EF, FSE / Soluções, and Heros Custom.
4. `eletrofidalgo.com.br` stays parked; `.net` remains the live content source.
5. This file is not a publish, deploy, or Wix edit.
