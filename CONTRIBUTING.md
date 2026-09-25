# Contribuir a este repositorio

Antes de nada, una aclaración honesta: esto es el cuaderno de lectura de
una niña real, de 6 años. Los personajes (Lucía, Dani, Toby, Mamá, Papá,
Abuela Rosa), las frases y la trama semanal son una decisión editorial de
su autor, no un contenido abierto a propuestas -- así que **no es un
proyecto que busque contribuciones de historia** (nuevas frases, nuevos
personajes, cambios de trama). Ver `notes/01-curriculum.md` para el
razonamiento completo detrás del programa del curso.

Lo que sí tiene sentido, y es bienvenido:

## Lo que encaja aquí

- **Errores del motor**: algo que no compila, un caracter que se renderiza
  mal (el propio repositorio tuvo uno real -- babel-spanish convierte `"`
  en un carácter activo, y una comilla suelta en un diálogo se corrompía
  en silencio; el arreglo está documentado en `preamble.tex` junto al
  código, como ejemplo del tipo de problema que merece un *issue* o un PR).
- **Los generadores** (`tools/gen_days.py`, `tools/gen_palabras.py`,
  `tools/lupa.py`, `tools/english.py`, `tools/fonetica.py`, `tools/sylaby.py`) y sus validaciones -- por ejemplo, si detectas un
  caso que debería fallar la validación y no lo hace, o al revés (una
  tabla lógica con dos soluciones que el generador no detecta, una ruta
  de mapa que llega a otra casilla...).
- **El silabeo** (`tools/silabas.py`) -- una palabra real que las reglas
  parten mal es exactamente el tipo de error que merece un *issue* (con
  la palabra y el silabeo correcto; si es un caso legítimo que las
  reglas no cubren, se añade a `EXCEPCIONES` y a `CASOS_PRUEBA`). Lo
  mismo con el partido en sonidos del inglés (`tools/fonetica.py`): una
  palabra que `segmentar()` parte mal, o una trampa que no rechaza (una
  letra que no suena y que tendría botón), va a `EXCEPCIONES`, a
  `PRUEBA` o a `PRUEBA_TRAMPAS`. Y con el silabeo del polaco
  (`tools/sylaby.py`): una palabra que `podziel()` parte mal va a
  `WYJATKI` y a `CASOS_PRUEBA`, con su porqué.
- **`tools/check_pages.py`** y el invariante "1 día = 1 página" -- si
  encuentras un caso donde se rompe sin que el *build* lo detecte.
- **CI** (`.github/workflows/`), el `Makefile`, o cualquier parte de la
  infraestructura de construcción.

## Lo que no

- Frases nuevas, personajes nuevos, cambios de trama -- eso es una
  decisión editorial del autor sobre la historia de su propia hija.

## La vía principal: haz un fork

El repositorio está deliberadamente construido para esto: el motor LaTeX
(`preamble*.tex`, `lang/es.tex`, `lang/en.tex`, `lang/pl.tex`, `tools/`) es
independiente del contenido (`content/*.json`, `content/palabras/*.json`,
`content/lupa/*.json`, `content/english/*.json`,
`content/firstwords/*.json`, `content/slowa/*.json`,
`content/zdania/*.json`, `content/czytam/*.json`). Si
quieres un cuaderno parecido para otro niño o niña, haz un fork,
sustituye `content/q1.json` a `q4.json` (frases), `content/palabras/q1.json`
a `q4.json` (primeras palabras), `content/lupa/q1.json` a `q4.json`
(Leo con lupa), `content/english/q1.json` a `q4.json` (Read and
Draw, en inglés), `content/firstwords/q1.json` a `q4.json` (First
Words, en inglés), `content/slowa/q1.json` a `q4.json` (Pierwsze
słowa, en polaco), `content/zdania/q1.json` a `q4.json` (Zdania, en
polaco) y/o `content/czytam/q1.json` a `q4.json` (Czytam z lupą, en
polaco) por tus propios personajes, frases y palabras, y
conserva el resto tal cual -- es exactamente el reparto MIT/CC BY-NC-SA de `LICENSE`: el motor
es tuyo para reutilizar, la historia concreta de esta familia no.

## Flujo de trabajo

```sh
make generate       # content/q*.json, content/{palabras,lupa,english,firstwords,slowa,zdania,czytam}/q*.json -> .tex generados
make build           # compila el cuaderno de frases en color (main.tex)
make palabras        # genera, compila y comprueba el de primeras palabras (palabras.tex)
make lupa            # genera, compila y comprueba Leo con lupa (lupa.tex)
make english         # genera, compila y comprueba Read and Draw (english.tex)
make firstwords      # genera, compila y comprueba First Words (firstwords.tex)
make slowa           # genera, compila y comprueba Pierwsze słowa (slowa.tex)
make zdania          # genera, compila y comprueba Zdania (zdania.tex)
make czytam          # genera, compila y comprueba Czytam z lupą (czytam.tex)
make check            # tools/checklog.py + tools/check_pages.py + tools/gen_days.py --check + tools/metricas.py
make verano           # los siete cuadernos de verano, color Y blanco-y-negro
make muestra          # las siete muestras gratuitas, color Y blanco-y-negro
make all-formats      # los ocho cuadernos, sus cuadernos de verano y sus
                       # muestras, color Y blanco-y-negro -- ejecútalo antes de
                       # abrir un PR, es lo mismo que corre el CI
```

Las barreras duras que tienen que quedar en verde:

- **1 día = exactamente 1 página** (`tools/check_pages.py`, lee el `.aux`
  después de compilar -- es la única forma de saber si un día se ha
  desbordado a una segunda página sin mirar las 260 páginas una a una).
- **El log sin errores ni `Overfull`** (`tools/checklog.py` -- nunca
  `grep '^!'`: con `-file-line-error` la línea de error empieza por una
  ruta, no por `!`, y `-interaction=nonstopmode` escribe igualmente un PDF
  encima del error, así que el código de salida y el propio PDF dicen
  "todo bien" aunque no lo esté).
- **El JSON y el `.tex` generado coinciden** (`tools/gen_days.py --check`
  -- si alguien toca `content/generated-days.tex` a mano y luego cambia el
  JSON, el desajuste se detecta).
- **La escalera de sílabas** del cuaderno de primeras palabras
  (`tools/gen_palabras.py --check`): cada palabra escrita a mano con sus
  sílabas (`"pe-lo-ta"`) tiene que coincidir con el silabeo automático
  de `tools/silabas.py`, y no puede usar estructuras de sílaba que su
  semana todavía no admite (una `rr` en otoño, por ejemplo).
- **La escalera de sonidos** de First Words (`tools/gen_palabras.py
  --libro firstwords --check`, ver `notes/06-first-words.md`): cada
  palabra escrita a mano con sus sonidos (`"sh-ee-p"`) tiene que
  coincidir con el partido automático de `tools/fonetica.py`, usar solo
  los sonidos que su semana ya admite, no ser una trampa (*house*,
  *knee*) ni una *tricky word*; en verano, cada palabra de una frase
  tiene que leerse sonido a sonido con lo aprendido, o ser una *tricky
  word* ya presentada un viernes de primavera, o un nombre del reparto.
  Cada *tricky word* se presenta una sola vez. Y la tabla de sonidos del principio,
  generada de la misma escalera, sin ningún sonido sin ejemplo, y con
  cada uno de sus sonidos en alguna tarjeta antes de que acabe su
  estación.
- **La escalera de sílabas del polaco** de Pierwsze słowa
  (`tools/gen_palabras.py --libro slowa --check`, ver
  `notes/08-pierwsze-slowa.md`): cada palabra escrita con sus sílabas
  (`"ło-pa-ta"`) tiene que coincidir con `tools/sylaby.py`, y no usar lo
  que su semana todavía no admite (una sílaba cerrada o blanda, un
  dígrafo o una nasal en otoño); los nombres que se leen de un golpe
  van enteros, y al terminar el año tienen que estar trazadas las 32
  letras del abecedario polaco.
- **Zdania** (`tools/gen_days.py --libro zdania --check` y
  `tools/metricas.py --libro zdania`, ver `notes/09-zdania.md`): las
  mismas reglas que el cuaderno de frases, y su escalera medida en
  palabras polacas (`content/zdania/progresion.json`); cada letra de
  *Pisz po śladzie* es del abecedario polaco, tiene su palabra de
  ejemplo (`content/zdania/palabras-trazo.json`) y, con el libro
  entero, están las 32.
- **Czytam z lupą** (`tools/gen_days.py --libro czytam --check` y
  `tools/metricas.py --libro czytam`, ver `notes/10-czytam-z-lupa.md`):
  las mismas reglas que *Leo con lupa* -- la tabla de pistas con una
  sola solución, las rutas del mapa, las correcciones de *Wyłap błędy*
  en el texto de la semana, el mensaje secreto con las 32 letras del
  alfabeto polaco, las respuestas de *Prawda czy fałsz* con P o F -- y
  su escalera medida en palabras polacas, con los nexos del polaco
  (`content/czytam/progresion.json`).
- **Los dibujos para colorear** de First Words (el mismo `--check`): el
  `"dibujo"` de cada día existe en `diagrams/` y es el de una palabra que
  se lee ese día; ningún dibujo de `diagrams/firstwords/` se queda sin
  usar. Un dibujo nuevo va en `diagrams/firstwords/<palabra>.tex`, en un
  `tikzpicture` con el estilo `dibujofw`, con cada parte cerrada y
  rellena de blanco, y con los personajes y las cosas de
  `diagrams/firstwords/kit.tex` (la cabeza de cada uno, Toby, Pip, la
  jaula...) para que sean siempre los mismos. El tamaño lo pone la
  página: no hace falta escalarlo a mano.
- **La escalera de progresión** (`tools/metricas.py`, contra
  `content/progresion.json` -- ver `notes/02-revision-y-plan.md`, Parte
  C): palabras por página y frase más larga no pueden superar el
  objetivo de esa semana. El vocabulario nuevo por día solo avisa, no
  bloquea. En Leo con lupa (`--libro lupa`, contra
  `content/lupa/progresion.json`) y en Read and Draw (`--libro english`,
  contra `content/english/progresion.json`) hay además un mínimo de
  oraciones subordinadas por texto.
- **Las actividades de Leo con lupa** (`tools/gen_days.py --libro lupa
  --check`, ver `tools/lupa.py`): cada tabla lógica con una sola
  solución, cada ruta de mapa llegando a donde dice la clave, cada
  corrección de «Caza los errores» presente de verdad en el texto de la
  semana, y el libro entero, con sus 260 días.
- **Las actividades de Read and Draw** (`tools/gen_days.py --libro
  english --check`, ver `tools/english.py`): cada frase de «The missing
  words» y de «Match the halves» presente tal cual en el texto de la
  semana, cada palabra de «Word hunt» en el del día, cada dibujo de
  `diagrams/english/` que se pide existiendo, y el texto en inglés
  británico, sin rastros del español; y el libro entero, con sus 260
  días.

`.github/workflows/build.yml` corre exactamente estas mismas comprobaciones
en cada *push* y *pull request*, así que un PR con `make all-formats` en
verde localmente debería pasar el CI sin sorpresas.

## Cómo reportar un problema

Abre un [*issue*](https://github.com/konradcinkusz/learning-to-read/issues)
describiendo qué esperabas y qué ha pasado -- si es un problema de
compilación, adjunta la línea exacta del log (`tools/checklog.py` te la da
ya localizada, con el fichero y el número de línea).
