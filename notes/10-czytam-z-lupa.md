# «Czytam z lupą» — "Leo con lupa" en polaco

El octavo cuaderno, y el tercero en polaco: lo que *Leo con lupa*
(`lupa.tex`, `notes/04-nivel-lupa.md`) es en español, en polaco, día a
día y párrafo a párrafo. Es el nivel 3 de la serie polaca *Uczę się
czytać*, después de *Pierwsze słowa* (`notes/08-pierwsze-slowa.md`) y
*Zdania* (`notes/09-zdania.md`): para una niña o un niño que ya lee con
soltura frases compuestas en polaco y ahora aprende a leer con atención.
Todo está en polaco: los textos, las actividades, la portada, la página
para el adulto, *Jak czyta detektyw* con la legitymacja del club, el
mapa del año, la clave y el diploma.

Ficheros: `czytam.tex` / `czytam-bw.tex`, `body-czytam.tex`,
`frontmatter/czytam/`, `backmatter/czytam/`, `content/czytam/q1.json`…,
`content/czytam/progresion.json`, y el mismo generador que *Leo con
lupa*, `tools/gen_days.py --libro czytam` con `tools/lupa.py` (lo que
cambia de uno a otro está en `CZYTAM`, `tools/libros.py`, y en
`IDIOMAS`, `tools/lupa.py`). La portada es la de *Leo con lupa*
(`frontmatter/lupa/portada.tex`): solo lleva cadenas de `lang/`, que
`lang/pl.tex` ya tenía en polaco. `make czytam` lo genera, compila y
comprueba.

## Lo que se mantiene igual que en "Leo con lupa"

- **260 días, 52 semanas, cuatro partes = cuatro estaciones**, con
  vacaciones incluidas, y una medalla al final de otoño, invierno y
  primavera (*Medal za jesień!*, como en *Zdania*).
- **La misma historia, día a día**: cada día es el mismo día de *Leo
  con lupa*, traducido, con su misma actividad, y los mismos casos del
  Club de la Lupa (*Klub Lupy*) con las mismas pistas, repartidas por la
  semana de la misma manera. El texto polaco tiene los mismos párrafos,
  con las mismas marcas (diálogo, nota, lista), salvo donde se dice
  abajo.
- **Las mismas comprobaciones**, las de `tools/lupa.py`: la tabla de
  pistas tiene una sola solución y es la del JSON; las rutas del mapa
  llegan adonde dicen; cada error de *Wyłap błędy* está en el resumen
  equivocado y cada corrección, tal cual, en los textos de la semana; el
  mensaje secreto se cifra a máquina; la solución de cada caso es una de
  sus opciones.
- **Las barreras duras** en `make` y en CI: 1 día = 1 página, log sin
  errores ni `Overfull`, JSON y `.tex` generado al día (`--check`) y
  la escalera.

## Cómo se traduce

Un polaco natural para una niña o un niño de siete u ocho años, con el
mismo sentido que el texto español y las mismas pistas, no una
traducción palabra por palabra. Las decisiones de *Zdania* valen aquí
también (los nombres, *mama*, *tata* y *babcia*, el diálogo con la raya
entre espacios, nada de género cuando se le habla al lector); lo propio
de este cuaderno:

- **Los nombres nuevos** se declinan como los de *Zdania*: *Hugo, Huga,
  Hugowi, z Hugiem*; *pan Tomás, pana Tomása*. Los mayores llevan
  *pan* y *pani*, como los llama en polaco un niño: *pani Marta*, *pan
  Pedro*, *pan Tomás* y *pan Paco*, el conserje (*woźny*). *Paco* no se
  declina bien en polaco (*Paca* se leería con *c* de *cebula*), así
  que no se declina: el caso lo dice *pan* (*pana Paco, z panem Paco*),
  como se hace en polaco con los nombres de fuera. *Lector X* es
  *Czytelnik X*, y *el Club de la Lupa*, *Klub Lupy*. Cuando Lucía se
  hace pasar por *la Lectora X* (día 171), es *Czytelniczka X*, y el
  chiste de Dani sale igual: *Jak Czytelnik X, tylko że dziewczyna!*
- **Los que llegan en invierno y en primavera**, igual: Nora; *Piorun*,
  la tortuga de Hugo (*Rayo*: el chiste de llamar así a una tortuga
  funciona igual en polaco); *pani Pilar*, la maestra de Marta, y *pan
  Luis*, el director de entonces; *pan Julián*, el granjero, y Lola, su
  cabra; y Elena, Jorge y Nacho, los niños de la foto de la cápsula.
  Pilar e Irene no se declinan, como en polaco los nombres de mujer de
  fuera que no acaban en *-a*.
- **La historia sigue en España**, como en *Zdania*: las castañas
  asadas, los Reyes, las doce uvas, el Carnaval. Solo se adapta lo que
  en polaco no se entendería o engañaría: *la función de Navidad* del
  colegio son *jasełka* (la obra de Navidad de los colegios polacos,
  también con su estrella que guía a los pastores), y la hoja del
  *castaño* es la del *kasztan jadalny*, el castaño de verdad, porque en
  polaco *kasztan* hace pensar en el castaño de Indias, cuya hoja parece
  una mano abierta -- que es justo la pista de la hoja del arce. Las
  *torrijas* son *słodkie grzanki*, como en *Pierwsze słowa* y
  *Zdania*, y *la granja escuela* es *zielona szkoła*, los días de
  campo con la clase de los colegios polacos, en una granja
  (*gospodarstwo*, y el granjero, *gospodarz*).
- **El patio del colegio es *podwórko***, en todo el cuaderno: es donde
  está la cápsula del tiempo, con su *piaskownica* (el arenero), su
  *fontanna z głową lwa* y sus dos *platany*. Por eso el día 7, que en
  el otoño decía *boisko*, dice ahora también *podwórko*. En el plano
  del patio, *piaskownica* no cabe en una casilla de siete columnas, y
  va partida en dos líneas por donde se parte en polaco (*piaskow-
  nica*).
- **Las adivinanzas riman en polaco**: la cama (*Mam cztery nogi, lecz
  nie chodzę wcale, / a nocą przynoszę ci sny wspaniałe*) y el reloj,
  con el juego de palabras que en polaco dan las agujas, que se llaman
  *wskazówki*, como las pistas (*Mam wskazówki, lecz drogi nie
  wskazuję*); y las de la búsqueda del tesoro de Dani, la lavadora
  (*Mam okrągłą buzię / i w brzuchu się kręcę*) y la nevera (*Choć na
  dworze słońce praży, / w moim brzuchu mróz i chłód*).
- **La pista de la carta sin firma** (día 193) es la misma: en español,
  quien la escribió era una niña porque pone *nerviosísima* y no
  *nerviosísimo*; en polaco, *zdenerwowana* y no *zdenerwowany*.
- **Donde el cuaderno en español no cuadra, el polaco sí**: el día 195,
  a Marta se le quiebra la voz «cuando llegó a la última frase» de su
  carta, y la frase que se cita es la penúltima (la última es la
  pregunta, *Y tú, ¿qué quieres ser?*); en polaco, cuando llega a la
  frase del colegio (*Kiedy doszła do zdania o szkole*).
- **Las citas**, entre „ ”, como se escribe en polaco (en español,
  «»): `tools/lupa.py` acepta que un párrafo acabe en ” en un cuaderno
  en polaco, y » en uno en español.
- **Prawda czy fałsz**: las respuestas son *P* o *F* (en español, *V* o
  *F*), las letras de las casillas.
- **Porównaj**: en medio del diagrama, lo que tienen en común las dos
  cosas es *wspólne*, que vale para personas, animales y cosas (el *los
  dos* del español tendría en polaco tres formas, *oba*, *obie* u
  *oboje*); y la clave dice *Psy: … Wspólne: … Koty: …*.
- **T. rex** lleva un espacio que no se parte (U+00A0), para que *T.* no
  se quede sola al final de una línea.

## El mensaje secreto, con el abecedario polaco

En español, el código de números va de la A (1) a la Z (27), con la Ñ,
y el del club cambia las cinco vocales por un número. En polaco, las
dos cosas cambian, porque cambia el abecedario (`IDIOMAS` en
`tools/lupa.py`):

- **El código de números** va de la A (1) a la Ż (32), por el orden del
  alfabeto polaco: *A, Ą, B, C, Ć, D, E, Ę*… Su tabla tiene dos filas de
  16 columnas (`\begin{tablaCodigo}[16]`, `preamble-lupa.tex`; la del
  español sigue con sus 14). *Ą, Ć, Ę, Ł, Ń, Ó, Ś, Ź* y *Ż* son letras
  del abecedario, así que el mensaje las conserva; las tildes que no son
  del polaco se quitan (*Lucía*, *LUCIA*).
- **El código del club** cambia las nueve vocales del polaco, las que
  aprenden los niños en el colegio (*samogłoski*), también por el orden
  del alfabeto: A = 1, Ą = 2, E = 3, Ę = 4, I = 5, O = 6, Ó = 7, U = 8, Y
  = 9. Así, *lupa* es *l8p1*. El día 13, donde Hugo lo inventa, las
  nueve no cabían en una frase como las cinco del español: el texto dice
  que Hugo lo escribe en la pizarra, y el código va en una nota (`> `),
  en tres líneas.

## La escalera, en palabras polacas

Traducidos, los 65 días del otoño tienen de mediana 0,84 veces las
palabras del español (de 0,74 a 1,07), y su frase más larga, 0,88 veces
la del español; y casi siempre tienen tantos nexos de subordinación
como en español, o más (de mediana, cuatro; en español, tres).
`content/czytam/progresion.json` es la escalera de *Leo con lupa*
medida en palabras polacas con la misma regla que la de *Zdania*:
`palabras_min`, la del español por 0,8, redondeada; `palabras_max` y
`frase_max`, las del español por 0,9, hacia arriba; `subordinadas_min` y
`nuevas_max`, las mismas. Los textos españoles están casi siempre en el
máximo de su semana, así que un día que en polaco no se acorta se sale:
ocho días del otoño (el 1, el 2, el 27, el 28, el 31, el 49, el 52 y el
63) quitan en polaco una palabra que sobraba o dicen lo mismo con una
frase más corta, el 13 lleva el código en una nota (ver arriba), y dos
(el 31 y el 64) ganan la subordinada que les faltaba (*To był pan
Pedro, który używał liści...*). En invierno y en primavera, lo mismo:
trece días del invierno y quince de la primavera se salían, casi
siempre por una frase más larga que la de su semana (se parte en dos)
o por una subordinada de menos -- en español cuentan siempre *como*,
*si* y *mientras*, también en *como si*, *por si acaso* o *mientras
tanto*, y su traducción polaca es un solo nexo (*jakby*) o ninguno (*na
wszelki wypadek*, *tymczasem*): se dice con una subordinada de verdad
(*z taką miną, jakby nic się nie stało*). Y tres
días que en polaco se quedaban a una o tres palabras del mínimo de su
semana (el 114, el 129 y el 150) las ganan (*co już wiemy*). Con eso,
ningún día tiene errores, y los que tienen aviso, todos de vocabulario
nuevo, son menos que en español: en otoño, dos (en español, cuatro);
en invierno, tres (en español, ocho), y en primavera, uno (en español,
dos).

`tools/metricas.py --libro czytam` mide lo mismo que en *Leo con lupa*,
con el polaco de *Zdania* (sus palabras funcionales y su lematización)
y, además:

- **Los nexos de subordinación del polaco** (`SUBORDINANTES_PL`): *że,
  bo, ponieważ, gdy, kiedy, jeśli, żeby, chociaż, zanim*… (y *żeby,
  aby, gdyby* y *jakby* con la persona pegada: *żebyśmy, gdybyś*…), el
  relativo *który* en todas sus formas, y *co, gdzie, jak, czy, kto* y
  *dlaczego*, que abren una relativa o una interrogativa indirecta. Si
  abren una pregunta directa (*Gdzie jest Toby?*), no cuentan, como en
  inglés: es la primera palabra de una frase que acaba en *?* -- en
  polaco, la primera palabra, no la raya suelta que va delante.
- **Dónde acaba una frase** (`_FIN_DE_FRASE_PL`): después de . ! ? … (y
  de la ” o la raya que vayan detrás), cuando lo que sigue empieza por
  mayúscula, por „ o por una raya.
- **El vocabulario nuevo** se cuenta contra todo lo ya leído en
  *Zdania*, como el de *Leo con lupa* contra el cuaderno de frases:
  `Libro.libro_previo`.

## Una página por día

El polaco ocupa más que el español, y ocho días de la primavera (el
132, el 149, el 154, el 175, el 181, el 182, el 187 y el 195), con de
un 2 a un 10 % más letras que en español, no cabían en su página: la
actividad pasaba entera a la siguiente, y `tools/check_pages.py` lo
paraba. Cada uno se acorta lo justo, sin salirse de la escalera y sin
perder ninguna pista: un párrafo cuya última línea eran una o dos
palabras las pierde (*na zakończenie roku*, sin *szkolnego*), o una
frase de la actividad que ocupaba dos líneas cabe en una.

## Lo que cambia en el motor

- `tools/lupa.py`: `IDIOMAS`, lo que cambia de un idioma a otro -- el
  abecedario y las vocales del mensaje secreto, la *y* de *1, 2 y 3*
  (en polaco, *i*), las letras de verdadero y falso, la comilla que
  puede cerrar un párrafo, la instrucción de *Połącz* cuando el día no
  trae la suya y las palabras de la clave de *Porównaj*. `validar_texto`
  y `entrada_clave` reciben el libro, como ya lo recibía `pagina_dia`
  (y `tools/english.py`, con la misma forma, lo acepta).
- `preamble-lupa.tex`: `tablaCodigo` admite el número de columnas.
- `tools/metricas.py`: el polaco de "Leo con lupa" (`SUBORDINANTES_PL`,
  `_FIN_DE_FRASE_PL`), la pregunta directa también en polaco, y el
  vocabulario del nivel anterior de cada libro (`libro_previo`).
  `SUBORDINANTES_PL` solo se usa en este cuaderno (en *Zdania* no se
  cuentan subordinadas).
- `tools/libros.py`: el `Libro` `CZYTAM` y el campo `libro_previo` (en
  *Leo con lupa*, `"frases"`, lo de siempre).
- `lang/pl.tex`: `\lblLosDos` es *wspólne*.

Lo generado para los otros siete cuadernos es, letra por letra, lo que
era antes, y sus tablas de `tools/metricas.py`, también.

## Las fases

Un PR por fase, cada uno en verde antes del siguiente. Mientras tanto,
`CZYTAM.dias_escritos` dice cuántos días hay escritos, y se validan
exactamente esos.

1. **El motor y el otoño** (días 1–65): `CZYTAM`, `IDIOMAS` en
   `tools/lupa.py`, los nexos del polaco en `tools/metricas.py`, la
   escalera en palabras polacas, las páginas para el adulto y para el
   detective, la clave, el diploma y los 65 días, con el caso de
   *Czytelnik X*. **Hecho.**
2. **El invierno y la primavera** (días 66–195): la narración en pasado,
   el mapa de la abuela Rosa, la cápsula del tiempo y las dos medallas.
   **Hecho.**
3. **El verano** (días 196–260), el tesoro de Rosa, el cuaderno de
   verano y la muestra, y publicarlo en GitHub Pages con los demás.
