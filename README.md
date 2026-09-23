# motion-por-referencia

Skill do Claude Code para recriar um motion graphic **no nível de um vídeo de
referência** — sem copiar o conteúdo dele.

Você entrega um vídeo (ou link) e diz o que quer fazer. A skill desmonta a
referência em três camadas — estrutura, design e **movimento, medido em
números** —, monta identidade e assets, te entrega **cards estáticos** para
aprovar beat a beat, e só depois anima. No fim, compara a assinatura de
movimento do resultado contra a da referência e diz se passou.

Nasceu de um caso real: a recriação de um promo de app de viagem (estilo
Apple/SaaS, 15s, mudo) para uma agência fictícia. O primeiro resultado tinha
estrutura, cor e tipografia certas — e um movimento morno que ninguém sabia
nomear. A perícia de movimento é o que nomeia.

## Instalar

**Jeito 1 — clonar direto na pasta de skills:**

```bash
git clone https://github.com/Felpborges/motion-por-referencia.git ~/.claude/skills/motion-por-referencia
chmod +x ~/.claude/skills/motion-por-referencia/scripts/*.py
```

**Jeito 2 — sem git:** abra o [`INSTALAR.md`](INSTALAR.md), copie o conteúdo
inteiro e cole no Claude Code. Ele cria os arquivos sozinho.

Depois de instalar, reinicie a sessão do Claude Code para a skill aparecer.

## O que precisa ter na máquina

| Para | Precisa de |
|---|---|
| perícia de movimento e grades de quadros | `ffmpeg` + `ffprobe` |
| portão de glifos | `python3` + `pip install fonttools` |
| construir e renderizar (motor padrão) | Node + `npx hyperframes` |
| gerar fotos, objetos 3D, identidade | conta no Higgsfield (MCP ou CLI) |

Skills que ela chama quando existem (opcionais): `loop-de-design`,
`higgsfield-brandkit`, `higgsfield-generate`, `hyperframes`,
`product-launch-video`, `motion-graphics-2`, `higgsfield-youtube-thumbnail`.
Sem elas a skill continua funcionando; faz aquela parte à mão.

## Estrutura

```
motion-por-referencia/
├── SKILL.md                              ← as 8 fases
├── scripts/
│   ├── pericia-movimento.py              ← mede o movimento em números; teste de aceite
│   ├── portoes.py                        ← 5 checagens que pegam o que só quebra no render
│   └── gerar-instalador.py               ← regenera o INSTALAR.md
├── referencias/
│   ├── pericia-da-referencia.md          ← como desmontar em 3 camadas
│   └── esqueleto-de-frame.md             ← o contrato que vai junto com cada worker
├── INSTALAR.md                           ← a skill inteira num arquivo só, pra copiar e colar
└── README.md
```

## As 8 fases

0. **Entrada** — referência + brief; escolhe o motor pelo que a máquina tem.
1. **Perícia** — estrutura, design e movimento medido. Nomeia o mecanismo.
2. **Identidade** — tokens ou marca inventada, com uma âncora que lê em todo frame.
3. **Assets** — foto e 3D gerados; logo, ícone e UI feitos na mão.
4. **Cards estáticos** — o design final parado, beat a beat. **Portão principal.**
5. **Construção** — esqueleto compartilhado primeiro, depois um worker por beat.
6. **Portões mecânicos** — seek-safety, determinismo, glifos, tipografia, paleta.
7. **Montagem e render** — transições calibradas pela referência, contact sheet nas emendas.
8. **Teste de aceite** — a assinatura de movimento do resultado contra a da referência.

## As duas ferramentas

```bash
# mede uma referência e gera as metas
python3 scripts/pericia-movimento.py REF.mp4 --json pericia/movimento.json

# testa o nosso render contra ela (sai 1 se reprovar)
python3 scripts/pericia-movimento.py NOSSO.mp4 --contra REF.mp4

# os 5 portões, antes de montar (sai 1 se reprovar)
python3 scripts/portoes.py FRAMES/ --fonte FONTE.woff2 --copy copy.txt --paleta "#FFFFFF,#0B0B0C,#FF5B2E"
```

## Atualizar o INSTALAR.md

Mudou qualquer arquivo? Regenere o instalador antes de commitar:

```bash
python3 scripts/gerar-instalador.py
```

## Licença

MIT — Felipe Borges.
