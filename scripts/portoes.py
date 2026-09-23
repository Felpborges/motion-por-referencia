#!/usr/bin/env python3
"""Portões mecânicos — os defeitos que passam no preview e só aparecem no render.

Cada checagem aqui nasceu de um bug real que custou tempo. Rodar isto leva
segundos; descobrir qualquer um destes depois do render custa uma rodada
inteira de trabalho.

  1. SEEK-SAFETY   Callbacks do GSAP (onUpdate/onStart/onComplete/onRepeat) não
                   disparam sob tl.seek(), e o render avança por seek. Animação
                   dirigida por callback funciona no preview e SOME no MP4.
  2. DETERMINISMO  Math.random / Date.now / fetch fazem quadros divergirem entre
                   os workers paralelos do render.
  3. GLIFOS        A fonte recortada pode não ter os símbolos da copy. Setas (→),
                   checks (✓) e travessões são os que mais faltam — viram
                   quadrado vazio num render headless sem fontes de sistema.
  4. TIPOGRAFIA    Workers paralelos resolvem fonte de jeitos diferentes. Se os
                   arquivos não convergirem, o peso do texto muda de cena
                   para cena.
  5. PALETA        Cores fora do sistema aprovado entrando por descuido.

Uso:
    portoes.py PASTA_DOS_FRAMES
    portoes.py PASTA_DOS_FRAMES --fonte assets/fonts/X.woff2 --copy copy.txt
    portoes.py PASTA_DOS_FRAMES --paleta "#FFFFFF,#0B0B0C,#FF5B2E"
"""

import argparse
import re
import sys
from pathlib import Path

CALLBACKS = ("onUpdate", "onStart", "onComplete", "onRepeat")
NAO_DETERMINISTICO = ("Math.random", "Date.now", "fetch(", "performance.now")


def _linhas_de_codigo(texto):
    """Ignora comentários /* */ e // — uma menção em comentário não é um bug."""
    texto = re.sub(r"/\*.*?\*/", "", texto, flags=re.S)
    return [l for l in texto.splitlines() if not l.strip().startswith("//")]


def portao_seek(frames):
    achados = []
    for f in frames:
        for i, l in enumerate(_linhas_de_codigo(f.read_text(encoding="utf-8")), 1):
            for c in CALLBACKS:
                if c + ":" in l or c + " :" in l:
                    achados.append((f.name, i, c, l.strip()[:70]))
    return achados


def portao_determinismo(frames):
    achados = []
    for f in frames:
        for i, l in enumerate(_linhas_de_codigo(f.read_text(encoding="utf-8")), 1):
            for t in NAO_DETERMINISTICO:
                if t in l:
                    achados.append((f.name, i, t, l.strip()[:70]))
    return achados


def portao_glifos(fonte, textos):
    try:
        from fontTools.ttLib import TTFont
    except ImportError:
        return None, "fontTools não instalado (pip install fonttools) — pulado"
    try:
        cmap = TTFont(str(fonte)).getBestCmap()
    except Exception as e:
        return None, "não consegui ler %s: %s" % (fonte, e)
    faltando = {}
    for ch in sorted(set("".join(textos))):
        if ch in "\n\r\t":
            continue
        if ord(ch) not in cmap:
            faltando.setdefault(ch, ord(ch))
    return faltando, None


def portao_tipografia(frames):
    """Todos os frames devem convergir para a MESMA fonte."""
    modos = {}
    for f in frames:
        t = f.read_text(encoding="utf-8")
        srcs = set(re.findall(r'src:\s*url\(["\']?([^"\')]+)', t))
        if any(s.startswith("data:") for s in srcs):
            modo = "base64 embutido"
        elif srcs:
            modo = "arquivo: " + ", ".join(sorted(srcs))
        elif "@font-face" in t:
            modo = "@font-face sem src legível"
        else:
            modo = "sem @font-face (depende da fonte do renderizador)"
        modos.setdefault(modo, []).append(f.name)
    return modos


def portao_paleta(frames, permitidas):
    permitidas = {c.lower().lstrip("#") for c in permitidas}
    intrusas = {}
    for f in frames:
        for m in re.findall(r"#([0-9a-fA-F]{6})\b", f.read_text(encoding="utf-8")):
            if m.lower() not in permitidas:
                intrusas.setdefault("#" + m.upper(), set()).add(f.name)
    return intrusas


def main():
    ap = argparse.ArgumentParser(description="Portões mecânicos antes da montagem.")
    ap.add_argument("frames", help="pasta com os .html dos frames")
    ap.add_argument("--fonte", help="arquivo da fonte (.woff2/.ttf) para conferir glifos")
    ap.add_argument("--copy", help="arquivo .txt com toda a copy que aparece em tela")
    ap.add_argument("--paleta", help="cores permitidas, separadas por vírgula")
    a = ap.parse_args()

    frames = sorted(Path(a.frames).glob("*.html"))
    if not frames:
        sys.exit("erro: nenhum .html em %s" % a.frames)
    print("\n  %d frame(s) em %s\n" % (len(frames), a.frames))
    falhas = 0

    print("  1. SEEK-SAFETY")
    r = portao_seek(frames)
    if r:
        falhas += 1
        for n, i, c, l in r:
            print("     FALHA %s:%d  %s  %s" % (n, i, c, l))
        print("     -> converta em tween de propriedade; callback não renderiza.")
    else:
        print("     ok — nenhum callback")

    print("\n  2. DETERMINISMO")
    r = portao_determinismo(frames)
    if r:
        falhas += 1
        for n, i, c, l in r:
            print("     FALHA %s:%d  %s  %s" % (n, i, c, l))
    else:
        print("     ok — nada não-determinístico")

    print("\n  3. GLIFOS")
    if a.fonte and a.copy:
        faltando, erro = portao_glifos(a.fonte, [Path(a.copy).read_text(encoding="utf-8")])
        if erro:
            print("     %s" % erro)
        elif faltando:
            falhas += 1
            for ch, cp in faltando.items():
                print("     FALHA  U+%04X  %s  não existe na fonte" % (cp, ch))
            print("     -> troque a fonte por um recorte que cubra, ou desenhe em SVG.")
        else:
            print("     ok — a fonte cobre toda a copy")
    else:
        print("     pulado (passe --fonte e --copy)")

    print("\n  4. TIPOGRAFIA CONSISTENTE")
    modos = portao_tipografia(frames)
    if len(modos) > 1:
        falhas += 1
        print("     FALHA — %d abordagens diferentes:" % len(modos))
        for m, fs in modos.items():
            print("       %-46s %s" % (m[:46], ", ".join(fs)))
        print("     -> injete UM bloco @font-face canônico em todos.")
    else:
        print("     ok — %s" % list(modos)[0][:60])

    print("\n  5. PALETA")
    if a.paleta:
        intrusas = portao_paleta(frames, a.paleta.split(","))
        if intrusas:
            falhas += 1
            for c, fs in sorted(intrusas.items()):
                print("     FALHA %s em %s" % (c, ", ".join(sorted(fs))))
        else:
            print("     ok — só cores do sistema")
    else:
        print("     pulado (passe --paleta)")

    print("\n  %s\n" % ("%d PORTÃO(ÕES) REPROVADO(S)" % falhas if falhas
                        else "TODOS OS PORTÕES PASSARAM"))
    sys.exit(1 if falhas else 0)


if __name__ == "__main__":
    main()
