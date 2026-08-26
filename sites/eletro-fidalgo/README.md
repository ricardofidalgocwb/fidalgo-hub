# Eletro Fidalgo (unpublished sibling-grid face)

Static preview of **Face 1** from the sibling-grid spec. It lives in this repo because a separate Origin namespace was not available.

**This site is unpublished.** It must **not** replace [eletrofidalgo.net](https://www.eletrofidalgo.net/) until Ricardo says so.

Do **not**:

- Deploy this folder to production
- Point a custom domain at it
- Touch the live Wix site on eletrofidalgo.net
- Use eletrofidalgo.com.br (that domain stays parked)
- Copy this NAP onto FSE / Soluções or Heros Custom
- Add FSE or Heros pages here

## Routes (canonical IA)

Only these five items appear in the header and footer:

| Label   | Path       |
|---------|------------|
| Início  | `/`        |
| Serviços| `/servicos`|
| Prova   | `/prova`   |
| Como    | `/como`    |
| Contato | `/contato` |

Grupo Fidalgo is a footer endorsement chip. It is not a link and not a fourth site.

## NAP (EF only)

- **Address:** Rodovia BR 116 - Linha Verde Km 101 nº 13238, Vila Fany, Curitiba – PR
- **Telefone:** (41) 3333-8644
- **WhatsApp:** (41) 99979-3395 — `https://wa.me/5541999793395`

## How to run locally

From this folder:

```bash
cd sites/eletro-fidalgo
python3 -m http.server 4173 --bind 127.0.0.1
```

Or:

```bash
npm start
```

Then open:

- http://127.0.0.1:4173/
- http://127.0.0.1:4173/servicos/
- http://127.0.0.1:4173/prova/
- http://127.0.0.1:4173/como/
- http://127.0.0.1:4173/contato/

No Netlify site, no production publish, no secrets.

## Stack

Plain HTML, CSS, and a small script for the mobile menu and the contact-form notice. Montserrat (headings) + Inter (body). Navy `#1C2E4A` plus steel-gray UI. Copy is pt-BR, mapped from eletrofidalgo.net and `docs/sites/sibling-grid.md`.

Proof photos are 4:3 placeholders. Named obras (Cocelpa, Fundição Tupy, Perfilados Paraná, Darnel) are text, not invented plant photos.

The contact form does not send mail and does not invent an email address. Use the phone or WhatsApp numbers above.
