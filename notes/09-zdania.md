# «Zdania» — el cuaderno de frases en polaco

El séptimo cuaderno, y el segundo en polaco: lo que el cuaderno de
frases (`main.tex`, `notes/01-curriculum.md`,
`notes/02-revision-y-plan.md`) es en español, en polaco, día a día y
frase a frase. Es el paso siguiente a *Pierwsze słowa*
(`notes/08-pierwsze-slowa.md`), cuyo diploma ya lo anuncia ("Następny
krok: zeszyt ze zdaniami"): para una niña o un niño que ya lee palabras
en polaco y empieza a leer frases enteras. Todo está en polaco: las
frases, las actividades, la portada, la página para el adulto, el mapa
del año, la clave y el diploma.

Ficheros: `zdania.tex` / `zdania-bw.tex`, `body-zdania.tex`,
`frontmatter/zdania/`, `backmatter/zdania/`, `content/zdania/q1.json`…,
`content/zdania/progresion.json`, `content/zdania/palabras-trazo.json`,
y el mismo generador que el cuaderno en español, `tools/gen_days.py
--libro zdania` (lo que cambia de uno a otro está en `ZDANIA`,
`tools/libros.py`). `make zdania` lo genera, compila y comprueba.

## Lo que se mantiene igual que en el cuaderno de frases

- **260 días, 52 semanas, cuatro partes = cuatro estaciones**, con
  vacaciones incluidas, y una medalla al final de otoño, invierno y
  primavera (*Medal za jesień!*).
- **La misma historia, día a día**: cada día es el mismo día del
  cuaderno en español, traducido, con su misma actividad (salvo los
  días de más de *Pisz po śladzie*, ver abajo). Los temas de la semana
  son los de *Pierwsze słowa* (*Rodzina Lucíi*, *Toby, wesoły
  piesek*...), que ya eran los mismos: si en casa hay dos hermanos, uno
  con el cuaderno en español y otro con el polaco, esa semana leen los
  dos sobre lo mismo.
- **Una frase al día en otoño, dos en invierno, tres en primavera y
  cuatro en verano**, y sin *Odpowiedz* (*Responde*) en otoño: son las
  reglas de `FRASES`, que `ZDANIA` usa tal cual.
- **La página**: la misma plantilla, las mismas cajas, las mismas
  instrucciones (en `lang/pl.tex`, que ya las tenía todas en polaco).
- **Las barreras duras** en `make` y en CI: 1 día = 1 página, log sin
  errores ni `Overfull`, JSON y `.tex` generado al día (`--check`) y
  la escalera de palabras.

## Cómo se traduce

Un polaco natural para una niña o un niño de seis o siete años, con el
mismo sentido que la frase española, no una traducción palabra por
palabra. Algunas decisiones:

- **Los nombres**: *Lucía* y *Sofía* conservan la *í* (como en
  *Pierwsze słowa*), y todos se declinan: *Lucíi, Lucíę*; *Daniego,
  Daniemu, z Danim*; *Toby'ego, Toby'emu, z Tobym*; *Pedra*; *Rosy*.
  *Mamá* y *Papá* son *mama* y *tata*, con minúscula dentro de la frase,
  como se escribe en polaco; *la abuela*, *babcia*; *la profesora Marta*,
  *pani Marta*.
- **La historia sigue en España**: las castañas asadas del 1 de
  noviembre, los Reyes, el Carnaval, la tortilla de patata. Solo se
  adapta lo que en polaco no se entendería: el *turrón* del mercado de
  Navidad son *pierniki* (lo que huele a Navidad en un mercado polaco),
  y lo que le cantan a Lucía por su cumpleaños es *sto lat*.
- **Lo que se le dice a la niña o al niño no tiene género**, como en
  *Pierwsze słowa*: *Narysuj obiad, który chcesz przygotować*, y no
  *który przygotowałbyś / przygotowałabyś*.
- **El diálogo**, con raya (—), como en español: la plantilla sangra
  las líneas que empiezan por ella.
- **Los carteles de cada diez páginas**: *10 przeczytanych stron! Tak
  trzymaj!* El genitivo plural vale para todos los números del
  cuaderno (10, 20... 260, y 65, 130 y 195), y también para los del
  cuaderno de verano (5, 15... 65).

## La escalera, en palabras polacas

Una frase polaca tiene menos palabras que la misma en español: no hay
artículos, el sujeto a menudo no se dice y muchas preposiciones van
dentro de la terminación (*Lucía le da un hueso a Toby*, 7 palabras;
*Lucía daje Toby'emu smaczną kość*, 5). Traducidos, los 65 días del
otoño tienen de mediana 0,8 veces las palabras del español (de 0,6 a
1,1 según la frase). La escalera de `content/progresion.json` no vale
tal cual: casi ningún día llegaría a su mínimo, y el máximo nunca
frenaría nada.

`content/zdania/progresion.json` es la misma escalera, medida en
palabras polacas: `palabras_min`, el del español por 0,8, redondeado;
`palabras_max` y `frase_max`, los límites duros, el del español por
0,9, hacia arriba (el mismo ritmo de subida, con sitio para las frases
que en polaco no se acortan); `nuevas_max`, el mismo, que es solo un
aviso. Donde una traducción fiel quedaba muy por debajo del mínimo de
su semana, la frase polaca recupera lo que dice la española (*llamada
Luna*: *która nazywa się Luna*; *faltan pocos días*: *już za kilka
dni*), en vez de bajar la escalera. Con eso, el otoño queda sin errores
y con 18 días con aviso de vocabulario nuevo, los mismos que el otoño
en español.

`tools/metricas.py --libro zdania` mide lo mismo que en el cuaderno de
frases, con las palabras funcionales del polaco y una lematización
igual de sencilla, pero para una lengua que declina: se quita una
terminación y se corta a cinco letras, así que *kot, kota, kotem* son
una palabra, y *czyta, czytają, czytać* también. Los nombres del
reparto cuentan en todas sus formas (`ZDANIA.nombres_propios`).

## Las 32 letras de «Pisz po śladzie»

En español, *Traza* recorre 27 letras (de la *a* a la *z*, con la *ñ*),
una cada diez días más o menos. En polaco son 32: sin *ñ, q, v* ni *x*,
y con *ą, ć, ę, ł, ń, ó, ś, ź, ż*. Van en el orden del alfabeto, ocho
en cada parte del año: los días de *Traza* del cuaderno en español y
cinco más, dos en otoño y uno en cada una de las otras partes, en
lunes de semana impar cuyo viernes ya pide otro dibujo del mismo tema
(en otoño, el 31, la semana de los juguetes de Dani, y el 51, la del
día de lluvia).

La palabra de ejemplo de cada letra está en
`content/zdania/palabras-trazo.json` (la del español es
`content/palabras-trazo.json`), como en las cartillas polacas: *A jak
arbuz*, *Ą jak ząb*, *B jak babcia*. Donde encaja, viene del propio
cuaderno (*Dani, Luna, mama, tata, babcia*, la *huśtawka* del parque, el
*łóżko* debajo del que se esconde Toby); los nombres, con mayúscula, y
las demás, con minúscula. Ninguna palabra polaca empieza por *ą, ę, ń*
o *y*: para esas, una palabra que la lleva dentro (*ząb, gęś, koń,
motyl*). Con abecedario en su `Libro`, `tools/gen_days.py` comprueba
que cada letra que se traza es del abecedario polaco y que, con el
libro entero, están las 32 (`comprobar_trazo`).

En otoño: *a* (*arbuz*), *ą* (*ząb*), *b* (*babcia*), *c* (*cytryna*),
*ć* (*ćma*), *d* (*Dani*), *e* (*elf*) y *ę* (*gęś*).

## Lo que cambia en el motor

- `tools/libros.py`: el `Libro` `ZDANIA` (`idioma="pl"`), y tres campos
  nuevos en `Libro`, que por defecto son lo del cuaderno en español: la
  instrucción de *Połącz* (`instruccion_relaciona`; en español sigue
  siendo la frase de siempre, y en polaco,
  `\lblInstruccionRelaciona`), el fichero de las palabras de ejemplo de
  *Traza* (`palabras_trazo`) y el abecedario (`alfabeto`). Los
  abecedarios del español, el inglés y el polaco pasan aquí desde
  `tools/gen_palabras.py`, que los importa: los usan los dos
  generadores.
- `tools/gen_days.py`: la instrucción de *Połącz* y la palabra de
  ejemplo de *Traza*, del libro; `comprobar_trazo`.
- `tools/metricas.py`: el polaco (`PALABRAS_FUNCIONALES_PL`,
  `lematizar_pl`).
- `lang/pl.tex`: `\lblZdNivelPortada` (en polaco, los dos cuadernos de
  la serie se llaman *Uczę się czytać*, y la portada dice el nivel,
  como en *Pierwsze słowa*) y `\lblInstruccionRelaciona`.

Lo generado para los otros seis cuadernos es, letra por letra, lo que
era antes.

## Las fases

Un PR por fase, cada uno en verde antes del siguiente. Mientras tanto,
`ZDANIA.dias_escritos` dice cuántos días hay escritos, y se validan
exactamente esos.

1. **El motor y el otoño** (días 1–65): `ZDANIA`, la escalera en
   palabras polacas, las palabras de *Pisz po śladzie*, las páginas para
   el adulto, la clave, el diploma y los 65 días. **Hecho.**
2. **El invierno y la primavera** (días 66–195): dos y tres frases al
   día, y *Odpowiedz* desde el invierno.
3. **El verano** (días 196–260), las 32 letras, el cuaderno de verano y
   la muestra, y publicarlo.
