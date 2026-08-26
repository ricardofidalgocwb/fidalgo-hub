# Heros Custom (unpublished sibling-grid face)

Static preview of **Face 3** from the sibling-grid spec. It lives in this repo because a separate Origin namespace was not available.

**This site is unpublished.** It must **not** go live until Ricardo says so.

The public door today is [Instagram @heroseletric](https://www.instagram.com/heroseletric). Instagram remains the vitrine until Ricardo publishes.

Do **not**:

- Deploy this folder to production
- Point a custom domain at it
- Use `heroscustom.com` or `@heroscustom` (those are not this oficina)
- Copy this NAP onto Eletro Fidalgo or FSE / Soluções
- Copy EF NAP (BR-116, 3333-8644, 99979-3395) onto this site
- Put **557** on Contato, in the footer, or in the five-item IA (557 is garage / clube only)
- Add Clube to the nav
- Add FSE or Eletro Fidalgo pages here

## Routes (canonical IA)

Only these five items appear in the header and footer:

| Label    | Path       |
|----------|------------|
| Início   | `/`        |
| Serviços | `/servicos`|
| Prova    | `/prova`   |
| Como     | `/como`    |
| Contato  | `/contato` |

Grupo Fidalgo is a footer endorsement chip. It is not a link and not a fourth site.

## NAP (Heros Custom only)

- **Address:** Olímio Monteiro Soares 439, Fanny
- **WhatsApp:** (41) 99187-8091 — `https://wa.me/5541991878091`
- **Instagram:** @heroseletric — `https://www.instagram.com/heroseletric`
- **E-mail:** heroscustomeletric@gmail.com

No landline in this spec. No CEP, CNPJ, CPF, or a second street number.

## How to run locally

From this folder:

```bash
cd sites/heros-custom
python3 -m http.server 4174 --bind 127.0.0.1
```

Or:

```bash
npm start
```

Then open:

- http://127.0.0.1:4174/
- http://127.0.0.1:4174/servicos/
- http://127.0.0.1:4174/prova/
- http://127.0.0.1:4174/como/
- http://127.0.0.1:4174/contato/

No Netlify site, no production publish, no secrets, no custom domain.

## Stack

Plain HTML, CSS, and a small script for the mobile menu. Montserrat (headings) + Inter (body). Gold `#C9A227` plus carbon-gray UI (no second brand hex). Copy is pt-BR from `docs/sites/heros-custom.md`.

Proof photos are 4:3 placeholders. Do not name live OS, client, plate, or vehicle. Do not invent metrics.
