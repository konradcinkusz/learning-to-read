# Aprendo a leer

Cuaderno diario de lectura en español, en A4, una página por día de
colegio (lunes a viernes, 260 días = un curso entero). Cada página
tiene un hueco para la fecha y una nota del adulto, la frase (o frases)
del día, y una actividad corta (dibujar, colorear, responder,
relacionar, adivinar o crear).

Pensado para una niña que ya vive y escolariza en español y está
consolidando la lectura, no para empezar desde cero: las frases son
completas desde el primer día, y lo que aumenta con el curso es cuántas
frases hay que leer (1 → 2 → 3 → 4, una vez por trimestre) y su
complejidad, no el alfabeto disponible.

Ver `notes/01-curriculum.md` para el plan completo del curso (reparto
de personajes, arco de cada trimestre, disciplina de vocabulario) y
para qué falta escribir todavía.

## Descargar el PDF sin instalar nada

- **Cada push a `main` lo compila** — pestaña *Actions* → workflow
  *Build* → artefacto `pdf` (se guarda 30 días, hace falta estar
  identificado en GitHub para descargarlo).
- **Enlace fijo, siempre la última versión** (una vez que alguien con
  permisos de administrador active Pages una sola vez — ver
  `.github/workflows/pages.yml`):
  `https://konradcinkusz.github.io/learning-to-read/aprendo-a-leer.pdf`

## Construir el PDF a mano

Necesita una distribución de TeX (pdflatex + latexmk) con `babel`,
`tcolorbox` y `tikz` — cualquier TeX Live razonablemente completo los
trae.

```sh
make            # genera content/generated-days.tex, compila, comprueba
make generate   # solo regenera content/generated-days.tex desde el JSON
make build      # solo compila (asume que ya está generado)
make check      # lee el log + 1 día = 1 página (lee main.aux) + valida el JSON
make clean
```

## Estructura

```
main.tex, preamble.tex, lang/es.tex   -- el motor LaTeX
body.tex                              -- orden del documento
frontmatter/                          -- portada, instrucciones, mapa del curso
content/q1.json                       -- días 1-10 escritos (Trimestre 1, semanas 1-2)
content/generated-days.tex            -- GENERADO por tools/gen_days.py, no editar
diagrams/                             -- dibujos de línea (TikZ) para las páginas "Colorea"
backmatter/diploma.tex                -- página final
tools/gen_days.py                     -- JSON -> LaTeX + validación
tools/check_pages.py                  -- comprueba que cada día ocupa una sola página
tools/checklog.py                     -- lee el .log de pdflatex correctamente (nunca grep '^!')
docs/index.html                       -- la página que publica .github/workflows/pages.yml
.github/workflows/build.yml           -- compila y valida en cada push/PR
.github/workflows/pages.yml           -- publica el PDF en GitHub Pages en cada push a main
notes/01-curriculum.md                -- el plan del curso completo
```

## Estado

Días 1–10 escritos y con sus actividades. El resto del Trimestre 1
(semanas 3–13) y los Trimestres 2–4 están esquematizados en
`notes/01-curriculum.md` pero sin frases escritas todavía.
