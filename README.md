<p align="center"><img src="assets/logo.png" width="140" alt="Aprendo a leer"></p>

# Aprendo a leer

[![Build](https://github.com/konradcinkusz/learning-to-read/actions/workflows/build.yml/badge.svg)](https://github.com/konradcinkusz/learning-to-read/actions/workflows/build.yml)
[![Licencia](https://img.shields.io/github/license/konradcinkusz/learning-to-read)](LICENSE)
[![Hecho con](https://img.shields.io/badge/hecho%20con-LaTeX-2E7D32)](preamble.tex)

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

## Nivel 2: *Leo con lupa*

El segundo cuaderno, para el año siguiente: la misma niña, un año
mayor, y un nivel por encima. Mismo formato (A4, 260 días, cuatro
trimestres que son las cuatro estaciones) y mismos personajes, pero:

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
*Club de la Lupa*: cada semana es un caso, y cada trimestre tiene uno
grande (¿quién es *Lector X*?, el mapa del tesoro de la abuela, la
cápsula del tiempo del colegio). Ver `notes/03-nivel2.md` para el diseño
completo: escalera de progresión, catálogo de actividades y plan de las
52 semanas. Al generar el libro se comprueba a máquina lo que se puede
comprobar de cada actividad -- que cada tabla lógica tenga una sola
solución, que cada ruta de un mapa llegue a donde dice, que cada
corrección de *Caza los errores* esté de verdad en el texto de la
semana -- y todo lo que tiene solución va a una clave de respuestas al
final del cuaderno.

## Descargar el PDF sin instalar nada

Nivel 1, *Aprendo a leer*:
**[⬇ PDF (color)](https://konradcinkusz.github.io/learning-to-read/aprendo-a-leer.pdf)**
· **[⬇ PDF (blanco y negro)](https://konradcinkusz.github.io/learning-to-read/aprendo-a-leer-bn.pdf)**

Nivel 2, *Leo con lupa*:
**[⬇ PDF (color)](https://konradcinkusz.github.io/learning-to-read/leo-con-lupa.pdf)**
· **[⬇ PDF (blanco y negro)](https://konradcinkusz.github.io/learning-to-read/leo-con-lupa-bn.pdf)**

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
→ el último run de *Build* → artefactos `pdf-color` / `pdf-bw` (nivel 1)
y `pdf-nivel2-color` / `pdf-nivel2-bw` (nivel 2) -- se guardan 30 días,
hace falta estar identificado en GitHub para descargarlos.

## Construir el PDF a mano

Necesita una distribución de TeX con **LuaLaTeX** (no pdflatex: la letra
del cuaderno es Andika, cargada con `fontspec` desde `fonts/andika/` —
ver preamble.tex) + `latexmk`, con `babel`, `tcolorbox`, `tikz` y
`fontspec` — cualquier TeX Live razonablemente completo los trae.

```sh
make              # nivel 1: genera content/generated-days.tex, compila (color), comprueba
make nivel2       # nivel 2: lo mismo con content/nivel2/ y main-nivel2.tex
make all-formats  # los dos niveles, en color Y en blanco y negro (lo que corre el CI)
make generate     # solo regenera content/generated-days.tex desde el JSON (nivel 1)
make generate-nivel2  # lo mismo para el nivel 2 (content/nivel2/generated-days.tex)
make build        # solo compila la versión en color (asume que ya está generado)
make build-bw     # solo compila la versión en blanco y negro
make build-nivel2 build-nivel2-bw   # lo mismo para el nivel 2
make check        # lee main.log + 1 día = 1 página (lee main.aux) + valida el JSON + escalera
make check-bw     # lo mismo, sobre main-bw.log / main-bw.aux
make check-nivel2 check-nivel2-bw   # lo mismo para el nivel 2
make clean
```

## Estructura

```
main.tex, main-bw.tex                 -- color y blanco-y-negro; solo fijan \bookcolor y comparten todo lo demás
main-nivel2.tex, main-nivel2-bw.tex   -- lo mismo para el nivel 2 ("Leo con lupa")
preamble.tex, lang/es.tex             -- el motor LaTeX, compartido por los dos niveles (la paleta de main-bw.tex está en preamble.tex)
body.tex, body-nivel2.tex             -- orden del documento de cada nivel
frontmatter/                          -- portada, instrucciones, mapa del curso (frontmatter/nivel2/: los del nivel 2, más la página "Cómo lee un detective" y el carné del club)
content/q1.json, q2.json, q3.json, q4.json  -- los 260 días, uno por trimestre, editados a mano
content/nivel2/q1.json ... q4.json    -- los 260 días del nivel 2, editados a mano
content/nivel2/progresion.json        -- la escalera del nivel 2 (palabras, frase más larga, subordinadas)
content/nivel2/generated-*.tex        -- GENERADOS por tools/gen_days.py --libro nivel2, no editar
content/generated-days.tex            -- GENERADO por tools/gen_days.py, no editar
content/progresion.json               -- objetivos semanales de la escalera de progresión (52 filas)
content/generated-clave.tex           -- GENERADO por tools/gen_days.py, no editar
content/letras-trazo.json             -- contorno real de cada letra (Andika), generado por tools/gen_letras_puntos.py
content/palabras-trazo.json           -- palabra de ejemplo de cada letra ("A de Abuela"), editado a mano
diagrams/                             -- dibujos de línea (TikZ) para las páginas "Completa"
backmatter/diploma.tex, clave-respuestas.tex -- diploma y clave de respuestas (backmatter/nivel2/: los del nivel 2)
fonts/andika/                         -- letra del cuaderno (Andika, SIL, OFL -- ver "Licencia")
tools/gen_days.py                     -- JSON -> LaTeX + validación + medallas + clave de respuestas + trazo (--libro nivel1|nivel2)
tools/libros.py                       -- lo que distingue un libro de otro: rutas, reglas, tipos de actividad
tools/nivel2.py                       -- plantillas y comprobaciones de las actividades del nivel 2 (tablas lógicas, mapas, errores...)
tools/comun.py                        -- lo que comparten gen_days.py y nivel2.py
tools/gen_letras_puntos.py            -- fuente -> contorno de cada letra (matplotlib/fonttools; no forma parte de `make`)
tools/check_pages.py                  -- comprueba que cada día ocupa una sola página
tools/checklog.py                     -- lee el .log de LuaLaTeX correctamente (nunca grep '^!')
tools/metricas.py                     -- mide palabras/frase/vocabulario nuevo (y subordinadas, en el nivel 2) contra la escalera de cada libro
docs/index.html                       -- la página que publica .github/workflows/pages.yml
assets/logo.tex, logo.png, logo.svg   -- logo del repositorio (standalone TikZ, reutiliza el icono de portada.tex)
LICENSE, LICENSE-CODE, LICENSE-CONTENT -- ver "Licencia" más abajo
CONTRIBUTING.md                       -- cómo colaborar (o hacer tu propio fork)
.github/workflows/build.yml           -- compila (color + blanco-y-negro) y valida en cada push/PR
.github/workflows/pages.yml           -- publica los dos PDF en GitHub Pages en cada push a main
notes/01-curriculum.md                -- el plan del curso completo
notes/02-revision-y-plan.md           -- revisión del cuaderno y plan de desarrollo del resto del año
notes/03-nivel2.md                    -- el diseño del nivel 2: escalera, actividades, reparto y las 52 semanas
```

## Licencia

El motor -- LaTeX (`preamble.tex`, `lang/es.tex`, `main*.tex`, `body.tex`),
las herramientas Python (`tools/`), el `Makefile` y la configuración de CI
(`.github/`) -- está bajo MIT ([`LICENSE-CODE`](LICENSE-CODE)): reutilízalo
libremente, incluido un fork para otro niño o niña.

El contenido narrativo -- las frases, los nombres y la trama de
`content/*.json`, y lo que se genera de ahí a las páginas del cuaderno --
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

Los dos niveles están completos. Nivel 1: los 260 días están escritos,
con sus actividades, y compilan como un cuaderno completo (`make all-formats` en verde: 1 día = 1 página, sin
huecos, dentro de la escalera de progresión de
`content/progresion.json`). Las medallas de trimestre, la clave de
respuestas y las 27 páginas "Traza" (una por letra, repartidas por
todo el año) también están escritas y compilan. Ver `notes/01-curriculum.md` para el arco
narrativo de cada trimestre y `notes/02-revision-y-plan.md` para la
revisión completa del cuaderno (qué mejorar y en qué orden) y el
calendario del curso completo -- por qué los cuatro trimestres son las
cuatro estaciones del año, con vacaciones incluidas, y no los tres
trimestres del curso escolar español.

Nivel 2 (*Leo con lupa*): los 260 días, con sus 52 casos, compilan
igual (`make nivel2`, o `make all-formats` para los dos niveles en los
dos formatos): 1 día = 1 página, dentro de su escalera
(`content/nivel2/progresion.json`), y con todas las comprobaciones de
`tools/nivel2.py` en verde. Ver `notes/03-nivel2.md`.
