# MovieFlow: 13 modelos

[![MovieFlow: 13 modelos](guia/assets/banner-es.jpg)](https://inematds.github.io/movieflow-modelos/guia/es/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## Qué es

MovieFlow (movieflow.ai) es un estudio de películas con IA: escribes una idea y arma la historia, los personajes, las escenas y la película. Detrás de él hay 13 modelos de otras empresas (Seedance, Kling, Veo, MiniMax, Vidu, Nano Banana, GPT Image y otros), y cada uno es mejor en algo. Este proyecto reúne, en una guía y en un archivo de datos, qué hace cada modelo, sus límites y cuándo usarlo. Para usarlo basta con leer la página; quien quiera puede ejecutar el selector en la terminal con Python, sin instalar nada.

## 📖 Guía de uso

Guía completa (landing + paso a paso): **https://inematds.github.io/movieflow-modelos/guia/es/**

## Los 13 modelos

| Modelo | Tipo | Úsalo cuando |
|---|---|---|
| Seedance 2.5 | video | plano largo (hasta 30 s) con sonido y el mismo personaje |
| MovieFlow 2.0 Ultra | video | borrador rápido y barato (US$ 0,008/s) |
| MiniMax H3 | video | imagen 2K nítida, referencias, corregir un detalle |
| Kling 3.0 | video | cortes (2 a 6 planos), acción, habla sincronizada |
| Seedance 2.0 | video | copiar movimiento/estilo de una referencia |
| Vidu Q3 Pro | video | conversación entre varios personajes, anime |
| Veo 3 | video | plano corto realista con habla y ambiente |
| Seedance Fast | video | probar varias versiones barato (hasta 720p) |
| Kling 2.6 | video | escena simple de 5–10 s, copiar un gesto |
| Nano Banana Pro | imagen | texto en la imagen, cuadro clave del personaje |
| Nano Banana 2 | imagen | muchas imágenes rápidas (storyboard) |
| GPT Image 2 | imagen | texto denso, diagrama, panel de cómic, retoque |
| Seedream 5.0 | imagen | 4K barato, editar solo una región |

Fuentes y límites de cada uno en `modelos.json` (datos del 06/11/2026; "no coincide" = las fuentes no coinciden).

## El proceso, de principio a fin

1. 🧠 **Elegir el modelo de la escena** — `python3 escolher.py "descrição da cena"` (o los botones de la guía; la herramienta entiende palabras clave en portugués).
2. 🧠 **Ver la ficha** — `python3 escolher.py --modelo kling-3.0` / `--lista --tipo video`.
3. 🧠 **Crear en MovieFlow** — movieflow.ai → Agent V2 → idea, idioma, duración, formato → Create; borrador en el modelo barato, escena final en el indicado.
4. 🧠 **Actualizar los datos** cuando cambie la lista de MovieFlow — editar `modelos.json`.
5. ⚙️ **Volver a armar la página** — `python3 montar_guia.py` (genera `guia/index.html`); 🤖 volver a traducir `guia/en/` y `guia/es/`.
6. ⚙️ **Publicar** — commit + push; GitHub Pages (Actions) publica solo.

Leyenda: 🧠 sesión con Nei · ⚙️ script · 🤖 agente.

## Archivos

- `modelos.json` — los 13 modelos (fabricante, duración, audio, destacado, úsalo cuando, límites, fuentes).
- `escolher.py` — indica el modelo según la descripción de la escena (Python 3, sin dependencias, sin red).
- `montar_guia.py` — arma `guia/index.html` a partir de `modelos.json`.
- `guia/` — página en PT, `guia/en/` y `guia/es/`.

Licencia MIT · [INEMA.CLUB](https://inema.club)
