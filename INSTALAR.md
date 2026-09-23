# Instalar a skill `motion-por-referencia` v1.1

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
### ARQUIVO: SKILL.md

````markdown
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
````

---
### ARQUIVO: referencias/pericia-da-referencia.md

````markdown
# Perícia da referência — como desmontar um vídeo em três camadas

> A camada que todo mundo esquece é a terceira. Estrutura e design a gente
> extrai bem no olho; **movimento, não** — e movimento é o que faz um motion
> parecer premium. "Transição excelente" e "dinâmica boa" são impressões. Esta
> fase transforma impressão em número.

Roda **antes de desenhar qualquer coisa**. Saída: `pericia/` com os três
arquivos abaixo.

---

## Camada 1 — Estrutura (`pericia/estrutura.md`)

```bash
ffprobe -v error -show_entries format=duration -show_entries \
  stream=width,height,r_frame_rate,nb_frames -of default=noprint_wrappers=1 REF.mp4

# visão geral: 1 quadro por segundo, em grade
ffmpeg -y -v error -i REF.mp4 -vf "fps=1,scale=480:-1,tile=4x4" pericia/grade-1fps.png

# detalhe: 4 quadros por segundo, para achar onde cada beat começa e termina
ffmpeg -y -v error -i REF.mp4 -vf "fps=4,scale=340:-1,tile=8x7" pericia/grade-4fps.png
```

Leia as grades e escreva: quantos beats, o que cada um diz, quanto dura, e
**qual elemento conduz cada emenda** (o que o olho segue de um beat para o
outro). Anote também se há áudio — `ffprobe -select_streams a` vazio significa
filme mudo, e um filme mudo carrega todo o ritmo no timing.

**Nomeie o mecanismo.** Uma frase, sem vocabulário técnico, que um espectador
usaria para descrever o motor do filme: "o cursor dirige a tela e ela
responde"; "um objeto atravessa o quadro e onde passa o beat troca"; "tudo é
monocromático menos o produto"; "uma morfose contínua, sem corte". Os beats
são a prova do mecanismo — se você não consegue escrever a frase, a referência
é uma sequência de cenas, não um filme, e vale escolher outra.

Registre como o filme **fecha**. Se não fechar com clareza, o padrão que
funciona é: lockup (marca + linha secundária + chip de CTA) → segura 0,8–1,0s
→ sai para o fundo → cauda quieta.

## Camada 2 — Design (`pericia/design.md`)

Amostre cores de quadros reais em vez de adivinhar:

```bash
ffmpeg -y -v error -i REF.mp4 -vf "fps=1,scale=120:-1,palettegen=max_colors=12" pericia/paleta.png
```

Registre: fundo, tinta, secundário, superfície, **e quantos acentos existem**
(os bons costumam ter UM). Depois: família e pesos tipográficos, tracking,
geometria (raios, espessura de borda, sombra — dura ou difusa), e se há objeto
3D/fotográfico e como ele se separa do 2D.

**Prescreva com restrições, não com adjetivos.** "Limpo" não é instrução;
"sem grain, sem flare, sem vinheta, sem gradiente em texto, sem itálico" é.
Estilo caótico ganha regras ("tremor só no pouso do beat, nunca contínuo");
estilo limpo ganha lista de proibições. É a lista de proibições que os workers
conseguem obedecer e os críticos conseguem conferir.

**Se o estilo é híbrido (2D chapado + objeto 3D ou fotográfico), escreva a lei
de separação de camadas:** as camadas interagem fisicamente — o objeto projeta
sombra no papel — mas **nunca trocam propriedades de render**. O 2D não recebe
luz, reflexo nem sombra própria; o 3D nunca vira chapado. Quebrar isso quebra o
estilo. Foi exatamente o caso da referência Passo/TRAVAI: UI plana com mala e
celular fotográficos.

**Movimento permitido e proibido.** Liste os dois: o que o filme faz (sobe e
assenta, cascata, risco, self-draw, clique com ripple) e o que ele nunca faz
(zoom, tremor de câmera, motion blur em 2D, partículas, luz vazando, texto 3D).
A lista de proibidos vale mais que a de permitidos.

**Política de câmera.** Fixa ou móvel? Se móvel, que movimentos (push, pan,
drift) e em que beats. Se fixa, escreva "fixa" — é o que impede um worker de
inventar um push-in "sutil" que destoa dos outros sete frames.

O `design.md` está completo quando responde a tudo isto:

| Bloco | Pergunta |
|---|---|
| Paleta | cada cor com papel, e onde cada uma **não** pode aparecer |
| Herói + âncora | o objeto/marca central e o traço que precisa ler em todo frame |
| Tipografia | família, pesos, tracking, e a física de entrada/saída do texto |
| Regra de acento | uma palavra por título? o acento marca sempre a ação? |
| Movimento | permitido / proibido |
| Câmera | fixa, ou quais movimentos em quais beats |
| Render | grain, flare, vinheta, blur: política de cada um |
| Camadas | a lei de separação, se híbrido |

## Camada 3 — Movimento (`pericia/movimento.md`) ← a que importa

```bash
python3 scripts/pericia-movimento.py REF.mp4 --json pericia/movimento.json
```

Devolve:

| Medida | O que diz |
|---|---|
| **cortes duros** | Nenhum detectado = filme todo em transição suave. Muitos = filme percussivo. |
| **perfil de energia** | Quanto muda por quadro, ao longo do tempo. É o "áudio" visual do filme. |
| **vales** | Os momentos de quase-parada. A respiração. |
| **picos** | Os socos. |
| **amplitude** (pico ÷ mediana) | **O número mais revelador.** |

**Por que a amplitude é o número-chave.** Um motion premium alterna rajada e
silêncio. Um motion morno anda no mesmo volume o tempo todo — e "morno" é
exatamente o defeito que ninguém consegue nomear ao assistir. Medido:

```
                         amplitude   em quase-parada
referência premium          19.9x          64%
primeira tentativa nossa     9.2x          48%
```

Os dois filmes tinham a mesma estrutura, a mesma paleta e a mesma tipografia. A
diferença inteira estava aqui: o nosso **nunca batia**. Tudo tinha sido
crossfadeado em 0,3s, então nada nunca socava. Isso não aparece numa folha de
cards, não aparece num lint, e não aparece numa olhada distraída no preview.

## As metas

A ferramenta converte a medida da referência em metas para o nosso filme
(amplitude mínima, fração mínima em quase-parada, número mínimo de picos). Elas
entram no storyboard como direção obrigatória e voltam no fim como teste de
aceite:

```bash
python3 scripts/pericia-movimento.py NOSSO.mp4 --contra REF.mp4   # sai 1 se reprovar
```

## Quando reprova, o conserto quase sempre é o mesmo

O filme está uniforme demais. Não adianta acelerar tudo — isso só sobe a
mediana e a amplitude continua igual. O que funciona:

1. **Eleja UM beat para ser o soco.** Corte duro em vez de crossfade; entrada
   mais rápida e mais curta; objeto maior atravessando mais tela.
2. **Aprofunde as paradas ao redor dele.** O soco só existe contra o silêncio.
   Tire o movimento ocioso dos beats vizinhos — nada de "respiração" em
   elemento parado, nada de drift decorativo.
3. **Não distribua a energia igualmente.** Alternar denso/esparso é o que cria
   ritmo; distribuir é o que cria monotonia.
````

---
### ARQUIVO: referencias/esqueleto-de-frame.md

````markdown
# Esqueleto de frame — o contrato que vai junto com CADA worker

> **Por que existe:** numa produção real com 8 workers em paralelo, cada um
> resolveu fonte de um jeito (base64 embutido, `@font-face` para arquivo, e
> confiança na fonte do renderizador), cada um inventou seu próprio reset de
> CSS, e **um deles descobriu sozinho, tarde, que callback do GSAP não roda sob
> `seek()`** — depois de já ter escrito o frame errado. Todos esses são
> problemas GLOBAIS. Resolver oito vezes em isolamento gera oito respostas
> diferentes e uma passada de normalização depois.
>
> Decida tudo isto **uma vez, antes de despachar**, e cole neste arquivo. O
> worker recebe as decisões prontas e gasta o raciocínio dele no movimento, que
> é o que importa.

---

## 1. Fonte — decidida pelo orquestrador, nunca pelo worker

O orquestrador escolhe o arquivo, coloca em `assets/fonts/`, e entrega o bloco
pronto. O worker **não declara `@font-face`** e **não embute base64**.

```css
@font-face {
  font-family: "<FAMÍLIA>";
  src: url("assets/fonts/<ARQUIVO>.woff2") format("woff2");
  font-weight: 100 900;   /* fonte variável: todo peso autorado vira peso real */
  font-style: normal;
  font-display: block;
}
```

**Prefira uma fonte variável.** Um recorte estático traz só alguns pesos
(tipicamente 400/700/900); qualquer `font-weight: 500/600/800` do design é então
arredondado em silêncio, e o vídeo sai com peso diferente do card aprovado.

**Confira os glifos antes** (`scripts/portoes.py --fonte --copy`). Recortes de
CDN costumam cobrir acentos do português mas **não** cobrem `→` (U+2192) nem
`✓` (U+2713). Num render headless isso vira quadrado vazio.

## 2. Reset — mínimo e sem especificidade

```css
#root, #root * { box-sizing: border-box; }
```

Só `box-sizing`. Um seletor `#root *` tem especificidade (1,0,0) e **vence
qualquer regra de classe**: se ele zerar `margin`/`padding`, todo o espaçamento
do frame colapsa em silêncio — erro invisível numa olhada casual e óbvio quando
se medem as posições.

## 3. Movimento seek-safe — a regra que mais quebra render

O render avança por `tl.seek(t)`, e `seek()` roda com `suppressEvents = true`.
**`onUpdate`, `onStart`, `onComplete` e `onRepeat` nunca disparam.** Animação
dirigida por callback funciona perfeitamente no preview e **simplesmente não
existe no MP4**.

- Tudo tem que ser **tween de propriedade**. Um drift de câmera é
  `tl.fromTo(el,{x:-2},{x:2,...})`, nunca um `onUpdate` escrevendo `style.transform`.
- Digitação letra a letra é uma sequência de `tl.set(char,{display:"inline"})`,
  não um contador em callback.
- Nada de `Math.random`, `Date.now`, `performance.now` ou `fetch`: o render usa
  vários workers em paralelo e os quadros precisam ser reproduzíveis.

## 4. Estado inicial — nem `tl.set` na posição 0

Um `tl.set(...)` de duração zero na posição 0 **não renderiza com o playhead
exatamente em 0** — o primeiro quadro sai com o estado errado. Para fixar
repouso antes do primeiro tween, use `gsap.set()` **fora da timeline**, ou
declare no CSS.

Isso importa sempre que dois `fromTo` dividem o mesmo instante no mesmo
elemento: as "from-values" são aplicadas na hora da autoria, então o repouso
passa a depender de qual foi escrito por último.

## 5. Fundo full-bleed

O fundo do frame vive numa camada própria com `class="clip"` e duração cheia —
**nunca** um `background` no `#root`. Um fundo no root é limitado à janela do
clipe e pode deixar conteúdo pousar no `body` do host.

## 6. Ids

Prefixe os ids com o frame (`f03-...`), e **nunca comece com dígito**:
`#03-titulo` é seletor CSS inválido e quebra o GSAP em silêncio. Use `f03-titulo`.

## 7. O que o worker recebe pronto

- o card estático aprovado (ele **veste**, não redesenha)
- a paleta com os hex exatos e o papel de cada cor
- a escala tipográfica com os pesos
- as janelas de cena cronometradas
- os números de emenda (posição/escala/opacidade exatas onde algo continua
  entre frames) — sem isso, dois workers paralelos inventam duas versões da
  mesma costura
- estas 6 regras acima
````

---
### ARQUIVO: scripts/pericia-movimento.py

````python
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
````

---
### ARQUIVO: scripts/portoes.py

````python
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
````

---
### ARQUIVO: scripts/gerar-instalador.py

````python
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
````

---
### ARQUIVO: README.md

````markdown
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
````

---
*Gerado por `scripts/gerar-instalador.py` em 2026-09-22 · 7 arquivos · skill v1.1. Não edite este arquivo à mão — edite a skill e regenere.*
