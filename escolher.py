#!/usr/bin/env python3
"""Indica o modelo do MovieFlow para a sua cena.

Uso:
  python3 escolher.py "conversa entre dois personagens em anime"
  python3 escolher.py --lista            # os 13 modelos, um por linha
  python3 escolher.py --lista --tipo imagem
  python3 escolher.py --modelo kling-3.0 # ficha completa de um modelo

Lê modelos.json (mesma pasta). Sem rede, sem API: só compara as palavras da cena com as etiquetas de cada modelo.
"""
import argparse, json, sys, unicodedata
from pathlib import Path

DADOS = json.loads((Path(__file__).resolve().parent / 'modelos.json').read_text(encoding='utf-8'))
MODELOS = DADOS['modelos']

# palavra da cena -> etiqueta(s) do modelo
SINONIMOS = {
    'longo': ['longo'], 'longa': ['longo'], 'comprido': ['longo'], '30': ['longo'],
    'som': ['audio'], 'audio': ['audio'], 'musica': ['audio'], 'trilha': ['audio'],
    'personagem': ['personagem'], 'rosto': ['personagem', 'referencia'], 'mesmo': ['personagem', 'referencia'],
    'referencia': ['referencia'], 'foto': ['referencia', 'personagem'], 'copiar': ['copiar', 'movimento'],
    'barato': ['barato'], 'economico': ['barato'], 'rapido': ['rapido'], 'teste': ['rascunho', 'variacoes'],
    'testar': ['rascunho', 'variacoes'], 'rascunho': ['rascunho'], 'versoes': ['variacoes'], 'variacoes': ['variacoes'],
    'nitido': ['nitido'], '2k': ['2k'], '4k': ['4k'], 'detalhe': ['detalhe', 'nitido'], 'corrigir': ['editar'],
    'editar': ['editar'], 'ajustar': ['editar', 'regiao'], 'retocar': ['retocar', 'editar'],
    'corte': ['cortes'], 'cortes': ['cortes'], 'planos': ['multishot', 'cortes'], 'sequencia': ['multishot', 'cortes'],
    'acao': ['acao', 'movimento'], 'luta': ['acao', 'movimento'], 'perseguicao': ['acao', 'cortes'],
    'movimento': ['movimento'], 'danca': ['danca', 'movimento'], 'coreografia': ['danca'], 'gesto': ['gesto'],
    'dialogo': ['dialogo'], 'conversa': ['conversa', 'dialogo'], 'fala': ['fala', 'labial'], 'falando': ['fala', 'labial'],
    'entrevista': ['fala', 'realista'], 'labial': ['labial'], 'dublagem': ['labial'],
    'anime': ['anime'], 'desenho': ['desenho', 'animacao'], 'animacao': ['animacao'], 'cartoon': ['desenho'],
    'realista': ['realista'], 'real': ['real'], 'cinema': ['realista'], 'comercial': ['comercial'], 'propaganda': ['comercial'],
    'ambiente': ['ambiente'], 'camera': ['camera'], 'estilo': ['estilo'],
    'texto': ['texto'], 'letreiro': ['texto'], 'cartaz': ['cartaz', 'texto'], 'capa': ['capa'], 'poster': ['cartaz'],
    'diagrama': ['diagrama'], 'infografico': ['diagrama', 'texto'], 'hq': ['hq', 'painel'], 'quadrinho': ['hq'],
    'storyboard': ['storyboard', 'painel', 'grade'], 'muitas': ['muitas'], 'imagens': ['muitas'], 'regiao': ['regiao'],
}
PALAVRAS_IMAGEM = {'imagem', 'imagens', 'foto', 'cartaz', 'capa', 'poster', 'diagrama', 'infografico', 'hq', 'quadrinho', 'storyboard', 'quadro'}


def norm(t):
    t = unicodedata.normalize('NFD', t.lower())
    return ''.join(c for c in t if unicodedata.category(c) != 'Mn')


def recomendar(cena, n=3):
    palavras = [p.strip('.,;:!?') for p in norm(cena).split()]
    etiquetas = []
    for p in palavras:
        etiquetas += SINONIMOS.get(p, [])
    quer_imagem = any(p in PALAVRAS_IMAGEM for p in palavras) and not any(p in ('video', 'clipe', 'filme', 'cena') for p in palavras)
    notas = []
    for m in MODELOS:
        pontos = sum(1 for e in etiquetas if e in m['tags'])
        if quer_imagem and m['tipo'] == 'imagem':
            pontos += 1
        if not quer_imagem and m['tipo'] == 'video':
            pontos += 0.5
        notas.append((pontos, m))
    notas.sort(key=lambda x: -x[0])
    if notas[0][0] < 1:
        return []
    return [m for p, m in notas[:n] if p >= 1]


def ficha(m):
    return (f"{m['nome']} ({m['tipo']}, {m['fabricante']})\n"
            f"  destaque:   {m['destaque']}\n  use quando: {m['use_quando']}\n"
            f"  duração:    {m['duracao_max']} · áudio: {m['audio']}\n  limites:    {m['limites']}\n"
            f"  fontes:     {' · '.join(m['fontes'])}")


def main():
    ap = argparse.ArgumentParser(description='Indica o modelo do MovieFlow para a sua cena.')
    ap.add_argument('cena', nargs='?', help='descreva a cena em poucas palavras')
    ap.add_argument('--lista', action='store_true', help='lista os 13 modelos')
    ap.add_argument('--tipo', choices=['video', 'imagem'], help='filtra a lista')
    ap.add_argument('--modelo', help='mostra a ficha de um modelo (id, ex.: kling-3.0)')
    a = ap.parse_args()
    if a.modelo:
        m = next((x for x in MODELOS if x['id'] == a.modelo or norm(x['nome']) == norm(a.modelo)), None)
        if not m:
            sys.exit(f"modelo '{a.modelo}' não está na lista; veja --lista")
        print(ficha(m)); return
    if a.lista or not a.cena:
        for m in MODELOS:
            if not a.tipo or m['tipo'] == a.tipo:
                print(f"{m['id']:<20} {m['tipo']:<7} {m['destaque']}")
        print(f"\n(dados de {DADOS['atualizado']}; {DADOS['aviso']})")
        return
    r = recomendar(a.cena)
    if not r:
        print('Não reconheci a cena. Tente palavras como: diálogo, ação, cortes, anime, realista, barato, texto, storyboard.')
        print('Na dúvida: comece no MovieFlow 2.0 Ultra (rascunho barato) e refaça a melhor cena no Kling 3.0 ou Seedance 2.5.')
        return
    print(f'Para "{a.cena}":\n')
    for i, m in enumerate(r, 1):
        print(f"{i}. {ficha(m)}\n")


if __name__ == '__main__':
    main()
