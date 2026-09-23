#!/usr/bin/env python3
"""Gera o INSTALAR.md — a skill inteira num arquivo só, para copiar e colar.

Quem recebe o INSTALAR.md não precisa de git nem de terminal: copia o conteúdo
inteiro, cola no Claude Code, e o Claude recria cada arquivo no caminho certo.

Rode de qualquer pasta; ele acha a raiz da skill sozinho. Rode de novo sempre
que mudar qualquer arquivo, senão o instalador fica defasado do repositório.
"""

import datetime
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "INSTALAR.md"

# ordem fixa: o SKILL.md primeiro, porque é o que o Claude lê para entender o resto
ARQUIVOS = [
    "SKILL.md",
    "referencias/pericia-da-referencia.md",
    "referencias/esqueleto-de-frame.md",
    "scripts/pericia-movimento.py",
    "scripts/portoes.py",
    "scripts/gerar-instalador.py",
    "README.md",
]

LINGUAGEM = {".md": "markdown", ".py": "python"}


def versao():
    m = re.search(r'version:\s*"([^"]+)"', (RAIZ / "SKILL.md").read_text(encoding="utf-8"))
    return m.group(1) if m else "?"


def cerca(conteudo):
    """Cerca de crases mais longa do que qualquer cerca dentro do arquivo, para
    que os blocos ```bash do SKILL.md continuem válidos dentro do bloco maior."""
    maior = max((len(m) for m in re.findall(r"`{3,}", conteudo)), default=0)
    return "`" * max(4, maior + 1)


def main():
    partes = []
    partes.append(f"""# Instalar a skill `motion-por-referencia` v{versao()}

> **Como usar este arquivo:** copie o conteúdo INTEIRO (do início ao fim) e cole
> numa conversa do Claude Code. A instrução para o Claude já está aqui embaixo.
> Depois que ele terminar, reinicie a sessão do Claude Code para a skill aparecer.

---

## Instrução para o Claude Code

Instale a skill abaixo na minha máquina. Faça exatamente isto:

1. Crie a pasta `~/.claude/skills/motion-por-referencia/` (e as subpastas
   `scripts/` e `referencias/`).
2. Para cada bloco marcado com `### ARQUIVO: <caminho>`, grave um arquivo nesse
   caminho, relativo à pasta da skill, com **exatamente** o conteúdo que está
   dentro da cerca de código logo abaixo do título — sem acrescentar, remover
   ou reformatar nada.
3. Dê permissão de execução aos scripts: `chmod +x ~/.claude/skills/motion-por-referencia/scripts/*.py`.
4. Confirme listando a árvore final e rodando
   `python3 ~/.claude/skills/motion-por-referencia/scripts/pericia-movimento.py --help`.
5. Me avise que preciso reiniciar a sessão para a skill carregar.

Não instale dependências sem me perguntar. As opcionais são: `ffmpeg`,
`pip install fonttools`, e `npx hyperframes`.

---
""")
    for rel in ARQUIVOS:
        caminho = RAIZ / rel
        conteudo = caminho.read_text(encoding="utf-8")
        if not conteudo.endswith("\n"):
            conteudo += "\n"
        c = cerca(conteudo)
        lang = LINGUAGEM.get(caminho.suffix, "")
        partes.append(f"### ARQUIVO: {rel}\n\n{c}{lang}\n{conteudo}{c}\n\n---\n")

    partes.append(
        f"*Gerado por `scripts/gerar-instalador.py` em "
        f"{datetime.date.today().isoformat()} · {len(ARQUIVOS)} arquivos · "
        f"skill v{versao()}. Não edite este arquivo à mão — edite a skill e regenere.*\n"
    )
    SAIDA.write_text("".join(partes), encoding="utf-8")
    print(f"INSTALAR.md gerado: {len(ARQUIVOS)} arquivos, {SAIDA.stat().st_size} bytes")


if __name__ == "__main__":
    main()
