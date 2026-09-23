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
