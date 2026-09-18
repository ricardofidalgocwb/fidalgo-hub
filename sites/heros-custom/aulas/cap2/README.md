# Cap.2 / Fusca F-P0-1…6 — player unpublished

Player/páginas da trilha Cap.2 / Passaporte P0 (Fusca Type 1) em
`sites/heros-custom/aulas/cap2/`. **Irmão do player N0 A1–A6** (`#29`) e do
MVP de agendamento — não é publish.

**Status:** unpublished. Banner `UNPUBLISHED · DRAFT · Founder OK required to go live`.
`meta robots noindex, nofollow`. Sem domínio. Sem YouTube / Vimeo / Hotmart / n8n.

Roteiros SSOT (COM):
[COM- · Roteiros Cap.2 / Fusca Passaporte F-P0-1…6 · P0 unpublished](https://app.notion.com/p/3de7d36bae64811286aad405b7ad3059)

Checklist TEC:
[Checklist TEC](https://app.notion.com/p/3de7d36bae6481938a1bf1bbbb31a0d4)

O miolo do aluno **não** cita estes URLs, nem jargão de Staff, nem G-PASS.

## Rotas

| Página | Path |
|--------|------|
| Índice aulas (N0 + atalho Cap.2) | `/aulas/` |
| Índice F-P0-1…6 | `/aulas/cap2/` |
| F-P0-1 Bandeja da bateria | `/aulas/cap2/f-p0-1/` |
| F-P0-2 Assoalho e canais | `/aulas/cap2/f-p0-2/` |
| F-P0-3 Tinware e aletas | `/aulas/cap2/f-p0-3/` |
| F-P0-4 Linha de combustível | `/aulas/cap2/f-p0-4/` |
| F-P0-5 Massas · caixa · 6/12 V | `/aulas/cap2/f-p0-5/` |
| F-P0-6 Chicote + evidência | `/aulas/cap2/f-p0-6/` |

Cada aula: placeholder de player («vídeo em elaboração · unpublished») + arco
O quê · Por quê · Como · Cheque · Erro comum · Próximo.

Sem iframe. Sem URL de MP4 inventada.

IA: header **Aulas** intacto. Sub-nav nas páginas de aulas: **N0 | Cap.2 / Passaporte P0**.

IDs oficiais: **F-P0-1** … **F-P0-6** (não F1–F6 sozinhos).

Narrador unpublished (persona): **Oliver**. Crédito no player / rodapé — sem embed real.

## Tipadas (TEC veredito — embute só PASS)

| Slot | Veredito | Ação no player |
|------|----------|----------------|
| F-P0-2 pans | PASS `1I3gVHstGfNQtUYju3y9ExeTyDPHMMkGQ` | Embutir tipada |
| F-P0-4 fuel | PASS `1kZYhT9CnNh3tBNgr6WvAj09dknNxCPY6` | Embutir tipada |
| F-P0-3 tinware | PASS Cap.2 AUR+cocc (+prefix BD) | Reuso byte-exact do repo |
| F-P0-1 bandeja | FAIL `1qgrDeJIZFBEdXFq3bvCNQFsJtr-IegD8` | Still textual |
| F-P0-5 massa | FAIL `1OMUS4dfI9CEedI-TfQMA5hJUlnm4q28T` | Still textual; N0 caixa/dínamo/alt = cite only |
| F-P0-6 loom | HOLD `1F7ZMuIvCoEFy7UsW3ppt9yfacLPUTP-7` | Sem tipada viva no miolo |

PASS no player (bytes exactos, sem recomprimir):

| Aula | Ficheiro | Bytes | Legenda humana |
|------|----------|------:|----------------|
| F-P0-2 | `assets/F-P0_pans_channels_SRC-heritage-111701061mr.jpg` | 407659 | pans e canais |
| F-P0-4 | `assets/F-P0_fuel_linha_combustivel_SRC-commons-3564060578.jpg` | 747961 | linha de combustível |
| F-P0-3 | `assets/Cap2_P0_tinware_AUR1500_SRC-commons.jpg` | 483449 | latas no lugar (motor 1500) |
| F-P0-3 | `assets/Cap2_P0_tinware_coccinelle_SRC-commons.jpg` | 1111977 | latas no lugar (Coccinelle) |
| F-P0-3 | `assets/Cap2_P0_prefixBD_crop_SRC-commons.jpg` | 241948 | prefixo no bloco |
| F-P0-3 | `assets/Cap2_P0_prefixBD_fanbelt_SRC-commons.jpg` | 708229 | ventoinha e correia |
| F-P0-3 | `assets/Cap2_P0_tinware_1965AVI_SRC-commons.jpg` | 409825 | foto extra — não substitui o par |

F-P0-5 elétrico (cite only no miolo, **não** no player; origem N0):

| Cite | Ficheiro | Bytes | Legenda humana |
|------|----------|------:|----------------|
| F-P0-5 | `assets/N0_caixa8_fuseBox8polos_SRC-appletree.jpg` | 129434 | 8 pólos |
| F-P0-5 | `assets/N0_caixa12_fuseBox12polos_SRC-cip1-505M.jpg` | 239795 | 12 pólos |
| F-P0-5 | `assets/N0_A8_dinam_SRC-heritagestocks.jpg` | 443360 | isto é dínamo |
| F-P0-5 | `assets/N0_A8_alt_SRC-appletreekit.jpg` | 141153 | isto é alternador |

F-P0-1 e F-P0-6: still textual. Sem foto de stock inventada. Sem tipada FAIL/HOLD no miolo.

Legendas no miolo são humanas. IDs de Drive ficam **fora** das captions e do HTML do aluno.
Sem PN / Ω / torque inventados. Type 1 only.

## Local

```bash
cd sites/heros-custom
python3 -m http.server 4174 --bind 127.0.0.1
```

http://127.0.0.1:4174/aulas/cap2/

## Guarda

`tests/test_fp0_aulas_player.py`

Miolo do aluno: sem R$, sem NAP, sem WhatsApp, sem OS viva, sem Hotmart.
Merge = Founder. Hotmart STOP.
