---
name: motion-por-referencia
description: |
  Recria um motion graphic no nível de um vídeo de referência: desmonta a
  referência em três camadas (estrutura, design e — a que todo mundo pula —
  MOVIMENTO, medido em números), monta a identidade e os assets, entrega
  CARDS ESTÁTICOS card a card para aprovação, e só depois anima, com portões
  mecânicos e um teste de aceite que compara a assinatura de movimento do
  resultado contra a da referência. Use SEMPRE que a pessoa passar um vídeo
  (ou link) de referência e pedir algo "nesse nível", "igual a esse", "recria
  esse vídeo para X", "estuda esse motion e faz um parecido", "quero as
  transições assim", ou quando ela quiser um motion graphic, vídeo de
  lançamento, promo de app/produto ou abertura com acabamento premium a partir
  de um exemplo concreto. Também para diagnosticar um motion pronto que "está
  morno" sem saber por quê — a perícia de movimento nomeia o defeito. NÃO use
  para roteiro de vídeo falado (isso é criador-de-roteiros), para edição de
  gravação do canal (edicao-video / edicao-kallaway), nem para material de aula
  (aula-html).
license: MIT
metadata:
  author: Felipe Borges
  version: "1.1"
---

# Motion por referência

Oito fases. **Não construa nada antes da fase 4 ser aprovada.**

A tentação de já ir animando é forte e é exatamente o que produz um filme
"quase bom": estrutura certa, cor certa, tipografia certa, e um movimento morno
que ninguém consegue nomear. As fases 1 a 3 existem para tornar esse defeito
impossível.

> **Regra-mãe:** da referência a gente copia **método e sensação** — o esqueleto,
> o ritmo, a física do movimento. **Nunca o conteúdo** — tema, exemplos, copy,
> marca e destinos são sempre do projeto da pessoa.

---

## Fase 0 — Entrada

Precisa de: **a referência** (arquivo ou link) e **o que vamos fazer** (marca,
produto, mensagem, idioma). Se vier link, baixe (`yt-dlp`) — a perícia precisa
dos quadros, não da descrição.

**Escolha o motor pelo que a máquina tem.** Não anuncie um caminho sem conferir:

| Motor | Confira | Quando |
|---|---|---|
| **HyperFrames** | `npx hyperframes --version` | Padrão. Controle quadro a quadro, texto PT-BR exato, render determinístico, iteração grátis. |
| **After Effects** via `/saas-animation` do Higgsfield | `ls /Applications | grep -i "After Effects"` | Quando o AE existe E a pessoa quer projeto editável em camadas. **Se o AE não estiver instalado, essa rota não roda** — a receita é explícita em não aceitar substituto em nuvem. |
| **Geração direta** (Higgsfield `generate_video`) | — | Só para peças sem UI e sem texto crítico. Modelo erra letra, checkbox e logo. **Nesta rota, o prompt é escrito pela `motion-graphics-2`** (arquitetura de blocos, plano de segmentação, plano B) — a perícia e os cards continuam sendo desta skill. |

Se a rota que a pessoa pediu não existir na máquina, **diga antes de começar** e
ofereça a alternativa. Não troque em silêncio.

## Fase 1 — Perícia da referência

Leia `referencias/pericia-da-referencia.md` e execute as três camadas. Saída em
`pericia/`: `estrutura.md`, `design.md`, `movimento.md` + `movimento.json`.

```bash
python3 scripts/pericia-movimento.py REF.mp4 --json pericia/movimento.json
```

Na camada 1, **nomeie o mecanismo da referência em uma frase** — o motor
conceitual que um espectador descreveria sem vocabulário técnico ("o cursor
dirige a tela e ela responde", "o objeto atravessa e onde passa o beat troca",
"um mundo monocromático onde só o produto tem cor"). Sem isso a perícia vira
lista de cenas bonitas, e cenas bonitas não dão filme.

**Portão:** as metas numéricas de movimento existem por escrito, e o mecanismo
da referência está nomeado. Sem elas, a fase 8 não tem contra o que julgar e
aprova qualquer coisa.

## Fase 2 — Identidade

Se a marca já existe, extraia os tokens. Se for inventada, **use
`higgsfield-brandkit`** — ele faz paleta, marca SVG e sistema tipográfico com
aprovações persistidas, e regenera só o que depende. (Fazer à mão funciona, mas
é trabalho que já está resolvido.)

Escolha o acento pensando nos **assets que vão entrar**: um acento que briga com
a fotografia do projeto estraga os dois. E se a referência tem uma cor de
assinatura, a nossa precisa ser **outra** — senão o filme parece cópia.

**Âncora de identidade.** Dê à marca UM traço de assinatura — o detalhe que
torna a silhueta própria e que **precisa ler em todo frame** (na TRAVAI: o pé
do T que curva e decola). Nomeie-o por escrito. É o que os workers preservam,
o que os críticos conferem, e o que faz a marca ser reconhecida de longe.

Entregue uma **prancha de identidade** (HTML): marca com a âncora, paleta com
papéis, escala tipográfica, componentes. É barata e evita retrabalho caro.

## Fase 3 — Assets

**Rode em paralelo com a fase 4** — geração leva minutos e não bloqueia o desenho.

- Fotografia, objeto 3D, textura → `higgsfield-generate` (`generate_image_batch`
  para vários de uma vez).
- Logo, ícone, seta, marcador → **SVG na mão**. Modelo de imagem erra geometria
  de marca, e SVG escala sem perda.
- Mapa, gráfico, dado real → **dados de verdade**. Silhueta de continentes
  inventada parece mancha; Natural Earth é domínio público e resolve.
- Interface (celular, tela, card) → **CSS/HTML**, nunca imagem gerada: a tela
  precisa do texto exato, legível e em português.

**Confira cada asset antes de aceitar.** Um PNG "de fundo branco" costuma vir em
254,254,254 — sobre `#FFFFFF` isso desenha um retângulo fantasma visível.

## Fase 4 — Cards estáticos ← **o portão principal**

**Primeiro, uma frase: o mecanismo do NOSSO filme.** Antes de qualquer card,
escreva o motor conceitual em uma frase que um espectador repetiria. Pode ser o
da referência ou uma adaptação, mas tem que existir — os beats existem para
provar o mecanismo. Um filme sem mecanismo é "cenas bonitas do produto", e é o
defeito mais comum e mais difícil de nomear depois.

Depois, uma página HTML com um card por beat, **em 16:9**, mostrando o beat no
seu momento-chave com:

- as palavras reais, na fonte real, nas cores reais
- os assets reais já posicionados (não caixas cinzas)
- rótulo `NN · nome` e a janela de tempo
- uma nota dizendo **o que se move primeiro e para onde vai a emenda**
- ao final: um **mapa de emendas** e uma cartela de **tokens + proibições**
- o **elemento de maior risco** da construção e o seu plano B — a emenda de
  posição entre dois beats? a composição fotográfica sobre branco? o 3D em
  CSS? Nomear o risco aqui é o que evita descobri-lo na fase 7.

Junto com a página, **`copy.txt` — a lista de copy é contrato.** Toda string
que aparece em tela, literal, com acentos, uma por linha, fechando com "nada
além disso aparece em tela". No máximo uma palavra de acento por título. Este
arquivo alimenta o portão de glifos da fase 6 e é o que garante que o
português sai certo no render.

Escreva as janelas de cena com **física, não adjetivo**: "sobe 24px e assenta
em 300ms" em vez de "entra suavemente"; "escala 1.06→1.0 atrás da máscara" em
vez de "a foto respira". Cada transição tem **um** elemento condutor que o olho
segue. Nada acontece "porque fica bonito".

Isto é o design final parado. Só falta o movimento. É o passo de maior
alavancagem do processo inteiro: corrigir aqui é conversa, corrigir depois de
animar é retrabalho.

**Antes de mandar para a pessoa, rode a crítica adversarial:** invoque
`loop-de-design`. Ela desmonta a referência em 5-7 mecanismos verificáveis e
roda três críticos independentes (briefing, sistema de design, e um visual que
compara às cegas contra a referência). Acrescente as metas de movimento da fase
1 como mecanismos. Corrija o que os críticos reprovarem, **e só então** entregue.

**Portão:** a pessoa aprova os cards. Não anime antes.

## Fase 5 — Construção

**Primeiro o esqueleto, depois os workers.** Leia
`referencias/esqueleto-de-frame.md`, decida fonte/reset/regras **uma vez**, e
cole as decisões no pacote de cada worker.

> Sem isso: numa produção real com 8 workers paralelos, saíram três abordagens
> de fonte diferentes, três resets diferentes, e um bug de `seek()` descoberto
> tarde por um worker sozinho. Tudo problema global resolvido oito vezes.

Um worker por beat, em paralelo. Cada um recebe: o card aprovado (ele **veste**,
não redesenha), as janelas de cena, os números exatos de emenda, e o esqueleto.

## Fase 6 — Portões mecânicos

```bash
python3 scripts/portoes.py FRAMES/ --fonte FONTE.woff2 --copy copy.txt --paleta "#..,#.."
```

Cinco checagens, todas nascidas de bug real: seek-safety, determinismo,
cobertura de glifos, tipografia consistente entre frames, paleta. Sai 1 se
reprovar. **Rode antes de montar** — cada um destes custa uma rodada inteira se
for descoberto depois do render.

Some a varredura de consistência que só o orquestrador enxerga: raios, sombras,
escalas e durações batendo entre frames que foram escritos isolados.

## Fase 7 — Montagem e render

Monte a timeline, injete transições, rode os checks do motor.

**Calibre a duração da transição contra a referência**, não contra o padrão da
ferramenta. Um crossfade de 0,5s num beat de 1,8s come um terço do beat e borra
justamente as emendas de posição que você projetou. Se a perícia mostrou
transições rápidas, use rápidas.

Tire um contact sheet no **meio de cada beat e nos dois lados de cada emenda** —
é onde continuidade quebra — e inspecione antes de renderizar.

## Fase 8 — Teste de aceite

```bash
python3 scripts/pericia-movimento.py NOSSO.mp4 --contra REF.mp4
```

Compara amplitude, fração em quase-parada e número de picos contra as metas da
fase 1. **Sai 1 se reprovar.**

Se reprovar, o conserto quase nunca é "acelerar tudo" — isso sobe a mediana e a
amplitude fica igual. É eleger **um** beat para socar e aprofundar as paradas
ao redor. Detalhe em `referencias/pericia-da-referencia.md`.

Entregue com: o MP4, o contact sheet, os ids dos beats (para revisão dirigida a
um só) e o resultado do teste de aceite — inclusive quando reprovou e por quê.

---

## Versão vertical (9:16)

Quando pedirem Reels/Stories/Shorts: **recomponha, não corte.** 1080×1920, com
zonas seguras — os 12% do topo e os 15% de baixo livres de texto e de UI
crítica (o objeto herói pode invadir). Títulos viram 2–3 linhas empilhadas;
chips lado a lado viram coluna; o que era movimento horizontal vira vertical
(um atravessar de tela vira um mergulho, uma linha de cards vira uma torre com
subida de câmera, um deslizar lateral vira uma queda de altura inteira);
split-screen vira cima/baixo. Ao entregar, **diga quais beats ficaram mais
fortes na vertical** — sempre há alguns, e é informação útil pra decidir qual
versão publicar onde.

## Iterações

- **"Refaz para X" / "agora é Y"** → mantém a base (estilo, estrutura, tempos)
  e troca só a camada semântica: marca, copy, assets. Diga no início o que
  ficou e o que mudou.
- **"Muda o estilo"** → muda o DNA — física de easing, tipo de transição,
  linguagem de render —, não só a cosmética. Carrega só produto e duração.
- **"Muda a cor"** → reconstrói a paleta como **sistema com papéis** (fundo,
  tinta, acento, onde cada uma pode e não pode aparecer). Nunca é um recolor.
- **Reprovou no teste de aceite** → veja a fase 8; o conserto quase nunca é
  "acelerar tudo".

---

## O que NÃO fazer

- Animar antes dos cards aprovados.
- Pular a fase 1 porque "dá para ver no olho". Movimento não dá.
- Deixar cada worker resolver fonte, reset ou seek-safety por conta.
- Aceitar o padrão de transição da ferramenta sem comparar com a referência.
- Copiar copy, exemplos, analogias ou marca da referência.
- Anunciar um motor sem verificar se ele existe na máquina.
- Chamar de pronto um filme que reprovou no teste de aceite sem dizer isso.
- Logo de terceiro, chrome de sistema operacional, marca d'água de motor,
  pessoa real ou obra protegida em tela. Texto de preenchimento (feeds, listas
  de fundo) é *greeked* — ilegível de propósito. Se a referência tem uma trade
  dress reconhecível, escreva o que a nossa NÃO copia.

## Skills que esta orquestra

| Skill | Fase |
|---|---|
| `loop-de-design` | 4 — crítica adversarial dos cards contra a referência |
| `higgsfield-brandkit` | 2 — identidade inventada (paleta, marca SVG, tipografia) |
| `higgsfield-generate` | 3 — fotografia, objeto 3D, textura |
| `hyperframes` + `product-launch-video` | 5-7 — construção, montagem e render |
| `higgsfield-youtube-thumbnail` | entrega — a capa, quando o vídeo for publicado |
| `motion-graphics-2` | 0 — só na rota de geração direta: escreve o prompt (blocos, segmentação, plano B) |
