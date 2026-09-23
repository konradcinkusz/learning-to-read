# Las ediciones — el cuaderno de verano y la muestra gratuita

Cada uno de los cinco cuadernos tiene 260 páginas, una por día laborable
del año. Una **edición** es el mismo cuaderno con otra selección de
días, y con lo que tiene que cambiar para que esa selección sea un
cuaderno de verdad: su portada, su página para el adulto, su mapa, su
clave y su diploma. Hay dos, las dos del issue #16: el **cuaderno de
verano** y la **muestra gratuita**.

## El cuaderno de verano

El verano de cada cuaderno — sus últimas 13 semanas, del día 196 al 260
— en un cuaderno aparte, para quien solo quiere leer un poco cada día
de las vacaciones: 65 páginas, impresas como días 1 a 65 y semanas 1 a
13, sin trimestre. Diez PDF, los cinco cuadernos en color y en blanco y
negro: `ediciones/<raíz>-verano.tex` (`main-verano.tex`,
`main-bw-verano.tex`, `palabras-verano.tex`...). `make verano` los
compila y los comprueba; `make build-lupa-verano` o `make
check-lupa-verano`, uno.

Lo que lleva, en orden:

- **La portada del libro**, con una insignia debajo del título (un sol y
  "Cuaderno de verano" / "Summer book", `\insigniaEdicion`). En el
  cuaderno de primeras palabras y en *First Words* cambia también el
  subtítulo: en verano ya no se lee una palabra al día, sino una frase
  corta.
- **Una página para el adulto propia** (`frontmatter/verano.tex` y
  `frontmatter/<libro>/verano.tex`), en vez de "Cómo usar este cuaderno",
  que habla del año entero: para quién es el verano de ese cuaderno (lo
  que tiene que saber leer ya quien empieza por él), cómo es una página,
  qué actividades salen **en el verano** (no las de todo el año), la
  historia del verano y el ritmo. En *First Words*, además, todas las
  *tricky words* que el libro entero presenta los viernes de primavera
  (`\trickyLista`, la lista la escribe el generador): el verano las usa y
  ya no las presenta.
- Las páginas del libro que siguen valiendo tal cual: "Cómo lee un
  detective" y el carné en *Leo con lupa*, las palabras de las
  instrucciones y "Who's who?" en *Read and Draw* (en verano, con la
  edad que tienen los niños en verano y los vecinos ya con nombre: en el
  libro entero se descubren leyendo la semana 1), la tabla de sonidos en
  *First Words* (sin las estaciones en que llega cada sonido).
- **El mapa del verano** (`\mapaEdicion`), en vez del mapa del curso: las
  13 semanas, cada una con sus días y su tema, y cinco soles por semana,
  uno por día, para colorear cada día que se lee.
- **Los 65 días**.
- **Su parte de la clave de respuestas** y **un diploma del verano**
  ("Has leído una página cada día del verano", con 65 en la medalla).

No lleva medallas: la única del verano es el diploma, como en el libro
entero.

## La muestra gratuita

Las cuatro primeras semanas de cada cuaderno (días 1 a 20), para probar
con unas pocas páginas antes de imprimir el año entero. Diez PDF más:
`ediciones/<raíz>-muestra.tex`; `make muestra` los compila y los
comprueba.

A diferencia del cuaderno de verano, la muestra **es el principio del
libro entero**, y se nota: los días llevan su número de siempre ("Día 1
/ 260", semana y trimestre), y delante van las páginas del principio del
libro, tal cual — "Cómo usar este cuaderno", el mapa del curso, y lo que
tenga cada uno (el carné de detective, "Who's who?", la tabla de
sonidos). Lo que cambia:

- **la portada**, con la insignia "Muestra gratuita: las cuatro primeras
  semanas" / "Free sample: the first four weeks";
- **su parte de la clave**;
- **la última página**, en vez del diploma (`\paginaFinMuestra`):
  "¿Seguimos leyendo?", dónde está el cuaderno entero — la página de los
  cuadernos, `konradcinkusz.github.io/learning-to-read` —, y un código QR
  con esa misma dirección, para abrirla desde el móvil.

Como no cambia los números, no toca los carteles de "¡10 páginas
leídas!", no necesita `banner_muestra` y no tiene mapa propio
(`Edicion.mapa`).

## Cómo está hecho: las páginas no se escriben dos veces

Una página de un día es la misma en el libro entero y en el cuaderno de
verano, así que no se vuelve a generar: **se escoge**. Cada generador
(`tools/gen_days.py`, `tools/gen_palabras.py`) genera las páginas del
libro entero una vez y escribe con ellas, además de
`generated-days.tex` y `generated-clave.tex`, los `.tex` de cada edición
(`tools/ediciones.py`, `salidas_ediciones`):

- `generated-days-verano.tex`: las páginas de los días 196 a 260, una a
  una, sin las medallas;
- `generated-clave-verano.tex`: sus entradas de la clave;
- `generated-mapa-verano.tex`: las filas del mapa del verano, una por
  semana, con el tema de su primer día;
- en *First Words*, `generated-tricky-verano.tex`: las *tricky words*
  que el verano da por sabidas.

Dentro de una página solo cambia una cosa: **el cartel de cada diez
páginas**. "¡200 páginas leídas!" es, en el cuaderno de verano, "¡5
páginas leídas!": el número de páginas leídas es siempre el del día, y
`banner_edicion` le resta el desplazamiento de la edición (y comprueba
que el cartel empieza de verdad por ese número). Si el resto del cartel
habla del número o del año ("¡Doscientas!", "Un año entero leyendo con
lupa"), la actividad lleva el suyo propio para la edición, en
`banner_verano`: hay tres, en el día 200 del cuaderno de primeras
palabras y de *First Words* y en el 260 de *Leo con lupa*. Un
`banner_verano` en un día que no es del verano, o sin `banner`, es un
error.

En la muestra, que no cambia los números, el cartel se queda como está.

El número del día y de la semana que se imprime lo resta LaTeX, no el
generador (`\numeroDia`, `\numeroSemana` en `preamble.tex`): la etiqueta
`dia:N` de cada página sigue siendo la del libro entero, así que
`tools/check_pages.py` comprueba el cuaderno de verano sin saber que
existe (días 196 a 260, uno por página, y la clave justo detrás). Los
números de la edición (qué días, cuánto se resta, `\totaldias`) están
dos veces, en `tools/ediciones.py` y en `preamble.tex`, y los dos
generadores comprueban que coinciden (`comprobar_preamble`; lo que el
bloque de una edición no fija es lo del libro entero, como en la
muestra).

La edición la elige el `.tex` raíz: `ediciones/main-verano.tex` es
`\def\edicion{verano}` y `\input{main}` — lo mismo que hace `main-bw.tex`
con `\bookcolor` —, así que cada edición sale en color y en blanco y
negro sin una línea más. `preamble.tex` traduce `\edicion` en
`\ifedicionverano` e `\ifedicionmuestra`, `\sufijoEdicion` (el
`-verano` o `-muestra` de los `.tex` generados que se leen) y
`\segunEdicion{todo el año}{todo el verano}`, para las frases de la
portada, la tabla de sonidos, "Who's who?" y los diplomas que dicen "el
año" (la muestra dice lo del libro entero). Un `\edicion` que no es
ninguna de las tres para la compilación. El libro entero no cambia en
nada: sus `.tex` generados son los mismos, letra por letra, y sus PDF
también.

## Cómo se comprueba

- `make generate` escribe las ediciones con el libro entero, y los
  `--check` de los dos generadores comprueban que también las suyas
  están al día.
- El CI compila los diez cuadernos de verano y las diez muestras con
  los mismos pasos que los libros enteros (`.github/workflows/build.yml`:
  log limpio y un día por página), y Pages los publica junto a ellos
  (`aprendo-a-leer-verano.pdf`, `leo-con-lupa-verano-bn.pdf`,
  `read-and-draw-summer.pdf`, `first-words-summer-bw.pdf`...;
  `aprendo-a-leer-muestra.pdf`, `read-and-draw-sample-bw.pdf`...).
