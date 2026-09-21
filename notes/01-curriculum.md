# Programa del curso — "Aprendo a leer"

Ver también `notes/02-revision-y-plan.md`: la revisión del cuaderno ya
escrito y el plan de desarrollo del resto del año (qué mejorar, en qué
orden, y la escalera de progresión completa).

## Punto de partida (y por qué cambió)

La primera versión de este cuaderno partía de un método silábico clásico
(una letra nueva por semana, frases restringidas a las letras ya vistas:
"Mamá me ama", etc.). Se corrigió porque no corresponde a la situación
real: la niña vive en España, habla español a diario y **ya ha dado esto
en el colegio** — decodifica sílabas y letras sin problema. Un cuaderno
de refuerzo para ella no puede empezar por "mamá me ama"; tiene que
empezar donde ella ya está.

**Regla del curso, a partir de ahora:** las frases son siempre
**completas y compuestas**, con vocabulario y gramática normales para su
edad — no hay ninguna restricción de qué letras "están permitidas" ese
día. Lo que sube con el curso no es qué letras se conocen, sino:

- cuántas frases hay que leer cada día (1 → 2 → 3 → 4, un salto por
  trimestre, ver la tabla de `frontmatter/mapa-del-curso.tex`);
- la complejidad de la frase (conectores, subordinadas, diálogo);
- el tipo de actividad, que pasa de "dibuja/colorea/responde" sencillos a
  tareas de comprensión e invención más abiertas.

## El reparto

Un elenco fijo de personajes, para que cada semana sea un capítulo nuevo
de la misma historia en vez de frases sueltas sin relación:

| Personaje | Quién es |
|---|---|
| **Lucía** | protagonista, 6 años — la misma edad que la lectora |
| **Dani** | su hermano pequeño, 4 años |
| **Toby** | el perro de la familia |
| **Mamá** y **Papá** | presentes pero de fondo |
| **Abuela Rosa** | abuela materna, aparece los domingos |
| *(por decidir)* | quizá un vecino/a con un gato, para más adelante |

Los nombres se pueden cambiar sin tocar la estructura del cuaderno —
están escritos directamente en `content/q*.json`, no hay ninguna
dependencia técnica de que se llame "Lucía".

## Los cuatro trimestres

Los cuatro trimestres del cuaderno son las cuatro estaciones del año —
**no** los tres trimestres del curso escolar español. El cuaderno se lee
también durante las vacaciones (Navidad, Semana Santa, verano): es
precisamente cuando más se agradece no perder el ritmo de lectura. Ver
`notes/02-revision-y-plan.md`, punto 1, para el razonamiento completo.

| Trimestre | Semanas | Días | Frases/día | Época | Qué pasa |
|---|---|---|---|---|---|
| 1 | 1–13 | 1–65 | 1 | septiembre–diciembre | Se presenta a la familia y el entorno cercano (casa, colegio, barrio); llega el otoño y el trimestre cierra con la Navidad (semana 13). Frases independientes. Ya escrito: semanas 1–3 (días 1–15). |
| 2 | 14–26 | 66–130 | 2 | diciembre–marzo | Abre con Nochebuena y Reyes (semanas 14–17), sigue con la nieve y el Carnaval. Pequeñas escenas de dos frases; empiezan los conectores (`y`, `pero`, `porque`, `cuando`) y algún diálogo suelto. |
| 3 | 27–39 | 131–195 | 3 | marzo–junio | Semana Santa, el Día del Libro (semanas 31–32), y el fin del curso escolar cerrando el trimestre (excursión final, feria del libro). Mini-historias de tres frases por semana, con principio y final. |
| 4 | 40–52 | 196–260 | 4 | junio–septiembre | Vacaciones de verano: el pueblo de la abuela Rosa, la playa, tormentas de verano. La última semana es la vuelta al cole, con Dani empezando a leer — cierre de la serie. Historias más largas, diálogo con raya. |

## Escalera de progresión

El número de frases por página (1 → 2 → 3 → 4) es la parte visible de
la progresión, pero no la única: dentro de cada trimestre, la longitud
de las frases, el vocabulario nuevo y el tipo de comprensión que se pide
también tienen que subir, semana a semana, no solo en el salto de
trimestre. Objetivos al final de cada trimestre (ver
`notes/02-revision-y-plan.md`, Parte C, para el detalle):

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

Esta tabla ya se comprueba automáticamente: `content/progresion.json`
tiene los 52 objetivos semanales (interpolados linealmente entre los
puntos de control de arriba) y `tools/metricas.py` mide cada día
escrito contra su semana -- `make check` y el job `gates` de CI fallan
si algún día supera `palabras_max` o `frase_max` (avisan, sin fallar,
si supera `nuevas_max`).

### Semanas ya escritas (Trimestre 1)

- **Semana 1 — "La familia de Lucía"** (días 1–5): se presentan Lucía,
  Dani, Toby y la abuela Rosa, uno por día.
- **Semana 2 — "Toby, el perro juguetón"** (días 6–10): una semana
  entera centrada en el perro, cerrando con una página de repaso.
- **Semana 3 — "El colegio de Lucía"** (días 11–15): se presenta el
  colegio, la profesora (Marta) y una amiga nueva (Sofía).

### Semanas siguientes del Trimestre 1 (esquema, sin frases escritas aún)

Un tema por semana, siguiendo el patrón de las tres primeras (un
personaje o escenario nuevo se presenta, se explora durante la semana, y
el viernes hay repaso/celebración cada dos semanas). Las semanas 4–13
caen entre finales de septiembre y diciembre (ver la tabla de arriba):
de ahí que la Navidad cierre el trimestre y no haya ninguna semana de
playa, que ya no encajaría en el calendario:

4. El barrio y el parque
5. La comida en casa (algo que le gusta, algo que no)
6. Llega el otoño (las hojas, el viento, la ropa de abrigo)
7. Los juguetes de Dani
8. Castañas y Todos los Santos
9. El cumpleaños de Lucía (cumple 7 años)
10. Los animales del barrio (el gato del vecino, los pájaros)
11. Un día de lluvia
12. Ir al mercado con Mamá — ya huele a Navidad
13. Nochebuena — repaso de fin de trimestre + puente hacia el Trimestre 2

Cada semana son 5 frases independientes (una por día) sobre el mismo
tema; no hace falta que se sigan unas a otras como una historia
continua todavía — eso empieza a tener más peso en el Trimestre 3.

## Vocabulario: crecimiento controlado, sin restricción de letras

No hay ninguna letra "prohibida", pero sí conviene seguir una disciplina
sencilla al escribir cada semana, para que el cuaderno construya
vocabulario de forma deliberada en vez de aleatoria:

- No introducir más de 2–3 palabras genuinamente nuevas por día (nombres
  propios del reparto no cuentan, se repiten constantemente).
- Reutilizar activamente el vocabulario de semanas anteriores en las
  frases nuevas, para que se consolide con la repetición.
- Evitar vocabulario muy raro o regional salvo que sea relevante para el
  tema de la semana.

Ya no es solo una disciplina editorial: `tools/metricas.py` cuenta los
lemas de contenido nuevos de cada día (sin lematización de verdad,
"simple" a propósito -- ver su cabecera) y avisa si se supera
`nuevas_max` de `content/progresion.json`, aunque no bloquea `make
check` -- ver `notes/02-revision-y-plan.md`, punto 6.

## Rotación de actividades

Un ciclo de 5 días, repetido cada semana con contenido distinto (visto
en los días 1–15):

| Día | Actividad | Qué comprueba |
|---|---|---|
| Lunes | **Dibuja** | Comprensión, vía dibujo libre de lo leído |
| Martes | **Completa** | Creatividad, no motricidad fina — unas pocas líneas sin forma, y ella inventa el dibujo a partir de ahí (nunca un dibujo ya cerrado para colorear dentro de los márgenes, eso no exige nada) |
| Miércoles | **Copia** (T1) / **Responde** (T2 en adelante) | T1: copiar la frase una vez — practica la letra, no exige componer una respuesta, que a esta edad todavía no sabe hacer sola. Desde T2: pregunta corta con respuesta objetiva, comprensión explícita |
| Jueves | **Relaciona** / **Adivina** | Vocabulario — emparejar palabras, o una adivinanza sencilla |
| Viernes | **Crea** | Tarea abierta; cada dos viernes es además **Repasa** (checklist + celebración) |

`tools/gen_days.py` ya sabe generar trece tipos de actividad: los ocho
de este ciclo (`dibuja`, `completa`, `copia`, `responde`, `relaciona`,
`adivina`, `crea`, `repasa`) y los cinco del ciclo objetivo de más
abajo (`rodea`, `verdadero_falso`, `busca`, `ordena`, `relee`); añadir
más días solo requiere añadir entradas al JSON, no tocar el generador,
salvo que se necesite un tipo de actividad genuinamente nuevo.
`responde` está bloqueado en el trimestre 1 por el propio validador
(`TRIMESTRES_SIN_RESPONDE`) — no es solo una convención editorial,
`tools/gen_days.py --check` falla si un día de T1 lo usa.

### Ciclo objetivo (el motor ya lo soporta — ver `notes/02-revision-y-plan.md`, punto 3)

El ciclo de arriba ejercita el dibujo mucho más que la lectura: dos de
cada cinco días (*Dibuja*, *Completa*) no exigen volver al texto ni una
vez. El ciclo pensado para sustituirlo:

| Día | Actividad | Qué entrena |
|---|---|---|
| Lunes | Lee y dibuja | comprensión vía dibujo, con una tarea dentro del texto |
| Martes | Busca / Completa (alternando) | nivel de palabra |
| Miércoles | Comprende (Rodea / Verdadero-Falso en T1, Responde desde T2) | comprensión, sin exigir escritura en T1 |
| Jueves | Relaciona / Adivina | vocabulario (sin cambios) |
| Viernes | Relee la semana + Crea; cada 2 semanas, Repasa | soltura — relee las frases de lunes a jueves compuestas como un texto |

`tools/gen_days.py` ya sabe generar los cinco tipos que le faltaban
(`rodea`, `verdadero_falso`, `busca`, `ordena`, `relee` — este último
compone el texto de la semana solo, a partir de los días anteriores
con la misma `semana`, sin repetirlo en el JSON) — la Etapa 2 del plan
de desarrollo los implementó y los probó con contenido de prueba, pero
**ningún día real usa ninguno todavía**: `content/q*.json` y
`content/muestra/` siguen con el ciclo de arriba porque escribir estos
días es trabajo de contenido (Etapa 3), no del motor. Al escribir una
semana nueva, ya se puede usar el ciclo objetivo directamente.

## Estructura técnica (resumen; ver el propio código para el detalle)

```
main.tex, main-bw.tex, preamble.tex, lang/es.tex   -- el motor LaTeX (pdflatex + babel[spanish])
body.tex                              -- portada + cómo-usar + mapa + días + diploma
content/q1.json, q2.json, ...         -- UN fichero por trimestre, editado a mano
content/generated-days.tex            -- GENERADO, no tocar a mano
tools/gen_days.py                     -- JSON -> LaTeX, valida antes de escribir
tools/check_pages.py                  -- después de compilar: 1 día = 1 página, exacto
diagrams/*.tex                        -- dibujos de línea en TikZ, para las páginas "Completa"
main-muestra.tex, tools/gen_muestra.py, content/muestra/  -- ver "La muestra de progresión" abajo
```

`tools/gen_days.py --check` falla si: los días no son consecutivos, un
día tiene un número de frases distinto al de su trimestre, una
actividad no tiene los campos que necesita, o el `.tex` generado no
coincide con lo que hay en el JSON (es decir, si alguien ha tocado
`content/generated-days.tex` a mano y luego cambia el JSON, el
desajuste se detecta).

`tools/check_pages.py` se ejecuta **después** de compilar
(`make build`) y lee las páginas reales del `.aux` — es la única forma
de saber si un día se ha desbordado a una segunda página sin mirar las
260 páginas del PDF una por una.

## La muestra de progresión

`main-muestra.tex` (`make muestra`) no es el cuaderno: son 60 páginas,
los 15 primeros días **reales** de cada trimestre uno detrás de otro
(1–15, 66–80, 131–145, 196–210), para ver de un vistazo cómo sube el
nivel — más frases, frases más largas, aparece el diálogo, cambia el
tipo de actividad de miércoles (`copia` en T1, `responde` desde T2).

Los tres bloques que no son T1 viven en `content/muestra/q{2,3,4}.json`,
**no** en `content/q{2,3,4}.json` — a propósito: el glob `q*.json` que
usa el libro real (`tools/gen_days.py`) exige continuidad 1..260 sin
huecos, y estos tres bloques dejan huecos deliberados (16–65, 81–130,
146–195) porque esas semanas todavía no están escritas. Es contenido
real, con su número de día, semana y trimestre definitivo — no un
borrador desechable — así que cuando se escriban las semanas que faltan
alrededor de cada bloque, el fichero correspondiente se traslada tal
cual a `content/qN.json` y no hay que rehacer nada.

`tools/check_pages.py --allow-gaps` es la misma comprobación de siempre
(el salto de página entre dos días seguidos tiene que ser exactamente
1) sin la parte que exige que los números de día sean consecutivos —
necesaria aquí porque los cuatro bloques, tomados juntos, tienen huecos
por diseño.

## Qué queda pendiente

Ver `notes/02-revision-y-plan.md` para la revisión completa del
cuaderno (qué mejorar y en qué orden) — esta lista es solo la de
contenido por escribir.

1. **Escribir las semanas 4–13 del Trimestre 1** (días 16–65) siguiendo
   el esquema de temas de arriba y la escalera de progresión.
2. **Escribir los Trimestres 2, 3 y 4** (`content/q2.json`, `q3.json`,
   `q4.json`) — cada uno con su propio arco narrativo más largo. **Las
   primeras 15 jornadas reales de cada uno ya están escritas**, en
   `content/muestra/q{2,3,4}.json` (ver arriba); lo que falta es el
   resto de cada trimestre y trasladar estos tres ficheros a su sitio
   definitivo cuando ese resto exista. La muestra de T4 todavía da por
   hecho un calendario que no cuadra (`notes/02-revision-y-plan.md`,
   punto 1) y hay que reescribirla como verano antes de darla por buena.
3. **Más ilustraciones** en `diagrams/` a medida que aparecen escenarios
   nuevos (el colegio, la playa, el cumpleaños...). Las de `completa`
   (`lineas-ondas`, `lineas-circulo`) son deliberadamente genéricas —
   unas pocas líneas sin forma — y sirven para cualquier día sin
   necesitar un dibujo nuevo cada vez.
4. ~~Automatizar el aviso de "palabra nueva"~~ — hecho: `tools/metricas.py`.
5. ~~CI (GitHub Actions) que compile el PDF en cada cambio~~ — hecho:
   `.github/workflows/build.yml` y `pages.yml`.
