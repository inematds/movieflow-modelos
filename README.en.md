# MovieFlow: 13 models

[![MovieFlow: 13 models](guia/assets/banner-en.jpg)](https://inematds.github.io/movieflow-modelos/guia/en/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## What it is

MovieFlow (movieflow.ai) is an AI film studio: you write an idea, and it creates the story, characters, scenes, and film. It uses 13 models from other companies (Seedance, Kling, Veo, MiniMax, Vidu, Nano Banana, GPT Image, and others), each best at something different. This project brings together what each model can do, its limits, and when to use it in a guide and a data file. To use it, just read the page; if you want, you can run the selector in the terminal with Python, without installing anything.

## 📖 User guide

Complete guide (landing page + step-by-step instructions): **https://inematds.github.io/movieflow-modelos/guia/en/**

## The 13 models

| Model | Type | Use when |
|---|---|---|
| Seedance 2.5 | video | creating a long shot (up to 30 s) with sound and the same character |
| MovieFlow 2.0 Ultra | video | making a quick, low-cost draft (US$0.008/s) |
| MiniMax H3 | video | creating a sharp 2K image, using references, or fixing a detail |
| Kling 3.0 | video | creating cuts (2 to 6 shots), action, or synchronized dialogue |
| Seedance 2.0 | video | copying movement or style from a reference |
| Vidu Q3 Pro | video | creating conversations between several characters or anime |
| Veo 3 | video | creating a short, realistic shot with dialogue and ambient sound |
| Seedance Fast | video | testing several versions at low cost (up to 720p) |
| Kling 2.6 | video | creating a simple 5–10 s scene or copying a gesture |
| Nano Banana Pro | image | adding text to an image or creating a character keyframe |
| Nano Banana 2 | image | creating many images quickly (storyboard) |
| GPT Image 2 | image | creating dense text, a diagram, a comic panel, or a retouch |
| Seedream 5.0 | image | creating an inexpensive 4K image or editing just one region |

Sources and limits for each model are in `modelos.json` (data from 06/11/2026; “conflicting” = sources don’t match).

## The process, start to finish

1. 🧠 **Choose the scene model** — `python3 escolher.py "descrição da cena"` (the tool understands Portuguese keywords) (or use the guide buttons).
2. 🧠 **View the model details** — `python3 escolher.py --modelo kling-3.0` / `--lista --tipo video`.
3. 🧠 **Create in MovieFlow** — movieflow.ai → Agent V2 → idea, language, duration, format → Create; draft with the low-cost model, final scene with the recommended one.
4. 🧠 **Update the data** when MovieFlow’s list changes — edit `modelos.json`.
5. ⚙️ **Rebuild the page** — `python3 montar_guia.py` (generates `guia/index.html`); 🤖 translate `guia/en/` and `guia/es/` again.
6. ⚙️ **Publish** — commit + push; GitHub Pages (Actions) publishes automatically.

Legend: 🧠 session with Nei · ⚙️ script · 🤖 agent.

## Files

- `modelos.json` — the 13 models (manufacturer, duration, audio, highlight, when to use, limits, sources).
- `escolher.py` — recommends a model based on the scene description (Python 3, no dependencies, no network).
- `montar_guia.py` — builds `guia/index.html` from `modelos.json`.
- `guia/` — page in Portuguese, `guia/en/`, and `guia/es/`.

MIT License · [INEMA.CLUB](https://inema.club)