# Programa del curso — "Aprendo a leer"

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

| Trimestre | Días | Frases/día | Arco narrativo |
|---|---|---|---|
| 1 | 1–65 | 1 | Frases independientes que presentan a la familia y el entorno cercano (casa, colegio, barrio, estaciones). Ya escrito: semanas 1–2 (días 1–10). |
| 2 | 66–130 | 2 | Pequeñas escenas de dos frases; empiezan los conectores (`y`, `pero`, `porque`, `cuando`) y algún diálogo suelto. |
| 3 | 131–195 | 3 | Mini-historias de tres frases por semana, con principio y final (problema/solución sencillo). |
| 4 | 196–260 | 4 | Historias más largas, diálogo con comillas, alguna nota informativa curiosa, final de curso con la última semana cerrando la serie. |

### Semanas ya escritas (Trimestre 1)

- **Semana 1 — "La familia de Lucía"** (días 1–5): se presentan Lucía,
  Dani, Toby y la abuela Rosa, uno por día.
- **Semana 2 — "Toby, el perro juguetón"** (días 6–10): una semana
  entera centrada en el perro, cerrando con una página de repaso.

### Semanas siguientes del Trimestre 1 (esquema, sin frases escritas aún)

Un tema por semana, siguiendo el patrón de las dos primeras (un
personaje o escenario nuevo se presenta, se explora durante la semana, y
el viernes hay repaso/celebración cada dos semanas):

3. El colegio de Lucía (la clase, la profesora, un amigo/a nuevo)
4. El barrio y el parque
5. La comida en casa (algo que le gusta, algo que no)
6. Las estaciones — llega el otoño
7. Los juguetes de Dani
8. Un día de lluvia
9. El cumpleaños de alguien de la familia
10. Los animales del barrio (el gato del vecino, los pájaros)
11. Ir al mercado con Mamá
12. Un día en la playa o la montaña (según la zona)
13. Repaso de fin de trimestre + puente hacia el Trimestre 2

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

Esto se puede automatizar más adelante (una lista de "palabras vistas"
en `tools/gen_days.py` que avise si una palabra nueva no se ha visto
antes, a modo de nota informativa, no de error bloqueante) — de momento
es una disciplina editorial, no una regla que el generador compruebe.

## Rotación de actividades

Un ciclo de 5 días, repetido cada semana con contenido distinto (visto
en los días 1–10):

| Día | Actividad | Qué comprueba |
|---|---|---|
| Lunes | **Dibuja** | Comprensión, vía dibujo libre de lo leído |
| Martes | **Completa** | Creatividad, no motricidad fina — unas pocas líneas sin forma, y ella inventa el dibujo a partir de ahí (nunca un dibujo ya cerrado para colorear dentro de los márgenes, eso no exige nada) |
| Miércoles | **Copia** (T1) / **Responde** (T2 en adelante) | T1: copiar la frase, tres veces — practica la letra, no exige componer una respuesta, que a esta edad todavía no sabe hacer sola. Desde T2: pregunta corta con respuesta objetiva, comprensión explícita |
| Jueves | **Relaciona** / **Adivina** | Vocabulario — emparejar palabras, o una adivinanza sencilla |
| Viernes | **Crea** | Tarea abierta; cada dos viernes es además **Repasa** (checklist + celebración) |

`tools/gen_days.py` ya sabe generar los ocho tipos (`dibuja`,
`completa`, `copia`, `responde`, `relaciona`, `adivina`, `crea`,
`repasa`); añadir más días solo requiere añadir entradas al JSON, no
tocar el generador, salvo que se necesite un tipo de actividad
genuinamente nuevo. `responde` está bloqueado en el trimestre 1 por el
propio validador (`TRIMESTRES_SIN_RESPONDE`) — no es solo una
convención editorial, `tools/gen_days.py --check` falla si un día de T1
lo usa.

## Estructura técnica (resumen; ver el propio código para el detalle)

```
main.tex, preamble.tex, lang/es.tex   -- el motor LaTeX (pdflatex + babel[spanish])
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

1. **Escribir las semanas 3–13 del Trimestre 1** (días 11–65) siguiendo
   el esquema de temas de arriba.
2. **Escribir los Trimestres 2, 3 y 4** (`content/q2.json`, `q3.json`,
   `q4.json`) — cada uno con su propio arco narrativo más largo.
3. **Más ilustraciones** en `diagrams/` a medida que aparecen escenarios
   nuevos (el colegio, la playa, el cumpleaños...).
4. Considerar automatizar el aviso de "palabra nueva" descrito arriba.
5. CI (GitHub Actions) que compile el PDF en cada cambio — opcional,
   una vez el resto esté estable.
