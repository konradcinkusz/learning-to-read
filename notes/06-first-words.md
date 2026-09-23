# «First Words» — primeras palabras en inglés

El quinto cuaderno, y el segundo en inglés: el nivel más bajo en inglés,
**muy por debajo** de *Read and Draw* (`english.tex`, ver
`notes/05-english.md`). *Read and Draw* es para quien ya lee con soltura
y lee textos cortos de oraciones compuestas; *First Words* es para quien
**empieza** a leer en inglés: conoce las letras (o casi todas) y empieza
a juntar sus sonidos. Es, en inglés, lo que el cuaderno de primeras
palabras (`palabras.tex`, `notes/03-nivel-palabras.md`) es en español:
una palabra al día y casi siempre un dibujo — aquí, para colorear: el
de una palabra que se acaba de leer (ver *Los dibujos para colorear*,
más abajo). Todo está en inglés — la
palabra, las instrucciones, la portada, la página para el adulto, la
clave y el diploma.

Ficheros: `firstwords.tex` / `firstwords-bw.tex`, `body-firstwords.tex`,
`preamble-firstwords.tex` (encima de `preamble-palabras.tex`),
`frontmatter/firstwords/`, `backmatter/firstwords/`,
`content/firstwords/q1.json`…`q4.json`, `tools/fonetica.py`, y el mismo
generador que el español, `tools/gen_palabras.py --libro firstwords`
(todo lo que cambia de un cuaderno a otro está en su `Perfil`). `make
firstwords` lo genera, compila y comprueba.

## Lo que se mantiene igual que en el cuaderno de primeras palabras

- **260 días, 52 semanas, cuatro partes = cuatro estaciones**, con
  vacaciones incluidas, y una medalla al final de otoño, invierno y
  primavera.
- **La escalera de cuánto se lee**: una palabra al día en otoño, dos en
  invierno, tres en primavera y una frase en verano, de dos palabras a
  cuatro — los mismos tramos que el español (`ESCALERA_EN`, al lado de
  `ESCALERA` en `tools/gen_palabras.py`).
- **La página**: la caja de lectura arriba y la caja de actividad
  llenando todo lo que queda (`preamble-palabras.tex`, las mismas cajas y
  las mismas plantillas). Las instrucciones son para el adulto, pequeñas
  y en gris; lo que lee la niña o el niño va siempre grande.
- **El ciclo semanal y las actividades** (ver la tabla de
  `notes/03-nivel-palabras.md`): lunes *Draw* (con dibujo para
  colorear, *Colour*); martes *Trace* (semanas
  pares) o *Finish the picture* (impares); miércoles *Sounds* → *Find it*
  → *Write*, rotando cada semana (en verano, *Yes or no?*); jueves
  *Riddle* (pares) o *Match* (impares); viernes *Read again* (impares) o
  *Look back* (pares, con el cartel de "10 pages read!").
- **Las barreras duras** en `make` y en CI: 1 día = 1 página
  (`tools/check_pages.py`), log sin errores ni `Overfull`
  (`tools/checklog.py`), JSON y `.tex` generado al día (`--check`).

## Los temas: los de *Read and Draw*

Las 52 semanas tienen los mismos temas, en el mismo orden, que *Read and
Draw* (*New neighbours*, *Amy's first day*, *Toby meets Pip*…, ver
`notes/05-english.md`): el mismo año, la misma familia y los mismos
vecinos de Londres — Amy, su hermano Sam y Pip, el loro. Si en casa hay
dos hermanos, uno con cada cuaderno, esa semana leen los dos sobre lo
mismo. Con una palabra al día no se puede contar la historia: la cuenta
el adulto, que lee la instrucción de cada actividad (*A big van stops
next to Lucía's house. Draw the van.*), y la palabra del día es una pieza
de ella (*van*, *mum*, *Pip*, *Amy*).

## Lo que cambia: se lee por sonidos, no por sílabas

En español se aprende a leer por sílabas (*pe·lo·ta*); en inglés, por
sonidos (*phonics*): se dice cada sonido y se juntan — *c, a, t: cat*.
La unidad es el **grafema**, la letra o grupo de letras que se lee como
un solo sonido: *c-a-t*, *sh-ee-p*, *n-igh-t*, y la "e mágica" (*split
digraph*) de *cake*, que es un solo sonido escrito con dos letras
separadas (`c-a_e-k`).

La tarjeta de la palabra no la parte en trozos: la enseña entera, con un
**botón de sonido** debajo de cada grafema, como en los colegios
ingleses — un punto si el sonido es una letra, una raya si son varias
(*sh*, *ee*, *ck*), un arco de la vocal a la *e* si es una e mágica. Se
lee tocando cada botón, diciendo su sonido, y luego la palabra de
corrido. Cada grafema es un nodo de TikZ pegado al anterior por la línea
base (`tarjeta_sonidos` en `tools/gen_palabras.py`, `\tarjetaSonidos`
en `preamble-firstwords.tex`): la palabra se ve como un solo texto, y
los botones, medidos en `em`, caen debajo de sus letras a cualquier
tamaño. La letra es Andika sin ligaduras (en *off*, las dos efes tienen
que verse como dos).

### La escalera de sonidos

| Parte | Semanas | Lee | Sonidos nuevos | Máx. sonidos | Dos consonantes seguidas |
|---|---|---|---|---|---|
| 1 (otoño) | 1–5 | 1 palabra | una letra = un sonido: todas menos q, x, y (*van, mum, Pip, bag*) | 3 | no |
| 1 (otoño) | 6–13 | 1 palabra | + ck ff ll ss zz gg, x, y, qu (*duck, bell, box, yes, quack*) | 3 | no |
| 2 (invierno) | 14–26 | 2 palabras | + sh ch th ng, ai ee igh oa oo ar or ur ow oi ear air ure er, bb dd mm nn pp rr tt (*ship, rain, night, moon, car, letter*) | 4 | no |
| 3 (primavera) | 27–39 | 3 palabras | + ay ou ie ea oy ir ue aw ew oe au ey wh ph tch dge, la e mágica (*day, bird, blue, cake, bike, bone*) | 5 | sí (*frog, nest*) |
| 4 (verano) | 40–43 | frase de 2 palabras | ninguno: palabras que se leen sonido a sonido, tricky words ya presentadas y nombres | — (5) | sí |
| 4 (verano) | 44–47 | frase de 2–3 palabras | ídem | — (5) | sí |
| 4 (verano) | 48–52 | frase de 3–4 palabras | ídem | — (5) | sí |

**Por qué este orden.** Es el de *Letters and Sounds* (DfE, 2007), el
programa de los colegios ingleses: primero una letra = un sonido (fase
2–3), después dos o tres letras para un sonido (fase 3), después dos
consonantes seguidas (fase 4) y otras formas de escribir los mismos
sonidos (fase 5). Las fases 4 y 5 van juntas en primavera: con tres
palabras al día y cinco sonidos por palabra hay sitio para las dos. Hasta
la primavera, ninguna palabra lleva dos consonantes seguidas: en
invierno se juntan hasta cuatro sonidos, pero cada uno está solo entre
vocales (*b-oa-t*, *h-a-mm-er*).

**La tabla de sonidos.** La página *The sounds in this book*, justo
después de la del adulto, enseña todos los sonidos del cuaderno en el
orden en que llegan, cada uno con una palabra que lo tiene (*sh — ship*,
*a–e — cake*). No está escrita a mano: la genera `tools/gen_palabras.py`
(`content/firstwords/generated-sonidos.tex`) a partir de `ESCALERA_EN` y
de `fonetica.EJEMPLOS`, y falla si a un grafema le falta su ejemplo, si
sobra alguno o si un ejemplo no se puede leer todavía en su tramo — así
la tabla no puede decir una cosa y la escalera otra.

**Nombres que se leen de un golpe.** Como *Lucía* y *Toby* en el
cuaderno español, los nombres del reparto que no se pueden leer sonido a
sonido con lo que se sabe (*Lucía, Toby, Amy, Dani, Grandma, Brown*…)
se saltan la escalera (`PALABRAS_GLOBALES_EN`): van enteros en el JSON,
sin guiones, y su tarjeta no lleva botones (y, si es la única del día,
la instrucción dice que se lee "in one go, like your own name"). *Pip*,
*Sam*, *mum* y *dad* no están: se leen sonido a sonido desde el primer
día.

**Tricky words.** Las palabras muy frecuentes que no se leen como se
escriben (*the, was, said, you*) o que se leen antes de haber visto sus
sonidos (*he, my, no*) se aprenden enteras (`fonetica.TRICKY`, las 47
de las listas de los colegios ingleses, más *a, is, his, has, as, of*).
Hasta el verano no hacen falta — se leen palabras sueltas — y nunca
pueden salir como una palabra de tarjeta (`tools/gen_palabras.py` lo
rechaza). Se presentan en primavera: cada viernes, debajo de las
palabras de la semana, tres o cuatro tricky words, cada una en un marco
y con su casilla, sin botones (`"tricky"` en el JSON; `presentar_tricky`
exige que cada una sea de la lista, que no se haya presentado antes y
que sea un viernes de primavera). En trece viernes salen las 47, más o
menos en el orden de *Letters and Sounds*: *a, the, I, is* el primero;
*Mr, Mrs, called, asked* el último.

**Por qué el verano ya son frases.** Por lo mismo que en el cuaderno
español: *Read and Draw* empieza con textos de unas 30 palabras, y pasar
de 39 semanas de palabras sueltas a eso de golpe sería demasiado. El
verano es el puente, y en él **nada es nuevo**: las frases son lo que en
los colegios ingleses se llama *decodable text* — cada palabra se lee
sonido a sonido con todo lo aprendido (cabe en la escalera de la
primavera: todos los grafemas, hasta cinco sonidos), o es una tricky
word que ya se ha presentado un viernes, o un nombre del reparto (con
su *'s*: *Toby's*). Sin tarjetas ni botones: ya no hacen falta.

## Los dibujos para colorear

La primera versión del cuaderno se dibujaba, como el español: *Draw the
van*, y una caja en blanco. Pero quien empieza a leer en inglés tiene
cuatro o cinco años, y dibujar una furgoneta a partir de una palabra es
más difícil que leerla. Así que cada día trae **el dibujo de una palabra
que se acaba de leer, para colorearlo**: si se lee *van*, se colorea una
furgoneta. Colorearlo es comprobar que la palabra se ha entendido, no
solo sonorizado — y la adivinanza y *Match* lo comprueban de verdad:
hay que elegir el dibujo que corresponde a lo que se ha leído.

**En el JSON.** Cada día lleva su `"dibujo"`: `"van"` es
`diagrams/firstwords/van.tex`, y su palabra es *van*; si el fichero no se
llama como la palabra, `{"imagen": "disfraz", "palabra": "cat"}` (con
una barra, la ruta desde `diagrams/`, para los dibujos que ya tenía *Read
and Draw*: `english/calabaza`). De lunes a jueves, la palabra tiene que
ser **una de las leídas ese día** — lo que se colorea es lo que se acaba
de leer —; los viernes, el dibujo es una escena de la semana (la casa de
los vecinos, la fiesta de Lucía) y no necesita palabra.

**En la página.**

- **Lunes, *Colour*** (`"colorea"`): el enunciado y el dibujo, que llena
  la caja.
- **Martes, *Finish the picture*** (`"completa"`, sin `"diagrama"`): el
  dibujo, al que le falta algo que dibujar — Toby sin cola, el árbol sin
  estrella, el regalo sin lazo.
- ***Trace*, *Sounds*, *Find it*, *Write*, *Yes or no?***: la actividad,
  y debajo *Now colour: …* con el dibujo, en todo el sitio que quede. Para
  que el dibujo no salga diminuto, con dibujo la actividad ocupa algo
  menos: en *Write*, la palabra hueca va una vez, no dos; en *Trace*, las
  letras de puntos son un poco más pequeñas (siguen siendo grandes para
  repasarlas con el dedo); en *Find it*, las filas van más juntas.
- ***Riddle***: la respuesta no se dibuja, se elige — tres tarjetas con
  tres dibujos, el del día y dos `"otros"`, en un orden que cambia de un
  día a otro; se colorea el que contesta la adivinanza. La adivinanza
  describe la palabra del día (*I help sick animals… Who am I?* el día
  de *vet*).
- ***Match***: cada palabra con su dibujo, no con sus MAYÚSCULAS — las
  cuatro palabras más recientes que tienen dibujo, la del día incluida, o
  las que diga `"dibujos"` cuando dos dibujos recientes se parecen
  demasiado (la semana de *Toby, dog, wag, nap* son cuatro Tobys).
- **Viernes**: la escena de la semana, para colorear, debajo de las
  palabras de la semana (y del cartel, en *Look back*).

**Cómo están hechos.** En TikZ, a línea gruesa (1,5 pt, extremos
redondos), y **cada parte es una zona cerrada y rellena de blanco**, para
colorearla aparte y sin que se vea lo que queda detrás. Los personajes
son siempre los mismos: `diagrams/firstwords/kit.tex` (cargado por
`preamble-firstwords.tex`) tiene la cabeza de cada uno — la coleta de
Lucía, los rizos de Amy, la melena de Mrs Brown, el remolino de Dani, el
bigote de Dad, el moño y las gafas de Grandma —, los cuerpos con los
brazos en cuatro posturas, Toby (de pie, sentado, dormido), Pip, Luna,
la jaula, la valla, la cama, el sofá, el árbol, la tarta… Cada dibujo
los coloca con un `scope` (`shift`, `scale`). El flequillo tapa el borde
de arriba de la cara (se rellena de blanco sin borde y solo se traza su
línea), así que todo el pelo es una sola zona.

**Del tamaño del sitio que quede.** El dibujo va en la parte de abajo
de la caja (`\tcblower`), y `\dibujoHueco` le da justo el sitio que deja
la actividad: la altura del texto de la caja (fija, con `height fill`)
menos lo que ocupa la parte de arriba, que tcolorbox ya ha compuesto.
Si no quedan 30 mm, es un error de compilación: la actividad es
demasiado larga para ese día. Para escalar, `\dibujoColorear` cambia la
escala de las coordenadas, no la de la caja — así las líneas salen
igual de gruesas en un dibujo grande que en uno pequeño —, y como la
caja de TikZ incluye el grueso de la línea, que no se escala, mide el
dibujo dos veces (a escala 1 y 2) y calcula la escala exacta para que
quepa sin una caja *overfull*.

**Por partes.** Los dibujos se hacen estación por estación, un PR cada
una: `dias_con_dibujo`, en el `Perfil`, dice cuántos días (del 1 en
adelante) los llevan ya, y se exigen exactamente esos; los demás siguen
dibujándose.

## Cómo se comprueba

- Cada palabra de una tarjeta se escribe en el JSON **ya partida en sus
  sonidos** (`"sh-ee-p"`, `"c-a_e-k"`), y tiene que coincidir con el
  partido automático de `tools/fonetica.py`, `segmentar()`: un
  emparejamiento voraz, de izquierda a derecha, que prueba primero los
  grafemas más largos (*igh* antes que *i*), con dos reglas — la e
  mágica (vocal + una consonante + *e* final) y la *rr* (*cherry* es
  *ch-e-rr-y*, no *ch-er-r-y*). Dos fuentes que tienen que estar de
  acuerdo, como el silabeo del español.
- `segmentar()` rechaza las **trampas**: palabras que se pueden partir
  pero cuyos botones mentirían — una *e* final que no suena y no es una e
  mágica (*house, apple, tables*), letras mudas (*knee, write, lamb,
  ghost*), una *c* que suena /s/ (*nice, city*), la *a* de *ball*,
  *talk* y *want* y la *o* de *cold*, y la *e* del pasado en -ed
  (*played*). Mejor un error que una tarjeta con un botón debajo de una
  letra que no suena.
- `tools/fonetica.py --prueba` comprueba el partido automático contra 78
  palabras con respuesta conocida (también los plurales con e mágica,
  *cakes*: c-a_e-k-s, y los que no lo son, *boxes*: b-o-x-e-s), que las
  27 trampas de prueba se rechacen y que cada ejemplo de la tabla de
  sonidos tenga su sonido — en CI, antes que nada.
- Cada palabra que lee la niña o el niño — en la tarjeta y **dentro de
  una actividad** (los distractores de *Find it*, los pares escritos a
  mano de *Match*) — pasa por la escalera de su semana: solo grafemas ya
  vistos, no más sonidos de los que admite, dos consonantes seguidas
  solo desde la primavera, nunca una tricky word. El error dice qué
  palabra, qué sonido y por qué: *«ship» (sh-i-p) tiene sh, que la
  escalera no admite hasta más adelante (semana 3)*.
- En verano, cada palabra de cada frase — y de *Yes or no?* y *Match* —
  tiene que ser *decodable* (ver arriba): una tricky word que todavía
  no se ha presentado es un error que dice en qué viernes de primavera
  falta.
- **Cada sonido de la tabla se practica**: todo grafema que la escalera
  trae en una estación tiene que salir en alguna tarjeta antes de que
  esa estación se acabe (`comprobar_cobertura`) — la tabla de sonidos
  dice "every sound in the book", y tiene que ser verdad. En el otoño,
  por ejemplo, la *z* sola solo cabía en *zip* (día 36): sin esa
  palabra, el libro no se genera.
- La clave de respuestas trae, además de lo del cuaderno español,
  cuántos sonidos tiene cada palabra de *Sounds*: quien no aprendió a
  leer en inglés no tiene por qué saber que *sheep* tiene tres.
- `tools/gen_palabras.py --libro firstwords --tabla` resume la escalera
  semana a semana (qué se lee, sonidos máximos, grafemas que salen por
  primera vez) y CI la publica en el resumen del job.
- Mientras el cuaderno se escribe por partes, su `Perfil` dice cuántos
  días tiene ya (`dias_escritos`) y se validan exactamente esos.
- **Los dibujos**: cada día hasta `dias_con_dibujo` tiene el suyo, su
  fichero existe y su palabra es una de las leídas ese día (o, un
  viernes, de las de la semana); un día con dibujo no es *Draw*, sino
  *Colour*; la adivinanza trae dos `"otros"` distintos del suyo; *Match*
  junta al menos tres palabras, cada una con un dibujo distinto, la del
  día incluida; y ningún dibujo de `diagrams/firstwords/` se queda sin
  salir en ningún día (`comprobar_dibujos`).

## Las fases

Como *Read and Draw*, un PR por fase, cada una en verde antes de la
siguiente:

1. **El motor, el diseño y las dos primeras semanas** (días 1–10):
   `tools/fonetica.py`, el perfil `firstwords` de `tools/gen_palabras.py`
   (el cuaderno español sale idéntico, byte a byte), la tarjeta con
   botones, la portada, *How to use this book*, la tabla de sonidos, el
   mapa del año, la clave y el diploma.
2. **Otoño** (días 1–65): una letra = un sonido; desde la semana 6, las
   letras dobles, x, y, qu. Las palabras de las tarjetas son piezas de
   la historia de *Read and Draw* de cada semana (*Toby, dog, wag, nap*;
   *cat, bat, ten, yell* en Halloween; *six, top, sock, yes* en
   Navidad), y las seis letras de *Trace* (*s, d, h, m, f, b*) son las
   iniciales de una de ellas.
3. **Invierno** (días 66–130): dos palabras al día, dos o tres letras
   para un sonido (*king, night*; *torch, cherry*; *teeth, short*;
   *root, shoot*), con los 25 grafemas nuevos en alguna tarjeta antes
   del día 130 — la *ure* en *cure*, cuando Dani está malo; la *bb* en
   el muñeco de nieve *chubby*. Las adivinanzas ya se contestan
   escribiendo, así que su respuesta es siempre una palabra que se puede
   leer (*Pip, hat, Toby, sorry, pan, book*), y las letras de *Trace*
   son *g, l, c, r, n, k, j*.
4. **Primavera** (días 131–195): tres palabras al día, las otras formas
   de escribir los sonidos, la e mágica, dos consonantes seguidas
   (*party, badge*; *nest, blue, chick*; *wheel, ride*; *phone*; *June,
   summer, play*), con los 21 grafemas nuevos en alguna tarjeta antes
   del día 195 — la *oe* en *goes*, la *au* en *August*, la *e_e* en
   *these*. Los viernes, las 47 tricky words. *Trace*: *p, t, w, v, q,
   x* (*X as in next*: casi ninguna palabra que se pueda leer empieza
   por x).
5. **Verano** (días 196–260) y publicación: una frase al día, de
   *decodable text* — de dos palabras (*Amy packs.*, *Hens cluck.*) a
   cuatro (*The hens lay eggs.*, *Dani zips his bag.*) —, con *Yes or
   no?* los miércoles (*Toby barks. / Toby sings.*) y parejas escritas a
   mano en *Match* (animales y sus sonidos, contrarios, rimas, dónde
   vive cada animal, sus crías). *Trace*: *a, u, i, o, e, y, z*, con lo
   que están las 26 letras. Para leer bien las frases, el partido en
   sonidos aprende los plurales con e mágica (*cakes*: c-a_e-k-s) y dos
   trampas más (*played*, *talk*, *want*), y una tricky word con -s
   (*comes*) es la misma tricky word. El libro entero, sin
   `dias_escritos`, y los dos PDF en GitHub Pages (`first-words.pdf`,
   `first-words-bw.pdf`) con los demás.

Y después, **los dibujos para colorear** (ver arriba), otra vez un PR
por estación:

1. **El motor y el otoño** (días 1–65): el campo `"dibujo"`, *Colour*,
   *Now colour*, la adivinanza con tres dibujos y *Match* con dibujos;
   `diagrams/firstwords/kit.tex` con el reparto entero; y los dibujos
   del otoño — la furgoneta de los vecinos, Pip en su jaula, Toby (con
   cola, sin cola, moviéndola, durmiendo), la cama de Lucía, las
   castañas, Grandma tejiendo, el murciélago, el cohete de Bonfire
   Night, la tarta de Lucía, la consulta de Mrs Brown, el desayuno
   inglés, Luna en la valla, el árbol de Navidad sin estrella.
2. **Invierno** (días 66–130): los Reyes en la estantería, la cena de
   Nochebuena, el cracker, el pudin de Mr Brown, las uvas de Año Nuevo,
   la cabalgata con su camello, las botas de nieve, el muñeco gordito,
   Dani resfriado, la paloma de la paz, los dinosaurios del museo, los
   disfraces de Carnaval, la tortita en el aire, las cometas, la niña
   del barco, las alubias de clase, la mariquita. Las adivinanzas del
   invierno se contestan también escribiendo, así que su respuesta es
   siempre una de las dos palabras del día (*letter, pair, Toby, hug,
   turn, win, Pip*), y *Match*, cuando dos dibujos recientes son de la
   misma persona, elige otros (`"dibujos"`).
3. **Primavera** (días 131–195).
4. **Verano** (días 196–260), y ya todo el cuaderno se colorea.
