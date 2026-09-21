<p align="center"><img src="assets/logo.png" width="140" alt="Aprendo a leer"></p>

# Aprendo a leer

[![Build](https://github.com/konradcinkusz/learning-to-read/actions/workflows/build.yml/badge.svg)](https://github.com/konradcinkusz/learning-to-read/actions/workflows/build.yml)
[![Licencia](https://img.shields.io/github/license/konradcinkusz/learning-to-read)](LICENSE)
[![Hecho con](https://img.shields.io/badge/hecho%20con-LaTeX-2E7D32)](preamble.tex)

Cuaderno diario de lectura en español, en A4, una página por día de
colegio (lunes a viernes, 260 días = un curso entero). Cada página
tiene un hueco para la fecha y una nota del adulto, la frase (o frases)
del día, y una actividad corta (dibujar, completar unas líneas sueltas,
copiar la frase, responder, relacionar, adivinar o crear).

Pensado para una niña que ya vive y escolariza en español y está
consolidando la lectura, no para empezar desde cero: las frases son
completas desde el primer día, y lo que aumenta con el curso es cuántas
frases hay que leer (1 → 2 → 3 → 4, una vez por trimestre) y su
complejidad, no el alfabeto disponible.

Ver `notes/01-curriculum.md` para el plan completo del curso (reparto
de personajes, arco de cada trimestre, disciplina de vocabulario) y
para qué falta escribir todavía.

## Descargar el PDF sin instalar nada

**[⬇ Descargar el PDF (color)](https://konradcinkusz.github.io/learning-to-read/aprendo-a-leer.pdf)**
· **[⬇ Descargar el PDF (blanco y negro)](https://konradcinkusz.github.io/learning-to-read/aprendo-a-leer-bn.pdf)**

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
→ el último run de *Build* → artefactos `pdf-color` / `pdf-bw` (se
guardan 30 días, hace falta estar identificado en GitHub para
descargarlos).

## Construir el PDF a mano

Necesita una distribución de TeX (pdflatex + latexmk) con `babel`,
`tcolorbox` y `tikz` — cualquier TeX Live razonablemente completo los
trae.

```sh
make              # genera content/generated-days.tex, compila (color), comprueba
make all-formats  # lo mismo, pero compila y comprueba color Y blanco-y-negro
make generate     # solo regenera content/generated-days.tex desde el JSON
make build        # solo compila la versión en color (asume que ya está generado)
make build-bw     # solo compila la versión en blanco y negro
make check        # lee main.log + 1 día = 1 página (lee main.aux) + valida el JSON
make check-bw     # lo mismo, sobre main-bw.log / main-bw.aux
make muestra      # 60 páginas -- los 15 primeros días reales de cada trimestre, para
                  # comparar el nivel; NO es el cuaderno, ver notes/01-curriculum.md
make clean
```

## Estructura

```
main.tex, main-bw.tex                 -- color y blanco-y-negro; solo fijan \bookcolor y comparten todo lo demás
preamble.tex, lang/es.tex             -- el motor LaTeX (la paleta de main-bw.tex está en preamble.tex)
body.tex                              -- orden del documento
frontmatter/                          -- portada, instrucciones, mapa del curso
content/q1.json                       -- días 1-15 escritos (Trimestre 1, semanas 1-3)
content/generated-days.tex            -- GENERADO por tools/gen_days.py, no editar
diagrams/                             -- dibujos de línea (TikZ) para las páginas "Completa"
backmatter/diploma.tex                -- página final
tools/gen_days.py                     -- JSON -> LaTeX + validación
tools/check_pages.py                  -- comprueba que cada día ocupa una sola página
tools/checklog.py                     -- lee el .log de pdflatex correctamente (nunca grep '^!')
main-muestra.tex, tools/gen_muestra.py, content/muestra/  -- muestra de progresión, no el libro (ver notes/01-curriculum.md)
docs/index.html                       -- la página que publica .github/workflows/pages.yml
assets/logo.tex, logo.png, logo.svg   -- logo del repositorio (standalone TikZ, reutiliza el icono de portada.tex)
LICENSE, LICENSE-CODE, LICENSE-CONTENT -- ver "Licencia" más abajo
CONTRIBUTING.md                       -- cómo colaborar (o hacer tu propio fork)
.github/workflows/build.yml           -- compila (color + blanco-y-negro) y valida en cada push/PR
.github/workflows/pages.yml           -- publica los dos PDF en GitHub Pages en cada push a main
notes/01-curriculum.md                -- el plan del curso completo
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

Ver [`LICENSE`](LICENSE) para el reparto exacto de qué cae en cada lado, y
[`CONTRIBUTING.md`](CONTRIBUTING.md) para qué tipo de colaboración encaja
aquí.

## Estado

Días 1–15 (Trimestre 1) escritos y con sus actividades -- son los que
publica el cuaderno real. Los 15 primeros días reales de cada uno de
los Trimestres 2, 3 y 4 también están escritos, como muestra de
progresión (`content/muestra/`, `make muestra`) -- no forman parte
todavía del cuaderno real porque las semanas que faltan entre medias no
están escritas. El resto está esquematizado en `notes/01-curriculum.md`.
