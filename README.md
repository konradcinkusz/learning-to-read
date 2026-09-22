<p align="center"><img src="assets/logo.png" width="140" alt="Aprendo a leer"></p>

# Aprendo a leer

[![Build](https://github.com/konradcinkusz/learning-to-read/actions/workflows/build.yml/badge.svg)](https://github.com/konradcinkusz/learning-to-read/actions/workflows/build.yml)
[![Licencia](https://img.shields.io/github/license/konradcinkusz/learning-to-read)](LICENSE)
[![Hecho con](https://img.shields.io/badge/hecho%20con-LaTeX-2E7D32)](preamble.tex)

Dos cuadernos diarios de lectura en español, uno por nivel, con la
misma historia y los mismos temas semana a semana:

- **Nivel 1 · Primeras palabras** (`palabras.tex`) -- para quien empieza
  a juntar sílabas: una palabra al día, partida en sílabas, y casi
  siempre un dibujo. Ver "El cuaderno de primeras palabras" más abajo.
- **Nivel 2 · Frases** (`main.tex`) -- el cuaderno original, para quien
  ya lee frases completas. Es lo que describe el resto de esta
  introducción.

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

## Descargar el PDF sin instalar nada

Nivel 1, primeras palabras:
**[⬇ PDF (color)](https://konradcinkusz.github.io/learning-to-read/aprendo-a-leer-palabras.pdf)**
· **[⬇ PDF (blanco y negro)](https://konradcinkusz.github.io/learning-to-read/aprendo-a-leer-palabras-bn.pdf)**

Nivel 2, frases:
**[⬇ PDF (color)](https://konradcinkusz.github.io/learning-to-read/aprendo-a-leer.pdf)**
· **[⬇ PDF (blanco y negro)](https://konradcinkusz.github.io/learning-to-read/aprendo-a-leer-bn.pdf)**

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
`pdf-palabras-color` / `pdf-palabras-bw` (se guardan 30 días, hace
falta estar identificado en GitHub para descargarlos).

## Construir el PDF a mano

Necesita una distribución de TeX con **LuaLaTeX** (no pdflatex: la letra
del cuaderno es Andika, cargada con `fontspec` desde `fonts/andika/` —
ver preamble.tex) + `latexmk`, con `babel`, `tcolorbox`, `tikz` y
`fontspec` — cualquier TeX Live razonablemente completo los trae.

```sh
make              # genera, compila el cuaderno de frases (color), comprueba
make palabras     # lo mismo para el cuaderno de primeras palabras (color)
make all-formats  # los cuatro PDF: frases y palabras, color Y blanco-y-negro
make generate     # solo regenera los .tex de los dos cuadernos desde el JSON
make build        # solo compila frases en color (asume que ya está generado)
make build-bw     # solo compila frases en blanco y negro
make build-palabras / build-palabras-bw   # lo mismo, primeras palabras
make check        # lee main.log + 1 día = 1 página (lee main.aux) + valida el JSON
make check-bw     # lo mismo, sobre main-bw.log / main-bw.aux
make check-palabras / check-palabras-bw   # lo mismo, primeras palabras (+ silabeo)
make clean
```

## Estructura

```
main.tex, main-bw.tex                 -- cuaderno de frases, color y blanco-y-negro; solo fijan \bookcolor
palabras.tex, palabras-bw.tex         -- cuaderno de primeras palabras, color y blanco-y-negro
preamble.tex, lang/es.tex             -- el motor LaTeX (la paleta de main-bw.tex está en preamble.tex)
preamble-palabras.tex                 -- lo propio del cuaderno de primeras palabras (tarjetas, cajas que llenan la página)
body.tex, body-palabras.tex           -- orden del documento de cada cuaderno
frontmatter/                          -- portada, instrucciones, mapa del curso (frontmatter/palabras/: nivel 1)
content/q1.json, q2.json, q3.json, q4.json  -- los 260 días, uno por trimestre, editados a mano
content/generated-days.tex            -- GENERADO por tools/gen_days.py, no editar
content/progresion.json               -- objetivos semanales de la escalera de progresión (52 filas)
content/generated-clave.tex           -- GENERADO por tools/gen_days.py, no editar
content/letras-trazo.json             -- contorno real de cada letra (Andika), generado por tools/gen_letras_puntos.py
content/palabras-trazo.json           -- palabra de ejemplo de cada letra ("A de Abuela"), editado a mano
content/palabras/q1.json ... q4.json  -- los 260 días del cuaderno de primeras palabras, editados a mano
content/palabras/generated-*.tex      -- GENERADO por tools/gen_palabras.py, no editar
diagrams/                             -- dibujos de línea (TikZ) para las páginas "Completa"
backmatter/diploma.tex, clave-respuestas.tex -- diploma y clave de respuestas (backmatter/palabras/: nivel 1)
fonts/andika/                         -- letra del cuaderno (Andika, SIL, OFL -- ver "Licencia")
tools/gen_days.py                     -- JSON -> LaTeX + validación + medallas + clave de respuestas + trazo
tools/gen_palabras.py                 -- lo mismo para el cuaderno de primeras palabras, + la escalera de sílabas
tools/silabas.py                      -- silabeo automático del español y rasgos de cada sílaba (cerrada, trabada...)
tools/gen_letras_puntos.py            -- fuente -> contorno de cada letra (matplotlib/fonttools; no forma parte de `make`)
tools/check_pages.py                  -- comprueba que cada día ocupa una sola página
tools/checklog.py                     -- lee el .log de LuaLaTeX correctamente (nunca grep '^!')
tools/metricas.py                     -- mide palabras/frase/vocabulario nuevo contra content/progresion.json
docs/index.html                       -- la página que publica .github/workflows/pages.yml
assets/logo.tex, logo.png, logo.svg   -- logo del repositorio (standalone TikZ, reutiliza el icono de portada.tex)
LICENSE, LICENSE-CODE, LICENSE-CONTENT -- ver "Licencia" más abajo
CONTRIBUTING.md                       -- cómo colaborar (o hacer tu propio fork)
.github/workflows/build.yml           -- compila (color + blanco-y-negro) y valida en cada push/PR
.github/workflows/pages.yml           -- publica los dos PDF en GitHub Pages en cada push a main
notes/01-curriculum.md                -- el plan del curso completo
notes/02-revision-y-plan.md           -- revisión del cuaderno y plan de desarrollo del resto del año
notes/03-nivel-palabras.md            -- diseño del cuaderno de primeras palabras (nivel 1)
```

## Licencia

El motor -- LaTeX (`preamble*.tex`, `lang/es.tex`, `main*.tex`, `palabras*.tex`, `body*.tex`),
las herramientas Python (`tools/`), el `Makefile` y la configuración de CI
(`.github/`) -- está bajo MIT ([`LICENSE-CODE`](LICENSE-CODE)): reutilízalo
libremente, incluido un fork para otro niño o niña.

El contenido narrativo -- las frases, las palabras, los nombres y la
trama de `content/*.json` y `content/palabras/*.json`, y lo que se
genera de ahí a las páginas de los dos cuadernos --
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
