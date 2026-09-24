# «Pierwsze słowa» — primeras palabras en polaco

El sexto cuaderno, y el primero en polaco: lo que el cuaderno de
primeras palabras (`palabras.tex`, `notes/03-nivel-palabras.md`) es en
español, para una niña o un niño que ya conoce las letras y empieza a
juntarlas en polaco. Es para una familia que habla polaco en casa, o
para quien lo aprende, y es de la misma familia que *Poznaję liczby*
(https://github.com/konradcinkusz/learning-to-count) y *Poznaję
ekonomię* (https://github.com/konradcinkusz/learning-economics). Todo
está en polaco: las palabras, las instrucciones, la portada, la página
para el adulto, el mapa del año, la clave y el diploma.

Ficheros: `slowa.tex` / `slowa-bw.tex`, `body-slowa.tex`,
`frontmatter/slowa/`, `backmatter/slowa/`, `content/slowa/q1.json`…,
`lang/pl.tex`, `tools/sylaby.py`, y el mismo generador que el español y
el inglés, `tools/gen_palabras.py --libro slowa` (todo lo que cambia de
un cuaderno a otro está en su `Perfil`). `make slowa` lo genera,
compila y comprueba.

## Lo que se mantiene igual que en el cuaderno de primeras palabras

- **260 días, 52 semanas, cuatro partes = cuatro estaciones**, con
  vacaciones incluidas, y una medalla al final de otoño, invierno y
  primavera (*Medal za jesień!*).
- **Los mismos 52 temas**, en el mismo orden (*Rodzina Lucíi*, *Toby,
  wesoły piesek*...): si en casa hay dos hermanos, uno con el cuaderno
  en español y otro con el polaco, esa semana leen los dos sobre lo
  mismo.
- **La escalera de cuánto se lee**: una palabra al día en otoño, dos en
  invierno, tres en primavera, y en verano una frase, de dos palabras a
  cuatro.
- **La página y el ciclo semanal**: la caja de lectura arriba, la de
  actividad llenando lo que queda, y las mismas actividades, los mismos
  días (ver la tabla de `notes/03-nivel-palabras.md`). Las instrucciones
  son para el adulto, pequeñas y en gris; lo que lee la niña o el niño
  va siempre grande.
- **Las barreras duras** en `make` y en CI: 1 día = 1 página, log sin
  errores ni `Overfull`, JSON y `.tex` generado al día (`--check`).

## Las sílabas del polaco

El polaco se aprende a leer por sílabas, como el español, pero sus
sílabas son otras, y `tools/sylaby.py` las parte con las reglas de la
escuela:

- cada sílaba tiene una vocal (*a, ą, e, ę, i, o, ó, u, y*), y no hay
  diptongos (*na-u-ka*);
- *ch, cz, dz, dź, dż, rz, sz* son una consonante (dos letras, un
  sonido) y no se separan;
- la *i* entre una consonante y una vocal no es vocal: ablanda la
  consonante (*pies*, *nie-bo*, *zie-mia*);
- entre dos vocales, una consonante va con la sílaba siguiente
  (*ko-ło*); de dos o más, solo la última -- o las dos últimas si son
  una consonante con *r, l, ł* o *rz* (*ko-bra*, *ma-sło*,
  *po-krzy-wa*) --, y las demás se quedan con la anterior (*lal-ka*,
  *jabł-ko*, *wios-na*, *sios-tra*).

El polaco admite varios silabeos para la misma palabra (*sio-stra,
sios-tra, siost-ra*): el cuaderno usa siempre ese, para que las sílabas
que se imprimen sean previsibles, y porque es el que deja las sílabas
más fáciles. Una palabra que necesite otro (un prefijo:
*przed-szko-le*) va en `WYJATKI`, con su porqué.

Cada palabra se escribe en el JSON ya partida (`"ło-pa-ta"`) y tiene
que coincidir con `tools/sylaby.py`, como en español con
`tools/silabas.py`. `tools/sylaby.py --prueba` comprueba el silabeo
contra 54 palabras con respuesta conocida y los rasgos de 17 sílabas,
en CI antes que nada.

### La escalera

`cechy()` dice qué tiene de difícil cada sílaba, y `ESCALERA_PL`
(`tools/gen_palabras.py`) qué admite cada tramo:

| Parte | Semanas | Lee | Sílabas admitidas | Máx. sílabas |
|---|---|---|---|---|
| 1 (otoño) | 1–5 | 1 palabra | solo directas: una letra y una vocal (*ma-ma, ko-ło, ły, ki*) | 2 |
| 1 (otoño) | 6–13 | 1 palabra | solo directas (*ło-pa-ta, ko-le-ja*) | 3 |
| 2 (invierno) | 14–26 | 2 palabras | + cerradas (*kot, lal-ka*), blandas (*zi-ma, pies, koń*), *ó* y *ż* | 3 |
| 3 (primavera) | 27–39 | 3 palabras | todas: + dígrafos (*szko-ła, rze-ka*), nasales (*rę-ka*), dos consonantes delante (*kro-wa, słoń*), *q, v, x* | 4 |
| 4 (verano) | 40–52 | frase de 2 a 4 palabras | sin restricción | — |

**Por qué este orden.** Es el de las cartillas polacas: primero lo que
se lee letra a letra (*ma, ło, ty*); después lo que cambia de sonido --
la *i* que ablanda (*si, ci, zi, ni*: *zi-ma* se lee *źi-ma*), las
blandas con tilde (*ś, ć, ź, ń*), la *ó*, que suena como *u*, y la *ż*
--; y al final dos letras para un sonido (*sz, cz, rz, ch, dz*), las
nasales, que cambian según lo que tengan detrás, y dos consonantes
juntas, que en polaco son muchas y muy seguidas. El otoño es el tramo
más estrecho, y aun así hay de sobra para cada tema (*ma-ma, ta-ta,
ła-pa, bu-da, lo-dy, zu-pa, so-wa, ko-le-ja, ko-ro-na, pa-pu-ga,
u-li-ca, mo-ne-ta, ko-me-ta*).

**Nombres que se leen de un golpe.** *Lucía*, *Dani* y *Toby* se saltan
la escalera (`PALABRAS_GLOBALES_PL`): la *í* de *Lucía* no es polaca, la
*ni* de *Dani* sería blanda (*ńi*) y la *y* de *Toby* suena como una
*i*. Van enteros en el JSON, sin guiones, y su tarjeta no se parte
(`\tarjetaEntera`, la de *First Words*); si es lo único que se lee ese
día, la instrucción dice que se lee entero, "jak swoje własne imię".
*Mama*, *tata* y *Rosa* se leen por sílabas desde el primer día.

**Para quien lee también en español.** La página para el adulto avisa
de las letras que en polaco suenan distinto: *c, j, h, w, z, y, ł*, y
la *ó*, que suena como *u* (y no como una *o* con tilde).

## Las 32 letras de «Pisz po śladzie»

*Traza* es la misma actividad que en español (el glifo real de Andika,
en puntos), y la letra es la inicial de una palabra que se lee ese día
(*Ł jak łapa*). En polaco son 32 letras, cinco más que en español, así
que además de los martes de las semanas pares hay seis martes más en
las semanas impares; `content/letras-trazo.json` trae las nueve que el
español no tiene (*ą, ć, ę, ł, ń, ó, ś, ź, ż*: `tools/gen_letras_puntos.py`
las añade al final, y las 27 de antes salen igual, letra por letra).
Ninguna palabra polaca empieza por *ą, ę, ń* o *y*: para esas vale que
estén dentro de una palabra del día (*Ą jak wąż*, *Y jak ryby*), como la
*x* en inglés. Al terminar el año tienen que estar las 32
(`comprobar_trazo`, con el abecedario del `Perfil`).

En otoño: *ł* (*łapa*), *r* (*ryba*), *s* (*sowa*), *k* (*kora*), *p*
(*papuga*) y *m* (*morele*).

## Lo que cambia en el motor

- `tools/sylaby.py`: el silabeo y los rasgos del polaco (`podziel`,
  `cechy`), con su `--prueba`.
- `tools/gen_palabras.py`: el `Perfil` `SLOWA` (`idioma="pl"`), con su
  escalera, sus nombres globales, su abecedario, las letras que se
  trazan dentro de una palabra y la instrucción de los nombres. El
  silabeo y los rasgos se eligen por idioma (`partir`, `rasgos_de`), y
  en polaco la inicial conserva su tilde (*ó* es una letra).
- `preamble.tex`: `\booklang{pl}` carga babel en polaco (con
  `\shorthandoff{"}`, como el español) y lee `lang/pl.tex`, con todas
  las cadenas de `lang/es.tex` en polaco. Lo que se le dice a la niña o
  al niño no tiene género (*umiesz*, *samodzielnie*); en la cabecera,
  *Czytanie:*, porque *Przeczytane:* no cabía.
- `\tarjetaEntera` pasa de `preamble-firstwords.tex` a
  `preamble-palabras.tex`, para los dos cuadernos.

Lo generado para los otros cinco cuadernos es, letra por letra, lo que
era antes.

## Las fases

Un PR por fase, cada uno en verde antes del siguiente. El `Perfil` dice
cuántos días están escritos (`dias_escritos`).

1. **El motor y el otoño** (días 1–65): `tools/sylaby.py`, el `Perfil`,
   `lang/pl.tex`, las páginas para el adulto, la clave, el diploma, las
   nueve letras nuevas y los 65 días. **Hecho.**
2. **El invierno y la primavera** (días 66–195): las cerradas, las
   blandas, la *ó* y la *ż*; después los dígrafos, las nasales y dos
   consonantes juntas.
3. **El verano** (días 196–260), las 32 letras, el cuaderno de verano y
   la muestra, y publicarlo.
