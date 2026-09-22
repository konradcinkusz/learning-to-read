# "Leo con lupa" — nivel 3

El tercer cuaderno del repositorio, después de *Primeras palabras*
(nivel 1, `notes/03-nivel-palabras.md`) y del cuaderno de frases
(nivel 2, `notes/01-curriculum.md`): un año más de lectura diaria para
la misma niña, un nivel por encima del cuaderno de frases. Mismo motor
(`tools/gen_days.py --libro lupa`), mismo formato (A4, una página por
día laborable, 260 días, cuatro trimestres que son las cuatro
estaciones), mismos personajes un año después. Ficheros: `lupa.tex` /
`lupa-bw.tex`, `body-lupa.tex`, `preamble-lupa.tex`,
`frontmatter/lupa/`, `backmatter/lupa/`, `content/lupa/q1.json`…`q4.json`,
`tools/lupa.py`. `make lupa` lo genera, compila y comprueba; `make
all-formats` hace los tres cuadernos en color y en blanco y negro.

Ver `notes/01-curriculum.md` y `notes/02-revision-y-plan.md` para el
cuaderno de frases: este documento solo cuenta lo que cambia.

## Qué cambia respecto al cuaderno de frases

El cuaderno de frases termina con una lectora que lee con soltura
páginas de cuatro frases compuestas (55–70 palabras, frases de hasta 16
palabras, "porque", "cuando", "aunque", diálogo con raya). "Leo con
lupa" sube en las dos cosas que el cuaderno de frases apenas tocaba:

1. **El texto está hecho de oraciones complejas.** Subordinadas de
   todo tipo — relativas (*el cuaderno que le regaló la abuela*, *la
   caseta donde se reúne el club*), causales (*porque*, *ya que*,
   *como*), concesivas (*aunque*), temporales (*cuando*, *mientras*,
   *antes de que*, *en cuanto*, *hasta que*), condicionales (*si*),
   finales (*para que*), consecutivas (*así que*, *tan... que*) y
   comparativas — y en párrafos de verdad, no una frase por línea. Lo
   que crece durante el año es la longitud del texto, la de la frase y
   el número de subordinadas, pero también el tiempo verbal (presente →
   narración en pasado → pluscuamperfecto y subjuntivo → estilo
   indirecto) y el género (narración, nota, lista, carta, receta,
   instrucciones, entrevista, texto informativo, diario, poema,
   noticia).
2. **Cada actividad obliga a analizar lo leído.** No basta con haber
   entendido la idea general: hay que volver al texto y buscar, comparar
   y deducir. Dibujar *exactamente* lo que describe (dónde está cada
   cosa, cuántas hay, de qué color), resolver un caso con las pistas
   repartidas por la semana, completar una tabla lógica, seguir unas
   indicaciones en un mapa, cazar los errores de un resumen equivocado,
   descifrar un mensaje con un código que se explica en el texto,
   ordenar sucesos contados con "antes de que" y "después de que",
   justificar una respuesta con una frase del texto.

El hilo que lo une todo: Lucía recibe la lupa de su bisabuelo, que era
relojero ("un buen relojero se fija en todo"), y funda con Sofía y con
Hugo, un compañero nuevo, el **Club de la Lupa**. Cada semana es un
capítulo y, casi siempre, un caso: la niña que lee es un miembro más
del club, y lo resuelve con las mismas pistas que los personajes.

## El reparto

Los del cuaderno de frases, un año mayores, y tres nuevos.

| Personaje | Quién es |
|---|---|
| **Lucía** | protagonista; empieza 2.º de primaria con 7 años y cumple 8 en noviembre (semana 9). Fundadora del Club de la Lupa |
| **Dani** | su hermano, 5 años (cumple 6 en mayo, semana 35); ya junta palabras solo; en septiembre del año siguiente empieza 1.º |
| **Toby** | el perro de la familia: marrón, de orejas largas, con su pelota roja; esconde cosas debajo del sofá y duerme allí; le dan miedo los truenos |
| **Mamá** y **Papá** | de fondo; Papá tiene letra redonda y ordenada, y se acuesta tarde leyendo |
| **Abuela Rosa** | la abuela; vive en la ciudad y pasa el verano en su casa del pueblo; su padre era relojero y la lupa era suya |
| **Sofía** | la mejor amiga de Lucía desde 1.º; impaciente, valiente, dibuja muy bien |
| **Hugo** *(nuevo)* | compañero nuevo en 2.º; viene de una ciudad junto al mar; gafas redondas azules; tímido al principio; le encantan los mapas y los códigos; tiene una tortuga, **Rayo** |
| **Marta** | la maestra de Lucía (también en 2.º) |
| **Paco** *(nuevo)* | el conserje del colegio, que lleva allí treinta años |
| **Tomás** *(nuevo)* | el bibliotecario del barrio |
| **Pedro** y **Luna** | el vecino y su gata blanca (un ojo verde y otro azul, collar con cascabel) |
| **Andrés** y **Bigotes** | el vecino del pueblo, que tiene abejas, y su gato blanco y naranja |
| **Martín** | el amigo de Dani en el pueblo |

Todos los nombres propios del reparto están en `tools/libros.py`
(`LUPA.nombres_propios`), para que `tools/metricas.py` no los cuente
como vocabulario nuevo.

## La semana

Cada semana es un capítulo (y casi siempre un caso). El ciclo, con
variaciones cuando el tema lo pide:

| Día | Actividad | Qué entrena |
|---|---|---|
| lunes | **Dibuja con lupa** (`dibuja_detalle`) o **Mapa** | el texto describe un sitio o un objeto con detalle (posición, número, color, forma); se dibuja tal cual y se comprueba con preguntas que obligan a volver al texto — la lista pregunta, no da la respuesta |
| martes | **Caza los errores**, **Verdadero o falso** (con corrección), **Ficha** o **Relaciona** (causa → consecuencia) | lectura atenta del detalle |
| miércoles | **Responde** (1–2 preguntas de "¿por qué?", "¿cómo lo sabes?") u **Ordena** | inferencia y orden temporal |
| jueves | un enigma: **Tabla de pistas** (`logica`), **Mensaje secreto** (`codigo`), **Adivina**, **Mapa** o **Compara** | razonamiento a partir del texto |
| viernes | **Resuelve el caso** (`caso`), **Crea**, **Viñetas** o **Repasa** | juntar las pistas de toda la semana; escribir |

- Un caso es *de juego limpio*: todas las pistas están en los textos de
  lunes a jueves (y, como mucho, en el del viernes), y bastan para
  resolverlo. El texto del viernes reúne al club y deja la pregunta en
  el aire; la solución se confirma en la primera frase del lunes
  siguiente (y está en la clave de respuestas).
- Cada 10 días (los viernes de las semanas pares) la actividad lleva un
  **banner** ("¡20 páginas leídas!"). Los días 65, 130 y 195 cierran
  trimestre y su banner va también a la página de medalla.
- Las semanas 13, 26, 39 y 52 cierran trimestre: el caso grande se
  resuelve el jueves y el viernes es la revelación + **Repasa**.

## Las actividades

Todas usan la misma caja (`actividadLupa`, `preamble-lupa.tex`), que ocupa
todo el alto que le queda a la página: el sitio para dibujar o pensar
se adapta solo a lo largo que sea el texto. Campos en el JSON — ver
`tools/lupa.py` para el detalle y las comprobaciones:

| Tipo | Título | Campos | Qué se comprueba al generar |
|---|---|---|---|
| `dibuja_detalle` | Dibuja con lupa | `prompt`, `comprueba` (2–5 preguntas), `clave` | — |
| `mapa` | Mapa | `instruccion`, `columnas`, `filas`, `lugares` (`{"B2": "fuente"}`), `salida`, `preguntas`, `comprobar` (rutas), `clave` | casillas dentro del mapa; cada ruta llega a donde dice |
| `logica` | Tabla de pistas | `instruccion`, `filas`, `columnas`, `pistas` (opcional: si no están, están en el texto), `restricciones`, `solucion`, `pregunta` | **una sola solución**, y es la del JSON |
| `caso` | Resuelve el caso | `pregunta`, `opciones`, `solucion`, `clave`, `lineas` | la solución es una de las opciones |
| `errores` | Caza los errores | `instruccion`, `relato`, `errores` (`[mal, bien]`) | cada error está en el relato; cada corrección, en los textos de la semana |
| `codigo` | Mensaje secreto | `instruccion`, `mensaje`, `cifrado` (`vocales`, `numeros`, `reves`), `mostrar_clave` | el mensaje se cifra solo, sin erratas posibles |
| `ficha` | Ficha | `instruccion`, `titulo`, `campos`, `respuestas` | una respuesta por campo |
| `compara` | Compara | `instruccion`, `a`, `b`, `solucion` (`a`, `ambos`, `b`) | — |
| `vinetas` | Viñetas | `instruccion`, `pies` (3) | — |
| `responde` | Responde | `preguntas` (1–3), `respuestas` (modelo), `lineas` | una respuesta por pregunta |
| `ordena` | Ordena | `sucesos` (3–6, en el orden correcto; se barajan solos) | — |
| `relaciona` | Relaciona | `pares`, `instruccion`, `cabeceras` | — |
| `verdadero_falso` | Verdadero o falso | `afirmaciones`, `respuestas` ("V" o "F: corrección"), `corrige` | una respuesta por afirmación |
| `adivina` | Adivina | `adivinanza` (con `\n`), `respuesta` | — |
| `crea` | Crea | `prompt`, `lineas` (0 = espacio para dibujar) | — |
| `repasa` | Repasa | `checklist`, `prompt`, `banner` | — |

Cualquier actividad admite además `banner`. Todas menos `vinetas`,
`crea` y `repasa` llevan su solución, que va a la clave de respuestas
del final del cuaderno.

El texto del día (`texto`) es una lista de párrafos: `—` al principio es
diálogo, `> ` una nota o carta que los personajes leen (va en un
recuadro blanco), `- ` un elemento de lista, y `\n` dentro de un párrafo
un salto de línea. Nada de comillas rectas: raya para el diálogo, «»
para citar (`tools/lupa.py` lo comprueba).

## Escalera de progresión

Valores al final de cada trimestre; en medio crecen de forma lineal,
semana a semana (`content/lupa/progresion.json`, comprobado por
`tools/metricas.py --libro lupa`):

| Dimensión | inicio T1 | final T1 | final T2 | final T3 | final T4 |
|---|---|---|---|---|---|
| palabras/página | 55–70 | 70–85 | 85–100 | 100–115 | 110–125 |
| máx. palabras en una oración | 18 | 20 | 22 | 23 | 24 |
| nexos de subordinación por texto (mín.) | 2 | 3 | 4 | 4 | 5 |
| tiempo verbal | presente | presente, pretérito perfecto | narración en pasado (indefinido e imperfecto) | + pluscuamperfecto, subjuntivo (*para que*, *antes de que*) | todos; estilo indirecto |
| géneros | narración, nota | + lista, normas | + carta, informativo | + receta, instrucciones, entrevista | + diario, poema, noticia, cómic |
| análisis | detalle literal, V/F con corrección | + causa, tabla 3×3, mapa | + orden, código de números | + inferencia ("¿cómo lo sabes?"), tabla 4×4 | + predicción, resumen, opinión |
| letra del texto | 16 pt | 16 pt | 15 pt | 14,5 pt | 14 pt |

`palabras_max`, `frase_max` y `subordinadas_min` son límites duros (`make
check-lupa` falla); `palabras_min` y el vocabulario nuevo
(`nuevas_max`, contando como ya vistas todas las palabras del cuaderno
de frases) son avisos.

## Los cuatro trimestres

| Trimestre | Semanas | Días | Época | Hilo |
|---|---|---|---|---|
| 1 | 1–13 | 1–65 | otoño | **¿Quién es Lector X?** Unas notas con adivinanzas firmadas por "Lector X" aparecen por casa. Se resuelve en la semana 13: son Dani, que inventa las adivinanzas, y Papá, que las escribe |
| 2 | 14–26 | 66–130 | invierno | **El mapa de la abuela.** En Nochebuena, Lucía encuentra el mapa del tesoro que la abuela Rosa dibujó a los ocho años y nunca volvió a encontrar. Casos de invierno en la ciudad |
| 3 | 27–39 | 131–195 | primavera | **La cápsula del tiempo.** La clase de Marta, cuando ella era niña en ese mismo colegio, enterró una cápsula en el patio; nadie recuerda dónde |
| 4 | 40–52 | 196–260 | verano | **El tesoro de la abuela Rosa**, en el pueblo: el mapa se resuelve con los pasos de una niña de ocho años. Última semana: vuelta al cole, Lucía empieza 3.º y Dani 1.º |

### Trimestre 1 — otoño (presente)

| Sem. | Tema | Caso / hilo | Lunes | Martes | Miércoles | Jueves | Viernes |
|---|---|---|---|---|---|---|---|
| 1 | La lupa de la abuela | la abuela le regala la lupa del bisabuelo relojero; primera nota de Lector X (huele a fresa, letra redonda de mayor) | dibuja la lupa | V/F | responde | adivina (la nota) | crea |
| 2 | Un compañero nuevo | ¿De dónde viene Hugo? → de una ciudad junto al mar (concha, "aquí no huele a sal", dibujo del faro, veía el mar desde el colegio) | dibuja a Hugo | errores | responde | tabla (meriendas) | caso |
| 3 | El Club de la Lupa | fundan el club en la caseta del jardín; normas; código de vocales (A=1... U=5); segunda nota de Lector X | dibuja la caseta | V/F | responde | código | crea |
| 4 | El caso de las galletas | ¿quién vació el bote? → Toby (bote en la balda de abajo con la tapa floja, pelo corto y marrón, migas hasta el sofá; Dani en el baño, Papá llegó a las siete) | dibuja la estantería | errores | responde | mapa (migas) | caso |
| 5 | Huellas en el cemento | ¿quién pisó el cemento fresco? → Luna (cuatro dedos, sin uñas; pasó la noche fuera y volvió con las patas grises) | dibuja la huella | ficha (huellas) | responde | compara (perros / gatos) | caso |
| 6 | La hoja de los martes | ¿quién deja una hoja en el libro de los árboles cada martes? → Pedro (club de lectura los martes, cruza el parque; Tomás no sale de la biblioteca) | dibuja la biblioteca | V/F | responde | relaciona (hojas) | caso |
| 7 | Ruidos en el desván | ¿qué hace "toc, toc" en el desván? → una rama del castaño (solo con viento, arañazos en el cristal, polvo sin huellas); tercera nota de Lector X con un dinosaurio dibujado, mientras Mamá está de viaje | dibuja el desván | V/F | ordena | adivina (la nota) | caso |
| 8 | La lista de la compra | ¿dónde se quedó el pan? → en el puesto del pescado, donde Dani dejó la bolsa para ver los peces; la lista tiene la letra redonda de Papá y Dani la decora con rotuladores que huelen a fruta | mapa (mercado) | errores | responde | tabla (bolsas) | caso |
| 9 | Ocho años | cumpleaños de Lucía; nota de Lector X mientras la abuela está en el pueblo toda la semana | dibuja la tarta | relaciona (regalos) | responde | tabla (gorros) | adivina (dónde está el regalo) |
| 10 | ¿Dónde está Luna? | → dormida en la caja de lana de la abuela, en la caseta (cascabel de noche, pelos blancos en la ventana redonda, que se quedó abierta) | mapa (calle) | ficha (cartel "se busca") | responde | código de números | caso |
| 11 | El museo de los dinosaurios | excursión; nota de Lector X en la cocina y Toby, que ladra a cualquiera que entra de noche, no ladró → es alguien de casa | dibuja la sala | ficha (diplodocus) | ordena | compara (T. rex / diplodocus) | caso (¿alguien de casa o de fuera?) |
| 12 | La función de Navidad | ¿dónde está la estrella? → en la caja de objetos perdidos de Paco; nota de Lector X con una palabra en letras torcidas de niño | dibuja el escenario | errores | responde | tabla (papeles) | caso |
| 13 | ¡Lector X, descubierto! | el club repasa todas las pistas → Papá (letra) y Dani (fresa, dinosaurios, adivinanzas) | dibuja el tablero de pistas | V/F | responde | caso (¿quién es Lector X?) | repasa + medalla |

### Trimestre 2 — invierno (narración en pasado)

| Sem. | Tema | Caso / hilo |
|---|---|---|
| 14 | Los Reyes que caminan | los Reyes del belén avanzan un palmo cada noche → los mueve Papá (tradición de su infancia): el belén está en una balda alta, Mamá se acostaba pronto con catarro, Papá lee hasta tarde, una nota con su letra |
| 15 | Nochebuena y el mapa de la abuela | en casa de la abuela, dentro de un cuaderno viejo de su escuela, Lucía encuentra el mapa del tesoro que Rosa dibujó a los 8 años: el río a la izquierda, con un puente; el molino con su rueda, arriba a la izquierda; el pozo con un cubo en el centro; tres álamos en fila a la derecha y, junto a ellos, la piedra que parece una tortuga; una X roja debajo de la piedra. Detrás, a lápiz: «Desde el pozo, diez pasos hacia los álamos. El tesoro está debajo de la piedra que parece una tortuga» |
| 16 | Las doce uvas | ¿quién se comió tres uvas del cuenco de Dani? → Dani, que se entrenaba (mancha morada en el pijama, pepitas en la zapatilla); las uvas, lejos de Toby porque a los perros les sientan mal |
| 17 | El roscón de Reyes | la carta de Dani a los Reyes; ¿quién tiene el haba? (tabla lógica + caso) |
| 18 | Un muñeco de nieve madrugador | ¿quién hizo el muñeco del patio antes de que llegara nadie? → Paco (bufanda de rayas, huellas de botas desde la conserjería, llega a las siete) |
| 19 | El periscopio de Hugo | instrucciones para construirlo (ordena); misión de observación |
| 20 | El Día de la Paz | el club se pelea por quién manda; turnos; ¿quién rompió el cartel del club? → nadie: se despegó con el viento (norma 2: no acusar sin pruebas) |
| 21 | El cumpleaños de Papá | sorpresa organizada con mensajes en clave; Dani casi lo cuenta |
| 22 | Carnaval | disfraces (Lucía, de detective); ¿de quién es el antifaz perdido? |
| 23 | Una carta del pueblo | Martín escribe a Dani (carta): el molino se está restaurando para hacer un museo, y la piedra de la tortuga se la han llevado de la era al jardín del molino |
| 24 | Las plantas mustias | ¿por qué se mueren las plantas de la ventana de clase? → el frío: la ventana tiene el pestillo roto y se abre con el viento el fin de semana |
| 25 | El planetario | los planetas (informativo); ¿qué planeta eligió Hugo? → Marte |
| 26 | El nido del jardín | ¿quién se lleva la lana de la abuela? → una pareja de mirlos, para el nido de la hiedra; repasa + medalla |

### Trimestre 3 — primavera (pasado, pluscuamperfecto, subjuntivo)

| Sem. | Tema | Caso / hilo |
|---|---|---|
| 27 | Una foto de hace veinticinco años | Marta enseña una foto de su clase enterrando una cápsula del tiempo (fuente con cabeza de león, el plátano grande, el reloj de la fachada a las doce) |
| 28 | Torrijas, esta vez sola | Semana Santa: Lucía hace las torrijas que prometió en el cuaderno de frases (receta); ¿quién se comió la última? |
| 29 | La rueda pinchada | ¿dónde se pinchó la bici? (mapa del recorrido); cómo arreglar un pinchazo (instrucciones) |
| 30 | La entrevista a Paco | Paco recuerda: «a mediodía, a la sombra del plátano grande, a diez pasos de la fuente»; pero la fuente se cambió de sitio y ahora hay dos plátanos |
| 31 | El Día del Libro | ¿de quién es el libro sin nombre? (pistas dentro del libro) |
| 32 | El plano antiguo | un plano del colegio de hace 25 años: la fuente estaba donde hoy está el arenero |
| 33 | Rayo se escapa | la tortuga de Hugo; huellas en la tierra, mordiscos en la lechuga |
| 34 | El día de la madre | desayuno sorpresa; poema en clave |
| 35 | Dani cumple seis años | Lucía organiza para Dani una búsqueda del tesoro con adivinanzas (ahora es ella la Lectora X) |
| 36 | Las abejas del parque | informativo; ¿por qué hay abejas en la ventana de 2.º? → las macetas de lavanda |
| 37 | La granja escuela | ¿quién abrió la puerta del corral? → la cabra, que abre pestillos con la boca |
| 38 | ¡Aquí está la cápsula! | juntan las pistas (el plátano que existía entonces, la fuente en el arenero, diez pasos) y la encuentran con Paco |
| 39 | La fiesta de fin de curso | abren la cápsula: la carta de Marta niña («quiero ser maestra en este colegio»); el club escribe la suya; repasa + medalla |

### Trimestre 4 — verano (todos los tiempos y géneros)

| Sem. | Tema | Caso / hilo |
|---|---|---|
| 40 | La maleta | lista de la maleta; ¿qué se ha olvidado Dani? |
| 41 | Otra vez en el pueblo | el mapa de la abuela contra la era de hoy (un prado detrás de la iglesia, de la familia de Andrés): el pozo sigue (tapado con una tapa de madera), quedan dos álamos (el tercero lo tiró una tormenta; queda el tocón), la piedra de la tortuga está en el jardín del molino |
| 42 | Diez pasos | Papá cuenta diez pasos desde el pozo y no encuentran nada → ¿por qué? Porque los pasos de Papá son mucho más largos que los de una niña de ocho años |
| 43 | El diario de Lucía | (diario) ¿quién visita el huerto de noche? → un erizo (come caracoles, no lechugas) |
| 44 | Las abejas de Andrés | ¿quién abrió el tarro de miel? → las hormigas (a los gatos no les sabe el dulce) |
| 45 | La noche de las estrellas fugaces | las Perseidas; la Osa Mayor |
| 46 | Una carta de Hugo | carta desde el mar, con mensaje en clave |
| 47 | Las fiestas del pueblo | concurso de adivinanzas; poema; noticia en el bando del pueblo |
| 48 | ¡El tesoro de Rosa! | Lucía, con ocho años como Rosa, cuenta diez pasos suyos desde el pozo y llega a un círculo donde la hierba crece distinta, junto al tocón: con permiso de Andrés, desentierran la caja de lata, con una canica azul, una foto de Rosa niña con su padre, que sostiene la lupa, y una carta «Para la Rosa de mayor» |
| 49 | El mapa de Dani y Martín | Dani y Martín dibujan su propio mapa para el verano siguiente |
| 50 | Vuelta a la ciudad | despedidas; el verano en orden; cómic |
| 51 | Dani, al cole de los mayores | Lucía le enseña a Dani cómo lee un detective; Dani, miembro del club |
| 52 | Vuelta al cole | Lucía empieza 3.º y Dani 1.º; un sobre sin remite en el buzón del club...; repasa + diploma |

## Reglas para escribir (y revisar) un día

- Castellano de España, natural, cálido y con humor: *vosotros*, *cole*,
  *merendar*, *tobogán*. Narrador en tercera persona.
- Cada texto, dentro de la escalera de su semana (palabras, frase más
  larga, subordinadas). Variedad de nexos: no solo "que" y "porque".
- Todo lo que pide la actividad está en el texto de ese día o en los de
  días anteriores de la misma semana (y la instrucción lo dice cuando
  hay que volver atrás). Nada de preguntar por algo que el texto no
  dice.
- En `dibuja_detalle`, el texto da los detalles y las preguntas de
  comprobación solo los nombran ("¿De qué color es el borde?"), nunca
  los repiten: si la respuesta estuviera en la lista, no habría que
  volver al texto.
- En un `caso`, las pistas bastan y son justas; la solución la tiene
  que poder deducir una niña de 7–8 años con el texto delante, y se
  confirma en el lunes siguiente.
- Seguridad y valores: nada de secretos con desconocidos (las notas de
  Lector X son de la familia, y Lucía se las enseña a Mamá desde el
  primer día); los detectives no acusan sin pruebas; los perros no
  comen uvas ni chocolate.
