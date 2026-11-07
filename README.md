# MovieFlow: 13 modelos

[![MovieFlow: 13 modelos](guia/assets/banner.jpg)](https://inematds.github.io/movieflow-modelos/guia/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## O que é

O MovieFlow (movieflow.ai) é um estúdio de filmes com IA: você escreve uma ideia e ele monta a história, os personagens, as cenas e o filme. Por trás dele há 13 modelos de outras empresas (Seedance, Kling, Veo, MiniMax, Vidu, Nano Banana, GPT Image e outros), e cada um é melhor numa coisa. Este projeto reúne, num guia e num arquivo de dados, o que cada modelo faz, os limites e quando usar. Para usar é só ler a página; quem quiser pode rodar o escolhedor no terminal com Python, sem instalar nada.

## 📖 Guia de uso

Guia completo (landing + passo a passo): **https://inematds.github.io/movieflow-modelos/guia/**

## Os 13 modelos

| Modelo | Tipo | Use quando |
|---|---|---|
| Seedance 2.5 | vídeo | plano longo (até 30 s) com som e o mesmo personagem |
| MovieFlow 2.0 Ultra | vídeo | rascunho rápido e barato (US$ 0,008/s) |
| MiniMax H3 | vídeo | imagem 2K nítida, referências, corrigir um detalhe |
| Kling 3.0 | vídeo | cortes (2 a 6 planos), ação, fala sincronizada |
| Seedance 2.0 | vídeo | copiar movimento/estilo de uma referência |
| Vidu Q3 Pro | vídeo | conversa entre vários personagens, anime |
| Veo 3 | vídeo | plano curto realista com fala e ambiente |
| Seedance Fast | vídeo | testar várias versões barato (até 720p) |
| Kling 2.6 | vídeo | cena simples de 5–10 s, copiar gesto |
| Nano Banana Pro | imagem | texto na imagem, quadro-chave do personagem |
| Nano Banana 2 | imagem | muitas imagens rápidas (storyboard) |
| GPT Image 2 | imagem | texto denso, diagrama, painel de HQ, retoque |
| Seedream 5.0 | imagem | 4K barato, editar só uma região |

Fontes e limites de cada um em `modelos.json` (dados de 06/11/2026; "diverge" = fontes não batem).

## O processo, do início ao fim

1. 🧠 **Escolher o modelo da cena** — `python3 escolher.py "descrição da cena"` (ou os botões do guia).
2. 🧠 **Ver a ficha** — `python3 escolher.py --modelo kling-3.0` / `--lista --tipo video`.
3. 🧠 **Criar no MovieFlow** — movieflow.ai → Agent V2 → ideia, idioma, duração, formato → Create; rascunho no modelo barato, cena final no indicado.
4. 🧠 **Atualizar os dados** quando a lista do MovieFlow mudar — editar `modelos.json`.
5. ⚙️ **Remontar a página** — `python3 montar_guia.py` (gera `guia/index.html`); 🤖 retraduzir `guia/en/` e `guia/es/`.
6. ⚙️ **Publicar** — commit + push; o GitHub Pages (Actions) publica sozinho.

Legenda: 🧠 sessão com o Nei · ⚙️ script · 🤖 agente.

## Arquivos

- `modelos.json` — os 13 modelos (fabricante, duração, áudio, destaque, use quando, limites, fontes).
- `escolher.py` — indica o modelo pela descrição da cena (Python 3, sem dependências, sem rede).
- `montar_guia.py` — monta `guia/index.html` a partir do `modelos.json`.
- `guia/` — página em PT, `guia/en/` e `guia/es/`.

Licença MIT · [INEMA.CLUB](https://inema.club)
