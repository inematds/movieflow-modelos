#!/usr/bin/env python3
"""Monta guia/index.html (PT) a partir do CSS do template INEMA + modelos.json.
Os cartões dos 13 modelos e o escolhedor da página saem do modelos.json: mudou o JSON, rode de novo e retraduza en/ e es/.
Uso: python3 montar_guia.py [caminho-do-template]"""
import html, json, sys
from pathlib import Path

R = Path(__file__).resolve().parent
TPL = Path(sys.argv[1] if len(sys.argv) > 1 else Path.home() / '.claude/skills/projetos-landing-guia/assets/template.html')
t = TPL.read_text(encoding='utf-8')
css = t[t.index('<style>') + 7:t.index('</style>')]
D = json.loads((R / 'modelos.json').read_text(encoding='utf-8'))
E = html.escape

EXTRA = """
  .mods{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:14px}
  .mod{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px;min-width:0;transition:border-color .2s,transform .2s}
  .mod.on{border-color:var(--amb);transform:translateY(-2px);box-shadow:0 0 0 2px color-mix(in srgb,var(--amb) 35%,transparent)}
  .mod.off{opacity:.38}
  .mod h3{font-size:1.05rem;margin:0 0 .2em}
  .mod .fab{font-size:.78rem;color:var(--mut)}
  .mod .tp{float:right;font-size:.7rem;font-family:Sora;font-weight:700;border-radius:999px;padding:.15em .6em;border:1px solid var(--line);color:var(--amb)}
  .mod p{margin:.55em 0 0;font-size:.9rem}
  .mod .q{color:var(--txt)} .mod .l{color:var(--mut);font-size:.82rem}
  .mod .meta{margin-top:.6em;font-size:.78rem;color:var(--mut)}
  .mod .src{margin-top:.4em;font-size:.74rem;word-break:break-word}
  .need{display:flex;flex-wrap:wrap;gap:8px;margin:6px 0 18px}
  .need button{font:600 .85rem Sora,sans-serif;background:var(--bg2);color:var(--txt);border:1px solid var(--line);border-radius:999px;padding:.5em 1em;cursor:pointer}
  .need button.on{background:var(--amb);color:#1a1206;border-color:var(--amb)}
  .tbl{width:100%;border-collapse:collapse;font-size:.88rem}
  .tbl th,.tbl td{border-bottom:1px solid var(--line);padding:.55em .5em;text-align:left;vertical-align:top}
  .tbl th{font-family:Sora;color:var(--amb);font-size:.8rem}
  .scroll{overflow-x:auto}
  @media(max-width:680px){.flow{flex-direction:column;align-items:flex-start}.flow .arr{transform:rotate(90deg);margin-left:14px}}
  .gl{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:10px 18px;font-size:.9rem}
  .gl div{color:var(--mut)} .gl strong{color:var(--txt)}
  .note{font-size:.85rem;color:var(--mut);border-left:3px solid var(--amb);padding:.4em .9em;margin:14px 0}
"""

# necessidade -> ids (o escolhedor da página; o escolher.py usa as etiquetas do JSON)
NECESSIDADES = [
    ('Rascunho barato', ['movieflow-2.0-ultra', 'seedance-fast', 'nano-banana-2']),
    ('Diálogo com lábios', ['veo-3', 'kling-3.0', 'vidu-q3-pro']),
    ('Ação com cortes', ['kling-3.0', 'kling-2.6']),
    ('Plano longo com som', ['seedance-2.5']),
    ('Mesmo personagem', ['seedance-2.0', 'seedance-2.5', 'minimax-h3']),
    ('Anime / desenho', ['vidu-q3-pro']),
    ('Imagem nítida 2K', ['minimax-h3']),
    ('Copiar movimento', ['kling-2.6', 'seedance-2.0']),
    ('Texto na imagem', ['nano-banana-pro', 'gpt-image-2']),
    ('Storyboard rápido', ['nano-banana-2', 'gpt-image-2']),
    ('Corrigir um pedaço', ['minimax-h3', 'seedream-5.0', 'gpt-image-2']),
]


def card(m):
    fontes = ' · '.join(f'<a href="{E(u)}" target="_blank" rel="noopener">fonte {i}</a>' for i, u in enumerate(m['fontes'], 1))
    meta = f"Duração máx.: {E(m['duracao_max'])} · Áudio: {E(m['audio'])}" if m['tipo'] == 'video' else 'Imagem'
    return (f'<div class="mod" data-id="{m["id"]}"><span class="tp">{"VÍDEO" if m["tipo"] == "video" else "IMAGEM"}</span>'
            f'<h3>{E(m["nome"])}</h3><span class="fab">{E(m["fabricante"])}</span>'
            f'<p class="q"><strong>Use quando</strong> {E(m["use_quando"])}.</p>'
            f'<p>{E(m["destaque"][0].upper() + m["destaque"][1:])}.</p>'
            f'<p class="l">Limites: {E(m["limites"])}.</p>'
            f'<div class="meta">{meta}</div><div class="src">{fontes}</div></div>')


cards = '\n'.join(card(m) for m in D['modelos'])
botoes = '\n'.join(f'<button type="button" data-ids="{",".join(ids)}">{E(n)}</button>' for n, ids in NECESSIDADES)
linhas = '\n'.join(f'<tr><td><strong>{E(m["nome"])}</strong></td><td>{E(m["fabricante"])}</td><td>{E(m["duracao_max"])}</td>'
                   f'<td>{E(m["audio"])}</td><td>{E(m["destaque"])}</td></tr>' for m in D['modelos'] if m['tipo'] == 'video')
REPO = 'https://github.com/inematds/movieflow-modelos'

body = f"""
<nav><div class="wrap">
  <a class="brand" href="#top"><span class="emoji">🎬</span> MovieFlow: 13 modelos</a>
  <span class="sep">|</span>
  <span class="clubpro">
    <a class="inema" href="https://inema.club" target="_blank" rel="noopener">INEMA.CLUB</a>
    <span class="sep">-</span>
    <a class="pro" href="https://inema.pro" target="_blank" rel="noopener">PRO</a>
  </span>
  <div class="links">
    <a class="sec" href="#modelos">Modelos</a>
    <a class="sec" href="#escolher">Qual usar</a>
    <a class="sec" href="#fluxo">Como fazer</a>
    <a class="sec" href="#guia">Guia de uso</a>
    <a class="sec" href="#preco">Preço</a>
    <span class="lang"><a class="on" href="./">PT</a><a href="en/">EN</a><a href="es/">ES</a></span>
    <button class="tgl" id="themeToggle" aria-label="Alternar tema" title="Alternar tema">🌙</button>
    <a class="btn" href="{REPO}" target="_blank" rel="noopener">GitHub</a>
  </div>
</div></nav>

<header class="hero" id="top">
  <div class="glow"></div>
  <div class="wrap">
    <div>
      <span class="chip">Filme com IA · novembro de 2026</span>
      <h1>Cada cena do seu filme pede o <span class="amb">modelo certo</span></h1>
      <p class="lead">O MovieFlow junta 13 modelos de vídeo e imagem num lugar só. Este guia diz o que cada um faz bem, onde ele falha e qual escolher para a sua cena.</p>
      <div class="cta">
        <a class="btn" href="#escolher">Escolher meu modelo</a>
        <a class="btn ghost" href="{REPO}" target="_blank" rel="noopener">Ver no GitHub</a>
      </div>
    </div>
    <figure><img src="assets/banner.jpg" alt="Banner MovieFlow: 13 modelos — qual modelo usar em cada cena do seu filme de IA"></figure>
  </div>
</header>

<section id="resumo" class="resumo"><div class="wrap">
  <span class="chip">Em resumo</span>
  <p>O MovieFlow (movieflow.ai) é um estúdio de filmes com IA: você escreve uma ideia e ele monta a história, os personagens, as cenas e o filme. Por trás dele há 13 modelos de outras empresas (Seedance, Kling, Veo, MiniMax, Vidu, Nano Banana, GPT Image e outros), e cada um é melhor numa coisa. Este projeto reúne, num guia e num arquivo de dados, o que cada modelo faz, os limites e quando usar. Para usar é só ler a página; quem quiser pode rodar o escolhedor no terminal com Python, sem instalar nada.</p>
</div></section>

<section id="oque"><div class="wrap">
  <span class="chip">O que é</span>
  <h2>Uma central de modelos, não um modelo só</h2>
  <p class="sub">Em 2025 o MovieFlow era vendido como "filme grátis de até 10 minutos". Hoje ele cobra por créditos e virou um painel onde você escolhe o motor de cada cena.</p>
  <figure style="margin:0 0 26px;border-radius:16px;overflow:hidden;border:1px solid var(--line);box-shadow:0 30px 80px -30px #000"><img src="assets/banner-grade.jpg" alt="Os modelos principais do MovieFlow: Seedance 2.5, Kling 3.0, Veo 3, MiniMax H3, Nano Banana e GPT Image 2" loading="lazy" style="width:100%;display:block"></figure>
  <div class="grid g3">
    <div class="card"><h3>🎬 9 modelos de vídeo</h3><p>Seedance 2.5, 2.0 e Fast, Kling 3.0 e 2.6, MiniMax H3, Vidu Q3 Pro, Veo 3 e o próprio MovieFlow 2.0 Ultra.</p></div>
    <div class="card"><h3>🖼️ 4 modelos de imagem</h3><p>Nano Banana Pro e 2, GPT Image 2 e Seedream 5.0, para personagens, quadros-chave, cartazes e storyboard.</p></div>
    <div class="card"><h3>🧭 Quando usar cada um</h3><p>Uma linha "use quando" por modelo, os limites e as fontes. Onde as fontes não batem, a página avisa.</p></div>
  </div>
</div></section>

<section id="escolher"><div class="wrap">
  <span class="chip">Qual usar</span>
  <h2>Do que a sua cena precisa?</h2>
  <p class="sub">Toque numa necessidade: a resposta aparece aqui embaixo e os modelos indicados acendem nos cartões.</p>
  <div class="need" id="need">
{botoes}
  </div>
  <p class="note" id="resp" hidden></p>
</div></section>

<section id="modelos"><div class="wrap">
  <span class="chip">Os 13 modelos</span>
  <h2>O que cada modelo faz bem</h2>
  <p class="sub">Dados de páginas públicas lidas em 06/11/2026. "diverge" = as fontes não batem; "não confirmado" = não achei fonte.</p>
  <div class="mods" id="mods">
{cards}
  </div>
  <h3 style="margin-top:30px">Palavras que aparecem nos cartões</h3>
  <div class="gl">
    <div><strong>Lip-sync</strong> — a boca do personagem acompanha a fala.</div>
    <div><strong>Multi-shot</strong> — vários planos (cortes de câmera) gerados de uma vez, com o mesmo personagem.</div>
    <div><strong>Plano e contraplano</strong> — a câmera alterna entre duas pessoas que conversam.</div>
    <div><strong>Quadro-chave</strong> — a imagem principal que define como o personagem ou a cena vai ficar.</div>
    <div><strong>Storyboard</strong> — a sequência de desenhos das cenas antes do filme.</div>
    <div><strong>Referência</strong> — foto, vídeo ou áudio que você envia para o modelo copiar rosto, estilo ou movimento.</div>
    <div><strong>720p, 1080p, 2K, 4K</strong> — resolução: quanto maior, mais nítido (e em geral mais caro).</div>
    <div><strong>Motion Control</strong> — o modelo copia o movimento de um vídeo seu (dança, gesto).</div>
    <div><strong>Agent V2</strong> — o modo do MovieFlow em que a IA monta o filme inteiro a partir da sua ideia.</div>
  </div>
  <h3 style="margin-top:30px">Vídeo lado a lado</h3>
  <p class="sub" style="font-size:.85rem">No celular, arraste a tabela para o lado para ver todas as colunas.</p>
  <div class="scroll"><table class="tbl">
    <tr><th>Modelo</th><th>Fabricante</th><th>Duração máx.</th><th>Áudio</th><th>Destaque</th></tr>
{linhas}
  </table></div>
</div></section>

<section id="fluxo"><div class="wrap">
  <span class="chip">Como fazer</span>
  <h2>Da frase ao filme, gastando pouco</h2>
  <p class="sub">O caminho que economiza créditos: rascunho barato primeiro, modelo caro só na cena que vale.</p>
  <div class="flow">
    <span>Ideia em uma frase</span><span class="arr">→</span>
    <span>Agente monta história e storyboard</span><span class="arr">→</span>
    <span>Rascunho no MovieFlow 2.0 Ultra</span><span class="arr">→</span>
    <span>Personagem em imagem (Nano Banana Pro)</span><span class="arr">→</span>
    <span>Cena final no modelo certo</span><span class="arr">→</span>
    <span>Ajuste de um detalhe (MiniMax H3)</span>
  </div>
  <div class="ex" style="margin-top:22px">
    <figure><img src="assets/ex3.jpg" alt="Tela de criação do MovieFlow com a caixa da ideia" loading="lazy"><figcaption>Você escreve a ideia, escolhe idioma, duração e formato, e clica em criar.</figcaption></figure>
    <figure><img src="assets/ex1.jpg" alt="Cena de animação com um texugo e uma raposa de feltro" loading="lazy"><figcaption>Uma história infantil feita do zero a partir de uma frase.</figcaption></figure>
  </div>
</div></section>

<section id="guia"><div class="wrap">
  <span class="chip">Guia de uso · passo a passo</span>
  <h2>Use o guia e o escolhedor</h2>
  <p class="sub">O jeito mais fácil é usar os botões de <a href="#escolher">Qual usar</a> nesta página, sem instalar nada. Para o escolhedor no terminal: Python 3 (no Windows o comando é <code>python</code> em vez de <code>python3</code>) e o git — ou baixe o ZIP no GitHub (botão Code → Download ZIP). Roda na sua máquina, sem conta e sem chave.</p>

  <div class="step"><div class="b">1</div><div>
    <h3>Baixe o projeto</h3>
    <p>O repositório tem os dados dos 13 modelos (<code>modelos.json</code>) e o escolhedor (<code>escolher.py</code>).</p>
<pre><span class="k">git clone {REPO}.git</span>
<span class="k">cd movieflow-modelos</span></pre>
  </div></div>

  <div class="step"><div class="b">2</div><div>
    <h3>Descreva a cena e veja o modelo indicado</h3>
    <p>Escreva a cena em poucas palavras. O escolhedor compara com as etiquetas de cada modelo e mostra os 3 melhores, com o "use quando" e os limites.</p>
<pre><span class="k">python3 escolher.py "conversa entre dois personagens em anime"</span>  <span class="c"># 1. Vidu Q3 Pro  2. Kling 3.0  3. Veo 3</span>
<span class="k">python3 escolher.py "cartaz com texto do filme"</span>  <span class="c"># 1. Nano Banana Pro  2. GPT Image 2</span></pre>
  </div></div>

  <div class="step"><div class="b">3</div><div>
    <h3>Veja a lista ou a ficha de um modelo</h3>
    <p>A lista filtra por vídeo ou imagem; a ficha traz destaque, limites e as fontes.</p>
<pre><span class="k">python3 escolher.py --lista --tipo video</span>
<span class="k">python3 escolher.py --modelo kling-3.0</span></pre>
  </div></div>

  <div class="step"><div class="b">4</div><div>
    <h3>No MovieFlow, troque o modelo por cena</h3>
    <p>Crie a conta em movieflow.ai (vem com créditos de teste), faça o rascunho no modelo barato e refaça só as cenas importantes no modelo indicado. Personagem que aparece em várias cenas: crie a imagem dele primeiro e use como referência.</p>
<pre><span class="s">https://movieflow.ai</span>  <span class="c"># Agent V2 → ideia → idioma, duração, formato → Create</span></pre>
  </div></div>

  <div class="step"><div class="b">5</div><div>
    <h3>Mantenha os dados em dia</h3>
    <p>Modelos mudam rápido. Quando o MovieFlow trocar a lista, edite <code>modelos.json</code> e remonte a página.</p>
<pre><span class="k">python3 montar_guia.py</span>  <span class="c"># gera guia/index.html a partir do modelos.json</span></pre>
  </div></div>
</div></section>

<section id="preco"><div class="wrap">
  <span class="chip">Quanto custa</span>
  <h2>Grátis e ilimitado não é mais</h2>
  <p class="sub">O que dá para afirmar hoje, e o que ainda não.</p>
  <div class="grid g3">
    <div class="card"><h3>🎟️ Créditos no cadastro</h3><p>A conta nova ganha créditos para testar (100 créditos, segundo um diretório de preços de nov/2026). É teste, não uso ilimitado.</p></div>
    <div class="card"><h3>⚡ US$ 0,008 por segundo</h3><p>Preço anunciado no próprio site para o MovieFlow 2.0: 5 segundos de vídeo por cerca de 4 centavos de dólar.</p></div>
    <div class="card"><h3>📅 Plano Standard</h3><p>US$ 19 por mês com 1.800 créditos, download 1080p sem marca-d'água (diretório Kingy, nov/2026). Os créditos zeram a cada 31 dias.</p></div>
  </div>
  <p class="note">O custo em créditos de cada modelo só aparece com a conta aberta, e a tabela de planos do site carrega por JavaScript. Confira em movieflow.ai/pricing antes de assinar.</p>
</div></section>

<section id="exemplos"><div class="wrap">
  <span class="chip">Exemplos</span>
  <h2>Estilos que saem do MovieFlow</h2>
  <p class="sub">Cenas geradas na plataforma: cinema, terror, animação de feltro.</p>
  <div class="ex">
    <figure><img src="assets/ex2.jpg" alt="Casal num baile de máscaras, estilo cinema" loading="lazy"><figcaption>Cinema: baile de máscaras com câmera e luz de filme.</figcaption></figure>
    <figure><img src="assets/ex4.jpg" alt="Cena de terror com uma noiva assombrada" loading="lazy"><figcaption>Terror: a mesma ferramenta, outro estilo.</figcaption></figure>
  </div>
</div></section>

<section id="roadmap"><div class="wrap">
  <span class="chip">Roadmap</span>
  <h2>Próximos passos</h2>
  <p class="sub">O que falta medir.</p>
  <div class="phase"><div class="tag">Feito</div><div class="d"><strong>Os 13 modelos com fontes</strong><span>Dados, escolhedor e guia em português, inglês e espanhol.</span></div></div>
  <div class="phase"><div class="tag">Próximo</div><div class="d"><strong>Custo em créditos por modelo</strong><span>Medir dentro da conta quanto cada modelo gasta por segundo.</span></div></div>
  <div class="phase"><div class="tag">Depois</div><div class="d"><strong>Mesma cena nos 9 modelos de vídeo</strong><span>Comparar lado a lado com o mesmo prompt.</span></div></div>
</div></section>

<footer>
  <div class="wrap">
    <div class="pill">MovieFlow</div><div class="pill">Python 3</div><div class="pill">JSON</div>
    <p style="margin-top:18px">MovieFlow: 13 modelos · dados de 06/11/2026 ·
      <a href="{REPO}">inematds/movieflow-modelos</a> ·
      <a href="https://inema.club">INEMA.CLUB</a></p>
  </div>
</footer>

<script>
  (function(){{
    var KEY='movieflow-modelos-theme';
    var b=document.body, t=document.getElementById('themeToggle');
    try{{ if(localStorage.getItem(KEY)==='light'){{ b.classList.add('light'); t.textContent='☀️'; }} }}catch(e){{}}
    t.addEventListener('click',function(){{
      var light=b.classList.toggle('light');
      t.textContent=light?'☀️':'🌙';
      try{{ localStorage.setItem(KEY, light?'light':'dark'); }}catch(e){{}}
    }});
    var bts=document.querySelectorAll('#need button'), mods=document.querySelectorAll('#mods .mod');
    bts.forEach(function(bt){{ bt.addEventListener('click',function(){{
      var ativo=bt.classList.contains('on');
      bts.forEach(function(x){{x.classList.remove('on');}});
      mods.forEach(function(m){{m.classList.remove('on','off');}});
      if(ativo){{ document.getElementById('resp').hidden=true; return; }}
      bt.classList.add('on');
      var ids=bt.getAttribute('data-ids').split(',');
      mods.forEach(function(m){{ m.classList.add(ids.indexOf(m.getAttribute('data-id'))>=0?'on':'off'); }});
      var nomes=[];mods.forEach(function(m){{ if(m.classList.contains('on')) nomes.push(m.querySelector('h3').textContent); }});
      var r=document.getElementById('resp'); r.hidden=false; r.textContent=bt.textContent+': '+nomes.join(', ');
    }}); }});
  }})();
</script>
"""

head = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MovieFlow: 13 modelos — qual usar em cada cena</title>
<meta name="description" content="Os 13 modelos de vídeo e imagem do MovieFlow (Seedance, Kling, Veo, MiniMax, Vidu, Nano Banana, GPT Image, Seedream): o que cada um faz bem, limites e quando usar.">
<link rel="alternate" hreflang="pt-BR" href="https://inematds.github.io/movieflow-modelos/guia/">
<link rel="alternate" hreflang="en" href="https://inematds.github.io/movieflow-modelos/guia/en/">
<link rel="alternate" hreflang="es" href="https://inematds.github.io/movieflow-modelos/guia/es/">
"""
# fontes e o que mais houver entre o <title> e o <style> do template
pre = t[t.index('<head>') + 6:t.index('<style>')]
pre = '\n'.join(l for l in pre.splitlines() if not any(k in l for k in ('<meta charset', 'viewport', '<title', 'name="description"', 'hreflang')))
out = head + pre + '\n<style>' + css + EXTRA + '</style>\n</head>\n<body>\n' + body + '</body>\n</html>\n'
(R / 'guia').mkdir(exist_ok=True)
(R / 'guia/index.html').write_text(out, encoding='utf-8')
print('guia/index.html', len(out), 'bytes,', len(D['modelos']), 'modelos')
