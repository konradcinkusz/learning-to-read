# Aprendo a leer

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
make clean
```

## Estructura

```
main.tex, main-bw.tex                 -- color y blanco-y-negro; solo fijan \bookcolor y comparten todo lo demás
preamble.tex, lang/es.tex             -- el motor LaTeX (la paleta de main-bw.tex está en preamble.tex)
body.tex                              -- orden del documento
frontmatter/                          -- portada, instrucciones, mapa del curso
content/q1.json                       -- días 1-10 escritos (Trimestre 1, semanas 1-2)
content/generated-days.tex            -- GENERADO por tools/gen_days.py, no editar
diagrams/                             -- dibujos de línea (TikZ) para las páginas "Completa"
backmatter/diploma.tex                -- página final
tools/gen_days.py                     -- JSON -> LaTeX + validación
tools/check_pages.py                  -- comprueba que cada día ocupa una sola página
tools/checklog.py                     -- lee el .log de pdflatex correctamente (nunca grep '^!')
docs/index.html                       -- la página que publica .github/workflows/pages.yml
.github/workflows/build.yml           -- compila (color + blanco-y-negro) y valida en cada push/PR
.github/workflows/pages.yml           -- publica los dos PDF en GitHub Pages en cada push a main
notes/01-curriculum.md                -- el plan del curso completo
```

## Estado

Días 1–10 escritos y con sus actividades. El resto del Trimestre 1
(semanas 3–13) y los Trimestres 2–4 están esquematizados en
`notes/01-curriculum.md` pero sin frases escritas todavía.
