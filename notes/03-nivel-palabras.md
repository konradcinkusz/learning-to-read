# El cuaderno de primeras palabras — nivel 1

Un segundo cuaderno, el nivel **anterior** al de frases (`main.tex`,
`content/q*.json`): para una niña o un niño que ya conoce las letras y
empieza a juntarlas — lee sílabas, y tiene que pasar de las sílabas a
la palabra entera. Mismo motor, mismo calendario, misma familia; lo que
cambia es qué se lee cada día y cuánto se dibuja.

Ficheros: `palabras.tex` / `palabras-bw.tex`, `body-palabras.tex`,
`preamble-palabras.tex`, `frontmatter/palabras/`, `backmatter/palabras/`,
`content/palabras/q1.json`…`q4.json`, `tools/gen_palabras.py`,
`tools/silabas.py`. `make palabras` lo genera, compila y comprueba;
`make all-formats` hace los dos cuadernos en color y en blanco y negro.

## Lo que se mantiene igual que en el cuaderno de frases

- **260 días, 52 semanas, cuatro trimestres = cuatro estaciones**, con
  vacaciones incluidas (ver `notes/02-revision-y-plan.md`, punto 1) y
  una medalla al final de otoño, invierno y primavera.
- **Los mismos 52 temas semanales**, en el mismo orden (salvo la semana
  26, "Adiós al invierno"). Es deliberado: si en casa hay dos hermanos,
  cada uno lleva su cuaderno y esa semana leen los dos sobre lo mismo —
  el cumpleaños de Toby, la tormenta de verano, la vuelta al cole.
- **La misma cabecera** en cada página (día, semana, tema, fecha,
  "Leído: sola / con ayuda / con dificultad", notas) — de hecho la misma
  macro, `\cabeceraDia` en `preamble.tex`, compartida por los dos.
- Andika, la paleta, la versión en blanco y negro sin perder
  información, la clave de respuestas, el diploma, las 27 letras de la
  actividad "Traza" repartidas por el año.
- Las mismas barreras duras en `make` y en CI: 1 día = 1 página
  (`tools/check_pages.py`), log sin errores ni `Overfull`
  (`tools/checklog.py`), JSON y `.tex` generado al día (`--check`).

## La escalera: qué se lee cada trimestre

| Trimestre | Semanas | Lee | Sílabas admitidas | Máx. sílabas/palabra |
|---|---|---|---|---|
| 1 (otoño) | 1–5 | 1 palabra | solo directas: V o CV (*a, ma, pe, lo*) | 2 |
| 1 (otoño) | 6–13 | 1 palabra | solo directas | 3 |
| 2 (invierno) | 14–26 | 2 palabras | + cerradas (*sol, bu·fan·da*), c/g suaves (*ce, ci, ge, gi*), h | 3 |
| 3 (primavera) | 27–39 | 3 palabras | todas: + trabadas (*li·bro*), dígrafos (*ch, ll, rr, qu, gu, gü*), diptongos (*a·bue·la*), k/w/x | 4 |
| 4 (verano) | 40–43 | frase de 2 palabras | sin restricción | — |
| 4 (verano) | 44–47 | frase de 2–3 palabras | sin restricción | — |
| 4 (verano) | 48–52 | frase de 3–4 palabras | sin restricción | — |

**Por qué este orden de sílabas.** Es el orden de cualquier método de
lectoescritura en español: primero la sílaba directa (consonante +
vocal), que se lee tal cual suena; después la inversa y la cerrada
(*al, sol*), las grafías que cambian de sonido según la vocal (*ca/ce,
ga/gi*) y la *h*, que no suena; al final lo que más cuesta —dos
consonantes juntas (*bra, pla*), las letras dobles (*ch, ll, rr*), *qu*
y *gu* con la *u* muda, y dos vocales en la misma sílaba (*bue, cie*).
La *r* inicial fuerte (*ra·ma*) y la *ñ* van desde el principio: son una
sola letra y una sola sílaba directa.

**Por qué el verano ya son frases.** El cuaderno de frases empieza en
frases de 6–8 palabras. Pasar de 39 semanas de palabras sueltas a eso
de golpe sería el salto ×2 (o ×8) que `notes/02-revision-y-plan.md`
(punto 2) critica en el propio cuaderno de frases. El verano es el
puente: dos palabras que ya son una frase (*Toby espera.*), luego tres
(*La abuela riega.*), luego cuatro (*Dani lee un cuento.*). El último
día del nivel 1 está a un paso del primero del nivel 2.

**Por qué las sílabas se ven hasta la primavera y en verano no.** El
recuadro de lectura enseña cada palabra dos veces: partida (*pe · lo ·
ta*, en color) y entera (*pelota*, grande). Es un andamio: sirve
mientras hay que juntar sílabas, y estorba cuando lo que se entrena es
leer palabras enteras seguidas. En verano, con frases, desaparece.

**Palabras globales.** *Lucía* y *Toby* se saltan la escalera
(`PALABRAS_GLOBALES` en `tools/gen_palabras.py`): la protagonista y su
perro aparecen todo el año, y con la escalera estricta no podrían salir
hasta el invierno (*cí* es una c suave) o la primavera (la *y* de
*Toby*). Se leen "de un golpe", como el propio nombre — la lectura
global de unas pocas palabras muy frecuentes es normal a esta edad. Solo
nombres del reparto, nunca palabras comunes: *abuela* (diptongo) espera
a la primavera, y *perro* (*rr*) también.

## Cómo se comprueba (y por qué no es solo una intención)

- Cada palabra se escribe en el JSON **ya partida** (`"pe-lo-ta"`), y
  `tools/gen_palabras.py` exige que ese silabeo coincida con el
  automático de `tools/silabas.py`. Dos fuentes independientes que
  tienen que estar de acuerdo: si una se equivoca, la otra lo dice.
  `tools/silabas.py --prueba` comprueba el silabeo automático contra 42
  palabras con respuesta conocida (hiatos, *h* intercalada, *y*,
  *qu/gu/gü*, grupos de tres consonantes), en CI antes que nada.
- Cada sílaba se clasifica (`rasgos()`: cerrada, suave, h, trabada,
  dígrafo, diptongo, rara) y se compara con lo que admite su semana. El
  error dice qué palabra, qué sílaba y por qué: *«perro» tiene la sílaba
  «rro» (digrafo), que la escalera no admite hasta más adelante*.
- Lo mismo vale para las palabras que se leen **dentro de una
  actividad**, no solo en el recuadro verde: los distractores de
  *Encuentra* y los pares escritos a mano de *Une* pasan por la misma
  escalera. Las frases de T4 (día y *¿Sí o no?*) se cuentan por
  palabras.
- `tools/gen_palabras.py --tabla` resume la escalera semana a semana
  (qué se lee, sílabas máximas, qué estructuras de sílaba aparecen por
  primera vez) y CI la publica en el resumen del job.

## La página: casi todo es dibujar

La caja de actividad **ocupa todo lo que queda de página** (tcolorbox
`height fill`, `preamble-palabras.tex`). En el cuaderno de frases, los
días con poca actividad dejaban hasta un 40 % de página en blanco
(revisión, punto 5); aquí ese sitio es para dibujar. Para que la caja
pueda llegar abajo del todo, el pie "Día N / 260" sale de la página de
texto al pie de página de verdad (estilo `piepalabras`). Lo que tiene
que ir abajo del todo dentro de la caja (la línea de escribir de
*Adivina*, el cartel de *Repasa*) va en `\tcblower`: una caja de altura
fija no respeta un `\vfill` dentro.

Las instrucciones de cada actividad son para el adulto (pequeñas y en
gris, como en el cuaderno de frases); lo que lee la niña o el niño va
siempre grande.

### Ciclo semanal

| Día | Actividad | Qué entrena |
|---|---|---|
| lunes | **Dibuja** | comprensión: dibujar lo que se ha leído |
| martes | **Traza** (semanas pares) / **Completa** (impares) | trazo de la inicial de la palabra del día / dibujo libre a partir de unas líneas, con un enunciado ligado a la palabra |
| miércoles | **Palmadas** → **Encuentra** → **Escribe** (rotan cada semana; en verano *¿Sí o no?* en lugar de *Palmadas*) | conciencia silábica / discriminación visual / escritura repasando letras huecas |
| jueves | **Adivina** (pares) / **Une** (impares) | vocabulario: el adulto lee la adivinanza y se dibuja la respuesta / unir minúsculas con MAYÚSCULAS, y en verano animales con su sonido, contrarios o rimas |
| viernes | **Relee** (impares) / **Repasa** (pares, y el cierre de cada trimestre) | soltura: todas las palabras (o frases) de la semana juntas, con una casilla para marcar las que ya salen solas, y un dibujo; *Repasa* lleva además el cartel de "¡N páginas leídas!" |

La única excepción es la semana 35 ("Dani ya reconoce casi todas las
letras"), que trae un *Traza* extra el miércoles (*K de koala*): con 26
martes pares no salen las 27 letras, y esa es la semana de las letras.

Todas terminan dibujando: las que no son de dibujo en sí mismas llevan
un remate "Ahora, dibuja: …" y el resto de la caja para hacerlo.

Tipos de actividad nuevos en este nivel (en `tools/gen_palabras.py`):

- `escribe` — la palabra del día en letras huecas (contorno de Andika,
  `pdfrender`), dos veces, para repasar por dentro; después, una línea
  para escribirla sola.
- `encuentra` — la palabra del día escondida 2, 3 o 4 veces entre
  palabras que se le parecen (*cola / coma / copa / bola*). Obliga a
  mirar todas las letras, no solo la primera. La clave de respuestas
  dice cuántas veces.
- `palmadas` — cada palabra del día con una fila de círculos: una
  palmada por sílaba, un círculo coloreado por palmada.
- `une` — por defecto, sin nada que escribir en el JSON: las palabras
  más recientes de la semana con su versión en MAYÚSCULAS, barajadas sin
  que ninguna quede enfrente de su pareja. Con `pares` e `instruccion`,
  cualquier otra relación (sonidos, contrarios, rimas).
- `si_no` — (solo verano) frases de 2–4 palabras para decidir si tienen
  sentido (*Toby ladra* / *Toby vuela*).
- `traza` es el mismo del cuaderno de frases (el glifo real de Andika en
  puntos), pero la palabra de ejemplo es la del día: el validador exige
  que la letra sea la inicial de una palabra leída ese día (*M de
  mamá*), y que al final del año estén las 27.

## Formato del JSON

```json
{"dia": 66, "semana": 14, "trimestre": 2, "tema": "El frío de enero",
 "palabras": ["bu-fan-da", "man-ta"],
 "actividad": {"tipo": "dibuja", "prompt": "Dibuja a Lucía bien abrigada, con su bufanda."}}
```

En T4, `"frase": "Toby espera."` en lugar de `palabras`. Los viernes no
llevan ni una cosa ni otra: el recuadro de lectura recoge lo leído de
lunes a jueves. El validador exige además que cada día esté en su
semana (`semana = (día − 1) // 5 + 1`) y que los viernes, y solo los
viernes, sean `relee` o `repasa`.

## Qué queda abierto

- **Ilustraciones.** Como el cuaderno de frases, este no tiene dibujos
  hechos: los dibuja quien lo usa. Si algún día se añaden (por ejemplo,
  para un *Une* palabra–dibujo), el sitio natural es `diagrams/`.
- **Vocabulario repetido a propósito.** Algunas palabras vuelven en
  semanas distintas (*sol*, *calor*, *juntos*, *leer*). Es buscado — la
  repetición consolida —, pero no hay todavía una métrica de
  "palabras nuevas por semana" como la de `tools/metricas.py` para el
  cuaderno de frases.
- **"Leído: sola".** La cabecera es la misma que la del cuaderno de
  frases, en femenino. Si el cuaderno es para un niño, basta con
  cambiar `\lblLeidoSola` en `lang/es.tex` (afecta a los dos cuadernos).
