# Heros Custom (unpublished sibling-grid face)

Static preview of **Face 3** from the sibling-grid spec, extended as an MVP
landing for **agendamento + clube + vagas**. It lives in this repo because a
separate Origin namespace was not available.

**This site is unpublished.** Banner on every page:

`UNPUBLISHED · DRAFT · Founder OK required to go live`

It must **not** go live until Ricardo says so.

The public door today is [Instagram @heroseletric](https://www.instagram.com/heroseletric). Instagram remains the vitrine until Ricardo publishes.

Do **not**:

- Deploy this folder to production
- Point a custom domain at it
- Use `heroscustom.com` or `@heroscustom` (those are not this oficina)
- Copy this NAP onto Eletro Fidalgo or FSE / Soluções
- Copy EF NAP (BR-116, 3333-8644, 99979-3395) onto this site
- Put **557** on Contato as NAP, in the footer NAP, or in the five-item IA (557 is clube / curadoria / aluguel context only)
- Add Clube to the nav
- Add FSE or Eletro Fidalgo pages here
- Promise Trello as live ERP, NF automática, portal do cliente, Hotmart, n8n, NFT or checkout

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

Início is the MVP landing: hero, five service CTAs, jornada, clube & curadoria, formulário. Clube stays a section, not a sixth nav item.

## NAP (Heros Custom only)

- **Address:** Rua Olímio Monteiro Soares 439, Fanny, Curitiba
- **WhatsApp:** (41) 99187-8091 — `https://wa.me/5541991878091`
- **Instagram:** @heroseletric — `https://www.instagram.com/heroseletric`
- **E-mail:** heroscustomeletric@gmail.com

No landline. No CEP, CNPJ, CPF, or a second street number as NAP.

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

Plain HTML, CSS, and a small script for the mobile menu and the contact form.
Montserrat (headings) + Inter (body). Gold v1.1: `#C9A227` / `#0D0D0D` /
`#1A1A1A` / `#F5F0E6`. Copy is pt-BR.

The form does **not** use Formspree, Netlify Forms or n8n. Submit opens
WhatsApp (`wa.me/5541991878091`) or `mailto:heroscustomeletric@gmail.com`
with prefilled text.

Guarda price, if shown: “a partir de R$ 650/mês, sujeita a vaga” — reference
only, not a cart. Notion Vagas has no public free-slot count; do not invent one.

Proof photos are 4:3 placeholders. Do not name live OS, client, plate, or vehicle. Do not invent metrics.
