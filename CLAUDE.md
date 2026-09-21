# CLAUDE.md — trabajar en este cuaderno

Contexto para seguir escribiendo *Aprendo a leer*. Léelo antes de tocar
nada — sobre todo la regla de la siguiente sección, que ya se rompió una
vez al principio de este proyecto y costó rehacer todo el enfoque.

---

## La regla que no se puede romper

**Las frases son siempre completas y gramaticalmente compuestas, desde el
día 1.** No hay ninguna letra "prohibida" ni ningún alfabeto que crezca
día a día. La niña para la que se escribe este cuaderno ya vive y
escolariza en español y **ya sabe decodificar** — este no es un método
silábico de cero (nada de "Mamá me ama" limitado a las letras vistas esa
semana). Un cuaderno así, escrito desde cero como si ella no supiera leer
nada, sería un error de partida; ya se escribió una vez por error y hubo
que descartarlo entero.

Lo que sube con el trimestre es:

1. **cuántas frases hay que leer cada día** — 1 → 2 → 3 → 4, una vez por
   trimestre (ver tabla abajo);
2. **la complejidad de la frase** — conectores (`y`, `pero`, `porque`,
   `cuando`), diálogo con comillas, historias más largas con
   planteamiento y final;
3. **el tipo de actividad** — de "dibuja/completa" sencillos a tareas de
   comprensión e invención más abiertas.

Lo que **nunca** sube es el alfabeto disponible. Si alguna vez te
encuentras escribiendo una frase pensando "¿puedo usar esta letra
todavía?", estás aplicando el modelo equivocado — para.

## El reparto

Un elenco fijo, para que cada semana sea un capítulo nuevo de la misma
historia y no frases sueltas sin relación:

| Personaje | Quién es |
|---|---|
| **Lucía** | protagonista, 6 años — la misma edad que la lectora real |
| **Dani** | su hermano pequeño, 4 años |
| **Toby** | el perro de la familia |
| **Mamá** y **Papá** | presentes pero de fondo |
| **Abuela Rosa** | abuela materna |

Los nombres se pueden cambiar sin tocar nada técnico — viven solo en
`content/q*.json`. Pero si los cambias, cámbialos en **todos** los días
ya escritos también: la consistencia del reparto es lo que hace que el
cuaderno se lea como una historia y no como ejercicios sueltos.

## Los cuatro trimestres

| Trimestre | Días | Frases/día | Arco narrativo |
|---|---|---|---|
| 1 | 1–65 | 1 | Frases independientes, un tema por semana (familia, colegio, barrio, estaciones) |
| 2 | 66–130 | 2 | Pequeñas escenas de dos frases; empiezan los conectores y algún diálogo suelto |
| 3 | 131–195 | 3 | Mini-historias de tres frases por semana, con planteamiento y final |
| 4 | 196–260 | 4 | Historias más largas, diálogo con comillas, final de curso |

**Escrito ahora mismo:** días 1–10 (Trimestre 1, semanas 1–2, completos
con actividad) en `content/q1.json`, más los 10 primeros días reales de
cada uno de los Trimestres 2–4 en `content/muestra/q{2,3,4}.json` (ver
"La muestra de progresión" abajo — es contenido real con su número de
día definitivo, no un borrador).

**Temas de las semanas 3–13 del Trimestre 1** (sin frases escritas
todavía, un tema por semana): el colegio de Lucía, el barrio y el
parque, la comida en casa, llega el otoño, los juguetes de Dani, un día
de lluvia, un cumpleaños, los animales del barrio, el mercado con Mamá,
un día en la playa o la montaña, repaso de fin de trimestre. El detalle
completo y el resto de "qué falta" está en `notes/01-curriculum.md`.

## Disciplina de vocabulario

No hay restricción de letras, pero sí una disciplina editorial al
escribir cada semana:

- No introducir más de 2–3 palabras genuinamente nuevas por día (los
  nombres propios del reparto no cuentan, se repiten constantemente).
- Reutilizar activamente el vocabulario de semanas anteriores.
- Evitar vocabulario muy raro o regional salvo que sea relevante para el
  tema de la semana.

Esto todavía no lo comprueba ningún script — es criterio editorial al
escribir, no una regla que `tools/gen_days.py --check` valide.

## Rotación de actividades

Ciclo de 5 días, repetido cada semana con contenido distinto:

| Día | Actividad | Qué comprueba |
|---|---|---|
| Lunes | **Dibuja** | Comprensión, vía dibujo libre de lo leído |
| Martes | **Completa** | Creatividad — unas pocas líneas sin forma que ella convierte en un dibujo. **Nunca** un dibujo ya cerrado para colorear dentro de los márgenes, eso no exige nada |
| Miércoles | **Copia** (T1) / **Responde** (T2 en adelante) | T1: copiar la frase tres veces, practica la letra, no exige componer una respuesta (a esta edad todavía no sabe). Desde T2: pregunta corta con respuesta objetiva |
| Jueves | **Relaciona** / **Adivina** | Vocabulario — emparejar palabras, o una adivinanza sencilla |
| Viernes | **Crea** | Tarea abierta; cada dos viernes es además **Repasa** (checklist + celebración) |

**`responde` está bloqueado en el Trimestre 1 por el propio generador**
(`TRIMESTRES_SIN_RESPONDE = {1}` en `tools/gen_days.py`) — no es solo
convención, `--check` falla si un día de T1 lo usa. No lo quites sin
saber por qué está ahí: a esta edad, en el primer trimestre, la niña
copia y practica trazo, no compone respuestas propias.

Los ocho tipos que el generador ya sabe producir: `dibuja`, `completa`,
`copia`, `responde`, `relaciona`, `adivina`, `crea`, `repasa`. Añadir más
días con estos tipos solo requiere JSON, no tocar el generador.

## Arquitectura técnica

```
main.tex, main-bw.tex                 -- color y blanco-y-negro; solo fijan \bookcolor
preamble.tex, lang/es.tex             -- el motor LaTeX (la paleta de main-bw.tex está aquí)
body.tex                              -- orden del documento
frontmatter/, backmatter/             -- portada, instrucciones, mapa del curso, diploma
content/q1.json                       -- días 1-10, EDITAR A MANO
content/generated-days.tex            -- GENERADO por tools/gen_days.py, NO editar
diagrams/                             -- dibujos de línea (TikZ) para "Completa"
tools/gen_days.py                     -- JSON -> LaTeX + validación (nº de frases/trimestre,
                                          campos de actividad, responde bloqueado en T1)
tools/check_pages.py                  -- 1 día = 1 página, exacto (lee \newlabel del .aux)
tools/checklog.py                     -- lee el .log de pdflatex correctamente
main-muestra.tex, tools/gen_muestra.py, content/muestra/  -- ver más abajo
assets/logo.tex, logo.png, logo.svg   -- logo (standalone TikZ)
notes/01-curriculum.md                -- el plan del curso completo y "qué queda pendiente"
```

Flujo para añadir contenido:

```sh
make generate       # content/q*.json -> content/generated-days.tex
make all-formats     # compila y valida color Y blanco-y-negro -- esto es lo que
                      # corre .github/workflows/build.yml en cada PR
```

Tres bramas duras, en este orden de barato a caro:

1. **`tools/gen_days.py --check`** — el JSON es válido (frases por
   trimestre, campos de actividad completos, `responde` no en T1) y
   coincide con lo ya generado. Segundos, solo Python.
2. **`tools/checklog.py main.log`** — nunca `grep '^!'`: con
   `-file-line-error` la línea de error empieza por una ruta, y
   `-interaction=nonstopmode` escribe igual un PDF encima del error, así
   que el código de salida y el propio PDF dicen "todo bien" aunque no lo
   esté. Falla también en `Overfull \hbox`/`Overfull \vbox`.
3. **`tools/check_pages.py main.aux`** — cada día ocupa exactamente una
   página. Es la única forma de saber si un día se ha desbordado a una
   segunda página sin mirar el PDF entero página por página.

## Trampas de LaTeX ya encontradas

- **`babel[spanish]` hace de `"` un carácter activo** (atajo para `<<` y
  `>>`), así que una comilla suelta en un diálogo (`"¡Sorpresa!"`)
  choca con él y se corrompe en silencio, peor justo antes de una
  mayúscula. Un `\shorthandoff{"}` normal en el preámbulo **no
  funciona y falla en silencio** — babel reactiva sus atajos para el
  idioma principal en `\begin{document}`, DESPUÉS de que el preámbulo ya
  ha corrido, así que gana babel. El arreglo real, ya aplicado en
  `preamble.tex`, es `\AtBeginDocument{\shorthandoff{"}}`, que aplaza el
  comando al punto justo después de eso. Verificado contra un fichero
  mínimo aparte antes de confiar en ello — si alguna vez tocas esta
  línea, vuelve a verificarlo igual, no de memoria.
- **Nunca leas un `.log` con `grep '^!'`** — ver arriba, usa siempre
  `tools/checklog.py`.
- **`content/generated-days.tex` y `content/generated-muestra.tex` no se
  commitean** (están en `.gitignore`) — se regeneran con `make generate`
  / `make generate-muestra`. Si un `git status` los muestra como nuevos
  sin más, algo ha ido mal con el `.gitignore`, no los añadas a mano.
- **`assets/logo.pdf` tampoco se commitea** — cae bajo la regla `*.pdf`
  del `.gitignore`, igual que `main.pdf`. Solo se commitean `logo.tex`
  (fuente) y los renderizados `logo.png`/`logo.svg`.

## La muestra de progresión

`content/muestra/q{2,3,4}.json` (`make muestra`, `main-muestra.tex`) no
es el cuaderno: son los 10 primeros días **reales** de cada trimestre
2–4, con su número de día, semana y trimestre definitivo, para ver de un
vistazo cómo sube el nivel. Viven fuera de `content/q{2,3,4}.json` a
propósito, porque el generador real exige continuidad 1..260 sin huecos
y estos bloques dejan huecos deliberados (semanas que aún no están
escritas). **Cuando escribas el resto de un trimestre, el fichero de
`content/muestra/` correspondiente se traslada tal cual a
`content/qN.json`** — no lo reescribas desde cero, ya está escrito y
revisado.

## Licencia

Doble: el motor (LaTeX, `tools/`, `Makefile`, CI) está bajo MIT
(`LICENSE-CODE`) — reutilizable libremente, incluido un fork para otro
niño o niña. El contenido narrativo (`content/*.json` y lo que genera)
está bajo Creative Commons Atribución-NoComercial-CompartirIgual 4.0
(`LICENSE-CONTENT`) — adaptable pero no comercial, y cualquier
adaptación se comparte bajo la misma licencia. Ver `LICENSE` para el
reparto exacto y `CONTRIBUTING.md` para qué tipo de colaboración encaja
en este repositorio (en corto: bugs del motor sí, frases o personajes
nuevos no — eso es decisión editorial del autor sobre su propia hija).

## Qué falta (ver `notes/01-curriculum.md` para el detalle completo)

1. Escribir las semanas 3–13 del Trimestre 1 (días 11–65).
2. Escribir el resto de los Trimestres 2, 3 y 4 (los primeros 10 días de
   cada uno ya están en `content/muestra/`, ver arriba).
3. Más ilustraciones en `diagrams/` a medida que aparecen escenarios
   nuevos — las de "Completa" son deliberadamente genéricas (líneas sin
   forma) y sirven para cualquier día sin necesitar un dibujo nuevo cada
   vez.
4. Automatizar el aviso de "palabra nueva" de la disciplina de
   vocabulario (hoy es solo criterio editorial).

## Al terminar una sesión de trabajo

1. `make all-formats` — cero errores, cero warnings de `checklog.py`, 1
   día = 1 página en las dos versiones.
2. `python3 tools/gen_days.py --check` en verde.
3. Si has escrito contenido nuevo: revisa a mano que las frases suenan
   naturales para una niña de 6 años que ya lee — no simplificadas, no
   "español de libro de texto".
4. Commit, push, PR — nunca a `main` directamente. Ver `CONTRIBUTING.md`
   para el flujo exacto.
