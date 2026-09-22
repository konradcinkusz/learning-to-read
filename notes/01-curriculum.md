# Programa del curso — "Aprendo a leer"

Ver también `notes/02-revision-y-plan.md`: la revisión del cuaderno ya
escrito y el plan de desarrollo del resto del año (qué mejorar, en qué
orden, y la escalera de progresión completa).

Este fichero describe el cuaderno de **frases** (nivel 2). El nivel
anterior, el cuaderno de **primeras palabras** (`palabras.tex`, mismos
temas semana a semana, una palabra al día en vez de una frase), tiene su
propio diseño en `notes/03-nivel-palabras.md`.

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
| 1 | 1–13 | 1–65 | 1 | septiembre–diciembre | Se presenta a la familia y el entorno cercano (casa, colegio, barrio); llega el otoño y el trimestre cierra con la Navidad (semana 13). Frases independientes. |
| 2 | 14–26 | 66–130 | 2 | diciembre–marzo | Abre con el frío de enero y el Carnaval (semana 16), sigue con la vuelta a la rutina y la llegada de la primavera (semana 25). Pequeñas escenas de dos frases; empiezan los conectores (`y`, `pero`, `porque`, `cuando`) y algún diálogo suelto. |
| 3 | 27–39 | 131–195 | 3 | marzo–junio | El Día del Libro (semana 29) y la Semana Santa (semana 30), y el fin del curso escolar cerrando el trimestre (oruga-mariposa, feria del libro, último día de colegio, semanas 37–39). Mini-historias de tres frases por semana, con principio y final. |
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

### Las 52 semanas

Un tema por semana: un personaje o escenario nuevo se presenta, se
explora durante la semana, y el viernes hay repaso/celebración cada dos
semanas (o relee/soltura, según el ciclo objetivo de más abajo). Del
Trimestre 3 en adelante las frases de una semana empiezan a encadenarse
como una mini-historia con principio y final, no solo frases sueltas
sobre el mismo tema.

**Trimestre 1** (semanas 1–13, días 1–65, septiembre–diciembre):
1. La familia de Lucía · 2. Toby, el perro juguetón · 3. El colegio de
Lucía · 4. El barrio y el parque · 5. La comida en casa · 6. Llega el
otoño · 7. Los juguetes de Dani · 8. Castañas y Todos los Santos ·
9. El cumpleaños de Lucía (cumple 7 años) · 10. Los animales del barrio
· 11. Un día de lluvia · 12. Ir al mercado con Mamá · 13. Nochebuena.

**Trimestre 2** (semanas 14–26, días 66–130, diciembre–marzo):
14. El frío de enero · 15. El cumpleaños de Papá · 16. El disfraz de
Carnaval · 17. El Día de la Paz · 18. Lucía se pone mala · 19. Un
domingo de manualidades con la abuela · 20. La biblioteca del barrio ·
21. El cumpleaños de Toby · 22. Un día de mucho viento · 23. El
proyecto de plantas de Marta · 24. Dani rompe el dinosaurio de Lucía ·
25. Huele a primavera · 26. Despedida del segundo trimestre.

**Trimestre 3** (semanas 27–39, días 131–195, marzo–junio):
27. Toby se pierde en el parque · 28. A Dani se le cae un diente ·
29. El Día del Libro · 30. Empieza la Semana Santa · 31. El huerto del
colegio · 32. Lucía aprende a montar en bici · 33. Lucía se apunta a
natación · 34. El día de la madre · 35. Dani ya reconoce casi todas las
letras · 36. Se acerca el fin de curso · 37. La oruga se convierte en
mariposa · 38. La feria del libro de fin de curso · 39. Último día de
colegio.

**Trimestre 4** (semanas 40–52, días 196–260, junio–septiembre):
40. Empieza el verano · 41. Llegada al pueblo de la abuela Rosa ·
42. Andrés, el vecino, y su gato Bigotes · 43. Un día en el río del
pueblo · 44. El huerto de la abuela · 45. Una tormenta de verano ·
46. La excursión a la playa · 47. La verbena del pueblo · 48. Dani se
hace amigo de Martín · 49. Vuelta a la ciudad · 50. Preparativos para
la vuelta al cole · 51. Dani practica para leer en voz alta · 52.
Vuelta al cole — Lucía empieza 2º, Dani empieza a leer solo, cierre de
la serie.

Las semanas 37–39 (oruga-mariposa, feria del libro, último día de
colegio) adaptan lo que en un primer borrador vivía al principio del
Trimestre 4 bajo el título "el último trimestre" — un resto del
calendario escolar antiguo, antes de que el Trimestre 4 pasara a ser
verano puro (ver `notes/02-revision-y-plan.md`, punto 1). El sitio
correcto de esa trama de fin de curso era aquí, cerrando el Trimestre
3, no abriendo el 4.

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

`tools/gen_days.py` sabe generar cinco tipos además de los del ciclo
original (`rodea`, `verdadero_falso`, `busca`, `ordena`, `relee` — este
último compone el texto de la semana solo, a partir de los días
anteriores con la misma `semana`, sin repetirlo en el JSON). Las
semanas 1–3 (T1) y 14–16 (T2) se quedaron con el ciclo original de
arriba, por ser las primeras que se escribieron; el resto del libro
(semana 4 en adelante) ya usa el ciclo objetivo: lunes *Dibuja*,
martes *Busca*/*Completa* alternando, miércoles *Rodea*/*Verdadero-Falso*
alternando en T1 o *Responde* desde T2, jueves *Relaciona*/*Adivina*
alternando, y viernes *Relee* (soltura) o *Repasa* (cada dos semanas,
con el banner de páginas leídas), alternando entre sí. `ordena` es el
único tipo que ningún día real usa todavía — encaja mejor con
historias de varios sucesos encadenados, del Trimestre 3 en adelante.

## Estructura técnica (resumen; ver el propio código para el detalle)

```
main.tex, main-bw.tex, preamble.tex, lang/es.tex   -- el motor LaTeX (pdflatex + babel[spanish])
body.tex                              -- portada + cómo-usar + mapa + días + diploma
content/q1.json, q2.json, ...         -- UN fichero por trimestre, editado a mano
content/generated-days.tex            -- GENERADO, no tocar a mano
tools/gen_days.py                     -- JSON -> LaTeX, valida antes de escribir
tools/check_pages.py                  -- después de compilar: 1 día = 1 página, exacto
diagrams/*.tex                        -- dibujos de línea en TikZ, para las páginas "Completa"
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

## Qué queda pendiente

Ver `notes/02-revision-y-plan.md` para la revisión completa del
cuaderno (qué mejorar y en qué orden) y el estado de cada etapa del
plan de desarrollo. Los 260 días están escritos; lo que queda es
mantenimiento e ilustración, no contenido nuevo:

1. ~~Escribir el Trimestre 1~~, ~~Trimestres 2, 3 y 4~~ — hecho: los
   260 días compilan como un cuaderno completo (`make all-formats`).
2. **Más ilustraciones** en `diagrams/` a medida que aparecen escenarios
   nuevos (el colegio, la playa, el cumpleaños...). Las de `completa`
   (`lineas-ondas`, `lineas-circulo`) son deliberadamente genéricas —
   unas pocas líneas sin forma — y sirven para cualquier día sin
   necesitar un dibujo nuevo cada vez.
3. ~~Automatizar el aviso de "palabra nueva"~~ — hecho: `tools/metricas.py`.
4. ~~CI (GitHub Actions) que compile el PDF en cada cambio~~ — hecho:
   `.github/workflows/build.yml` y `pages.yml`.

Durante el desarrollo, mientras cada trimestre se iba escribiendo,
existió un mecanismo aparte (`content/muestra/`, `tools/gen_muestra.py`,
`main-muestra.tex`) para tener una muestra de progresión sin romper la
continuidad 1..260 que exige el libro real. Se retiró en cuanto dejó de
hacer falta, tal como decía su propia cabecera: con los cuatro
trimestres completos, comparar el nivel de un trimestre a otro es tan
simple como abrir `main.pdf` por las páginas 1, 66, 131 y 196.
