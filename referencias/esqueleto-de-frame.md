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
