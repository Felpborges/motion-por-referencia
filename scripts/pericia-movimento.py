#!/usr/bin/env python3
"""Perícia de movimento — desmonta a MOVIMENTAÇÃO de um vídeo em números.

Existe porque estrutura, paleta e tipografia a gente extrai bem no olho, mas
movimento não. "Transição premium" e "dinâmica excelente" são impressões; esta
ferramenta transforma isso em metas verificáveis ANTES de construir, e em teste
de aceite DEPOIS de renderizar.

O que mede, por vídeo:
  · mapa de cortes    — onde há corte duro (mudança brusca de conteúdo)
  · perfil de energia — quanto muda de quadro a quadro, ao longo do tempo
  · vales             — os momentos de quase-parada (a respiração do filme)
  · picos             — os momentos de soco
  · amplitude         — pico ÷ mediana. O número que mais distingue um motion
                        premium de um morno: filme bom alterna rajada e
                        silêncio; filme morno anda no mesmo volume o tempo todo.

Uso:
    pericia-movimento.py REFERENCIA.mp4
    pericia-movimento.py REFERENCIA.mp4 --json saida.json
    pericia-movimento.py NOSSO.mp4 --contra REFERENCIA.mp4      # teste de aceite
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

BUCKET = 0.5  # segundos por balde do perfil


def _need(tool):
    if not shutil.which(tool):
        sys.exit("erro: '%s' não encontrado no PATH." % tool)


def sonda(video):
    """Duração, fps e resolução."""
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height,r_frame_rate",
         "-show_entries", "format=duration",
         "-of", "json", str(video)],
        capture_output=True, text=True, check=True).stdout
    d = json.loads(out)
    st = d["stream" + "s"][0]
    num, den = st["r_frame_rate"].split("/")
    return {
        "duracao": float(d["format"]["duration"]),
        "fps": round(float(num) / float(den), 3),
        "largura": st["width"],
        "altura": st["height"],
    }


def energia(video):
    """Diferença média entre quadros consecutivos: [(t, valor), ...].

    Escala para 192x108 primeiro — a medida é de MOVIMENTO, não de detalhe, e
    trabalhar pequeno remove ruído de compressão e deixa rápido.
    """
    with tempfile.TemporaryDirectory() as tmp:
        alvo = Path(tmp) / "m.txt"
        subprocess.run(
            ["ffmpeg", "-v", "error", "-i", str(video),
             "-vf", "scale=192:108,tblend=all_mode=difference,signalstats,"
                    "metadata=print:key=lavfi.signalstats.YAVG:file=%s" % alvo,
             "-f", "null", "-"],
            capture_output=True, check=True)
        txt = alvo.read_text()
    pares = re.findall(r"pts_time:([\d.]+).*?YAVG=([\d.]+)", txt, re.S)
    return [(float(t), float(v)) for t, v in pares]


def cortes(video, limiar=0.18):
    """Instantes de corte duro. Transição suave NÃO aparece aqui — e isso é
    informação: um vídeo sem cortes detectados é um vídeo todo em transição."""
    out = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(video),
         "-filter:v", "select='gt(scene,%s)',metadata=print:file=-" % limiar,
         "-f", "null", "-"],
        capture_output=True, text=True).stdout
    ts = [float(m) for m in re.findall(r"pts_time:([\d.]+)", out)]
    # agrupa instantes vizinhos (<0.25s) — um corte gera vários quadros acima do limiar
    agrupado = []
    for t in ts:
        if not agrupado or t - agrupado[-1] > 0.25:
            agrupado.append(t)
    return agrupado


def perfil(amostras):
    """Agrupa a energia em baldes de BUCKET segundos."""
    b = {}
    for t, v in amostras:
        k = round(t / BUCKET) * BUCKET
        b.setdefault(k, []).append(v)
    return {k: sum(v) / len(v) for k, v in sorted(b.items())}


def medir(video):
    p = sonda(video)
    am = energia(video)
    pf = perfil(am)
    vals = sorted(pf.values())
    if not vals:
        sys.exit("erro: não consegui medir energia de %s" % video)
    mediana = vals[len(vals) // 2]
    pico = max(vals)
    teto = max(pico, 1e-6)
    vales = [k for k, v in pf.items() if v < teto * 0.10]
    picos = [k for k, v in pf.items() if v > teto * 0.60]
    return {
        "arquivo": str(video),
        "duracao": p["duracao"], "fps": p["fps"],
        "resolucao": "%dx%d" % (p["largura"], p["altura"]),
        "cortes_duros": cortes(video),
        "perfil": pf,
        "mediana": mediana,
        "pico": pico,
        "amplitude": pico / mediana if mediana else 0.0,
        "vales": vales,
        "picos": picos,
        "fracao_parada": len(vales) / len(pf),
    }


def barra(v, teto, largura=30):
    return "#" * int(round(v / teto * largura)) if teto else ""


def imprime(m):
    print("\n  %s" % Path(m["arquivo"]).name)
    print("  %.2fs · %s · %gfps" % (m["duracao"], m["resolucao"], m["fps"]))
    c = m["cortes_duros"]
    print("  cortes duros: %s" % (", ".join("%.2fs" % t for t in c) if c
                                  else "nenhum (filme todo em transição suave)"))
    print()
    teto = m["pico"]
    for k, v in m["perfil"].items():
        marca = "  <- pico" if k in m["picos"] else ("  <- parada" if k in m["vales"] else "")
        print("  %6.1fs %7.2f  %-30s%s" % (k, v, barra(v, teto), marca))
    print()
    print("  mediana %.2f | pico %.2f | AMPLITUDE %.1fx | em quase-parada %.0f%%"
          % (m["mediana"], m["pico"], m["amplitude"], m["fracao_parada"] * 100))


def metas(ref):
    """Converte a medida da referência em metas verificáveis para o nosso filme."""
    return {
        "amplitude_min": round(ref["amplitude"] * 0.70, 1),
        "fracao_parada_min": round(max(0.25, ref["fracao_parada"] - 0.10), 2),
        "picos_min": max(1, int(len(ref["picos"]) * 0.70)),
        "cortes_duros_ref": len(ref["cortes_duros"]),
    }


def imprime_metas(mt):
    print("\n  METAS PARA O NOSSO FILME (derivadas da referência)")
    print("  · amplitude (pico ÷ mediana) >= %.1fx" % mt["amplitude_min"])
    print("  · fração do filme em quase-parada >= %.0f%%" % (mt["fracao_parada_min"] * 100))
    print("  · pelo menos %d momento(s) de pico" % mt["picos_min"])
    print("  · a referência tem %d corte(s) duro(s) — um filme só de crossfade"
          % mt["cortes_duros_ref"])
    print("    nunca bate; se ela soca, o nosso precisa socar em algum lugar.")


def compara(nosso, ref):
    mt = metas(ref)
    print("\n" + "=" * 68)
    print("  TESTE DE ACEITE")
    print("=" * 68)
    linhas = [
        ("amplitude", "%.1fx" % nosso["amplitude"], "%.1fx" % ref["amplitude"],
         nosso["amplitude"] >= mt["amplitude_min"], ">= %.1fx" % mt["amplitude_min"]),
        ("quase-parada", "%.0f%%" % (nosso["fracao_parada"] * 100),
         "%.0f%%" % (ref["fracao_parada"] * 100),
         nosso["fracao_parada"] >= mt["fracao_parada_min"],
         ">= %.0f%%" % (mt["fracao_parada_min"] * 100)),
        ("picos", str(len(nosso["picos"])), str(len(ref["picos"])),
         len(nosso["picos"]) >= mt["picos_min"], ">= %d" % mt["picos_min"]),
    ]
    print("\n  %-14s %-10s %-12s %-10s %s" % ("", "nosso", "referência", "meta", ""))
    falhas = []
    for nome, a, b, ok, meta in linhas:
        print("  %-14s %-10s %-12s %-10s %s" % (nome, a, b, meta, "PASSA" if ok else "FALHA"))
        if not ok:
            falhas.append(nome)
    print()
    if falhas:
        print("  REPROVADO em: %s" % ", ".join(falhas))
        print("  O caminho quase sempre é o mesmo: o filme está uniforme demais.")
        print("  Escolha UM beat para ser o soco (corte duro em vez de crossfade,")
        print("  entrada mais rápida, objeto maior) e aprofunde as paradas dos vizinhos.")
        return 1
    print("  APROVADO — a assinatura de movimento bate com a referência.")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Perícia de movimento de um vídeo.")
    ap.add_argument("video")
    ap.add_argument("--contra", metavar="REFERENCIA",
                    help="mede os dois e roda o teste de aceite")
    ap.add_argument("--json", metavar="ARQUIVO", help="grava a medida em JSON")
    a = ap.parse_args()
    _need("ffmpeg"); _need("ffprobe")

    m = medir(a.video)
    imprime(m)

    code = 0
    if a.contra:
        r = medir(a.contra)
        imprime(r)
        imprime_metas(metas(r))
        code = compara(m, r)
    else:
        imprime_metas(metas(m))
        print("\n  (medido como REFERÊNCIA. Depois de renderizar, rode:")
        print("   pericia-movimento.py NOSSO.mp4 --contra %s)" % a.video)

    if a.json:
        Path(a.json).write_text(json.dumps(m, indent=2, ensure_ascii=False))
        print("\n  JSON -> %s" % a.json)
    sys.exit(code)


if __name__ == "__main__":
    main()
