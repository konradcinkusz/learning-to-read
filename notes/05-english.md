# "Read and Draw" — el cuaderno en inglés

Un cuarto cuaderno, y el primero que no es en español: 260 días de
lectura **en inglés** para la misma niña, que ya lee con soltura en
español y está aprendiendo inglés en el colegio. **Todo** el cuaderno
está en inglés: el texto de cada día, las instrucciones de cada
actividad, la portada, la página "How to use this book" para el adulto,
la clave de respuestas y el diploma.

Mismo motor (`tools/gen_days.py --libro english`), mismo formato (A4,
una página por día laborable, 260 días, cuatro partes que son las cuatro
estaciones, medallas y diploma), la misma familia. Ficheros:
`english.tex` / `english-bw.tex`, `body-english.tex`,
`preamble-english.tex`, `lang/en.tex`, `frontmatter/english/`,
`backmatter/english/`, `content/english/q1.json`…`q4.json`,
`content/english/progresion.json`, `content/english/vocabulario-base.json`,
`diagrams/english/`, `tools/english.py`. `make english` lo genera,
compila y comprueba; `make all-formats` hace los cuatro cuadernos en
color y en blanco y negro.

## Qué es, y por qué así

El encargo: un cuaderno completo **un nivel por debajo de "Leo con
lupa"** (`notes/04-nivel-lupa.md`), para aprender a leer en inglés. El
nivel de abajo en español ya existe (el cuaderno de frases), así que
este se escribe en inglés; y del nivel de "Leo con lupa" conserva dos
cosas, más sencillas:

1. **Oraciones compuestas desde el primer día.** Los textos son cortos
   (de ~30 palabras en otoño a ~70 en verano: la longitud del cuaderno
   de frases, no la de "Leo con lupa"), pero no son frases sueltas:
   cada texto tiene al menos una oración subordinada (*because*,
   *when*, *who*, *that*, *if*, *before*, *after*...), dos desde el
   invierno y tres en verano, además de las coordinadas con *and*,
   *but* y *so*.
2. **Cada actividad es un análisis de lo leído, pero muy sencillo:**
   casi siempre dibujar, colorear, marcar, rodear o unir, casi nunca
   escribir más de una palabra. Dibujar *exactamente* lo que dice el
   texto (cuántos, de qué color, dónde), colorear un dibujo como dice el
   texto, dibujar cosas en su sitio en una escena (*in*, *on*,
   *under*, *next to*...), unir las dos mitades de una frase compuesta
   del texto, rellenar la palabra que falta... Siempre hay que volver al
   texto para hacerla. Nada de tablas lógicas, mapas con rutas,
   mensajes cifrados ni casos: eso es "Leo con lupa".

Es, por tanto, "Leo con lupa" un nivel más abajo y en otro idioma: la
misma página (el texto en párrafos arriba, la caja de actividad que
llena lo que queda de página abajo), con la letra más grande, textos
del largo del cuaderno de frases y actividades de un nivel que se puede
hacer leyendo en un idioma que todavía se está aprendiendo.

**Inglés británico** (*colour*, *favourite*, *Mum*, *neighbour*, *Mr*
sin punto): es el que se enseña en los colegios de España, y el de los
vecinos nuevos, que vienen de Londres. `tools/english.py` lo comprueba.

## El reparto

La familia de siempre, en el mismo año que "Leo con lupa" (Lucía cumple
8 en la semana 9, Dani 6 en la 35, el verano en el pueblo de la abuela,
la vuelta al cole en la semana 52), y unos vecinos nuevos que son la
razón de que todo esté en inglés: vienen de Londres y todavía no hablan
español.

| Personaje | Quién es |
|---|---|
| **Lucía** | protagonista; 7 años, cumple 8 en noviembre (semana 9). Sabe algo de inglés del colegio, y ayuda a Amy |
| **Dani** | su hermano, 5 años (cumple 6 en mayo, semana 35); le encantan los dinosaurios |
| **Toby** | el perro: marrón, de orejas largas, con su pelota roja; le dan miedo los truenos (y los petardos) |
| **Mum** y **Dad** | de fondo |
| **Grandma Rosa** | la abuela, la madre de Mum; vive en la ciudad y pasa el verano en su casa del pueblo |
| **Amy Brown** *(nueva)* | la vecina de al lado, de Londres; 7 años, cumple 8 en primavera (semana 27); pelo rojo y rizado, mochila morada con dos chapas (una estrella amarilla y un gato negro). En la clase de Lucía. Cuando no sabe una palabra en español, **la dibuja** |
| **Sam Brown** *(nuevo)* | su hermano, 5 años; le encantan los dinosaurios (siempre lleva uno de juguete), así que se hace amigo de Dani |
| **Mrs Brown** y **Mr Brown** *(nuevos)* | Mrs Brown es veterinaria en la clínica del barrio; Mr Brown trabaja en casa y cocina (tortitas, *scones*, el desayuno inglés) |
| **Pip** *(nuevo)* | el loro de los Brown: verde, con las alas azules, la cola roja y el pico amarillo. Habla: *Hello!*, y en la semana 3 aprende *Toby!* |
| **Marta** | la maestra de Lucía y de Amy |
| **Pedro** y **Luna** | el vecino y su gata blanca (un ojo verde y otro azul, collar con cascabel), que vigila la jaula de Pip |
| **Tomás**, **Julián** y **Lola** | los mismos de «Leo con lupa»: el bibliotecario del barrio (invierno), y el granjero de la granja escuela y su cabra más curiosa, de manchas marrones (primavera) |
| **Andrés**, **Bigotes**, **Martín** | el pueblo, en verano: el vecino de las abejas, su gato blanco y naranja, y el amigo de Dani |

Todos los nombres propios del reparto están en `tools/libros.py`
(`ENGLISH.nombres_propios`): `tools/metricas.py` no los cuenta como
vocabulario nuevo, y `tools/english.py` solo deja pasar letras que no
son del inglés (la í de *Lucía*) en esos nombres.

## La página

- La cabecera de siempre, en inglés: *Day 12 (Week 3 · Part 1)*, el
  tema, *Date*, *Read: alone / with help / with difficulty*, *Notes*.
  «Part» y no «Term»: las cuatro partes del año son las estaciones, no
  los tres trimestres del curso inglés.
- El texto del día, en la caja verde, a 20 pt en otoño y 17 pt en verano
  (`\fuenteIngles`). El título de la caja dice cómo leerlo: con un
  adulto y luego sola (otoño), en voz alta y dos veces (invierno), como
  quien cuenta un cuento (primavera), primero en silencio (verano).
- La actividad, en una caja que llena lo que queda de página
  (`actividadIngles`), con un **icono** delante del título: un lápiz
  para dibujar, una cera para colorear, una casilla marcada para *Yes or
  no?*... Los mismos iconos, con su palabra, están en la página *The
  words in this book* del principio: quien empieza a leer en inglés
  reconoce antes un lápiz que la palabra *draw*.

Al principio del cuaderno: portada, *How to use this book* (para el
adulto), *The words in this book* (los iconos y las palabras de las
instrucciones, y las palabras de lugar dibujadas: *in*, *on*, *under*,
*next to*, *behind*, *in front of*, *between*), *Who's who?* (la familia
con un recuadro para dibujar a cada uno, y tres recuadros con una
interrogación para los vecinos nuevos, que se descubren en la primera
semana) y *The year in this book*.

## La semana

Cada semana es un capítulo de la historia, de lunes a viernes. El ciclo,
con variaciones cuando el tema lo pide:

| Día | Actividad | Qué entrena |
|---|---|---|
| lunes | **Read and draw** (`dibuja`) | el texto describe algo con detalle (cuántos, de qué color, dónde) y se dibuja tal cual; abajo, 2–4 preguntas para comprobar el dibujo con el texto delante |
| martes | **Yes or no?** (`si_no`) / **Read and circle** (`rodea`), una semana cada una | los detalles, sin escribir |
| miércoles | **Read and colour** (`colorea`), **Where is it?** (`donde`), **Read and match** (`relaciona`) o **Match the halves** (`mitades`) | dibujar a partir del texto; unir |
| jueves | **Match the halves**, **The missing words** (`huecos`), **What happened first?** (`ordena`), **Riddle** (`adivina`) o **Word hunt** (`busca`) | la frase compuesta (sus dos mitades, la palabra que falta), el orden, la palabra |
| viernes | **Draw the story** (`vinetas`) en las semanas impares; **Look back** (`repasa`) en las pares | la historia entera de la semana en tres dibujos; repasar dos semanas |

- Cada 10 días (los viernes de las semanas pares) la actividad lleva un
  **banner** ("10 pages read! Well done!"). Los días 65, 130 y 195
  cierran una parte del año, llevan banner, y detrás va la página de
  medalla (*Autumn medal!*, *Winter medal!*, *Spring medal!*). El 260
  termina en el diploma.

## Las actividades

Todas usan la misma caja (`actividadIngles`, `preamble-english.tex`).
Campos en el JSON — ver `tools/english.py` para el detalle:

| Tipo | Título | Campos | Qué se comprueba al generar |
|---|---|---|---|
| `dibuja` | Read and draw | `prompt`, `comprueba` (2–4 preguntas), `clave`, `rotula` (opcional: palabras para escribir en el dibujo) | — |
| `colorea` | Read and colour | `prompt`, `dibujo` (`diagrams/english/<dibujo>.tex`), `clave` | el dibujo existe |
| `donde` | Where is it? | `prompt`, `escena` (`diagrams/english/`), `cosas` (2–4: qué dibujar, nunca dónde), `clave` | la escena existe |
| `si_no` | Yes or no? | `afirmaciones` (3–5), `respuestas` (`yes`/`no`) | una respuesta por frase; de las dos |
| `rodea` | Read and circle | `preguntas` (2–4, cada una con `pregunta`, `opciones` (2–3) y `solucion`) | la solución es una de las opciones |
| `relaciona` | Read and match | `pares` (3–5), `instruccion` (opcional) | — |
| `mitades` | Match the halves | `mitades` (3–4 pares `[principio, final]`) | **cada frase, entera, está tal cual en los textos de la semana hasta hoy** |
| `ordena` | What happened first? | `sucesos` (3–4, en orden: se barajan solos), `instruccion` (opcional: «Put the recipe in order...») | — |
| `huecos` | The missing words | `frases` (3–4, con `___`), `soluciones`, `extra` (opcional: palabras que sobran) | **cada frase, con su palabra, está tal cual en los textos de la semana hasta hoy** |
| `busca` | Word hunt | `instruccion`, `soluciones` (2–4 palabras) | **cada palabra está en el texto de hoy** |
| `adivina` | Riddle | `adivinanza` (con `\n`), `respuesta` | — |
| `vinetas` | Draw the story | `instruccion`, `pies` (3) | — |
| `repasa` | Look back | `checklist` (2–4), `prompt`, `banner` | — |
| `crea` | Your turn | `prompt`, `lineas` (0–3) | — |

Cualquier actividad admite además `banner`. Todas menos `vinetas`,
`repasa` y `crea` llevan su solución a la clave de respuestas del
final.

El texto del día (`texto`) es una lista de párrafos, con las marcas de
"Leo con lupa": `> ` una nota, un cartel, una postal o una carta que los
personajes leen (recuadro blanco), `- ` un elemento de lista, `\n` un
salto de línea.

## La escalera

Valores al final de cada parte; en medio crecen de forma lineal, semana
a semana (`content/english/progresion.json`, comprobado por
`tools/metricas.py --libro english`):

| Dimensión | inicio P1 | final P1 | final P2 | final P3 | final P4 |
|---|---|---|---|---|---|
| palabras/página | 25–35 | 32–45 | 42–55 | 50–65 | 58–75 |
| máx. palabras en una oración | 12 | 13 | 14 | 15 | 16 |
| subordinadas por texto (mín.) | 1 | 1 | 2 | 2 | 3 |
| tiempo verbal | presente simple, *has got*, *can* | + *there is/are* | + presente continuo, *like* + -ing, comparativos | pasado simple: la historia se cuenta en pasado | + *going to*, futuro |
| géneros | narración, diálogo | + nota, cartel | + receta, lista | + invitación, texto informativo | + postal, carta, diario, poema |
| letra del texto | 20 pt | 20 pt | 19 pt | 18 pt | 17 pt |

`palabras_max`, `frase_max` y `subordinadas_min` son límites duros
(`make check-english` falla); `palabras_min` y el vocabulario nuevo
(`nuevas_max`) son avisos. El vocabulario nuevo se cuenta contra
`content/english/vocabulario-base.json`, las palabras que se dan por
sabidas del inglés del colegio (colores, números, la familia, animales,
comida, la casa, el colegio, verbos y adjetivos muy frecuentes): lo que
mide es cuántas palabras de verdad nuevas trae cada día.

Las subordinadas se cuentan por sus nexos (*because*, *when*, *if*,
*while*, *before*, *after*, *until*, *who*, *which*, *that*, *where*...;
`SUBORDINANTES_EN` en `tools/metricas.py`). Una palabra así al principio
de una pregunta (*Where is Pip?*) no cuenta; *that* demostrativo en
medio de una frase sí se cuela — es una aproximación, igual que en
español, así que al escribir un día conviene que su subordinada lo sea
de verdad.

## Las cuatro partes del año

| Parte | Semanas | Días | Época | Hilo |
|---|---|---|---|---|
| 1 | 1–13 | 1–65 | otoño | **Los vecinos nuevos.** Llega una furgoneta: los Brown, de Londres, con Amy, Sam y Pip, el loro que habla. Amy empieza en la clase de Lucía. Halloween a la inglesa, el cumpleaños de Lucía, la Navidad que se acerca |
| 2 | 14–26 | 66–130 | invierno | **Dos Navidades.** Crackers y calcetines en casa de Amy, las uvas y los Reyes en la de Lucía; nieve, Pancake Day, Carnaval, una cometa |
| 3 | 27–39 | 131–195 | primavera | **En pasado.** El cumpleaños de Amy, la búsqueda de huevos de Pascua, Toby y Pip se pierden (y cada uno encuentra al otro), el Día del Libro, las orugas, el día de la madre, el cumpleaños de Dani, la granja escuela, el último día de colegio |
| 4 | 40–52 | 196–260 | verano | **Postales, cartas y un diario.** Amy pasa julio en Londres y Lucía el verano en el pueblo de la abuela: las gallinas, el río, las abejas de Andrés, las estrellas fugaces, una tormenta; en agosto, los Brown llegan para las fiestas. Vuelta a la ciudad y al cole: Dani y Sam, en la clase de Marta |

### Parte 1 — otoño (presente)

| Sem. | Tema | Historia | Lunes | Martes | Miércoles | Jueves | Viernes |
|---|---|---|---|---|---|---|---|
| 1 | New neighbours | una furgoneta blanca; llegan los Brown en un coche verde: Amy (pelo rojo y rizado), Sam (con su dinosaurio) y Pip (verde, alas azules, cola roja, pico amarillo), que dice *Hello!*; Mum les lleva una tarta | dibuja (la furgoneta) | si_no | colorea (Pip) | relaciona (quién es quién) | vinetas |
| 2 | Amy's first day | Amy en la clase de Lucía; cuando no sabe una palabra, la dibuja; Mrs Brown es veterinaria; un cartel de bienvenida | dibuja (la mochila) | rodea | mitades | huecos | repasa |
| 3 | Toby meets Pip | la jaula de Pip en el jardín, junto a la valla; Pip aprende a decir *Toby!* y Toby corre a la valla cada vez, pero no hay nadie; Amy le enseña a Pip otra palabra, *Biscuit!*, y cada vez que la dice Toby se lleva una galleta | dibuja (los dos jardines) | si_no | donde (el jardín) | ordena | vinetas |
| 4 | Lucía's house | Lucía le enseña su casa a Amy: la cocina, el salón, su cuarto, la cesta de Toby | dibuja (el cuarto de Lucía) | rodea | donde (el cuarto) | busca (las habitaciones) | repasa |
| 5 | Autumn in the park | hojas rojas, amarillas y marrones; los patos del estanque; Amy enseña a jugar a los *conkers* | dibuja (el árbol) | si_no | colorea | mitades | vinetas |
| 6 | Grandma Rosa | la abuela teje una bufanda para Dani (rayas verdes y azules, dos pompones rojos); castañas asadas; el cuento del ratón que vive en un reloj, y Amy canta *Hickory, dickory, dock* | dibuja (la bufanda) | rodea | relaciona | huecos | repasa |
| 7 | Halloween | calabazas; disfraces (Amy de bruja, Sam de fantasma, Dani de dinosaurio, Lucía de gato negro); *trick or treat*; Toby y las máscaras; Pip dice *Boo!* | dibuja (los disfraces) | si_no | colorea (la calabaza) | adivina | vinetas |
| 8 | A rainy week | lluvia, botas de agua, paraguas, charcos; Toby lleno de barro; Amy cuenta la *Bonfire Night* | dibuja (Lucía bajo la lluvia) | rodea | donde (la entrada: abrigos, botas, paraguas) | mitades | repasa |
| 9 | Lucía is eight! | el cumpleaños, como en «Leo con lupa»: la tarta redonda de chocolate con ocho velas alrededor y tres fresas, la piedra con forma de corazón de Dani, el gorro que Dani le pone a Toby, y la abuela que vuelve del pueblo el sábado con un bizcocho de limón; Amy le regala un libro en inglés | dibuja (la tarta) | si_no | relaciona (quién hace qué) | ordena | vinetas |
| 10 | At the vet | Toby va a la clínica de Mrs Brown; en la sala de espera, un conejo, una tortuga y un gatito | dibuja (la sala de espera) | rodea | relaciona (cada animal con su dueño) | huecos | repasa |
| 11 | Mr Brown's kitchen | Mr Brown hace *scones* (receta) y un desayuno inglés; la lista de la compra | dibuja (el desayuno) | si_no | donde (la cocina) | ordena (la receta) | vinetas |
| 12 | Luna and Pip | Luna, la gata de Pedro, vigila la jaula de Pip; Pip le dice *Go away!*; al final, Luna solo quería jugar | dibuja (Luna) | rodea | mitades | adivina | repasa |
| 13 | Christmas is coming | la función de Navidad del colegio (Lucía y Amy cantan *Jingle Bells*); las tarjetas de Amy; el árbol de Navidad; los Brown pasan la Navidad en España | dibuja (el escenario) | si_no | colorea (el árbol) | busca | repasa + medalla |

### Parte 2 — invierno (presente continuo, *like* + -ing, comparativos)

Las fiestas coinciden con las de «Leo con lupa», que es el mismo año: el
belén en la balda más alta, la Nochebuena en casa de la abuela, los
cuatro cuencos de uvas (rojo de Papá, azul de Mamá, verde de Lucía,
amarillo de Dani), la carta de Dani con la linterna y la pelota roja
para Toby, la nieve en el patio del colegio con el muñeco de la escoba,
el desfile de Carnaval del martes (Lucía de detective, el antifaz
morado) y el mirlo del jardín. Nunca se desvela ningún caso de «Leo con
lupa»: quién mueve los Reyes o de quién es el antifaz se queda sin
decir.

| Sem. | Tema | Historia | Lunes | Martes | Miércoles | Jueves | Viernes |
|---|---|---|---|---|---|---|---|
| 14 | The holidays begin | el belén (los Reyes se acercan cada noche, y nadie sabe quién los mueve); el calcetín de Amy; Navidad en Inglaterra y en España; Pip grita *Merry Christmas!* | dibuja (el belén) | rodea | relaciona | huecos | repasa |
| 15 | Two Christmases | la Nochebuena en casa de la abuela; los calcetines de Amy y Sam; la comida de Navidad con los Brown: *crackers* y *Christmas pudding* | dibuja (la mesa) | si_no | donde (el salón) | mitades | vinetas |
| 16 | New Year | las doce uvas; Amy practica con pasas; los fuegos, y Toby debajo de la cama; los deseos del año nuevo | dibuja (la bandeja de las uvas) | si_no | ordena | busca | repasa |
| 17 | The Three Kings | la carta de Dani, la cabalgata, el *King cake* de los Brown: Amy encuentra el rey y Sam el haba | dibuja (la carta) | rodea | colorea (el roscón) | huecos | vinetas |
| 18 | Snow! | el muñeco del patio del colegio; bolas de nieve; el muñeco del jardín; Toby en la nieve y Pip: *Brrr!* | dibuja (el muñeco del patio) | rodea | colorea (el muñeco del jardín) | mitades | repasa |
| 19 | Dani is ill | Dani con catarro; la tarjeta de Sam con una adivinanza | dibuja (Dani en la cama) | si_no | donde (el cuarto de Dani) | adivina | vinetas |
| 20 | Friends again | el Día de la Paz; Lucía y Amy se enfadan por un juego, y hacen las paces; un poema | dibuja (la paloma) | rodea | mitades | ordena | repasa |
| 21 | Dinosaur day | Mr Brown lleva a Dani y a Sam al museo: el diplodocus y el tiranosaurio (más largo que, tan grande como) | dibuja (los dos dinosaurios) | si_no | relaciona | busca | vinetas |
| 22 | Carnival and pancakes | los disfraces; el desfile del martes; ese mismo martes, Pancake Day en casa de los Brown (receta); la última tortita cae encima de Toby | dibuja (el disfraz de Lucía) | rodea | ordena (la receta) | mitades | repasa |
| 23 | A windy day | la cometa de Dad, la de Amy y Sam; el sombrero que sale volando | dibuja (la cometa) | si_no | colorea (la cometa) | huecos | vinetas |
| 24 | The library | el rincón inglés de la biblioteca; Tomás, el bibliotecario; el primer libro en inglés de Lucía | dibuja (el rincón inglés) | rodea | donde (la biblioteca) | adivina | repasa |
| 25 | Beans in the classroom | la clase planta judías; cómo crece una judía; Lucía planta la suya en el huerto de Papá | dibuja (el vaso) | si_no | mitades | ordena | vinetas |
| 26 | Spring is coming | las primeras flores, el mirlo, una mariquita, una mariposa; Pip dice todas sus palabras | dibuja (el jardín) | rodea | colorea (la mariposa) | busca | repasa + medalla |

### Parte 3 — primavera (pasado)

La historia se cuenta en pasado simple; el diálogo, lo que dicen las
notas y los textos informativos (cómo se juega a *pass the parcel*, la
vida de una mariposa, la tarjeta de datos del zoo, cómo son las cabras
y las ovejas) siguen en presente. Como en invierno, las fechas son las
de «Leo con lupa»:

- las vacaciones de Semana Santa en la semana 28, con las torrijas del
  sábado, que Lucía hace sola y fríe la abuela;
- el Día del Libro, con su intercambio secreto, en la 31;
- el día de la madre en la 34, con la misma bandeja: dos tostadas con
  forma de corazón, el zumo de naranja a la izquierda, el café a la
  derecha y la rosa amarilla detrás. La rosa, escondida en la nevera; la
  lleva Dani, Papá lleva la bandeja y Toby vigila la puerta;
- el sexto cumpleaños de Dani en la 35: la tarta redonda de chocolate
  con seis velas azules y un dinosaurio verde de azúcar rodeado de
  fresas, y la búsqueda del tesoro de Lucía (la almohada, la lavadora,
  la nevera y el cuaderno rojo debajo de la cama);
- los dos días en la granja escuela en la 37: Julián, la cabra Lola que
  mordisquea la manga de Lucía, las cabras comiéndose las coles;
- la fiesta de fin de curso y el último día de clase, el viernes 195, en
  la 39.

No se desvela nada: quién abrió la puerta del corral no se dice, y ni la
cápsula ni la carta de Marta salen.

| Sem. | Tema | Historia | Lunes | Martes | Miércoles | Jueves | Viernes |
|---|---|---|---|---|---|---|---|
| 27 | Amy is eight | la invitación morada; *pass the parcel* y *musical chairs*; la tarta con forma de Pip; las bolsas de la fiesta | dibuja (la invitación) | si_no | relaciona (los regalos) | ordena (la fiesta) | vinetas |
| 28 | Easter | los huevos pintados; los *hot cross buns* y las torrijas; Mr Brown esconde huevos de chocolate en el jardín (el chocolate, nunca para Toby); un nido con tres huevos azules que no se toca | dibuja (los huevos) | rodea | donde (el jardín) | huecos | repasa |
| 29 | Toby is lost | Toby persigue una ardilla en el parque y se pierde; lo encuentra Pip, que grita *Toby! Biscuit!* desde su jaula | dibuja (Toby y la ardilla) | si_no | donde (el parque) | mitades | vinetas |
| 30 | Where is Pip? | Pip se escapa mientras limpian su jaula; el cartel LOST PARROT; una pluma verde en la valla; Toby lo encuentra en el castaño y Amy lo baja con un trozo de manzana | dibuja (el cartel) | rodea | relaciona (quién hizo qué) | ordena | repasa |
| 31 | Book Day | el 23 de abril, y el *World Book Day* inglés, en marzo; el libro de Amy, *Pip and the Big Tree*; el intercambio secreto | dibuja (la portada) | si_no | mitades | adivina (el reloj) | vinetas |
| 32 | The caterpillars | las orugas de la clase, la crisálida y las mariposas; la vida de una mariposa | dibuja (la caja de las orugas) | rodea | colorea (la mariposa) | busca (las cuatro etapas) | repasa |
| 33 | Sam's new bike | la bici roja, sin ruedines: Sam se cae, aprende a frenar y a girar, y da la vuelta al estanque él solo | dibuja (la bici) | si_no | ordena | mitades | vinetas |
| 34 | Mum's day | el desayuno sorpresa; la tarjeta con flores; en Inglaterra, el día de la madre es en marzo | dibuja (la bandeja) | rodea | colorea (las flores) | huecos | repasa |
| 35 | Dani is six | la tarta; la búsqueda del tesoro; los regalos (una bici azul, un jersey con un dinosaurio...) | dibuja (la tarta) | si_no | relaciona (los regalos) | adivina (la nevera) | vinetas |
| 36 | The zoo | las jirafas, los elefantes, el hipopótamo, los monos y los pingüinos: más alto que, tan alto como; la tarjeta de datos | dibuja (las jirafas) | rodea | mitades | busca (los animales) | repasa |
| 37 | The farm | la granja escuela: Lola, las cabras en el huerto, las ovejas, el burro y las gallinas | dibuja (el corral) | si_no | relaciona (cómo es cada animal) | ordena | vinetas |
| 38 | Sports day | el equipo amarillo; la carrera del huevo y la cuchara, la de sacos y la de tres piernas | dibuja (el equipo) | rodea | mitades | huecos | repasa |
| 39 | The last day of school | la tarjeta para Marta; la fiesta de fin de curso; la clase decorada; los planes del verano; Pip: *See you soon!* | dibuja (la tarjeta) | si_no | donde (la clase) | relaciona (el verano) | repasa + medalla |

### Parte 4 — verano (pasado y futuro; postales, cartas, diario, poemas)

El pasado sigue contando la historia, y el futuro entra con los planes
(*going to*, *will*): lo que Amy va a hacer en Londres, lo que harán el
verano que viene. Los géneros nuevos:

- la postal de Amy y la carta de Lucía (semana 42);
- el programa de las fiestas (47);
- el diario de Lucía, que es toda la semana 50;
- los poemas de Lucía (el de las abejas, el de las estrellas y, con
  Amy, el del año entero, que es la penúltima página).

Lo que pasa en el pueblo es, otra vez, lo de «Leo con lupa»:
- el viaje, el sábado de la semana 40;
- Andrés y Bigotes, blanco y naranja;
- en la 44, el traje de apicultor de Andrés: blanco, con guantes
  amarillos hasta los codos, sombrero de paja con red y el ahumador en
  la derecha;
- en la 45, la Osa Mayor (el cazo de siete estrellas, «el reloj de la
  noche» del bisabuelo relojero) y la noche del 12 de agosto en el
  jardín del molino, con la adivinanza de las estrellas;
- en la 47, las fiestas: los banderines rojos y amarillos, el escenario
  delante de la iglesia, el puesto de churros con su toldo de rayas
  verdes y blancas, el programa, el concurso que gana la adivinanza de
  la lupa de Lucía, Dani y Martín, y los fuegos del sábado;
- en la 50, la despedida del último lunes de agosto: la miel de romero
  con la abeja con lupa, la abuela que se queda hasta octubre, el sobre
  de Martín y el cómic de Dani en el que no sale Toby;
- en la 51, la mochila roja con el tiranosaurio verde y el estuche de
  tres cremalleras;
- en la 52, Paco en la puerta y la nube de Marta con las gotas de papel
  (la de Dani, azul y en el centro).

No se desvela nada:
- ni lo que se le olvidó a Dani en la maleta;
- ni el mapa de Rosa ni su tesoro;
- ni el erizo ni las hormigas;
- ni quién escribió el nombre de Dani en sus cosas.

| Sem. | Tema | Historia | Lunes | Martes | Miércoles | Jueves | Viernes |
|---|---|---|---|---|---|---|---|
| 40 | Packing | la maleta de Amy; el taxi a Londres (Sam le deja a Dani su dinosaurio); la maleta verde de Dani; la mochila de Lucía | dibuja (la maleta de Amy) | rodea | busca (los colores) | mitades | repasa |
| 41 | In the village | las cinco gallinas, el limonero, Andrés y Bigotes; la sandía en la pila; el pueblo; la postal de Lucía | dibuja (las gallinas) | si_no | donde (el patio) | huecos | vinetas |
| 42 | A postcard from London | la postal de Amy: la torre del reloj, el autobús de dos pisos, las ardillas grises; el autobús de Dani; la carta de Lucía; los buzones amarillos y los rojos | dibuja (la postal) | rodea | colorea (el autobús) | ordena | repasa |
| 43 | At the river | la merienda, el agua fría, la roca, los peces y la rana; la adivinanza del río; el barquito | dibuja (la merienda) | si_no | mitades | adivina (el río) | vinetas |
| 44 | Andrés and his bees | el traje de apicultor; cómo viven las abejas; tres mieles de tres colores; el poema de la abeja; una abeja en el brazo de Dani | dibuja (Andrés con su traje) | rodea | relaciona (las mieles) | huecos | repasa |
| 45 | Shooting stars | el cazo de siete estrellas (*the Plough*); qué son las estrellas fugaces; la noche en el jardín del molino; el poema de Lucía y la adivinanza de las estrellas | dibuja (las siete estrellas) | si_no | ordena | busca | vinetas |
| 46 | The storm | tres nubes negras y un rayo sobre la torre; se va la luz: velas y cuentos; el patio después de la tormenta; la carta de Amy | dibuja (la tormenta) | rodea | donde (el patio) | ordena | repasa |
| 47 | The village festival | la plaza en fiestas; el programa; los churros; el concurso de adivinanzas; los Brown llegan para los fuegos | dibuja (la plaza) | si_no | relaciona (quién tomó qué) | mitades | vinetas |
| 48 | Amy in the village | el pueblo dibujado desde el puente; Sam recupera su dinosaurio; el helado de tres bolas; el río; los *scones* de Mr Brown | dibuja (el pueblo) | rodea | colorea (el helado) | huecos | repasa |
| 49 | The treasure hunt | Lucía y Amy preparan una búsqueda del tesoro para Dani, Sam y Martín: el mapa del patio, las adivinanzas, las gafas de bucear | dibuja (el mapa) | si_no | adivina (el gallinero) | ordena | vinetas |
| 50 | Back to the city | el diario de Lucía: la miel de Andrés, el viaje, el jardín de casa (Pip: *Hello, Toby!*), el sobre de Martín, el cómic de Dani | dibuja (el tarro de miel) | rodea | donde (los jardines) | mitades | repasa |
| 51 | Ready for school | la mochila y el estuche de Dani; los consejos de Lucía para leer; la papelería; el uniforme inglés | dibuja (la mochila) | si_no | relaciona (quién eligió qué) | huecos | vinetas |
| 52 | Back to school | la nube de Marta; el dibujo de Sam; la clase nueva de Lucía y Amy; el poema del año; Pip: *Hello, Lucía! Hello, Amy! Hello, Toby!* | dibuja (la nube) | rodea | donde (la clase) | busca (las estaciones) | repasa + diploma |

Las tablas de las cuatro partes son lo que hay escrito. Sobre el plan
del principio, el verano cambió así:
- las estrellas fugaces, el 12 de agosto como en «Leo con lupa»;
- la tormenta pasa a la semana 46;
- el día de playa desaparece, y el helado se lo toma Amy en el pueblo;
- los Brown llegan para las fiestas.

## Los dibujos

`colorea` y `donde` necesitan un dibujo de línea hecho de antemano, en
`diagrams/english/` (TikZ, trazo negro de 1,4 pt sobre blanco, cada
parte cerrada para poder colorearla): un personaje u objeto para
colorear (Pip, un árbol de otoño, una calabaza, un árbol de Navidad, un
roscón, un muñeco de nieve, una cometa, una mariposa, unas flores en una
maceta, un autobús de Londres, un helado) o una escena donde dibujar
cosas en su sitio (los dos jardines, el cuarto de Lucía, la entrada, la
cocina, el salón de los Brown, la biblioteca, el parque, la clase y el
patio de la abuela, en el pueblo). Varios se usan más de una vez, con
otros colores u otras cosas que dibujar:
- la mariposa del invierno vuelve en primavera, naranja;
- el jardín de Pip es donde Mr Brown esconde los huevos de Pascua, y
  adonde vuelven todos al final del verano;
- el patio de la abuela sale antes y después de la tormenta;
- en la clase de Marta se prepara la fiesta de fin de curso, y es
  también la clase nueva de Lucía y Amy en septiembre.

## Reglas para escribir (y revisar) un día

- Inglés británico, natural y sencillo, el de un libro de lectura para
  niños de 7–8 años que aprenden inglés: frases cortas, vocabulario de
  todos los días, y las palabras nuevas de una en una (el aviso de
  `nuevas_max` lo vigila). Narrador en tercera persona.
- Cada texto, dentro de la escalera de su semana: palabras, frase más
  larga, y al menos las subordinadas que pide. Variedad de nexos: no
  solo *because*.
- Todo lo que pide la actividad está en el texto de ese día (o en los de
  días anteriores de la misma semana, y entonces la instrucción lo
  dice). En `dibuja`, el texto da los detalles y las preguntas de
  comprobación solo los nombran (*What colour is the van?*), nunca los
  repiten. En `donde`, la lista dice qué dibujar, nunca dónde.
- Diálogo entre comillas “ ”; el apóstrofo, recto (`'`: LaTeX ya lo
  imprime curvo). Nada de rayas de diálogo, ¿ ¡ « » ni letras con tilde
  fuera de los nombres del reparto: `tools/english.py` lo comprueba.
- Seguridad y valores, como en los otros cuadernos: los perros no comen
  chocolate ni uvas; un loro no se saca de la jaula sin un adulto.

## Las fases

El cuaderno se escribió en cinco fases, cada una con su PR, fusionado
en verde antes de empezar la siguiente:

1. **El motor** (este documento, `tools/english.py`, `lang/en.tex`,
   `preamble-english.tex`, portada y demás páginas, CI) con las dos
   primeras semanas escritas, para que haya algo real que generar,
   compilar y comprobar.
2. **Parte 1**, otoño: días 1–65.
3. **Parte 2**, invierno: días 66–130.
4. **Parte 3**, primavera: días 131–195.
5. **Parte 4**, verano: días 196–260; el cuaderno, completo, se publica
   en GitHub Pages con los otros tres.

Mientras tanto, `ENGLISH.dias_escritos` (en `tools/libros.py`) decía
cuántos días había escritos, y `tools/gen_days.py` exigía exactamente
esos, del 1 en adelante y sin huecos, en vez de los 260 de un libro
terminado. En la fase 5 se quitó, y el libro volvió a la regla de
siempre: los 260 días o nada. El campo sigue en `Libro` para el próximo
cuaderno que se escriba por partes.
