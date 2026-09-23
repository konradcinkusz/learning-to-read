<p align="center"><img src="assets/logo.png" width="140" alt="Aprendo a leer"></p>

# Aprendo a leer

[![Build](https://github.com/konradcinkusz/learning-to-read/actions/workflows/build.yml/badge.svg)](https://github.com/konradcinkusz/learning-to-read/actions/workflows/build.yml)
[![Licencia](https://img.shields.io/github/license/konradcinkusz/learning-to-read)](LICENSE)
[![Hecho con](https://img.shields.io/badge/hecho%20con-LaTeX-2E7D32)](preamble.tex)

Tres cuadernos diarios de lectura en español, uno por nivel, y dos en
inglés, con la misma familia (los dos primeros cuentan el mismo año con
los mismos temas semana a semana; el tercero, el año siguiente; los de
inglés, ese mismo año siguiente, desde la casa de al lado, y también
los dos con los mismos temas):

- **Nivel 1 · Primeras palabras** (`palabras.tex`) -- para quien empieza
  a juntar sílabas: una palabra al día, partida en sílabas, y casi
  siempre un dibujo. Ver "El cuaderno de primeras palabras" más abajo.
- **Nivel 2 · Frases** (`main.tex`) -- el cuaderno original, para quien
  ya lee frases completas. Es lo que describe el resto de esta
  introducción.
- **Nivel 3 · Leo con lupa** (`lupa.tex`) -- el año siguiente, para
  quien ya lee con soltura: oraciones complejas en párrafos y una
  actividad de análisis cada día. Ver "Leo con lupa" más abajo.
- **Read and Draw** (`english.tex`) -- todo en inglés, un nivel por
  debajo de *Leo con lupa*: textos cortos hechos de oraciones compuestas
  (*because*, *when*, *who*...) y cada día un análisis muy sencillo de lo
  leído, casi siempre un dibujo. Ver "Read and Draw" más abajo.
- **First Words** (`firstwords.tex`) -- en inglés, muy por debajo de
  *Read and Draw*: para quien empieza a leer en inglés, una palabra al
  día que se lee sonido a sonido (*c-a-t: cat*), con un "botón" debajo
  de cada sonido, y cada día un dibujo para colorear. Es el cuaderno de
  primeras palabras, en inglés. Ver "First Words" más abajo.

Y de cada uno, un **cuaderno de verano**: su verano -- las últimas 13
semanas, 65 páginas -- en un cuaderno aparte, para las vacaciones; y una
**muestra gratuita**: sus cuatro primeras semanas, para probar antes de
imprimir el año entero. Ver "Los cuadernos de verano y las muestras" más
abajo.

Cuaderno diario de lectura en español, en A4, una página por día
laborable (lunes a viernes, 260 días = un año completo, de una estación
a la siguiente -- no "un curso" en el sentido escolar: se lee también
en vacaciones, ver "Estado" más abajo). Cada página tiene un hueco para
la fecha y una nota del adulto, la frase (o frases) del día, y una
actividad corta (dibujar, completar unas líneas sueltas, copiar la
frase, responder, relacionar, adivinar o crear).

Pensado para una niña que ya vive y escolariza en español y está
consolidando la lectura, no para empezar desde cero: las frases son
completas desde el primer día, y lo que aumenta con el curso es cuántas
frases hay que leer (1 → 2 → 3 → 4, una vez por trimestre) y su
complejidad, no el alfabeto disponible.

Además de los 260 días, el cuaderno trae una medalla al final de cada
trimestre, una clave de respuestas para las páginas de Adivina y
Relaciona, y una actividad más en la rotación diaria, **Traza**: de vez
en cuando (cada dos semanas más o menos, repartida por todo el año),
en vez de dibujar se repasa el contorno real de una letra -- mayúscula
y minúscula, sacado del glifo real de la fuente del cuaderno, no un
dibujo aparte -- hasta cubrir las 27 letras del abecedario. Ver
"Estructura" más abajo.

Ver `notes/01-curriculum.md` para el plan completo del curso (reparto
de personajes, arco de cada trimestre, disciplina de vocabulario, qué
falta escribir) y `notes/02-revision-y-plan.md` para la revisión del
cuaderno y el plan de desarrollo del resto del año.

## El cuaderno de primeras palabras (nivel 1)

El nivel anterior al de frases: mismo calendario (260 días, cuatro
trimestres = cuatro estaciones, medalla al final de cada uno), mismos
personajes y mismo tema cada semana -- si en casa hay dos hermanos,
cada uno lleva su cuaderno y esa semana leen los dos sobre lo mismo --,
pero lo que se lee es mucho más sencillo:

| Trimestre | Qué se lee | Qué sílabas |
|---|---|---|
| 1 (otoño) | 1 palabra al día | solo directas: *ma·má, pa·to*; tres sílabas desde la semana 6 (*o·to·ño*) |
| 2 (invierno) | 2 palabras al día | + cerradas (*sol, bu·fan·da*), *c*/*g* suaves (*ce, gi*), *h* |
| 3 (primavera) | 3 palabras al día | todas: trabadas (*li·bro*), *ch, ll, rr, qu, gu*, diptongos (*a·bue·la*) |
| 4 (verano) | 1 frase de 2 a 4 palabras | el puente hacia el nivel 2, que empieza en 6–8 palabras |

Cada palabra se imprime partida en sílabas y entera, y casi todas las
actividades terminan dibujando (dibuja, completa, traza, escribe
repasando letras huecas, encuentra la palabra, palmadas por sílaba,
adivina y dibuja, une, ¿sí o no?, y el viernes relee la semana) -- la
caja de actividad ocupa todo lo que queda de página, para que haya
sitio de verdad para dibujar.

La escalera de sílabas no es una intención editorial: está en
`tools/gen_palabras.py` (`ESCALERA`) y el generador falla si una
palabra se la salta. Cada palabra se escribe en el JSON ya partida
(`"pe-lo-ta"`), y ese silabeo tiene que coincidir con el automático de
`tools/silabas.py` -- dos fuentes que tienen que estar de acuerdo. Ver
`notes/03-nivel-palabras.md` para el diseño completo.

## Leo con lupa (nivel 3)

El año siguiente al cuaderno de frases: la misma niña, un año mayor, y
un nivel por encima. Mismo formato (A4, 260 días, cuatro trimestres que
son las cuatro estaciones, medallas y diploma) y mismos personajes,
pero:

- **el texto está hecho de oraciones complejas** -- subordinadas con
  *que*, *porque*, *aunque*, *cuando*, *si*, *para que*, *antes de
  que*... --, en párrafos de 55 palabras al principio a unas 120 al
  final, primero en presente y desde el invierno narrado en pasado, con
  cartas, recetas, instrucciones, entrevistas, textos informativos, un
  diario, poemas y noticias;
- **cada actividad obliga a analizar lo leído**: dibujar exactamente lo
  que describe el texto (*Dibuja con lupa*: cuántos, de qué color,
  dónde, y luego comprobarlo con preguntas que mandan de vuelta al
  texto), resolver el caso de la semana con las pistas repartidas de
  lunes a jueves (*Resuelve el caso*), tablas lógicas, mapas en
  cuadrícula con indicaciones, mensajes secretos cuyo código explica el
  texto, cazar los errores de un resumen equivocado, ordenar sucesos,
  fichas de textos informativos, comparar...

Lucía recibe la lupa de su bisabuelo relojero y funda con sus amigos el
*Club de la Lupa*: cada semana es un capítulo, casi siempre con un caso,
y cada trimestre tiene uno grande (¿quién es *Lector X*?, el mapa del tesoro de la abuela, la
cápsula del tiempo del colegio, el tesoro del pueblo). Al generar el
libro se comprueba a máquina lo que se puede comprobar de cada actividad
-- que cada tabla lógica tenga una sola solución, que cada ruta de un
mapa llegue a donde dice, que cada corrección de *Caza los errores* esté
de verdad en el texto de la semana -- y todo lo que tiene solución va a
una clave de respuestas al final del cuaderno. La escalera
(`content/lupa/progresion.json`) mide, además de palabras y longitud de
frase, un mínimo de oraciones subordinadas por texto. Ver
`notes/04-nivel-lupa.md` para el diseño completo: escalera, catálogo de
actividades y plan de las 52 semanas.

## Read and Draw (en inglés)

El cuarto cuaderno, y el único que no es en español: **todo** está en
inglés (británico) -- el texto, las instrucciones, la portada, la página
para el adulto, la clave y el diploma --, para la misma niña, que ya lee
con soltura en español y está aprendiendo inglés en el colegio. Es un
nivel por debajo de *Leo con lupa*, con su misma página (A4, 260 días,
cuatro partes = cuatro estaciones, medallas y diploma):

- **textos cortos, de oraciones compuestas**: de unas 30 palabras en
  otoño a unas 70 en verano, pero siempre con alguna subordinada
  (*because*, *when*, *who*, *that*, *if*, *before*...) -- una por texto
  al principio, tres al final --, en presente hasta el invierno y en
  pasado desde la primavera;
- **cada día, un análisis muy sencillo de lo leído**: dibujar
  exactamente lo que dice el texto (*Read and draw*), colorear un dibujo
  como dice (*Read and colour*), dibujar cosas en su sitio en una escena
  (*Where is it?*: *in*, *on*, *under*, *next to*...), *Yes or no?*,
  rodear, unir, unir las dos mitades de una frase compuesta del texto
  (*Match the halves*), la palabra que falta, ordenar la historia,
  adivinanzas y, cada viernes, la semana en tres dibujos o un repaso.
  Cada actividad lleva un icono (un lápiz, una cera, una casilla...),
  explicado con su palabra al principio del cuaderno.

La familia de siempre y unos vecinos nuevos, que son la razón de que
todo esté en inglés: los Brown llegan de Londres -- Amy, que acaba en la
clase de Lucía y dibuja las palabras que no sabe decir en español; Sam,
su hermano, y Pip, un loro verde que habla. Al generar el libro se
comprueba a máquina lo que se puede comprobar: que cada frase de *The
missing words* y de *Match the halves* esté tal cual en el texto de la
semana, que el inglés sea británico y que no se cuele nada del español.
Ver `notes/05-english.md` para el diseño completo: escalera, actividades,
reparto y el plan de las 52 semanas.

## First Words (en inglés)

El quinto cuaderno, y el nivel más bajo en inglés: para quien conoce las
letras y empieza a juntar sus sonidos. Es el cuaderno de primeras
palabras en inglés -- el mismo generador (`tools/gen_palabras.py
--libro firstwords`), la misma página, el mismo ciclo semanal y las
mismas actividades --, con los temas de *Read and Draw* semana a semana,
y todo en inglés, también la portada, *How to use this book*, la clave y
el diploma:

- **una palabra al día en otoño, dos en invierno, tres en primavera y
  una frase en verano**, de dos palabras a cuatro -- el puente hacia
  *Read and Draw*;
- **se lee por sonidos, no por sílabas** (*phonics*, como en los
  colegios ingleses): la tarjeta enseña la palabra entera con un botón
  debajo de cada sonido -- un punto si es una letra (*c-a-t*), una raya
  si son varias (*sh-ee-p*), un arco si es una e mágica (*cake*) --, y se
  lee tocando cada botón y juntando los sonidos;
- **una escalera de sonidos**: primero una letra = un sonido, después
  las letras dobles, *x*, *y*, *qu*, en invierno dos o tres letras para
  un sonido (*sh, ee, igh, oa*...), en primavera las otras formas de
  escribirlos y la e mágica, y en verano frases que se leen enteras con
  lo aprendido. Una página al principio, *The sounds in this book*,
  enseña todos los sonidos en ese orden, cada uno con una palabra;
- **tricky words** (*the, said, you*...), las palabras que no se leen
  como se escriben: se presentan los viernes de primavera, enteras y en
  un marco, y son las únicas que no se leen sonido a sonido en las
  frases del verano;
- **un dibujo para colorear cada día**: el de una palabra que se acaba
  de leer -- si se lee *van*, se colorea una furgoneta --; en la
  adivinanza se colorea, de tres dibujos, el que la contesta, y en
  *Match* cada palabra se une con su dibujo. Siempre los mismos
  personajes (`diagrams/firstwords/kit.tex`), y cada parte del dibujo,
  cerrada, para colorearla aparte.

Al generar el libro se comprueba a máquina que cada palabra se parta en
sonidos igual a mano que en `tools/fonetica.py`, que solo use los
sonidos que ya se han visto, que no sea una palabra cuyos botones
mentirían (*house*, *knee*, *nice*: una letra que no suena) ni una
*tricky word* (*the, said*), que la tabla de sonidos diga lo mismo que
la escalera, que cada sonido de la tabla salga en alguna tarjeta de su
estación y que cada dibujo sea el de una palabra que se lee ese día.
Ver `notes/06-first-words.md` para el diseño completo y las fases.

## Los cuadernos de verano y las muestras

El verano de cada cuaderno (sus últimas 13 semanas, del día 196 al 260)
es también un cuaderno aparte, para quien solo quiere leer un poco cada
día de las vacaciones: 65 páginas, numeradas del día 1 al 65 y de la
semana 1 a la 13, con su propia portada (la del libro, con la insignia
"Cuaderno de verano"), una página para el adulto que explica el verano
y no el año entero, un mapa del verano -- cada semana con su tema y
cinco soles, uno por día, para colorear cada día que se lee --, su
parte de la clave de respuestas y un diploma del verano.

Las páginas de los días no se escriben dos veces: son las mismas del
libro entero, una a una. Los generadores escriben, además del libro,
los `.tex` de cada edición escogiendo esas páginas, y lo único que
cambia dentro de una es el cartel de cada diez páginas ("¡200 páginas
leídas!" es "¡5 páginas leídas!"); el número del día y de la semana que
se imprime lo resta LaTeX. `ediciones/<raíz>-verano.tex` es el `.tex`
raíz de siempre con `\edicion` fijado antes -- como `\bookcolor` para el
blanco y negro --, así que cada uno sale en los dos formatos. Ver
`notes/07-ediciones.md`.

La **muestra gratuita** de cada cuaderno son sus cuatro primeras semanas
(días 1 a 20), para probar con unas pocas páginas antes de imprimir el
año entero: la portada (con la insignia "Muestra gratuita"), las
páginas del principio del libro, los 20 días con su número de siempre
("Día 1 / 260": son el principio del libro), su parte de la clave y, en
vez del diploma, una página que dice dónde está el cuaderno entero, con
un código QR. Se hace con el mismo motor (`ediciones/<raíz>-muestra.tex`).

## Descargar el PDF sin instalar nada

Nivel 1, primeras palabras:
**[⬇ PDF (color)](https://konradcinkusz.github.io/learning-to-read/aprendo-a-leer-palabras.pdf)**
· **[⬇ PDF (blanco y negro)](https://konradcinkusz.github.io/learning-to-read/aprendo-a-leer-palabras-bn.pdf)**

Nivel 2, frases:
**[⬇ PDF (color)](https://konradcinkusz.github.io/learning-to-read/aprendo-a-leer.pdf)**
· **[⬇ PDF (blanco y negro)](https://konradcinkusz.github.io/learning-to-read/aprendo-a-leer-bn.pdf)**

Nivel 3, Leo con lupa:
**[⬇ PDF (color)](https://konradcinkusz.github.io/learning-to-read/leo-con-lupa.pdf)**
· **[⬇ PDF (blanco y negro)](https://konradcinkusz.github.io/learning-to-read/leo-con-lupa-bn.pdf)**

*Read and Draw*, en inglés:
**[⬇ PDF (color)](https://konradcinkusz.github.io/learning-to-read/read-and-draw.pdf)**
· **[⬇ PDF (blanco y negro)](https://konradcinkusz.github.io/learning-to-read/read-and-draw-bw.pdf)**

*First Words*, en inglés:
**[⬇ PDF (color)](https://konradcinkusz.github.io/learning-to-read/first-words.pdf)**
· **[⬇ PDF (blanco y negro)](https://konradcinkusz.github.io/learning-to-read/first-words-bw.pdf)**

Los cuadernos de verano (65 páginas cada uno):
nivel 1, primeras palabras
([color](https://konradcinkusz.github.io/learning-to-read/aprendo-a-leer-palabras-verano.pdf) ·
[blanco y negro](https://konradcinkusz.github.io/learning-to-read/aprendo-a-leer-palabras-verano-bn.pdf));
nivel 2, frases
([color](https://konradcinkusz.github.io/learning-to-read/aprendo-a-leer-verano.pdf) ·
[blanco y negro](https://konradcinkusz.github.io/learning-to-read/aprendo-a-leer-verano-bn.pdf));
nivel 3, Leo con lupa
([color](https://konradcinkusz.github.io/learning-to-read/leo-con-lupa-verano.pdf) ·
[blanco y negro](https://konradcinkusz.github.io/learning-to-read/leo-con-lupa-verano-bn.pdf));
*Read and Draw*
([color](https://konradcinkusz.github.io/learning-to-read/read-and-draw-summer.pdf) ·
[blanco y negro](https://konradcinkusz.github.io/learning-to-read/read-and-draw-summer-bw.pdf));
*First Words*
([color](https://konradcinkusz.github.io/learning-to-read/first-words-summer.pdf) ·
[blanco y negro](https://konradcinkusz.github.io/learning-to-read/first-words-summer-bw.pdf)).

Las muestras gratuitas (las cuatro primeras semanas, 20 días):
nivel 1, primeras palabras
([color](https://konradcinkusz.github.io/learning-to-read/aprendo-a-leer-palabras-muestra.pdf) ·
[blanco y negro](https://konradcinkusz.github.io/learning-to-read/aprendo-a-leer-palabras-muestra-bn.pdf));
nivel 2, frases
([color](https://konradcinkusz.github.io/learning-to-read/aprendo-a-leer-muestra.pdf) ·
[blanco y negro](https://konradcinkusz.github.io/learning-to-read/aprendo-a-leer-muestra-bn.pdf));
nivel 3, Leo con lupa
([color](https://konradcinkusz.github.io/learning-to-read/leo-con-lupa-muestra.pdf) ·
[blanco y negro](https://konradcinkusz.github.io/learning-to-read/leo-con-lupa-muestra-bn.pdf));
*Read and Draw*
([color](https://konradcinkusz.github.io/learning-to-read/read-and-draw-sample.pdf) ·
[blanco y negro](https://konradcinkusz.github.io/learning-to-read/read-and-draw-sample-bw.pdf));
*First Words*
([color](https://konradcinkusz.github.io/learning-to-read/first-words-sample.pdf) ·
[blanco y negro](https://konradcinkusz.github.io/learning-to-read/first-words-sample-bw.pdf)).

Enlaces fijos, publicados por GitHub Pages en cada push a `main` (ver
`.github/workflows/pages.yml`). Las dos versiones tienen exactamente el
mismo contenido y la misma paginación — la de blanco y negro es para
imprimir sin gastar tinta de color, no una versión reducida: nada en el
cuaderno se distingue solo por el color (el título en negrita de cada
caja ya dice qué actividad es).

Si esos enlaces todavía no responden (por ejemplo, justo después de
activar Pages por primera vez, antes de que corra el primer
despliegue), los mismos PDF están también en la pestaña
[*Actions*](https://github.com/konradcinkusz/learning-to-read/actions/workflows/build.yml)
→ el último run de *Build* → artefactos `pdf-color` / `pdf-bw` /
`pdf-palabras-color` / `pdf-palabras-bw` / `pdf-lupa-color` /
`pdf-lupa-bw` / `pdf-english-color` / `pdf-english-bw` /
`pdf-firstwords-color` / `pdf-firstwords-bw`, los de verano
`pdf-verano-color` / `pdf-verano-bw` / `pdf-palabras-verano-color`... y
las muestras `pdf-muestra-color` / `pdf-palabras-muestra-bw`... (se
guardan 30 días, hace falta estar identificado en GitHub para
descargarlos).

## Construir el PDF a mano

Necesita una distribución de TeX con **LuaLaTeX** (no pdflatex: la letra
del cuaderno es Andika, cargada con `fontspec` desde `fonts/andika/` —
ver preamble.tex) + `latexmk`, con `babel`, `tcolorbox`, `tikz` y
`fontspec` — cualquier TeX Live razonablemente completo los trae.

```sh
make              # genera, compila el cuaderno de frases (color), comprueba
make palabras     # lo mismo para el cuaderno de primeras palabras (color)
make lupa         # lo mismo para Leo con lupa (color)
make english      # lo mismo para Read and Draw, en inglés (color)
make firstwords   # lo mismo para First Words, en inglés (color)
make verano       # los diez cuadernos de verano: los cinco, color Y blanco-y-negro
make muestra      # las diez muestras gratuitas: los cinco, color Y blanco-y-negro
make all-formats  # los treinta PDF: palabras, frases, lupa, english y firstwords, color Y blanco-y-negro, y sus ediciones
make generate     # solo regenera los .tex de los cinco cuadernos desde el JSON
make build        # solo compila frases en color (asume que ya está generado)
make build-bw     # solo compila frases en blanco y negro
make build-palabras / build-palabras-bw   # lo mismo, primeras palabras
make check        # lee main.log + 1 día = 1 página (lee main.aux) + valida el JSON
make check-bw     # lo mismo, sobre main-bw.log / main-bw.aux
make check-palabras / check-palabras-bw   # lo mismo, primeras palabras (+ silabeo)
make build-lupa / build-lupa-bw           # lo mismo, Leo con lupa
make check-lupa / check-lupa-bw           # lo mismo, Leo con lupa (+ actividades y escalera)
make build-english / build-english-bw     # lo mismo, Read and Draw
make check-english / check-english-bw     # lo mismo, Read and Draw (+ actividades, inglés británico y escalera)
make build-firstwords / build-firstwords-bw   # lo mismo, First Words
make check-firstwords / check-firstwords-bw   # lo mismo, First Words (+ partido en sonidos y escalera de sonidos)
make build-lupa-verano / check-lupa-verano    # un cuaderno de verano (main, main-bw, palabras, lupa-bw...: <raíz>-verano)
make build-lupa-muestra / check-lupa-muestra  # una muestra gratuita (<raíz>-muestra)
make clean
```

## Estructura

```
main.tex, main-bw.tex                 -- cuaderno de frases, color y blanco-y-negro; solo fijan \bookcolor
palabras.tex, palabras-bw.tex         -- cuaderno de primeras palabras, color y blanco-y-negro
lupa.tex, lupa-bw.tex                 -- Leo con lupa (nivel 3), color y blanco-y-negro
english.tex, english-bw.tex           -- Read and Draw (en inglés), color y blanco-y-negro
firstwords.tex, firstwords-bw.tex     -- First Words (primeras palabras en inglés), color y blanco-y-negro
ediciones/<raíz>-verano.tex           -- los cuadernos de verano: cada .tex raíz de arriba con \edicion fijado antes
ediciones/<raíz>-muestra.tex          -- las muestras gratuitas (las cuatro primeras semanas), igual
preamble.tex, lang/es.tex             -- el motor LaTeX (la paleta de main-bw.tex está en preamble.tex)
lang/en.tex                           -- las cadenas en inglés (\booklang = en, ver preamble.tex)
preamble-palabras.tex                 -- lo propio del cuaderno de primeras palabras (tarjetas, cajas que llenan la página)
preamble-lupa.tex                     -- lo propio de Leo con lupa (caja de actividad a toda página, mapas, tablas, códigos, la lupa)
preamble-english.tex                  -- lo propio de Read and Draw (sobre preamble-lupa.tex: letra más grande, piezas de sus actividades, iconos)
preamble-firstwords.tex               -- lo propio de First Words (sobre preamble-palabras.tex: la tarjeta con botones de sonido, la tabla de sonidos)
body.tex, body-palabras.tex, body-lupa.tex, body-english.tex, body-firstwords.tex -- orden del documento de cada cuaderno
frontmatter/                          -- portada, instrucciones, mapa del curso (frontmatter/palabras/: nivel 1; frontmatter/lupa/: nivel 3, con "Cómo lee un detective" y el carné del club; frontmatter/english/: en inglés, con los iconos de las actividades y "Who's who?"; frontmatter/firstwords/: First Words, con la tabla de sonidos); verano.tex, en cada uno: la página para el adulto de su cuaderno de verano
content/q1.json, q2.json, q3.json, q4.json  -- los 260 días, uno por trimestre, editados a mano
content/generated-days.tex            -- GENERADO por tools/gen_days.py, no editar
content/progresion.json               -- objetivos semanales de la escalera de progresión (52 filas)
content/generated-clave.tex           -- GENERADO por tools/gen_days.py, no editar
content/letras-trazo.json             -- contorno real de cada letra (Andika), generado por tools/gen_letras_puntos.py
content/palabras-trazo.json           -- palabra de ejemplo de cada letra ("A de Abuela"), editado a mano
content/palabras/q1.json ... q4.json  -- los 260 días del cuaderno de primeras palabras, editados a mano
content/palabras/generated-*.tex      -- GENERADO por tools/gen_palabras.py, no editar
content/lupa/q1.json ... q4.json      -- los 260 días de Leo con lupa, editados a mano
content/lupa/progresion.json          -- la escalera de Leo con lupa (palabras, frase más larga, subordinadas)
content/lupa/generated-*.tex          -- GENERADO por tools/gen_days.py --libro lupa, no editar
content/english/q1.json ... q4.json   -- los días de Read and Draw, editados a mano
content/english/progresion.json       -- la escalera de Read and Draw (palabras, frase más larga, subordinadas)
content/english/vocabulario-base.json -- el inglés que se da por sabido (para el aviso de vocabulario nuevo)
content/english/generated-*.tex       -- GENERADO por tools/gen_days.py --libro english, no editar
content/firstwords/q1.json ... q4.json -- los días de First Words, editados a mano (cada palabra partida en sonidos)
content/firstwords/generated-*.tex    -- GENERADO por tools/gen_palabras.py --libro firstwords (días, clave, tabla de sonidos), no editar
diagrams/                             -- dibujos de línea (TikZ) para las páginas "Completa"
diagrams/english/                     -- dibujos para colorear y escenas donde dibujar, de Read and Draw
backmatter/diploma.tex, clave-respuestas.tex -- diploma y clave de respuestas (backmatter/palabras/: nivel 1; backmatter/lupa/: nivel 3; backmatter/english/: Read and Draw; backmatter/firstwords/: First Words)
fonts/andika/                         -- letra del cuaderno (Andika, SIL, OFL -- ver "Licencia")
tools/gen_days.py                     -- JSON -> LaTeX + validación + medallas + clave de respuestas + trazo (frases, y Leo con lupa con --libro lupa)
tools/libros.py                       -- lo que distingue el cuaderno de frases de Leo con lupa: rutas, reglas, tipos de actividad
tools/lupa.py                         -- plantillas y comprobaciones de las actividades de Leo con lupa (tablas lógicas, mapas, errores...)
tools/english.py                      -- lo mismo para Read and Draw (frases del texto, inglés británico, sin español)
tools/comun.py                        -- lo que comparten gen_days.py y lupa.py
tools/ediciones.py                    -- las ediciones (el cuaderno de verano, la muestra): qué días, cómo se renumeran, los carteles y los .tex que escriben los dos generadores
tools/gen_palabras.py                 -- lo mismo para el cuaderno de primeras palabras, + la escalera de sílabas (y First Words con --libro firstwords, + la escalera de sonidos)
tools/silabas.py                      -- silabeo automático del español y rasgos de cada sílaba (cerrada, trabada...)
tools/fonetica.py                     -- partido automático del inglés en sonidos (grafemas, e mágica), trampas, tricky words (First Words)
tools/gen_letras_puntos.py            -- fuente -> contorno de cada letra (matplotlib/fonttools; no forma parte de `make`)
tools/check_pages.py                  -- comprueba que cada día ocupa una sola página
tools/checklog.py                     -- lee el .log de LuaLaTeX correctamente (nunca grep '^!')
tools/metricas.py                     -- mide palabras/frase/vocabulario nuevo contra content/progresion.json (y subordinadas, con --libro lupa o --libro english)
docs/index.html                       -- la página que publica .github/workflows/pages.yml
assets/logo.tex, logo.png, logo.svg   -- logo del repositorio (standalone TikZ, reutiliza el icono de portada.tex)
LICENSE, LICENSE-CODE, LICENSE-CONTENT -- ver "Licencia" más abajo
CONTRIBUTING.md                       -- cómo colaborar (o hacer tu propio fork)
.github/workflows/build.yml           -- compila (color + blanco-y-negro) y valida en cada push/PR
.github/workflows/pages.yml           -- publica los dos PDF en GitHub Pages en cada push a main
notes/01-curriculum.md                -- el plan del curso completo
notes/02-revision-y-plan.md           -- revisión del cuaderno y plan de desarrollo del resto del año
notes/03-nivel-palabras.md            -- diseño del cuaderno de primeras palabras (nivel 1)
notes/04-nivel-lupa.md                -- diseño de Leo con lupa (nivel 3): escalera, actividades, reparto y las 52 semanas
notes/05-english.md                   -- diseño de Read and Draw (en inglés): escalera, actividades, reparto, las 52 semanas y las fases
notes/06-first-words.md               -- diseño de First Words (primeras palabras en inglés): escalera de sonidos, botones, comprobaciones y las fases
notes/07-ediciones.md                 -- las ediciones de los cinco cuadernos: el cuaderno de verano y la muestra gratuita
```

## Licencia

El motor -- LaTeX (`preamble*.tex`, `lang/*.tex`, `main*.tex`, `palabras*.tex`, `lupa*.tex`, `english*.tex`, `firstwords*.tex`, `body*.tex`, `ediciones/*.tex`),
las herramientas Python (`tools/`), el `Makefile` y la configuración de CI
(`.github/`) -- está bajo MIT ([`LICENSE-CODE`](LICENSE-CODE)): reutilízalo
libremente, incluido un fork para otro niño o niña.

El contenido narrativo -- las frases, las palabras, los nombres y la
trama de `content/*.json`, `content/palabras/*.json`,
`content/lupa/*.json`, `content/english/*.json` y
`content/firstwords/*.json`, y lo que se genera de ahí a las páginas de
los cinco cuadernos --
está bajo Creative Commons Atribución-NoComercial-CompartirIgual 4.0
([`LICENSE-CONTENT`](LICENSE-CONTENT)): se puede adaptar (por ejemplo,
cambiar los personajes) pero no usar comercialmente, y cualquier adaptación
tiene que compartirse bajo la misma licencia.

La letra del cuaderno -- Andika (`fonts/andika/`), de SIL International --
está bajo la SIL Open Font License 1.1 ([`fonts/andika/OFL.txt`](fonts/andika/OFL.txt)),
independiente de las dos licencias de arriba.

Ver [`LICENSE`](LICENSE) para el reparto exacto de qué cae en cada lado, y
[`CONTRIBUTING.md`](CONTRIBUTING.md) para qué tipo de colaboración encaja
aquí.

## Estado

**Nivel 1 (primeras palabras)**: los 260 días están escritos y compilan
como un cuaderno completo (`make all-formats` en verde: 1 día = 1
página, log limpio, cada palabra dentro de la escalera de sílabas de su
semana y con el silabeo comprobado), con sus tres medallas, la clave de
respuestas, el diploma y las 27 letras del abecedario en las páginas
"Traza". Ver `notes/03-nivel-palabras.md`.

**Nivel 2 (frases)**: los 260 días están escritos, con sus actividades, y compilan como un
cuaderno completo (`make all-formats` en verde: 1 día = 1 página, sin
huecos, dentro de la escalera de progresión de
`content/progresion.json`). Las medallas de trimestre, la clave de
respuestas y las 27 páginas "Traza" (una por letra, repartidas por
todo el año) también están escritas y compilan. Ver `notes/01-curriculum.md` para el arco
narrativo de cada trimestre y `notes/02-revision-y-plan.md` para la
revisión completa del cuaderno (qué mejorar y en qué orden) y el
calendario del curso completo -- por qué los cuatro trimestres son las
cuatro estaciones del año, con vacaciones incluidas, y no los tres
trimestres del curso escolar español.

**Nivel 3 (Leo con lupa)**: los 260 días están escritos (52 semanas y
35 casos, con su solución en la clave), y compilan como un cuaderno completo (`make all-formats` en
verde: 1 día = 1 página, log limpio, dentro de la escalera de
`content/lupa/progresion.json`, y todas las comprobaciones de
`tools/lupa.py` en verde: tablas lógicas con una sola solución, rutas de
mapa que llegan a donde dicen, correcciones que están en el texto), con
sus tres medallas, la clave de respuestas y el diploma. Ver
`notes/04-nivel-lupa.md`.

**Read and Draw (en inglés)**: completo, los 260 días (las cuatro
partes del año, con sus tres medallas, la clave de respuestas y el
diploma), escrito en cinco fases, una por PR (ver `notes/05-english.md`,
"Las fases"). Todo está en inglés, también la portada, *How to use this
book*, *The words in this book*, *Who's who?* y el mapa del año. Compila
en color y en blanco y negro con las mismas comprobaciones que los otros
tres cuadernos, y se publica en GitHub Pages con ellos.

**First Words (en inglés)**: completo, los 260 días (las cuatro
partes del año, con sus tres medallas, las 47 *tricky words* de los
viernes de primavera, la clave de respuestas y el diploma), escrito en
cinco fases, una por PR (ver `notes/06-first-words.md`, "Las fases").
Todo está en inglés, también la portada, *How to use this book*, *The
sounds in this book* y el mapa del año. El motor es el del cuaderno de
primeras palabras en español (`tools/gen_palabras.py`, que sigue
generándolo idéntico byte a byte) con `tools/fonetica.py`. Compila en
color y en blanco y negro con las mismas comprobaciones que los otros
cuatro cuadernos, y se publica en GitHub Pages con ellos.

**Los cuadernos de verano**: los cinco, en color y en blanco y negro --
el verano de cada cuaderno, con su portada, su página para el adulto,
su mapa del verano, su clave y su diploma. Compilan con las mismas
comprobaciones que los libros enteros (1 día = 1 página, log limpio), y
se publican en GitHub Pages con ellos. Ver `notes/07-ediciones.md`.

**Las muestras gratuitas**: las cinco, en color y en blanco y negro --
las cuatro primeras semanas de cada cuaderno, con una última página que
dice dónde está el cuaderno entero. Las mismas comprobaciones, y
también en GitHub Pages.
