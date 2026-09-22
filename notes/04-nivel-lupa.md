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

Los del cuaderno de frases, un año mayores, y algunos nuevos.

| Personaje | Quién es |
|---|---|
| **Lucía** | protagonista; empieza 2.º de primaria con 7 años y cumple 8 en noviembre (semana 9). Fundadora del Club de la Lupa |
| **Dani** | su hermano, 5 años (cumple 6 en mayo, semana 35); ya junta palabras solo; en septiembre del año siguiente empieza 1.º |
| **Toby** | el perro de la familia: marrón, de orejas largas, con su pelota roja; esconde cosas debajo del sofá y duerme allí; le dan miedo los truenos |
| **Mamá** y **Papá** | de fondo; Papá tiene letra redonda y ordenada, y se acuesta tarde leyendo |
| **Abuela Rosa** | la abuela; vive en la ciudad y pasa el verano en su casa del pueblo; su padre era relojero y la lupa era suya |
| **Sofía** | la mejor amiga de Lucía desde 1.º; impaciente, valiente, dibuja muy bien |
| **Hugo** *(nuevo)* | compañero nuevo en 2.º; viene de una ciudad junto al mar; gafas redondas azules; tímido al principio; le encantan los mapas y los códigos; tiene una tortuga, **Rayo** |
| **Marta** | la maestra de Lucía (también en 2.º); de niña estudió en ese mismo colegio (la cápsula del tiempo, T3), y el septiembre siguiente es la maestra de Dani en 1.º |
| **Paco** *(nuevo)* | el conserje del colegio, que lleva allí treinta años |
| **Tomás** *(nuevo)* | el bibliotecario del barrio |
| **Pedro** y **Luna** | el vecino y su gata blanca (un ojo verde y otro azul, collar con cascabel) |
| **Andrés** y **Bigotes** | el vecino del pueblo, que tiene abejas, y su gato blanco y naranja |
| **Martín** | el amigo de Dani en el pueblo |
| **Nora**, **Leo**, **Irene** y **Álex** | compañeros de clase de Lucía (Nora desde el invierno; los otros tres, en primavera) |
| **Pilar** y **Luis** | la maestra y el director del colegio cuando Marta era niña (T3) |
| **Julián** y **Lola** | el granjero de la granja escuela y su cabra más curiosa (semana 37) |

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

| Sem. | Tema | Caso / hilo | Lunes | Martes | Miércoles | Jueves | Viernes |
|---|---|---|---|---|---|---|---|
| 14 | Los Reyes que caminan | ¿quién mueve los Reyes del belén un palmo cada noche? → Papá (el belén está en la balda más alta, Toby no ladró, Mamá se acostaba pronto con catarro y Papá leía hasta las doce; la nota «Un palmo cada noche, hasta llegar al portal», sin firma, tiene la letra redonda de Lector X) | dibuja el belén | V/F | responde | tabla (a qué hora se acuesta cada uno) | caso |
| 15 | Nochebuena y el mapa | en el armario de la abuela, dentro de un cuaderno viejo de su colegio, Lucía encuentra el mapa del tesoro que Rosa dibujó a los 8 años (ver abajo); la abuela se lo da: lo buscarán en verano | dibuja el mapa | errores | ordena | compara (Rosa de niña / Lucía) | adivina (el pozo) |
| 16 | Las doce uvas | ¿quién se comió tres uvas del cuenco de Dani? → Dani, que se entrenaba para las campanadas (boca y pijama manchados de morado, pepitas en su zapatilla); las uvas, lejos de Toby, porque a los perros les sientan mal | dibuja la bandeja | ficha (las doce uvas) | responde | código de números | caso |
| 17 | El roscón de Reyes | la carta de Dani a los Reyes; ¿quién tiene el haba? → la abuela (el cuchillo chocó con algo duro en el trozo de la guinda, que no quisieron ni Mamá ni Papá) | relaciona (la carta) | dibuja el salón la noche de Reyes | responde | tabla (los trozos) | caso |
| 18 | Un muñeco de nieve madrugador | ¿quién hizo el muñeco del patio? → Paco (tan alto como un mayor, huellas de botas grandes que salen de la conserjería y vuelven a ella, bufanda que huele a café, llega a las siete) | dibuja el muñeco | errores | responde | mapa (las huellas) | caso |
| 19 | El periscopio de Hugo | instrucciones para construirlo; misión de observación desde el seto | dibuja el periscopio | ordena (instrucciones) | código al revés | tabla (quién vio a quién) | viñetas |
| 20 | El Día de la Paz | el club se pelea por quién manda; ¿quién quitó el cartel de la caseta? → nadie: el viento (cinta vieja, una noche de vendaval, la papelera de Pedro en medio de la calle). Desde entonces mandan por turnos | dibuja el cartel | V/F | responde | compara (Sofía / Hugo) | caso |
| 21 | El cumpleaños de Papá | búsqueda del tesoro por la casa, con un plano y mensajes en clave: Mamá se aprende el código del club, Papá no lo conoce | mapa (plano de la casa) | errores | responde | código de vocales | crea (felicitación con adivinanza) |
| 22 | Carnaval | Lucía, de detective; ¿de quién es el antifaz perdido? → Marta (goma de mayor, morado y plateado, apareció junto a la escalera del escenario); aparece Nora, compañera de clase | dibuja el disfraz | ordena | ficha (objeto perdido) | mapa (el patio) | caso |
| 23 | Una carta del pueblo | Martín escribe a Dani: el molino viejo será un museo, y la piedra de la tortuga se la han llevado del prado al jardín del molino. Pero el pozo no se mueve: «desde el pozo, diez pasos» sigue sirviendo | dibuja el dibujo de Martín | V/F | adivina (el molino) | código de vocales | crea (una carta) |
| 24 | Las plantas mustias | ¿por qué se ponen mustias los lunes las plantas de la ventana de clase? → pasan frío: el pestillo está roto, la ventana se abre con el viento y el fin de semana la calefacción está apagada | dibuja la ventana | ficha (lo que necesitan las plantas) | relaciona | compara (ventana / geranio de la mesa) | caso |
| 25 | El planetario | los planetas (informativo); ¿qué planeta eligió Hugo para su mural? → Marte (ni el más caliente ni el más grande, cartulina roja, dos lunas pequeñas) | dibuja el planetario | V/F | viñetas | código de números | caso |
| 26 | El nido del jardín | ¿quién se lleva los trocitos de lana de la cesta de la abuela? → una pareja de mirlos, para el nido de la hiedra (pluma marrón, hilo rojo muy arriba, un mirlo macho cantando en la tapia) | dibuja el jardín | ficha (el mirlo) | tabla (dónde durmió cada uno) | caso | repasa + medalla |

**El mapa de la abuela** (días 71–72), tal como lo tiene que encontrar
el trimestre 4: a la izquierda, un río que baja de arriba abajo, con un
puente pequeño; arriba, junto al río, el molino con su rueda; en el
centro, un pozo con un cubo; a la derecha, tres álamos en fila y, a su
lado, una piedra grande que parece una tortuga, con una X roja debajo.
Detrás, a lápiz: «Desde el pozo, diez pasos hacia los álamos. El tesoro
está debajo de la piedra que parece una tortuga. Rosa, 8 años». Rosa lo
dibujó en el pueblo «hace unos sesenta años»; lo que enterró es una caja
de lata.

Otros detalles fijos: el jardín de Lucía (en la ciudad) tiene el
castaño, a la derecha, con un banco debajo; el huerto de Papá, con
lechugas, a la izquierda; un seto y un rosal; y al fondo, delante de una
tapia cubierta de hiedra (donde anidan los mirlos), la caseta del club,
con la puerta verde y una ventana redonda. El limonero es el del patio
de la abuela, en el pueblo (como en el cuaderno de frases). Paco siempre
lleva una taza de café en la mano y llega a las siete. Toby tiene una
pelota roja nueva desde Reyes.

### Trimestre 3 — primavera (pasado, pluscuamperfecto, subjuntivo)

| Sem. | Tema | Caso / hilo | Lunes | Martes | Miércoles | Jueves | Viernes |
|---|---|---|---|---|---|---|---|
| 27 | Una foto de hace veinticinco años | Marta enseña la foto de su clase enterrando una cápsula del tiempo (ella, con dos trenzas, sujeta la caja roja; el plátano grande, la fuente con cabeza de león, el reloj a las doce). ¿Quién hizo la foto? → Paco («Foto de P.»: Pilar sale en la foto con la pala, no vino ningún padre, el director Luis estaba de viaje, Paco lleva treinta años en el colegio) | dibuja la foto | V/F | responde | tabla (los regalos de las clases a Paco) | caso |
| 28 | Torrijas, esta vez sola | Lucía hace las torrijas que prometió en el cuaderno de frases (receta: un adulto fríe); ¿quién se comió la última? → la abuela (balda alta sin silla movida; solo estaban ella y Toby; el rastro de azúcar acaba en su sillón) | dibuja la mesa | V/F (la receta) | responde | mapa (el rastro de azúcar) | caso |
| 29 | La rueda pinchada | ¿dónde se pinchó la bici? → en los rosales del parque (una espina de rosal; en la panadería la rueda estaba dura; por las obras, Papá llevó las bicis en brazos); cómo arreglar un pinchazo (instrucciones) | mapa (el paseo) | errores | viñetas (el pinchazo) | ordena | caso |
| 30 | La entrevista a Paco | entrevista con la adivinanza del reloj; Paco recuerda «a mediodía, a la sombra del plátano grande, a diez pasos de la fuente», pero hoy hay dos plátanos y la fuente se movió | dibuja el patio de hoy | adivina (el reloj) | responde | mapa (diez pasos desde la fuente de hoy) | crea (una entrevista) |
| 31 | El Día del Libro | ¿de quién es el libro sin nombre del intercambio? → de Leo (arena entre las hojas: Nora y Leo estuvieron en el mar; subrayado en verde: Leo e Irene) | dibuja el libro | relaciona (la Semana Santa de cada uno) | responde | tabla 4×4 (qué libro le tocó a cada uno) | caso |
| 32 | El plano antiguo | Paco encuentra un plano del patio de hace 25 años: un solo árbol, junto a la tapia de la izquierda, y la fuente tres cuadros a su derecha — donde hoy está el arenero. ¿Qué plátano estaba ya entonces? → el de la izquierda (el único del plano, y el tronco más gordo) | dibuja el plano antiguo | compara (plano antiguo / patio de hoy) | responde (los troncos) | mapa | caso |
| 33 | Rayo se escapa | la tortuga de Hugo (informativo); ¿dónde está Rayo? → enterrado en el huerto de Papá (mordiscos de media luna, la tarde más calurosa, tierra recién regada, huellas que se acaban de golpe) | dibuja el jardín | ficha (la tortuga de tierra) | responde | mapa (las huellas) | caso |
| 34 | El día de la madre | desayuno sorpresa; Mamá descifra ella sola el poema en clave | dibuja la bandeja | relaciona (causa → consecuencia) | tabla 4×4 (las tareas) | código de vocales (el poema) | crea (un poema) |
| 35 | Dani cumple seis años | Lucía es ahora la Lectora X: búsqueda del tesoro con adivinanzas y un mensaje en clave hasta un cuaderno de detective rojo (como el verde que encontró ella en septiembre) | dibuja la tarta | adivina (la lavadora) | ordena | código de números | viñetas |
| 36 | Las abejas del parque | informativo (abejas y avispas); ¿por qué van las abejas a la ventana de 2.º? → las macetas de lavanda (ven muy bien el morado; las cuatro ventanas tienen el marco azul; no hay panal) | dibuja la ventana | ficha (las abejas) | compara (abeja / avispa) | tabla 4×4 (los alféizares) | caso |
| 37 | La granja escuela | ¿quién abrió la puerta del corral? → Lola, la cabra (babas y dientes en el pestillo, pezuñas partidas, nadie salió del albergue, no hizo viento; algunas cabras aprenden a abrir pestillos) | mapa (la granja) | errores | responde | compara (cabra / oveja) | caso |
| 38 | ¡Aquí está la cápsula! | juntan las pistas: diez pasos de Paco (dos cuadros) desde el arenero hacia el plátano viejo → B3; la caja roja, oxidada, con un mensaje al revés en la tapa: «Abrir en la fiesta de fin de curso» | relaciona (qué sabe el club y cómo) | V/F | mapa | caso (el jueves: ¿dónde cavar?) | código al revés |
| 39 | La fiesta de fin de curso | abren la cápsula; ¿quién escribió la carta sin firma? → Marta («nerviosísima», ocho años, sujetaba la caja): «Cuando sea mayor, quiero ser maestra en este colegio». El club escribe su propia carta para una cápsula nueva | dibuja la mesa de la fiesta | tabla (qué quería ser cada niño) | responde (la carta) | caso | repasa + medalla |

**El patio del colegio** es el mismo en todos los planos del cuaderno
(los del invierno, días 89 y 109, y los de la primavera): 7 columnas y
4 filas; arriba, el edificio, con la conserjería (C1) a la izquierda de
la puerta con el reloj (D1) y la fuente de la cabeza de león a la
derecha (E1); abajo, un plátano junto a cada tapia (A3, el viejo; G3,
el que se plantó después) y el arenero en medio (D3), donde estaba la
fuente hace veinticinco años; la verja, en D4. Diez pasos de Paco son
dos cuadros: la cápsula estaba en B3.

### Trimestre 4 — verano (todos los tiempos y géneros)

| Sem. | Tema | Caso / hilo | Lunes | Martes | Miércoles | Jueves | Viernes |
|---|---|---|---|---|---|---|---|
| 40 | La maleta | la lista de la maleta de Dani; ¿qué se ha olvidado? → la gorra: leyó tan deprisa que metió un gorro de lana (el armario de invierno, la maleta que no cierra, un pompón rojo asomando) | dibuja la maleta | errores | responde | código de vocales | caso |
| 41 | Otra vez en el pueblo | el mapa de la abuela contra la era de hoy (el prado de detrás de la iglesia, de la familia de Andrés, que confirma lo de la carta de Martín): el pozo, tapado con una tapa de madera; de los tres álamos quedan dos y el tocón del de en medio; la piedra de la tortuga, en el jardín del molino | dibuja el mapa de Rosa | V/F | responde | mapa (la era de hoy) | compara (el mapa / la era de hoy) |
| 42 | Diez pasos | Papá cuenta diez pasos desde el pozo, acaba detrás de los álamos y no hay nada. ¿Por qué? → los pasos de Papá son mucho más largos que los de una niña de ocho años | dibuja el pozo | mapa (los pasos de Papá) | errores | tabla (cuántos pasos da cada uno) | caso |
| 43 | El diario de Lucía | (diario) ¿quién visita el huerto de noche? → un erizo (huellas de cinco dedos con uñas, lechugas enteras, caracoles que desaparecen, resoplidos, el rastro acaba en la leña) | dibuja la huella | V/F | responde | mapa (el rastro) | caso |
| 44 | Las abejas de Andrés | (informativo) ¿quién se metió en el tarro de miel? → las hormigas (la tapa solo apoyada, una fila de puntitos negros desde el limonero; a los gatos no les sabe el dulce, y a Bigotes lo que le gusta es el queso) | dibuja a Andrés con su traje | ficha (las abejas) | responde | compara (abejas / hormigas) | caso |
| 45 | La noche de las estrellas fugaces | las Perseidas (informativo) en el jardín del molino; la Osa Mayor, «el reloj de la noche» del bisabuelo relojero | dibuja la Osa Mayor | ficha (las estrellas fugaces) | ordena | tabla 4×4 (cuántas vio cada uno) | adivina (las estrellas) |
| 46 | Una carta de Hugo | carta desde el mar, una hoja cada día, con una adivinanza (el faro) y un mensaje en clave: «Cuenta tus propios pasos»; Lucía contesta | dibuja lo que ve Hugo | adivina | responde | código de números | crea (una carta) |
| 47 | Las fiestas del pueblo | el bando de fiestas (Andrés siega la era antes de los fuegos); el poema-adivinanza del club (la lupa) gana el concurso; la noticia en la hoja del pueblo | dibuja la plaza | ficha (el programa) | adivina (el poema) | tabla (los equipos) | viñetas (la noticia) |
| 48 | ¡El tesoro de Rosa! | Lucía, con ocho años como Rosa, cuenta diez pasos suyos desde el pozo y se para junto al tocón, en una mancha redonda donde la hierba crece distinta: la caja de lata, con una canica azul, una foto de Rosa niña con su padre (que sostiene la lupa de las tres rayas) y una carta «Para la Rosa de mayor» («Si algún día tienes nietos, enséñales a mirar con la lupa de papá» — «Ya lo hice») | mapa (los pasos de Lucía) | errores | dibuja la foto | responde | adivina (el reloj) |
| 49 | El mapa de Dani y Martín | Dani y Martín entierran su propia lata para el verano siguiente, medida en baldosas, «porque las baldosas no crecen» | dibuja la lata | tabla (qué pone cada uno) | responde | mapa (el patio de la abuela) | crea (tu mapa del tesoro) |
| 50 | Vuelta a la ciudad | despedidas; el verano en orden (leído del final al principio); el mensaje al revés de Martín; el cómic de Dani | dibuja el tarro de miel | tabla (quién va en cada sitio del coche) | ordena | código al revés | viñetas (el cómic) |
| 51 | Dani, al cole de los mayores | las reglas del club para leer; el primer caso de Dani: ¿quién escribió su nombre en todas sus cosas? → Papá (letra redonda y ordenada, el último en acostarse; Toby no ladró). Dani, cuarto miembro del club | dibuja la mochila | V/F (las reglas) | relaciona (la letra de cada uno) | tabla 4×4 (a qué hora se acostó cada uno) | caso |
| 52 | Vuelta al cole | Lucía empieza 3.º y Dani 1.º (con Marta); ¿qué ha traído Hugo del mar? → una brújula. Un sobre sin remite en el buzón de la caseta: «¿Os atrevéis con un caso más difícil?» | dibuja la puerta de 1.º | relaciona (el verano de cada uno) | código de vocales | caso | repasa + diploma |

**La era** (los tres planos del verano, 7 columnas y 4 filas): el río
baja por la columna A, con el molino en A1 y el puente en A3; el jardín
del molino, en B1; el pozo, en C2; la iglesia, en C4; los álamos, en F1
y F3, con el tocón en F2. Diez pasos de Papá son cuatro casillas (acaba
en G2, detrás de los álamos); diez pasos de Lucía, dos (E2, junto al
tocón, donde estuvo la piedra).

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
