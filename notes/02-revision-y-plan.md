# Revisión del cuaderno y plan de desarrollo — "Aprendo a leer"

## Contexto y alcance

Esta nota recoge la revisión completa del cuaderno — lectura de las 60
páginas ya escritas (días 1–15, 66–80, 131–145, 196–210) y de todo el
motor — y el plan para desarrollarlo durante el resto del año: qué
falta, en qué orden, y con qué criterio se sabe que cada paso está
terminado. Es la continuación natural de `notes/01-curriculum.md`: ese
fichero dice qué se ha escrito y qué falta por escribir; este dice qué
cambiaría, y por qué, antes de seguir escribiendo.

Destinataria: una niña de 6 años que vive y escolariza en España, ya
decodifica sílabas y letras, y usa el cuaderno para consolidar la
lectura — no para aprender desde cero. El objetivo del año es que a los
260 días lea con más soltura de la que tenía el primer día; no es un
concurso de cuántas frases caben en una página.

Dos supuestos de partida, porque el resto del documento depende de
ellos y conviene tenerlos explícitos (y confirmarlos antes de dar por
buena esta revisión):

- **"Un año de vida" = un año natural**, 52 semanas, **incluidas las
  vacaciones**. No el curso escolar español (~175–180 días lectivos):
  con eso sobrarían semanas o faltarían páginas, y el verano — que es
  cuando más se pierde soltura lectora — se quedaría fuera del
  cuaderno.
- **"Cada día" = de lunes a viernes**, como hoy (260 páginas). Un
  cuaderno de fin de semana es una opción aparte, no la asumida aquí
  (ver el punto 7.4).

**Método**: la maquetación (punto 5) se evaluó sobre el PDF real de T1
(portada, instrucciones, mapa, días 1–15, diploma) convertido a imagen.
Las muestras de T2–T4 (`content/muestra/`) no se revisaron como PDF
renderizado, sino a partir del JSON y de las plantillas de
`tools/gen_days.py` — antes de dar por buenos sus problemas de
maquetación (frases centradas, diálogo con comillas, etc.) conviene
compilarlas con `make muestra` y mirarlas página a página.

**Estado (actualizado tras Etapas 0–3): las cuatro etapas de la Parte D
están hechas.** Calendario y documentación (Etapa 0), la herramienta de
métricas (Etapa 1), el motor de página (Etapa 2) y los 260 días de
contenido (Etapa 3) — el cuaderno completo compila (`make all-formats`
en verde: 1 día = 1 página, sin huecos, dentro de la escalera de
`content/progresion.json`, 0 errores). Hubo un cambio de alcance
respecto al plan original en la Etapa 1: al construir
`content/progresion.json` se descubrió que la escalera, tal como está
escrita en la Parte C, no la cumplía casi ninguno de los 60 días
publicados en ese momento (no solo los que el punto 2 señalaba). En vez
de recalibrar la escalera o dejar el aviso pendiente, se reescribieron
esos 60 días para que la cumplan tal cual está escrita; de paso se
aplicó el punto 10 completo (frases más cortas, diálogos con raya, el
`relaciona` del día 14, las frases "meta" de los días 66/75/196/210).
Los temas/calendario de T4 (punto 1) también se reescribieron como
verano real en la Etapa 3, y la trama de fin de curso escolar que antes
vivía ahí (feria del libro, oruga-mariposa) se trasladó a las semanas
37–39 de T3, que es donde encaja de verdad. El mecanismo de muestra de
progresión (`content/muestra/`, `tools/gen_muestra.py`,
`main-muestra.tex`) se retiró al terminar la Etapa 3, tal como decía su
propia cabecera: con los cuatro trimestres completos ya no hace falta
un artefacto aparte para comparar el nivel entre trimestres. Detalle
exacto de qué se hizo, en cada Etapa más abajo.

## Parte A — Qué ya funciona bien (no tocar)

- Frases completas desde el primer día, sin restringir el alfabeto: es
  la decisión correcta para una niña que ya decodifica. El lenguaje es
  natural, correcto, de España (*vosotros*, *merendar*, *piruleta*).
- El reparto fijo de personajes y el hilo de "Dani aprende a leer" (días
  69, 145, 197) ya es un eje narrativo listo para sostener el año
  entero.
- El motor — JSON a LaTeX, validación, el invariante "1 día = 1 página"
  comprobado contra el `.aux`, la versión en blanco y negro sin perder
  información, CI — es sólido. Lo de abajo son cambios de contenido y de
  reglas, no de arquitectura.
- Los hitos (el banner cada 10 días, el diploma) y la página "Cómo usar"
  para el adulto.

## Parte B — Lista de mejoras, por prioridad

### 1. El calendario del año no está definido, y el contenido da por supuestos tres calendarios distintos a la vez

**El problema.** 260 páginas = 52 semanas = un año natural. El curso
escolar español tiene unos 175–180 días lectivos. El README dice «260
días = un curso entero» — no es verdad en ninguna de las dos lecturas.
Las muestras ya escritas dan por hecho calendarios distintos según el
trimestre:

- T2 (día 66, "el frío de enero"; semana 16, Carnaval) y T3 (semana 29,
  "el 23 de abril") dan por hecho un **calendario escolar que se salta
  las vacaciones**.
- T4 (día 196, "último trimestre del curso"; feria del libro, excursión
  final, "pronto llegará el verano") da por hecho **junio** — y eso no
  cuadra en ninguna de las dos variantes: leyendo todos los días
  laborables sin saltos, T4 cae entre mediados de junio y principios de
  septiembre aproximadamente (casi todo vacaciones de verano); si en
  cambio se saltan las vacaciones, T4 cae en septiembre-diciembre del
  curso escolar **siguiente**.
- El plan de T1 no incluye ni la Navidad ni Reyes (6 de enero) — para
  una niña de 6 años en España son las fechas más importantes del año,
  y las vacaciones de Navidad son dos o tres semanas de lectura en casa,
  perfectas para este cuaderno.
- La semana 12 del plan de T1 ("un día en la playa o la montaña") cae en
  diciembre.

**La solución.** Fijar explícitamente: los 4 trimestres del cuaderno son
las 4 estaciones del año, y hay una página cada día laborable también
durante las vacaciones — el verano es cuando más soltura lectora se
pierde, así que el cuaderno tiene que cubrirlo, no saltárselo.

| Trimestre | Semanas | Época | Qué hay que incluir |
|---|---|---|---|
| T1 | 1–13 | septiembre–diciembre | empieza el colegio, llega el otoño, castañas/Todos los Santos, cumpleaños de Lucía (cumple 7 años), la Navidad cierra el trimestre (semana 13) |
| T2 | 14–26 | diciembre–marzo | Nochebuena, Reyes (semanas 16–17), nieve, Carnaval, empieza a notarse la primavera |
| T3 | 27–39 | marzo–junio | Semana Santa, el Día del Libro (semanas 31–32), a Toby se le pierde, a Dani se le cae un diente, **fin de curso escolar, excursión y feria del libro** (trasladados desde la muestra de T4) |
| T4 | 40–52 | junio–septiembre | vacaciones: el pueblo de la abuela Rosa, la playa, el gato del vecino, una tormenta de verano; última semana: la vuelta al cole — Lucía empieza 2º, Dani empieza a leer = final de la serie |

Ficheros a tocar: `README.md` (la frase sobre "curso entero"),
`frontmatter/mapa-del-curso.tex`, `frontmatter/como-usar.tex` (una
frase: "también en vacaciones"), `notes/01-curriculum.md` (los temas de
las semanas 4–13 y todo el plan de T2–T4), la muestra
`content/muestra/q4.json` (reescribirla para verano), la muestra
`content/muestra/q3.json` (se queda, pero recibe el fin de curso en las
semanas 37–39). En el texto para la niña, considerar "otoño / invierno /
primavera / verano" en vez de "Trimestre 1–4" — en España *trimestre* se
asocia a los tres trimestres del curso escolar, no a cuatro.

### 2. La progresión es escalonada y de una sola dimensión — solo crece el número de frases

Medido sobre los 60 días ya escritos:

| Trimestre | Palabras/página (media, mín–máx) | Palabras/frase (media) | Frase más larga | Palabras nuevas/día |
|---|---|---|---|---|
| T1 | 12 (9–15) | 12,1 | 15 | 7,2 |
| T2 | 26 (18–36) | 12,9 | 19 | 9,1 |
| T3 | 37 (33–42) | 12,2 | 15 | 9,1 |
| T4 | 52 (43–60) | 13,1 | 18 | 11,9 |

**Los problemas.**

- **La longitud de frase no crece**: del día 1 al día 210 la frase mide,
  de media, 12–13 palabras. T1 empieza con frases de 9–15 palabras (el
  día 13 tiene 15), que ya es largo para la primera semana de un
  cuaderno de repaso; T4 no es más difícil por frase, solo más largo. La
  única dificultad añadida es "más de lo mismo".
- **Dentro de un trimestre no crece nada durante 13 semanas**, y en la
  frontera el texto da un salto al doble (12 a 26 palabras de un día
  para otro). En 13 semanas una niña de 6 años progresa mucho; un
  trimestre plano aburre al final y agobia al principio del siguiente.
- **La progresión no es monótona**: los días 76 y 79 (T2, semana 16)
  tienen 36 palabras cada uno — más que cualquier día de la primera
  semana de T3 (33–35). La dispersión dentro de T2 (18–36) es mayor que
  el salto entre trimestres.
- El validador (`FRASES_POR_TRIMESTRE` en `tools/gen_days.py`) exige
  **exactamente** N frases, pero no mide la longitud. La regla que se
  comprueba no es la que decide la dificultad real.

**La solución.** Definir la escalera de progresión a nivel de
**semana**, en varias dimensiones, y comprobarla con una herramienta
(Parte C y Etapa 1). El número de frases por trimestre puede seguir
siendo la regla "visible" para la niña, pero el presupuesto de palabras
por página y la longitud máxima de frase tienen que crecer cada semana,
de forma suave, sin saltos ×2.

### 3. La rotación de actividades ejercita más el dibujo que la lectura

Reparto de los 60 días ya escritos: *dibuja* 12, *completa* 12, *crea* 8
→ **32/60 (53 %) es dibujar**; *responde* 9, *relaciona* 8, *adivina* 4,
*repasa* 4, *copia* 3. Dos de cada cinco días (*Dibuja*, *Completa*) no
exigen volver al texto ni una vez. El objetivo del cuaderno es soltura y
comprensión — y los únicos mecanismos que las entrenan son **releer** y
**preguntar sobre el texto**.

**La solución — nuevo ciclo semanal** (cada día sigue cabiendo en ≤ 10
minutos, tal y como promete "Cómo usar"):

| Día | Actividad | Qué entrena |
|---|---|---|
| lunes | Lee y dibuja | comprensión vía dibujo, pero con una tarea dentro del texto ("rodea la palabra que dice de qué color es la pelota") |
| martes | Busca / Completa (alternando) | nivel de palabra: rodear un nombre, contar palabras, encontrar una palabra con "rr", la palabra más larga |
| miércoles | Comprende | T1: **Rodea** (3 respuestas para rodear) o **Verdadero/Falso**, sin escribir; desde T2: Responde; desde T3: pregunta de causa ("¿por qué crees que...?"); T4: **Ordena** (ordenar 3 sucesos) y "¿qué pasará mañana?" |
| jueves | Relaciona / Adivina | vocabulario (sin cambios) |
| viernes | **Relee la semana** + Crea; cada 2 semanas, Repasa | soltura: las frases de lunes a jueves, impresas juntas como "el capítulo de la semana" (en T1, ≈ 60 palabras — un texto de verdad, y un puente natural hacia T2). El texto de la semana **sustituye** la actividad de dibujo del viernes, para que quepa en una página |

Cambios necesarios: nuevos tipos en `tools/gen_days.py` (`rodea`,
`verdadero_falso`, `busca`, `ordena`, `relee`), las macros
correspondientes en `preamble.tex`, las etiquetas en `lang/es.tex`, y la
descripción en `frontmatter/como-usar.tex`. El tipo `relee` compone el
texto a partir de los días anteriores de la semana automáticamente — no
hace falta repetirlo en el JSON.

### 4. La comprobación de comprensión empieza en T2 y sigue siendo literal

- T1 bloquea `responde` (`TRIMESTRES_SIN_RESPONDE`) con una razón válida
  — todavía no escribe respuestas — pero la comprensión se puede
  comprobar sin escribir (rodear, verdadero/falso, señalar en un
  dibujo). Hoy T1 no tiene **ninguna** comprobación de comprensión, solo
  la autoevaluación "Sé..." de *Repasa*.
- Las preguntas de T3/T4 son literales justo donde el texto pide
  inferencia: el día 209 termina con la mejor frase del libro ("se
  parece un poco a ella: primero costaba, y ahora vuela sola"), y la
  pregunta del día 208 es "¿De qué colores es la mariposa?".
- El `relaciona` del día 14 incluye "Dani — va a la clase de los
  pequeños", algo que ninguna frase ha dicho. Regla: solo se relaciona
  lo que ha aparecido en el texto (el validador puede comprobarlo si los
  pares remiten a palabras de la semana).

**La solución.** Escalera de preguntas: T1 literal sin escribir → T2
literal con respuesta corta escrita → T3 causa y orden de los sucesos →
T4 predicción, resumen en 1–2 frases, opinión.

### 5. Maquetación de página: varias cosas dificultan la lectura en vez de ayudar

- **El texto que la niña tiene que leer sola está en tamaño de adulto en
  todas partes salvo la frase del día.** En el PDF, la frase del día
  tiene 28 pt, pero la adivinanza (día 9) va en 14 pt **cursiva**, las
  palabras de *Relaciona* en 12 pt, y la checklist de *Repasa* y los
  enunciados en 11 pt. La adivinanza es, de hecho, un segundo texto que
  leer; la cursiva y los 11–14 pt son una barrera a los 6 años. Regla:
  todo lo que lee la niña (adivinanza, palabras, opciones para rodear,
  checklist) a ≥ 16–18 pt, sin cursiva; la instrucción para el adulto
  puede seguir siendo pequeña y gris, como hoy ("Une cada nombre...").
- **Cerca del 40 % de la página queda en blanco** en los días de
  *Copia*, *Relaciona* y *Adivina* (la caja de actividad termina a media
  página y el `\vfill` empuja el pie hacia abajo). La caja de lectura
  ocupa ~15 % de la página — en un cuaderno de lectura, "leer" es el
  elemento más pequeño. Ese espacio se puede usar para: el texto de la
  semana, una caja de "palabras nuevas", casillas de "Leído", o la
  liniatura de *Copia*.
- **Todas las frases van pegadas en un único párrafo centrado**
  (`" ".join` en `generar_tex`, `\centering` en `PLANTILLA_DIA`). En
  T3/T4 son 5–8 líneas centradas que empiezan cada una en un sitio
  distinto — el peor formato posible para quien empieza a leer. Arreglo:
  desde T2, cada frase en su propia línea, alineado a la izquierda; el
  diálogo en línea aparte; T1 puede seguir centrado (una sola frase).
- **No hay ningún bloqueo de partición de palabras**; en cuanto se pase
  a alineado a la izquierda aparecerá ("en-canta"). Añadir
  `\hyphenpenalty=10000` dentro de `cajaLectura`.
- **El diálogo usa comillas rectas `"..."`** (días 73, 78, 143, 196...).
  Los libros infantiles en español usan **raya** (—¡Sorpresa! —grita
  toda la familia.) o «». La comilla recta es un artefacto de máquina de
  escribir — y fue la que provocó el error con `babel` documentado en
  `preamble.tex`. En el generador: una línea que empieza por "—" pasa a
  ser un párrafo aparte con sangría francesa.
- **Hay una sola instrucción de lectura para las 260 páginas**: "Lee en
  voz alta, despacio, señalando cada palabra" (`\lblInstruccionLectura`).
  En T4, "despacio, señalando cada palabra" es justo lo contrario de lo
  que se espera de quien ya lee con soltura. Que dependa del trimestre:
  T1 señala con el dedo; T2 léelo dos veces; T3 lee "con la voz del
  personaje"; T4 primero en silencio, luego en voz alta.
- **`Copia` es físicamente imposible de hacer**: `PLANTILLA_COPIA` da
  tres líneas cada 13 mm para **tres** copias de una frase de 10–15
  palabras. La propia frase a 28 pt ya ocupa 2–3 líneas impresas; la
  letra de una niña de 6 años es más grande todavía. Hacen falta unas 9
  líneas, no 3. Arreglo: una sola copia, con liniatura escolar (pauta
  doble de 5 mm o cuadrícula); desde T2, "copia tu frase favorita de la
  semana".
- **El tema de la semana no se imprime** — el campo `tema` del JSON no
  llega a `PLANTILLA_DIA`. La niña ve "Día 12 (Semana 3 · Trimestre 1)"
  pero no "El colegio de Lucía". Añadirlo como subtítulo; ayuda a
  anticipar de qué va el texto.
- **La tipografía**: Latin Modern Sans tiene una "a" de doble piso, y la
  "I" mayúscula y la "l" minúscula son casi idénticas. Para quien
  empieza a leer va mejor una fuente con "a"/"g" de un solo piso
  (Andika, ABeeZee — ambas OFL). Exige LuaLaTeX + `fontspec` y subir la
  fuente al repositorio (`fonts/`); la acción de CI ya admite
  `latexmk_use_lualatex`. Decisión aparte, prioridad media.
- El campo "Notas: ____ 55 mm" no sirve como diario de progreso.
  Cambiarlo por tres casillas "Leído: ☐ sola ☐ con ayuda ☐ con
  dificultad" + una línea corta — al cabo del año queda un registro de
  progreso sin ningún esfuerzo extra.

### 6. La disciplina de vocabulario solo existe sobre el papel

Las notas dicen "máximo 2–3 palabras nuevas al día". Medido (días 1–15,
seguidos): 4–12 formas nuevas por día, media 7 (contadas sin lematizar,
así que el número real es algo menor, pero no un tercio) — nadie lo
comprueba porque no hay herramienta para ello (los propios autores de la
nota ya lo preveían, punto 4 de "Qué queda pendiente" en
`notes/01-curriculum.md`).

**La solución.** `tools/metricas.py` (Etapa 1): lista de palabras
funcionales, lematización simple (género/número, y si hace falta un
`content/familias.json` a mano), conteo de lemas de contenido nuevos por
día y por semana, aviso al superar el umbral de `content/progresion.json`.
Más "palabras nuevas de la semana" el lunes (donde se presentan), que el
resto de la semana repite.

### 7. Motivación, medición del progreso y flexibilidad en 260 días

- **7.1 No hay medición de soltura.** Cada 4 semanas, una página "¿Cómo
  leo?": un texto fijo de ~60 palabras, y el adulto apunta el tiempo y
  el número de tropiezos. Es la única forma objetiva de saber si el
  ritmo del cuaderno es el adecuado.
- **7.2 No hay regla para ajustar el ritmo.** Añadir en "Cómo usar": si
  durante una semana lee la página sin fallos a la primera, se puede
  leer más de una página al día; si se atasca en casi cada palabra, que
  lea solo la primera frase y el resto lo lea un adulto. Sin esto, una
  única progresión fija solo le sirve a la niña "media".
- **7.3 Progreso visible.** Una página de "mapa de progreso" al
  principio: 52 casillas para colorear cada viernes (un camino de la
  casa de Lucía al colegio, o a través de las estaciones). El banner
  cada 10 días se queda igual.
- **7.4 Fines de semana (opcional).** Si "cada día" tuviera que
  significar 7 días: una página ligera de fin de semana ("sábado: lee un
  libro de verdad con un adulto y dibújalo"; "domingo: la página de la
  abuela Rosa"). Exige cambiar 260 → 364 en el validador, en el pie de
  página (`/ 260` en `preamble.tex`) y en el diploma. Por defecto: no.
- **7.5 Ganchos narrativos.** Las muestras de T3/T4 ya lo hacen; fijarlo
  como regla desde T3: el jueves termina en suspense, el viernes lo
  resuelve.

### 8. La guía para el adulto se queda corta para un año de trabajo

Añadir a `frontmatter/como-usar.tex` media página por trimestre: qué
esperar, cómo ayudar (lectura en eco en T1, lectura coral, "dile la
palabra a los 3 segundos, no corrijas cada error"), cuándo acelerar o
frenar (ver 7.2), y qué hacer con *Copia* y *Responde* cuando no quiere
escribir.

### 9. Herramientas y CI — detalles menores pero concretos

- `check-muestra` no está en CI (`.github/workflows/build.yml` solo
  ejecuta `gen_days.py --check` en el job `gates`); los 45 días de
  muestra se pueden romper en silencio — y de hecho fue en la muestra
  donde apareció el error de las comillas. Añadirlo al job `gates`.
- `260` está fijado a mano en `preamble.tex` (el pie de página) y en
  `backmatter/diploma.tex`; sacarlo a `lang/es.tex`/`preamble.tex` como
  `\totaldias`, alimentado por la misma constante que `TOTAL_DIAS` en
  Python.
- `gen_muestra.validar_dia` duplica las reglas de
  `gen_days.validar_dias` sin el bloqueo de `responde` en T1 — separar
  una función común de validación de un solo día.
- El resumen de CI (`GITHUB_STEP_SUMMARY`) podría imprimir la tabla de
  métricas de la Etapa 1 — así cada PR con contenido nuevo enseña si
  mantiene la escalera.

### 10. Detalles en los 60 días ya escritos

- Acortar las frases más largas de T1 (días 4, 9, 13, 14, 15: 13–15
  palabras) a 8–11 palabras — son las tres primeras semanas.
- Días 76, 77, 79 (T2, semana 16): 29–36 palabras; recortarlas a ~24,
  para que la semana 16 no sea más difícil que T3.
- Día 14, `relaciona`: el par sobre Dani no viene del texto —
  sustituirlo por algo que sí (p. ej. "Lucía — cuelga el abrigo").
- Las frases "meta" sobre el propio cuaderno (día 66, "El segundo
  trimestre empieza..."; 75; 196) son simpáticas, pero atan la trama a
  la numeración; tras el cambio de calendario del punto 1, reescribirlas
  en clave de estación.
- Diálogos (días 73, 78, 143, 196, 198, 202, 204, 206, 208) → raya
  (punto 5).

## Parte C — Escalera de progresión propuesta (especificación de `content/progresion.json`)

Valores objetivo **al final** de cada trimestre; dentro de un trimestre
crecen de forma lineal, semana a semana.

| Dimensión | inicio T1 | final T1 | final T2 | final T3 | final T4 |
|---|---|---|---|---|---|
| frases/página | 1 | 1 (viernes: texto de la semana ≈ 50 palabras) | 2 | 3 | 4 |
| palabras/página (lun–jue) | 6–8 | 10–12 | 22–26 | 36–42 | 55–70 |
| máx. palabras en una frase | 8 | 11 | 13 | 14 | 16 |
| lemas de contenido nuevos/día | ≤ 3 | ≤ 3 | ≤ 3 | ≤ 4 | ≤ 4 |
| sintaxis | frases simples + "y" | "porque", "cuando" | diálogo (raya), preguntas en el texto | subordinadas, "aunque", "mientras" | estilo indirecto, pretérito perfecto compuesto |
| géneros | narración | + nota/lista (lista de la compra) | + diálogo | + "¿Sabías que...?", receta | + poema/rima, carta, cómic (bocadillos) |
| comprensión | rodea / V-F | rodea / V-F | responde literal | "¿por qué...?", ordena | predicción, resumen, opinión |
| soltura | viernes: texto de la semana | viernes: texto de la semana | + medición cada 4 semanas | lectura con expresión | primero en silencio |
| escritura | Copia ×1 con liniatura | Copia ×1 | respuesta corta | 1 frase propia | 2 frases propias |

## Parte D — Orden de implementación

### Etapa 0 — documentación ✅ hecho

1. Este documento: Parte B, Parte C y el calendario del punto 1.
2. `notes/01-curriculum.md`: sustituir la tabla de trimestres y los
   temas de las semanas 4–13 por la versión estacional; añadir la tabla
   de la Parte C y el nuevo ciclo semanal del punto 3.
3. `README.md`: corregir «260 días = un curso entero» → un año natural
   con vacaciones; la sección "Estado" señala a este documento.
4. `frontmatter/mapa-del-curso.tex` y `frontmatter/como-usar.tex`:
   estaciones, frase sobre las vacaciones, regla 7.2.

### Etapa 1 — medir la progresión ✅ hecho, con un hallazgo que cambió el alcance

- `content/progresion.json`: 52 filas con los objetivos de la Parte C
  (generadas con una fórmula lineal por tramos entre los puntos de
  control de esa tabla, corregibles a mano).
- `tools/metricas.py`: métricas por día/semana (palabras/página, frase
  más larga, lemas de contenido nuevos), comparación con los objetivos;
  error si se supera `palabras_max`/`frase_max`, aviso si se supera
  `palabras_min` o `nuevas_max`. Modo `--tabla` para el resumen de CI.
- `Makefile` `check` + el job `gates` de `build.yml`: ejecutan las
  métricas, `gen_muestra.py --check` (antes no estaba en CI, punto 9) y
  publican la tabla en `GITHUB_STEP_SUMMARY`.
- **Hallazgo, antes de cerrar la Etapa**: al medir los 60 días
  contra la escalera tal como está escrita en la Parte C, la superaban
  no solo los días 76/77/79 (los que el punto 2 señalaba) sino
  **prácticamente los 60** — incluido el día 1 (9 palabras contra un
  objetivo de 8). Ante eso se preguntó cómo resolverlo (recalibrar la
  escalera / dejarla como aviso sin bloquear / reescribir los 60 días
  ya publicados) y se eligió **reescribir los 60 días** para que
  cumplan la escalera tal cual está escrita — esto adelanta aquí la
  parte del punto 10 y de la Etapa 3 que consistía en acortar frases y
  pasar los diálogos a raya (ver más abajo). Con eso, `tools/metricas.py`
  da 0 errores (`palabras_max`/`frase_max`) sobre los 60 días; quedan
  avisos de `nuevas_max` en la mayoría (43/60) — esperado y documentado
  en el punto 6, no bloquea `make check`.

### Etapa 2 — el motor de página ✅ hecho (`tools/gen_days.py`, `preamble.tex`, `lang/es.tex`)

- Imprimir `tema`; frases en líneas separadas desde T2, `\raggedright`,
  bloqueo de partición de palabras (`\hyphenpenalty=10000` dentro de
  `cajaLectura`); raya para el diálogo (con sangría francesa si envuelve
  a una segunda línea).
- Instrucción de lectura según el trimestre (`\lblInstruccionLecturaUno`
  a `Cuatro` en `lang/es.tex`); casillas "Leído: ☐ sola ☐ con ayuda ☐
  con dificultad" en la cabecera de `diapagina` (con `Notas` más corto,
  en la misma línea para no perder media página); `\totaldias` (una
  sola fuente de verdad, en `lang/es.tex`, usada por `preamble.tex` y
  `backmatter/diploma.tex`).
  Nota de implementación: `\begin{cajaLectura}[title=...]` (la sintaxis
  "de toda la vida" de tcolorbox para sobreescribir una opción) **no
  funciona** si el `\newtcolorbox` no declara un número de argumentos —
  el texto `[title=...]` aparece literalmente dentro de la caja en vez
  de fijar el título. Arreglo: declarar el título como argumento
  obligatorio (`\newtcolorbox{cajaLectura}[1]{...,title=#1,...}`) y
  pasarlo con `\begin{cajaLectura}{...}`.
- *Copia*: una sola copia (antes de esta Etapa pedía tres, que no
  cabían — punto 5). La liniatura sigue siendo una simple `\rule`, no
  la pauta doble/cuadrícula que proponía el punto 5 — pendiente, no
  bloqueante.
- Nuevos tipos `rodea`, `verdadero_falso`, `busca`, `ordena`, `relee`
  (con `relee` componiendo el texto de la semana automáticamente a
  partir de los días anteriores con el mismo `trimestre`+`semana`, sin
  tener que repetirlo en el JSON) — probados con un día de prueba de
  cada tipo (no forma parte del contenido real, `content/q*.json` no
  usa ninguno todavía; eso es la Etapa 3).
- Validador: `TRIMESTRES_SIN_RESPONDE` se queda, T1 admite
  `rodea`/`verdadero_falso`; `relee` sin ningún día anterior de su
  semana falla con un mensaje claro en vez de generar una página vacía.
  De paso, se separó `validar_dia` (un solo día) de `validar_dias` (la
  continuidad 1..260 del libro real) y `tools/gen_muestra.py` importa
  la misma función en vez de duplicarla (arregla el punto 9).
  "Comprobar que `relee` cabe en una página en T4" queda para cuando la
  Etapa 3 escriba el primer viernes de T4 con contenido real — la
  comprobación (`tools/check_pages.py`) ya es genérica, no necesita
  cambios, solo hace falta contenido real que la ejercite.
- Decisión aparte, sin tocar: LuaLaTeX + tipografía para primeros
  lectores (Andika/ABeeZee) — sigue pendiente.
- Sin tocar, fuera del alcance de esta Etapa (punto 5, pero no listado
  en los bullets de la Etapa 2): el tamaño de letra de lo que lee la
  niña en `relaciona`/`adivina`/`repasa` (sigue en 11–14 pt) y el ~40 %
  de página en blanco en los días de `relaciona`/`adivina`.

### Etapa 3 — contenido ✅ hecho

- ~~Acortar las frases del punto 10; diálogos con raya~~ — **hecho**,
  como parte del hallazgo de la Etapa 1 (ver arriba): los 60 días que
  ya estaban publicados al empezar la Etapa 3 cumplen la escalera y
  usan raya en los diálogos; el `relaciona` sin apoyo textual del día
  14 y las frases "meta" de los días 66/75/196/210 también se
  corrigieron.
- ~~Trasladar el fin de curso escolar de `content/muestra/q4.json` a
  las semanas 37–39; reescribir T4 como verano + final con Dani~~ —
  **hecho**: T4 (semanas 40–52) es verano real de principio a fin — el
  pueblo de la abuela Rosa, el río, una tormenta de verano, la playa en
  familia, el vecino Andrés y su gato Bigotes, y cierra con la vuelta
  al cole (Lucía empieza 2º, Dani empieza a leer solo). La trama de fin
  de curso escolar que antes vivía al principio de T4 (feria del libro,
  la oruga que se hace mariposa) se adaptó, con frases de tres en vez
  de cuatro, a las semanas 37–39 de T3, que es donde encaja con el
  calendario real.
- ~~Escribir las semanas 4–13 de T1, y el resto de T2, T3 y T4~~ —
  **hecho**: los 200 días que faltaban (16–65, 81–130, 146–195,
  196–260) están escritos, siguiendo el ciclo objetivo del punto 3
  (`busca`/`rodea`/`verdadero_falso`/`relee` desde la primera semana
  nueva de cada trimestre) y dentro de la escalera de
  `content/progresion.json`.
- **Hallazgo no previsto en el plan**: `relee` (Etapa 2) componía
  *todas* las frases de lunes a jueves de la semana, no solo una por
  día. Eso no se nota en T1 (1 frase/día = 4 frases compuestas), pero
  en T2 (2/día = 8 frases) ya desbordaba a una segunda página, y en T3
  (3/día = 12) y T4 (4/día = 16) habría sido imposible de encajar en la
  misma caja que la actividad, con cualquier tamaño de letra razonable.
  Arreglado componiendo solo la primera frase de cada día
  (`tools/gen_days.py`, `texto_semana`) — en T1 no cambia nada (ya era
  la única frase del día), y en el resto mantiene el texto compuesto
  siempre en torno a 4 frases, del mismo orden que ya funcionaba en T1.
- **Retirada la muestra de progresión** (`content/muestra/`,
  `tools/gen_muestra.py`, `main-muestra.tex`) una vez trasladado su
  contenido a `content/q2.json`, `q3.json` y `q4.json`: su propia
  cabecera decía que dejaría de hacer falta en este momento exacto, y
  mantenerla habría significado dos copias del mismo contenido
  divergiendo con el tiempo.

## Verificación

- **Etapa 0**: `make generate && python3 tools/gen_days.py --check` sin
  cambios en el resultado (solo hay documentación); revisión visual del
  Markdown. — Hecho, PR fusionado.
- **Etapa 1**: `python3 tools/metricas.py --tabla` sobre los 60 días
  publicados en ese momento **mostró** los problemas de los puntos 2 y
  6 antes de tocar nada (prácticamente los 60 días por encima del
  presupuesto, no solo 76/77/79) — eso fue la prueba de que la
  herramienta funciona; tras reescribirlos, la tabla quedó con 0
  errores. — Hecho, PR fusionado.
- **Etapa 2**: `make all-formats` en verde (checklog, check_pages,
  `--check`); los cinco tipos nuevos y `relee` probados con un
  documento de prueba aparte que compiló sin errores ni `Overfull` y se
  revisó página a página. — Hecho, PR fusionado.
- **Etapa 3**: `make all-formats` en verde sobre los 260 días —
  `checklog.py` sin errores ni `Overfull`, `check_pages.py` confirma
  que los 260 días ocupan exactamente una página cada uno, `gen_days.py
  --check` confirma que el `.tex` generado coincide con el JSON, y
  `metricas.py` da 0 errores (palabras/página y frase más larga dentro
  de la escalera en los 260 días; solo avisos de `nuevas_max` y de
  `palabras_min` en días concretos, ambos por diseño no bloqueantes).
  Revisión visual de una muestra de páginas de cada trimestre
  (incluidas varias `relee`, que fueron las que más iteración de
  maquetación necesitaron) convertidas a imagen. Confirmado localmente
  porque este entorno no tenía TeX instalado al empezar y se instaló
  para poder verificar en vez de adivinar.
